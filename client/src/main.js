import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import naive from 'naive-ui'
import { createDiscreteApi } from 'naive-ui'
import { router } from './common/router'
import { createPinia } from "pinia"
import axios from 'axios'
import { AdminStore } from './stores/AdminStore'

// 访问服务端地址
axios.defaults.baseURL = "http://localhost:8080"
// 独立API 提示消息
const { message, notification, dialog } = createDiscreteApi(["message", "dialog", "notification"])

const app = createApp(App)

// 需要让其他页面也能访问 ，全局属性
app.provide("axios", axios)
app.provide("message", message)
app.provide("notification", notification)
app.provide("dialog", dialog)
app.provide("server_url", axios.defaults.baseURL)

app.use(naive)
app.use(createPinia())
app.use(router)

/**
 * 拦截器功能实现
 * 注入adminStore函数后进行实例化
 * 每一个i请求都会先执行这段代码，给headers添加一个token，token来自 adminStore
 * 登录成功后，就有token值传入，每一个请求都携带一个token。
 * 也可以不用全局，则在每个需要的地方写一次，相对比较麻烦。
 * 使用token拦截，需要先载入Pinia，故代码必须放在 `app.use(createPinia())`之后
*/
const adminStore = AdminStore()
axios.interceptors.request.use((config) => {
    //每次请求都在headers中添加token
    config.headers.token = adminStore.token
    return config
})

app.mount('#app')

window.document.documentElement.setAttribute('data-theme', localStorage.getItem('data-theme') ? localStorage.getItem('data-theme') : '')