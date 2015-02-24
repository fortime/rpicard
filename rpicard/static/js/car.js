function init(maxLevel) {
    initRotationPanel(maxLevel);
    car.setMaxLevel(maxLevel);
    initEvent();
}

function rotate(element, angle) {
    element.style.transform = "rotate(" + angle + "deg)";
}

function findPos(element) {
    if (element) {
        var parentPos = findPos(element.offsetParent);
        return [
            parentPos[0]+ element.offsetLeft,
            parentPos[0]+ element.offsetTop
        ];
    } else {
        return [0, 0];
    }
}

function calAngle(pointA, pointB, pointO) {
    var aox = pointA[0] - pointO[0];
    var aoy = pointA[1] - pointO[1];
    var box = pointB[0] - pointO[0];
    var boy = pointB[1] - pointO[1];

    var part1 = aox * box + aoy * boy;
    var part2 = Math.sqrt((aox * aox + aoy * aoy) * (box * box + boy * boy));
    var angleAOB = Math.acos(part1 / part2) / Math.PI * 180;
    var msg = "A:" + pointA + " B:" + pointB + " O:" + pointO + " angle:" + Math.floor(angleAOB) + " md:" + car.getMd();
    showMsg(msg);

    var otherAoy = aox * boy / box;
    if (otherAoy > aoy) {
        angleAOB = -angleAOB; 
    }
    return angleAOB;
}

function findCenterPos(element) {
    var pos = findPos(element);
    return [
        element.offsetWidth / 2 + pos[0],
        element.offsetHeight / 2 + pos[1]
    ];
}

function initEvent() {
    var innerCycle = document.getElementById("inner_cycle");
    var pos = findCenterPos(innerCycle);
    var centerOfSelectorContainerX = pos[0], centerOfSelectorContainerY = pos[1];
    pos = findCenterPos(document.getElementById("selector"));
    var selectorStartX = pos[0], selectorStartY = pos[1];

    function preventEvent(event) {
        var e = event || window.event;
        e.preventDefault && e.preventDefault();
        e.stopPropagation && e.stopPropagation();
        e.cancelBubble = true;
        e.returnValue = false;
        return false;
    }

    function findTouchById(touches, id) {
        for (var i = 0; i < touches.length; ++i) {
            if (touches[i].target.id == id) {
                return touches[i];
            }
        }
        return null;
    }

    function onSelectorDown(event) {
        return preventEvent(event);
    }

    function onSelectorUp(event) {
        rotate(innerCycle, 0);
        car.setRl(0);
        return preventEvent(event);
    }

    function onSelectorMove(event) {
        var touchPoint = findTouchById(event.changedTouches, event.target.id);
        if (touchPoint != null) {
            var selectorStartX1 = parseInt(touchPoint.clientX);
            var selectorStartY1 = parseInt(touchPoint.clientY);
            var angle = calAngle([selectorStartX1, selectorStartY1], [selectorStartX, selectorStartY], [centerOfSelectorContainerX, centerOfSelectorContainerY]);
            rotate(innerCycle, angle);
            var level = angle / (360 / (car.getMaxLevel() * 2 + 1));
            car.setRl(level > 0 ? Math.floor(level): Math.ceil(level));
        }
        return preventEvent(event);
    }

    function onForwardBtnDown(event) {
        car.goForward();
        return preventEvent(event);
    }

    function onForwardBtnUp(event) {
        car.stop();
        return preventEvent(event);
    }

    function onBackwardBtnDown(event) {
        car.goBackward();
        return preventEvent(event);
    }

    function onBackwardBtnUp(event) {
        car.stop();
        return preventEvent(event);
    }

    var selector = document.getElementById("selector");
    selector.ontouchstart = onSelectorDown; 
    selector.ontouchend = onSelectorUp;
    selector.ontouchmove = onSelectorMove;

    var forwardBtn = document.getElementById("forward_btn");
    forwardBtn.ontouchstart = onForwardBtnDown; 
    forwardBtn.ontouchend = onForwardBtnUp;

    var backwardBtn = document.getElementById("backward_btn");
    backwardBtn.ontouchstart = onBackwardBtnDown; 
    backwardBtn.ontouchend = onBackwardBtnUp;
}

function initRotationPanel(maxLevel) {
    var amount = 2 * maxLevel + 1;
    var angle = 360 / amount;
    var template = document.getElementById("number_cycle_template");
    var container = template.parentNode;
    container.removeChild(template);

    for (var i = 1; i <= amount; ++i) {
        var pos = i - amount + maxLevel;
        var newNumber = template.cloneNode(true);
        newNumber.id = "number_cycle_" + i;
        rotate(newNumber, pos * angle);
        newNumber.style.backgroundColor = "transparent";
        var number = newNumber.getElementsByClassName("number")[0];
        rotate(number, -pos * angle);
        number.innerHTML = pos;
        container.appendChild(newNumber);
    }

    var innerCycle = document.getElementById("inner_cycle");
    container.removeChild(innerCycle);
    container.appendChild(innerCycle);
}

Car.prototype = {

    _init: function() {
        this._md = 0;
        this._rl = 0;
        this._xmlHttp = new XMLHttpRequest();
        this._xmlHttp.onreadystatechange = null;
    },

    setMaxLevel: function(maxLevel) {
        this._maxLevel = maxLevel
    },

    getMaxLevel: function() {
        return this._maxLevel;
    },

    getMd: function() {
        return this._md;
    },

    goForward: function() {
        this._md = 1;
        this.flush();
    },

    goBackward: function() {
        this._md = 2;
        this.flush();
    },

    stop: function() {
        this._md = 0;
        this.flush();
    },

    setRl: function(level) {
        if (level <= this._maxLevel && level >= -this._maxLevel && this._rl != level) {
            this._rl = level;
            this.flush();
        }
    },

    flush: function() {
        if (this._xmlHttp.onreadystatechange == null) {
            this._xmlHttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    // 4 = "loaded"
                    var error = true;
                    if (this.status == 200) {
                        // 200 = OK
                        var retObj = JSON.parse(this.responseText);
                        if (retObj.retcode == "0") {
                            msg = "md: " + this._md + " rl: " + this._rl;
                            error = false;
                        }
                        else {
                            msg = this.responseText;
                        }
                    }
                    else {
                        msg = "Http Error: " + this.status;
                    }
                    if (error) {
                        showErrMsg(msg);
                    }
                    else {
                        showMsg(msg);
                    }
                }
            }
        }
        url = "/control?rl=" + this._rl + "&md=" + this._md;
        this._xmlHttp.open("GET", url, true);
        this._xmlHttp.send(null);
    },
}

function showMsg(msg) {
    var msgContent = document.getElementById("msg_content");
    msgContent.innerHTML = msg;
    msgContent.classList.remove("error");
}

function showErrMsg(msg) {
    var msgContent = document.getElementById("msg_content");
    msgContent.innerHTML = msg;
    msgContent.classList.add("error");
}

function Car() {
    this._init();
}

car = new Car();
