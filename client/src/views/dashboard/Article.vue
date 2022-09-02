<template>
    <div class="section">
        <!-- 标签页双向绑定 -->
        <n-tabs v-model:value="tabValue" justify-content="start" type="line">
            <n-tab-pane name="list" tab="文章列表">
                <div v-for="(blog, index) in blogListInfo">
                    <n-card :title="blog.title">
                        {{ blog.content }}
                        <template #footer>
                            <n-space>
                                <div>发布时间: {{ blog.create_time }}</div>
                                <!-- 点击修改跳到修改页面 -->
                                <n-button @click="toUpdate(blog)">修改</n-button>
                                <n-button>删除</n-button>
                            </n-space>
                        </template>
                    </n-card>
                </div>
                <n-space>
                    <n-button @click="toPage(pageNum)" v-for="pageNum in pageInfo.pageCount">
                        <!-- <div :style="'color:' + (pageNum == pageInfo.page ? 'red' : '')">{{ pageNum }}</div> -->
                        <div :class="(pageNum == pageInfo.page ? 'active' : '')">{{ pageNum }}</div>
                    </n-button>
                </n-space>
            </n-tab-pane>

            <n-tab-pane name="add" tab="添加文章">
                <n-form>
                    <n-form-item label="标题">
                        <n-input v-model:value="addArticle.title" placeholder="请输入标题" />
                    </n-form-item>
                    <n-form-item label="分类">
                        <n-select v-model:value="addArticle.categoryId" :options="categortyOptions" />
                    </n-form-item>
                    <n-form-item label="内容">
                        <rich-text-editor v-model="addArticle.content"></rich-text-editor>
                    </n-form-item>
                    <n-form-item label="">
                        <n-button @click="add">提交</n-button>
                    </n-form-item>
                </n-form>
            </n-tab-pane>

            <n-tab-pane name="update" tab="修改">
                <n-form>
                    <n-form-item label="标题">
                        <n-input v-model:value="updateArticle.title" placeholder="请输入标题" />
                    </n-form-item>
                    <n-form-item label="分类">
                        <n-select v-model:value="updateArticle.categoryId" :options="categortyOptions" />
                    </n-form-item>
                    <n-form-item label="内容">
                        <rich-text-editor v-model="updateArticle.content"></rich-text-editor>
                    </n-form-item>
                    <n-form-item label="">
                        <n-button @click="update">提交</n-button>
                    </n-form-item>
                </n-form>
            </n-tab-pane>
        </n-tabs>
        <!-- {{ addArticle.content }} -->
    </div>
</template>

<script setup>
import { AdminStore } from '../../stores/AdminStore'
import { ref, reactive, inject, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import RichTextEditor from '../../components/RichTextEditor.vue'

const router = useRouter()
const route = useRoute()

const message = inject("message")
const dialog = inject("dialog")
const axios = inject("axios")

const adminStore = AdminStore()

// 添加文章需要传的内容
const addArticle = reactive({
    categoryId: 0,
    title: "",
    content: "",
})

// 修改文章需要传的内容
const updateArticle = reactive({
    id: 0,
    categoryId: 0,
    title: "",
    content: "",
})

// 定义变量：分类选项、列表信息、页面信息
const categortyOptions = ref([])
const blogListInfo = ref([])

// 默认tabValue的值为list
const tabValue = ref("list")
const pageInfo = reactive({
    page: 1,
    // 默认每页显示条数
    pageSize: 3,
    // 页数，默认为0
    pageCount: 0,
    // 文章数目服务端会传过来，默认为0
    count: 0
})

// 启动时读取服务端数据 分类、博客
onMounted(() => {
    loadBlogs()
    loadCategorys()
})

// 在现实的内容后加`...`
const loadBlogs = async () => {
    // let res = await axios.get("/blog/search")
    // 用模板方式传值，实现分页
    let res = await axios.get(`/blog/search?page=${pageInfo.page}&pageSize=${pageInfo.pageSize}`)
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

// 读取分类
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

// 新增文章提交 文章提交逻辑不严谨，需要全部不为空才能提交
const add = async () => {
    let res = await axios.post("/blog/_token/add", addArticle)
    if (res.data.code == 200) {
        message.info(res.data.msg)
        addArticle.title = ""
        addArticle.categoryId = ""
    } else {
        message.error(res.data.msg)
    }
}

// 分页跳转
const toPage = async (pageNum) => {
    pageInfo.page = pageNum
    loadBlogs()
}

// tab页切换到修改页
const toUpdate = async (blog) => {
    tabValue.value = "update"
    // 不能直接复制添加文章时的字段属性，要从服务端去读，直接复制会导致文章内容只显示部分，且分类读取不到
    // 从服务端获取文章数据
    let res = await axios.get("/blog/detail?id=" + blog.id)
    // 将服务端的数据填充到页面，最后的属性是数据库的字段名
    updateArticle.id = blog.id
    updateArticle.title = res.data.rows[0].title
    updateArticle.content = res.data.rows[0].content
    updateArticle.categoryId = res.data.rows[0].category_id
}

// 提交修改后的数据
const update = async () => {
    let res = await axios.put("/blog/_token/update", updateArticle)
    if (res.data.code == 200) {
        message.info(res.data.msg)
    } else {
        message.error(res.data.msg)
    }
}

// 需要写一个组件封装富文本
</script>

<style lang="scss" scoped>
@import "../../assets/scss/variable";
@import "../../assets/scss/mixin";

.section {
    width: 90%;
    margin: 30px auto;
}

button {
    & {
        .active {
            color: green;
            font-weight: 600;
        }
    }
}
</style>