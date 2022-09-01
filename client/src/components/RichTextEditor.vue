<!-- 富文本组件 -->
<template>
    <div>
        <Toolbar :editor="editorRef" :defaultConfig="toolbarConfig" :mode="mode"
            style="border-bottom: 1px solid #ccc" />
        <Editor :defaultConfig="editorConfig" :mode="mode" v-model="valueHtml"
            style="min-height: 400px; overflow-y: hidden" @onCreated="handleCreated" @onChange="handleChange" />
    </div>
</template>

<script setup>
import '@wangeditor/editor/dist/css/style.css';
import { ref, reactive, inject, onMounted, onBeforeUnmount, shallowRef } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue';

const server_url = inject("server_url")

// 编辑器实例，必须用 shallowRef，重要！
const editorRef = shallowRef();
// 屏蔽视频上传功能
const toolbarConfig = { excludeKeys: ["uploadVideo"] };
const editorConfig = { placeholder: '请输入内容...' };

// 初始化，避免报错
editorConfig.MENU_CONF = {}
// 图片上传成功后，服务端会返回图片地址
editorConfig.MENU_CONF['uploadImage'] = {
    // 小于10kb的图片不上传，直接转换为base64形式存储在文本上
    base64LimitSize: 10 * 1024, // 10kb
    server: server_url + '/upload/rich_editor_upload',
}
// 插入图片之前执行的一个函数，判断插入图片的路径是否包含http
editorConfig.MENU_CONF['insertImage'] = {
    parseImageSrc: (src) => {
        if (src.indexOf("http") !== 0) {
            return `${server_url}${src}`
        }
        return src
    }
}

const mode = ref("default")

// HTML双向绑定
const valueHtml = ref("")

// 定义属性，初始为空
const props = defineProps({
    modelValue: {
        type: String,
        default: ""
    }
})

// 定义事件，把修改后的数据往外抛，里面是一个数组，修改后往外抛数据
const emit = defineEmits(["update:model-value"])
let initFinished = false

// 等待10ms 赋值给valueHtml
onMounted(() => {
    setTimeout(() => {
        valueHtml.value = props.modelValue;
        initFinished = true;
    }, 10);
});

// 组件销毁时，也及时销毁编辑器，重要！
onBeforeUnmount(() => {
    const editor = editorRef.value;
    if (editor == null) return;
    editor.destroy();
});

// 编辑器回调函数
const handleCreated = (editor) => {
    console.log('created', editor);
    editorRef.value = editor; // 记录 editor 实例，重要！
};
// 在没有初始化时，不要抛出数据
const handleChange = (editor) => {
    if (initFinished) {
        emit("update:model-value", valueHtml.value)
    }
};

</script>

<style lang="scss" scoped>
@import "../assets/scss/variable";
@import "../assets/scss/mixin";
</style>