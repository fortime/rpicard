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

    var otherAoy = aox * boy / box;
    if (otherAoy < aoy) {
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
    var selectorStartX = 0, selectorStartY = 0;
    var innerCycle = document.getElementById("inner_cycle");
    var pos = findCenterPos(innerCycle);
    var centerOfSelectorContainerX = pos[0], centerOfSelectorContainerY = pos[1];

    function preventEvent(event) {
        var e = event || window.event;
        e.preventDefault && e.preventDefault();
        e.stopPropagation && e.stopPropagation();
        e.cancelBubble = true;
        e.returnValue = false;
        return false;
    }

    function onSelectorDown(event) {
        var e = event || window.event;
        var touchPoint = e.changedTouches[0];
        selectorStartX = parseInt(touchPoint.clientX);
        selectorStartY = parseInt(touchPoint.clientY);
        return preventEvent(event);
    }

    function onSelectorUp(event) {
        rotate(innerCycle, 0);
        selectorStartX = 0;
        selectorStartY = 0;
        car.setRl(0);
        return preventEvent(event);
    }

    function onSelectorMove(event) {
        var e = event || window.event;
        var touchPoint = e.changedTouches[0];
        var selectorStartX1 = parseInt(touchPoint.clientX);
        var selectorStartY1 = parseInt(touchPoint.clientY);
        var angle = calAngle([selectorStartX1, selectorStartY1], [selectorStartX, selectorStartY], [centerOfSelectorContainerX, centerOfSelectorContainerY]);
        rotate(innerCycle, angle);
        var level = angle / (360 / (car.getMaxLevel() * 2 + 1));
        car.setRl(Math.floor(level));
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
    },

    setMaxLevel: function(maxLevel) {
        this._maxLevel = maxLevel
    },

    getMaxLevel: function() {
        return this._maxLevel;
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
        var msgContent = document.getElementById("msg_content");
        msgContent.innerHTML = "md: " + this._md + " rl: " + this._rl;
    },
}

function Car() {
    this._init();
}

car = new Car();
