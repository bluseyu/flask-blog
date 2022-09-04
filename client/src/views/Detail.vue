<template>
    <div class="wrapper">
        <nav>
            <div class="container">
                <a href="" class="logo"><img src="../assets/blog.png" alt=""></a>
                <ul class="nav">
                    <li @click="back">首页</li>
                    <li @click="dashboard">后台</li>
                </ul>
            </div>
        </nav>
        <header class="header">
            <Random />
        </header>
        <main class="main">
            <div class="container">
                <section class="blog">
                    <n-h1>{{ blogInfo.title }}</n-h1>
                    <div class="blog-content">
                        <div class="content" v-html="blogInfo.content"></div>
                    </div>
                </section>
            </div>
        </main>
        <footer class="footer">
            <div class="container">
                <div>Power by bruce Yu</div>
                <div>XICP备XXXXX号-1</div>
            </div>
        </footer>
    </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Random from '../components/Random.vue'

// 路由
const router = useRouter()
const route = useRoute()
const blogInfo = ref({})

const axios = inject("axios")

// 页面载入时读取
onMounted(() => {
    loadBlog()
})

// 获取文章内容
const loadBlog = async () => {
    //获取首页跳转过来的文章ID
    let res = await axios.get("/blog/detail?id=" + route.query.id)
    // 读取文章的数据
    blogInfo.value = res.data.rows[0];
}

// 页面跳转
const back = () => {
    router.push("/")
}
const homePage = () => {
    router.push("/")
}

const dashboard = () => {
    router.push("/login")
}

</script>

<style lang="scss" scoped>
@import "../assets/scss/detail.scss";
</style>