<template>
    <div class="banner">
        <img src="../assets/img/3.jpg" class="carousel-img">
    </div>
</template>

<script>
import { ref, reactive, inject, onMounted, computed } from 'vue'

let pic = document.querySelector('img');
let path = `../src/assets/img/`;

function getRandom(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
let random = getRandom(1, 5);

let randomPic = () => {
    return pic.src = `${path}${random}.jpg`;
}

// 页面载入时读取
onMounted(() => {
    randomPic();
})
</script>

<style lang="scss" scoped>
.carousel-img {
    width: 100%;
    height: 360px;
    object-fit: cover;
}
</style>