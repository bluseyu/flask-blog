const express = require("express")
const router = express.Router()
const { db, genid } = require("../db/DbUtils")

// 查询博客

// 删除博客
router.delete("/blog/delete", async (req, res) => {

    let { id } = req.query.id
    const delete_sql = "DELETE FROM `blog` WHERE `id` = ?"
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

// 修改博客
router.put("/update", async (req, res) => {

    // 由前端传过来的数据 id(修改哪一篇), 标题(title)、分类(category ID) 、内容（content）
    let { id, title, categoryId, content } = req.body;

    // 文章的创建时间
    let create_time = new Date().getTime();

    // SQL数据记录
    const update_sql = "UPDATE `blog` SET `title` = ?, `content` = ?, `category_id` = ? WHERE `id` = ?"
    // 定义参数 对应数据的字段
    let params = [title, content, categoryId, id]
    // 插入语句
    let { err, rows } = await db.async.run(update_sql, params)

    // 判断有没有正确插入
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

// 添加博客
router.post("/add", async (req, res) => {

    // 由前端传过来的数据 标题(title)、分类(category ID) 、内容（content）
    let { title, categoryId, content } = req.body;
    // 生成文章ID
    let id = genid.NextId();
    // 生成文章的创建时间
    let create_time = new Date().getTime();

    // SQL数据记录
    const insert_sql = "INSERT INTO `blog`(`id`, `title`, `category_id`, `content`, `create_time`) VALUES (?,?,?,?,?)"
    // 定义参数 对应数据的字段
    let params = [id, title, categoryId, content, create_time]
    // 插入语句
    let { err, rows } = await db.async.run(insert_sql, params)

    // 判断有没有正确插入
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