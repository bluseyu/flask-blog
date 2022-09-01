<template>
    <div class="section">
        <n-button @click="showAddModel = true">添加分类</n-button>
        <n-table :bordered="false" :single-line="false">
            <thead>
                <tr>
                    <th>编号</th>
                    <th>名称</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(category, index) in categoryList">
                    <td>{{ category.id }}</td>
                    <td>{{ category.name }}</td>
                    <td>
                        <n-space>
                            <n-button @click="toUpdate(category)">修改</n-button>
                            <n-button @click="deleteCategory(category)">删除</n-button>
                        </n-space>
                    </td>
                </tr>
            </tbody>
        </n-table>

        <n-modal v-model:show="showAddModel" preset="dialog" title="Dialog">
            <template #header>
                <div>添加分类</div>
            </template>
            <div>
                <n-input v-model:value="addCategory.name" type="text" placeholder="请输入名称"></n-input>
            </div>
            <template #action>
                <div>
                    <n-button @click="add">提交</n-button>
                </div>
            </template>
        </n-modal>

        <n-modal v-model:show="showUpdateModel" preset="dialog" title="Dialog">
            <template #header>
                <div>修改分类</div>
            </template>
            <div>
                <n-input v-model:value="updateCategory.name" type="text" placeholder="请输入名称" />
            </div>
            <template #action>
                <div>
                    <n-button @click="update">提交</n-button>
                </div>
            </template>
        </n-modal>
    </div>
</template>

<script setup>

import { AdminStore } from '../../stores/AdminStore'
import { ref, reactive, inject, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()

const message = inject("message")
const dialog = inject("dialog")
const axios = inject("axios")

const adminStore = AdminStore()

const showAddModel = ref(false)
const showUpdateModel = ref(false)

const categoryList = ref([])
const addCategory = reactive({
    name: ""
})

const updateCategory = reactive({
    id: 0,
    name: ""
})

onMounted(() => {
    loadDatas()
})

const loadDatas = async () => {
    let res = await axios.get("/category/list")
    categoryList.value = res.data.rows
}

// 添加分类
const add = async () => {
    /**
     * 需要将登录后的Token传给服务端，通过服务端的验证
     * 问题：每一次发现需要用到Token，都需要加一个头(headers)，最好是封装一个方法，需要的时候自动添加 headers。
     * 使用拦截器可以满足上述需求，因为需要全局使用，故写在main.js文件中，
     * 使用拦截器后，就无需添加headers了
    */
    //let res = await axios.post("/category/_token/add", { name: addCategory.name }, { headers: { token: adminStore.token } })
    let res = await axios.post("/category/_token/add", { name: addCategory.name })
    // 添加成功后列表自动更新，提示相应的消息
    if (res.data.code == 200) {
        // 需要重新读一遍列表
        loadDatas()
        message.info(res.data.msg)
    } else {
        message.error(res.data.msg)
    }
    // 不管是否添加成功，隐藏添加弹出框
    showAddModel.value = false;
}

// 点击按钮时修改框弹出，弹窗会复制点击的name
const toUpdate = async (category) => {
    showUpdateModel.value = true
    updateCategory.id = category.id
    updateCategory.name = category.name
}

// 提交修改数据
const update = async () => {
    let res = await axios.put("/category/_token/update", { id: updateCategory.id, name: updateCategory.name })
    if (res.data.code == 200) {
        loadDatas()
        message.info(res.data.msg)
    } else {
        message.error(res.data.msg)
    }
    showUpdateModel.value = false;
}

// 删除分类 为防止误删，删除前需要先确认
const deleteCategory = async (category) => {

    dialog.warning({
        title: '警告',
        content: '是否要删除',
        positiveText: '确定',
        negativeText: '取消',
        onPositiveClick: async () => {
            let res = await axios.delete(`/category/_token/delete?id=${category.id}`)
            if (res.data.code == 200) {
                loadDatas()
                message.info(res.data.msg)
            } else {
                message.error(res.data.msg)
            }
        }
    })

}
</script>

<style lang="scss" scoped>
@import "../../assets/scss/variable";
@import "../../assets/scss/mixin";

.section {
    width: 90%;
    margin: 30px auto;
}
</style>