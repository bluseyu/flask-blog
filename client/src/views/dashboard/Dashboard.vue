<template>
    <div class="main-panel">
        <div class="title">后台管理系统</div>
        <div class="menus">
            <div v-for="(menu, index) in menus" @click="toPage(menu)">
                {{ menu.name }}
            </div>
        </div>
        <div class="content">
            <router-view></router-view>
        </div>
    </div>
</template>

<script setup>
import { AdminStore } from '../../stores/AdminStore'
import { ref, reactive, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const message = inject("message")
const axios = inject("axios")

const adminStore = AdminStore()

//菜单
let menus = [
    { name: "返回首页", href: "/" },
    { name: "文章管理", href: "/dashboard/article" },
    { name: "分类管理", href: "/dashboard/category" },
    { name: "退出", href: "logout" },
];

//路由跳转
const toPage = (menu) => {
    if (menu.href == 'logout') {
        router.push("/login")
    } else {
        router.push(menu.href)
    }
}

</script>

<style lang="scss" scoped>
@import "../../assets/scss/variable";
@import "../../assets/scss/mixin";

.main-panel {
    display: flex;
    margin: 0 auto;
    width: 100%;
    color: #64676a;
}

.menus {
    position: fixed;
    padding: 20px 0;
    box-sizing: border-box;
    line-height: 55px;
    text-align: center;
    width: 180px;
    height: 100vh;
    background: white;
    border-right: 1px solid #dadada;

    div {
        cursor: pointer;

        &:hover {
            color: #fd760e;
        }

        &:first-child {
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgb(10 10 10 / 10%);
        }
    }
}

.content {
    width: calc(100% - 180px);
    margin-left: 180px;
}

.title {
    font-size: 65px;
    font-weight: bold;
    text-align: right;
    position: fixed;
    color: rgba(0, 0, 0, 20%);
    right: calc((100vw - 1500px) / 2);
    bottom: 20px;
}
</style>