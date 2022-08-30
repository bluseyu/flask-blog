const express = require("express")
const router = express.Router()
const { db, genid } = require("../db/DbUtils")

// 列表接口
router.get("/list", async (req, res) => {

    const search_sql = "SELECT * FROM `category` "
    let { err, rows } = await db.async.run(search_sql, [])

    if (err == null) {
        res.send({
            code: 200,
            msg: "查询成功",
            rows // rows:rows
        })
    } else {
        res.send({
            code: 500,
            msg: "查询失败"
        })
    }

})


// 删除接口  /category/_token/delete?id=xxx
router.delete("/_token/delete", async (req, res) => {

    let { id } = req.query.id
    const delete_sql = "DELETE FROM `category` WHERE `id` = ?"
    let { err, rows } = await db.async.run(delete_sql, [id])

    if (err == null) {
        res.send({
            code: 200,
            msg: "删除成功"
        })
    } else {
        res.send({
            code: 500,
            msg: "删除失败"
        })
    }

})

// 修改接口 需要登录校验
router.put("/_token/update", async (req, res) => {

    /** 
     * Token是唯一的，每次登录都会产生一个唯一的值，之前的值将不存在如果要用这个接口，需要前端把token传过来进行验证，如果能查（已存在），说明已登录，不存在则无法登录
     * 在需要登录校验的接口都需要添加这一段代码，会比较麻烦，可以写一个中间件，在app.js
    

    let { token } = req.headers;
    console.log(token)

    let admin_token_sql = "SELECT * FROM `admin` WHERE `token` = ?"
    let adminResult = await db.async.all(admin_token_sql, [token])
    if (adminResult.err != null || adminResult.rows.length == 0) {
        res.send({
            code: 403,
            msg: "请先登录"
        })
    }
    **/

    let { id, name } = req.body
    const update_sql = "UPDATE `category` SET `name` = ? WHERE `id` = ?"
    let { err, rows } = await db.async.run(update_sql, [name, id])

    if (err == null) {
        res.send({
            code: 200,
            msg: "修改成功"
        })
    } else {
        res.send({
            code: 500,
            msg: "修改失败"
        })
    }

})

// 添加接口
router.post("/_token/add", async (req, res) => {

    let { name } = req.body
    const insert_sql = "INSERT INTO `category` (`id`, `name`) VALUES (?,?)"
    let { err, rows } = await db.async.run(insert_sql, [genid.NextId(), name])

    if (err == null) {
        res.send({
            code: 200,
            msg: "添加成功"
        })
    } else {
        res.send({
            code: 500,
            msg: "添加失败"
        })
    }

})


module.exports = router