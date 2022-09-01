<template>
    <div class="section">
        <n-tabs default-value="oasis" v-model:value="tabValue" justify-content="start" type="line">
            <n-tab-pane name="oasis" tab="oasis">
                helg
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

            <n-tab-pane name="jay" tab="周杰伦">爱起来</n-tab-pane>
        </n-tabs>
        {{ addArticle.content }}
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

//分类选项
const categortyOptions = ref([])

// 启动时读取服务端数据 分类、博客
onMounted(() => {
    loadCategorys()
})

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

// 需要写一个组件封装富文本
</script>

<style lang="scss" scoped>
@import "../../assets/scss/variable";
@import "../../assets/scss/mixin";

.section {
    width: 90%;
    margin: 30px auto;
}
</style>