/** 
"multer" 上传功能中间件
"sqlite3" 数据库
"uuid" 很难重复的ID生成
*/

const express = require("express")
const multer = require("multer")
const app = express();
const { db, genid } = require("./db/DbUtils")
const port = 8080

// 开放跨域请求
app.use(function (req, res, next) {
    // 设置允许跨域的域名，*代表允许任意域名跨域
    res.header("Access-Control-Allow-Origin", "*");
    // 允许的headre类型
    res.header("Access-Control-Allow-Header", "*");
    // 跨域允许的请求方式
    res.header("Acess-Control-Allow-Methods", "DELETE,PUT,POST,GET,OPTIONS");
    if (req.method == "OPTIONS") res.sendStatus(200);   // 让options尝试请求快速结束
    else next();
});

// 上传
app.use(express.json())
const update = multer({
    dest:"./public/upload/temp"
})
app.use(update.any())

// 注册路由
app.use("/test", require("./routers/TestRouter"))
app.use("/admin", require("./routers/AdminRouter"))

app.get("/", (req, res) => { 
    res.send("Hello world");
})

app.listen(port, () => {
    console.log(`启动成功 : http://localhost:${port}/`)
})
 