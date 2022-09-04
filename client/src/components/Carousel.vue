<template>
    <div class="banner">
        <div id="box" onmouseover="stop()" onmouseout="start()">
            <div id="red" class="slide"></div>
            <div id="green" class="slide"></div>
            <div id="blue" class="slide"></div>
        </div>
    </div>
</template>

<script>
const param = {
    picWidth: 100,
    time: 3000
};
const arr = document.getElementsByClassName("slide");

onload = function () {
    for (let i = 0; i < arr.length; i++) {
        arr[i].style.left = i * param.picWidth + "px";
    }
}

let LeftMove = () => {
    for (let i = 0; i < arr.length; i++) {
        let left = parseFloat(arr[i].style.left);
        left -= 2;
        const width = param.picWidth;
        if (left <= -width) {
            //当图片完全走出显示框，拼接到末尾
            left = (arr.length - 1) * width;
            clearInterval(moveId);
        }
        arr[i].style.left = left + "px";
    }
}

//设置一个10毫秒定时器
let divInterval = () => {
    moveId = setInterval(LeftMove, 10);
}

//设置一个3秒的定时器
timeId = setInterval(divInterval, param.time);

let stop = () => {
    clearInterval(timeId);
}
let start = () => {
    stop();
    timeId = setInterval(divInterval, param.time);
}

//页面失去焦点停止
onblur = function () {
    stop();
}
//页面获取焦点时开始
onfocus = function () {
    start();
}
</script>

<style>
#box {
    width: 100px;
    height: 100px;
    border: 1px solid black;
    position: relative;
    overflow: hidden;
}

#red {
    background-color: red;
    width: 100px;
}

#green {
    background-color: green;
    width: 100px;
}

#blue {
    background-color: blue;
    width: 100px;
}

.slide {
    width: 100px;
    height: 100px;
    position: absolute;
}
</style>