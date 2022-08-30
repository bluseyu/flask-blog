const express = require("express")
const router = express.Router()
const { db, genid } = require("../db/DbUtils")

// 查询博客

router.get("/search", async (req, res) => {

    /**
     * Keyword 
     * categoryId
     * 
     * 分页
     * page
     * pageSize 分页大小
     **/

    let { keyword, categoryId, page, pageSize } = req.query

    // 如果不传值则为空
    page = page == null ? 1 : page;
    pageSize = pageSize == null ? 10 : pageSize;
    categoryId = categoryId == null ? 0 : categoryId;
    keyword = keyword == null ? "" : keyword

    let params = []
    let whereSqls = []
    if (categoryId != 0) {
        whereSqls.push(" `category_id` = ? ")
        params.push(categoryId)
    }

    if (keyword != "") {
        // 如果标题或内容存在这个关键字，那么就可以被查询
        whereSqls.push(" (`title` LIKE ? OR `content` LIKE ?) ")
        params.push("%" + keyword + "%")
        params.push("%" + keyword + "%")
    }

    let whereSqlStr = "";
    if (whereSqls.length > 0) {
        whereSqlStr = " WHERE " + whereSqls.join(" AND ")
    }

    // 查询分页数据
    let searchSql = " SELECT `id`,`category_id`,`create_time`,`title`,substr(`content`,0,50) AS `content` FROM `blog` " + whereSqlStr + " ORDER BY `create_time` DESC LIMIT ?,? ";
    // 分页算法
    // 1 10（页数1 每页10条） 2,10
    // 0,10(从第0条开始往后查10条) 2,10(从第10条开始往后查10条)
    let searchSqlParams = params.concat([(page - 1) * pageSize, pageSize]);

    // 查询数据总数 计算总共有多少页,数据总数
    let searchCountSql = " SELECT count(*) AS `count` FROM `blog` " + whereSqlStr;
    let searchCountParams = params;

    // 分页数据
    let searchResult = await db.async.all(searchSql, searchSqlParams)
    let countResult = await db.async.all(searchCountSql, searchCountParams)

    console.log(searchSql, countResult)

    if (searchResult.err == null && countResult.err == null) {
        res.send({
            code: 200,
            msg: "查询成功",
            data: {
                keyword,
                categoryId,
                page,
                pageSize,
                rows: searchResult.rows,
                count: countResult.rows[0].count
            }
        })
    } else {
        res.send({
            code: 500,
            msg: "查询失败",
        })
    }

})

// 删除博客 /blog/delete?id=xxx
router.delete("/_token/delete", async (req, res) => {

    let id = req.query.id
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
router.put("/_token/update", async (req, res) => {

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
router.post("/_token/add", async (req, res) => {

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