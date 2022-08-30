const sqlite3 = require("sqlite3").verbose()
const path = require("path")
const GenId = require("../utils/SnowFlake")

var db = new sqlite3.Database(path.join(__dirname, "blog.sqlite3"))
const genid = new GenId({ WorkerId: 1 })

// Promise封装 调用数据库的方法
db.async = {}

db.async.all = (sql, params) => {
    // 异步处理变为同步
    return new Promise((resolve, reject) => {
        // 执行数据库语句，回调函数
        db.all(sql, params, (err, rows) => {
            resolve({ err, rows })
        })
    })
}

db.async.run = (sql, params) => {
    return new Promise((resolve, reject) => {
        db.run(sql, params, (err, rows) => {
            resolve({ err, rows })
        })
    })
}

module.exports = { db, genid }