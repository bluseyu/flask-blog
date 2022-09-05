<template>
    <div class="wrapper">
        <nav>
            <div class="container">
                <a href="" class="logo"><img src="../assets/blog.png" alt=""></a>
                <ul class="nav">
                    <li @click="homePage">首页</li>
                    <li>
                        <n-popselect @update:value="searchByCategory" v-model:value="selectedCategory"
                            :options="categortyOptions" trigger="click">
                            <div>分类
                                <span>{{ categoryName }}</span>
                            </div>
                        </n-popselect>
                    </li>
                    <li @click="dashboard">后台</li>
                </ul>
                <div class="actions">
                    <n-space class="menu-sub">
                        <n-button>换肤</n-button>
                        <ul class="menu-sub-item" id="dropdown">
                            <li @click="toggleTheme('light')">白天</li>
                            <li @click="toggleTheme('dark')">黑夜</li>
                            <li @click="toggleTheme('dusk')">薄暮</li>
                        </ul>
                    </n-space>
                    <n-space class="search">
                        <n-input v-model:value="pageInfo.keyword" placeholder="请输入关键字" />
                        <n-button type="primary" ghost @click="loadBlogs(0)">搜索</n-button>
                    </n-space>
                </div>
            </div>
        </nav>
        <header class="header">
            <div class="banner">
                <div class="carousel-item">
                    <img class="carousel-img" src="../assets/img/2.jpg" />
                </div>
                <div class="carousel-item">
                    <img class="carousel-img" src="../assets/img/3.jpg" />
                </div>
                <div class="carousel-item">
                    <img class="carousel-img" src="../assets/img/4.jpg" />
                </div>
            </div>
        </header>
        <main class="main">
            <div class="container">
                <div v-for="(blog, index) in blogListInfo" class="list-item">
                    <n-card :title="blog.title" @click="toDetail(blog)">
                        <!-- {{ blog.content }} -->
                        <div v-html="blog.content" class="blog-intro"></div>
                        <template #footer>
                            <n-space>
                                <div>发布时间: {{ blog.create_time }}</div>
                            </n-space>
                        </template>
                    </n-card>
                </div>
                <n-pagination @update:page="loadBlogs" v-model:page="pageInfo.page" :page-count="pageInfo.pageCount">
                </n-pagination>
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

// 路由
const router = useRouter()
const route = useRoute()

const message = inject("message")
const dialog = inject("dialog")
const axios = inject("axios")

// 选中的分类
const selectedCategory = ref(0)
// 分类选项
const categortyOptions = ref([])
// 文章列表
const blogListInfo = ref([])


const pageInfo = reactive({
    page: 1,
    // 默认每页显示条数
    pageSize: 10,
    // 页数，默认为0
    pageCount: 0,
    count: 0,
    keyword: "",
    categoryId: 0,
})

// 页面载入时读取
onMounted(() => {
    loadCategorys();
    loadBlogs()
})

// 获取博客列表
const loadBlogs = async (page = 0) => {
    // 解决套用UI库翻页组件后，第一次点击其他页不翻页的bug
    if (page != 0) {
        pageInfo.page = page
    }

    // let res = await axios.get("/blog/search")
    // 用模板方式传值，实现分页
    let res = await axios.get(`/blog/search?keyword=${pageInfo.keyword}&page=${pageInfo.page}&pageSize=${pageInfo.pageSize}&categoryId=${pageInfo.categoryId}`)
    let temp_rows = res.data.data.rows;
    for (let row of temp_rows) {
        row.content += "...";
        // 把时间戳转化为正常显示
        let d = new Date(row.create_time)
        row.create_time = `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours()}时${d.getMinutes()}分`
    }
    blogListInfo.value = temp_rows;
    // 获取服务端文章的数目
    pageInfo.count = res.data.data.count;
    // 计算一共有多少页，parseInt:向下取整
    pageInfo.pageCount = parseInt(pageInfo.count / pageInfo.pageSize) + (pageInfo.count % pageInfo.pageSize > 0 ? 1 : 0);
    console.log(res)
}

const categoryName = computed(() => {
    //获取选中的分类
    let selectedOption = categortyOptions.value.find((option) => { return option.value == selectedCategory.value })
    //返回分类的名称
    return selectedOption ? selectedOption.label : ""
})

/**
 * 获取分类列表
 */
const loadCategorys = async () => {
    let res = await axios.get("/category/list")
    categortyOptions.value = res.data.rows.map((item) => {
        return {
            label: item.name,
            value: item.id
        }
    })
    console.log(categortyOptions.value)
}

// 分类筛选
const searchByCategory = (categoryId) => {
    pageInfo.categoryId = categoryId;
    loadBlogs()
}

// 页面跳转
const toDetail = (blog) => {
    // 跳转到详情页及文章对应的ID
    router.push({ path: "/detail", query: { id: blog.id } })
}

const homePage = () => {
    router.push("/")
}

const dashboard = () => {
    router.push("/login")
}


// 样式切换
let toggleTheme = (theme) => {
    localStorage.setItem('data-theme', theme)
    window.document.documentElement.setAttribute('data-theme', theme)
}

</script>

<style lang="scss" scoped>
@import "../assets/scss/home.scss";
</style>