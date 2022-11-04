# -*- coding: UTF-8 -*-
from flask import (Blueprint, render_template, request, flash, redirect,
                   url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db
from app.auth.views.auth import login_required
from app.auth.models import User
from app.blog.models import Category, Post, Tag
from .forms import CategoryForm, PostForm, TagForm, CreateUserForm
import markdown

bp = Blueprint('admin',
               __name__,
               url_prefix='/admin',
               template_folder='templates',
               static_folder='static')


# 创建蓝图后，需在app里挂载
# 在RealProject/__init.py中注册
@bp.route('/')
# 装饰器 验证用户是否已登录
@login_required
# 模板路径追加admin，把名称相同的文件隔离开
def index():
    return render_template('admin/index.html')


""" 分类管理视图
category:      查看分类列表
category.add:  添加分类
category.edit: 编辑分类
category.del:  删除分类
"""


@bp.route('/category')
@login_required
def category():
    # 设置分页信息
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(-Category.add_date).paginate(
        page, per_page=10, error_out=False)
    category_list = pagination.items

    # 可以通过for循环获取页码值
    # print([i for i in pagination.iter_pages()])

    # 获取分页数据
    # print(pagination.items)

    return render_template('admin/category.html',
                           category_list=category_list,
                           pagination=pagination)


# 分类添加视图
@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def category_add():
    # 引入表单form类后实例化
    form = CategoryForm()
    # 判断提交的是哪一种请求模式
    if form.validate_on_submit():
        # 数据通过验证后则执行下列语句
        category = Category(name=form.name.data, icon=form.icon.data)
        db.session.add(category)
        db.session.commit()
        flash(f'{form.name.data}分类添加成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)


# 分类编辑视图 编辑哪一条要传入这一条的主键
@bp.route('/category/edit/<int:cate_id>', methods=['GET', 'POST'])
@login_required
# 编辑与添加可以公用表单 字段一致，编辑的核心是回显消息
def category_edit(cate_id):
    # 编辑博客分类
    cate = Category.query.get(cate_id)
    # 实例化表单 设置回显
    form = CategoryForm(name=cate.name, icon=cate.icon)

    if form.validate_on_submit():
        # 后台数据修改方法 重新赋值 form获取前端表单提交的值
        cate.name = form.name.data
        cate.icon = form.icon.data
        db.session.add(cate)
        db.session.commit()
        flash(f'{form.name.data}分类修改成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)


# 分类删除视图
@bp.route('/category/delete/<int:cate_id>')
@login_required
# 编辑与添加可以公用表单 字段一致，编辑的核心是回显消息
def category_del(cate_id):
    cate = Category.query.get(cate_id)
    if cate:
        db.session.delete(cate)
        db.session.commit()
        flash(f'{cate.name}分类删除成功')
        return redirect(url_for('admin.category'))


""" 文章管理视图
article:      查看文章列表
article.add:  添加文章
article.edit: 编辑文章
article.del:  删除文章
"""


@bp.route('/article')
@login_required
def article():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    # 对文章进行倒序排列并对其分页
    pagination = Post.query.order_by(-Post.add_date).paginate(page,
                                                              per_page=10,
                                                              error_out=False)
    post_list = pagination.items
    return render_template('admin/article.html',
                           post_list=post_list,
                           pagination=pagination)


# 添加文章视图
@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    # 增加文章
    form = PostForm()
    # 获取分类数据
    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    # 获取tag数据
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        # 一对多
        post = Post(
            title=form.title.data,
            desc=form.desc.data,
            has_type=form.has_type.data,
            category_id=int(form.category_id.data),
            # content=form.content.data,
            content=markdown.markdown(
                form.content.data,
                extensions=[
                    # toc 自动生成目录
                    'markdown.extensions.toc',
                    # fenced_code 格式化代码
                    'markdown.extensions.fenced_code',
                    # tables 解析表格
                    'markdown.extensions.tables',
                    # extra 含很多拓展
                    'markdown.extensions.extra',
                    # codehilite 语法高亮
                    'markdown.extensions.codehilite',
                ],
                safe_mode=True,
                enable_attributes=False))
        #  多对多
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章添加成功')
        return redirect(url_for('admin.article'))

    return render_template('admin/article_form.html', form=form)


@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    # 修改文章 回显数据
    post = Post.query.get(post_id)
    tags = [tag.id for tag in post.tags]
    form = PostForm(title=post.title,
                    desc=post.desc,
                    category_id=post.category.id,
                    has_type=post.has_type.value,
                    content=post.content,
                    tags=tags)

    form.category_id.choices = [(v.id, v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id, v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        # 这里才是修改文章的逻辑
        post.title = form.title.data
        post.desc = form.desc.data
        post.has_type = form.has_type.data
        post.category_id = int(form.category_id.data)
        # post.content = form.content.data
        post.content = markdown.markdown(form.content.data,
                                         extensions=[
                                             'markdown.extensions.toc',
                                             'markdown.extensions.fenced_code',
                                             'markdown.extensions.tables',
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                         ],
                                         safe_mode=True,
                                         enable_attributes=False)
        post.tags = [Tag.query.get(tag_id)
                     for tag_id in form.tags.data]  # 一对多保存
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章修改成功')
        return redirect(url_for('admin.article'))
    # 渲染表单
    return render_template('admin/article_form.html', form=form)


@bp.route('/article/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_del(post_id):
    # 删除文章
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title}文章删除成功')
        return redirect(url_for('admin.article'))


""" 标签管理视图
tag:      查看标签列表
tag.add:  添加标签
tag.edit: 编辑标签
tag.del:  删除标签
"""


@bp.route('/tag')
@login_required
def tag():
    # 查看标签列表
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(-Tag.add_date).paginate(page,
                                                            per_page=15,
                                                            error_out=False)
    tag_list = pagination.items
    return render_template('admin/tag.html',
                           tag_list=tag_list,
                           pagination=pagination)


@bp.route('/tag/add', methods=['GET', 'POST'])
@login_required
def tag_add():
    # 增加标签, 实例化标签类
    form = TagForm()
    if form.validate_on_submit():
        # 赋值 从表单获取tag数据
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}添加成功')
        return redirect(url_for('admin.tag'))
    # GET请求进入时展示的渲染页面
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/edit/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_edit(tag_id):
    # 修改标签 通过主键获取tag信息
    tag = Tag.query.get(tag_id)
    form = TagForm(name=tag.name)
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}修改成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html', form=form)


@bp.route('/tag/del/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_del(tag_id):
    # 删除标签
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash(f'{tag.name}删除成功')
        return redirect(url_for('admin.tag'))


""" 用户管理视图
user:      查看用户列表
user.add:  添加用户
user.edit: 编辑用户
user.del:  删除用户
"""


@bp.route('/user')
@login_required
def user():
    # 查看用户列表
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(-User.add_date).paginate(page,
                                                              per_page=10,
                                                              error_out=False)
    user_list = pagination.items
    return render_template('admin/user.html',
                           user_list=user_list,
                           pagination=pagination)


# 添加修改前要先创建模型相关的表单
@bp.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    form = CreateUserForm()

    # 先获取用户输入数据，验证前端传过来的数据的有效性
    if form.validate_on_submit():
        # 头像处理逻辑 需在表单提交后
        # 放在最外层则走GET请求，一开始就执行了
        from .utils import upload_file_path
        f = form.avatar.data
        avatar_path, filename = upload_file_path('avatar', f)
        f.save(avatar_path)

        user = User(username=form.username.data,
                    password=generate_password_hash(form.password.data),
                    avatar=f'avatar/{filename}',
                    is_super_user=form.is_super_user.data,
                    is_active=form.is_active.data,
                    is_staff=form.is_staff.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}添加成功！')
        return redirect(url_for('admin.user'))

    return render_template('admin/user_form.html', form=form)


@bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    # 修改用户信息
    user = User.query.get(user_id)
    form = CreateUserForm(username=user.username,
                          password=user.password,
                          avatar=user.avatar,
                          is_super_user=user.is_super_user,
                          is_active=user.is_active,
                          is_staff=user.is_staff)

    # 若这一句不添加，则修改密码后用户将无法登录，提示密码错误
    form.password.default = f'{user.password}'

    if form.validate_on_submit():
        user.username = form.username.data
        # 如果为空，则用户密码等于之前的密码，等同于不做修改
        if not form.password.data:
            user.password = user.password
        # 不为空，相当于重新输入新的密码
        else:
            user.password = generate_password_hash(form.password.data)

        from .utils import upload_file_path
        # 获取图片对象的数据
        f = form.avatar.data
        # 如果表单图片的值等于传过来的路径，则不做任何修改
        if user.avatar == f:
            user.avatar = user.avatar
        # 如果修改，则从表单获取新的数据，并保存
        else:
            avatar_path, filename = upload_file_path('avatar', f)
            f.save(avatar_path)
            user.avatar = f'avatar/{filename}'

        user.is_super_user = form.is_super_user.data
        user.is_active = form.is_active.data
        user.is_staff = form.is_staff.data
        db.session.add(user)
        db.session.commit()
        flash(f'{user.username}修改成功！')
        return redirect(url_for('admin.user'))

    return render_template('admin/user_form.html', form=form, user=user)


@bp.route('/user/del/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_del(user_id):
    # 删除标签
    user = User.query.get(user_id)
    if tag:
        db.session.delete(user)
        db.session.commit()
        flash(f'{user.username}删除成功')
        return redirect(url_for('admin.user'))


#后端图片上传接口
@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    # 上传图片
    if request.method == 'POST':
        # 获取一个文件类型 request.files
        f = request.files.get('upload')
        file_size = len(f.read())
        f.seek(0)  # reset cursor position to beginning of file

        if file_size > 2048000:  # 限制上传大小为2M
            return {
                'code': 'err',
                'message': '文件超过限制2048000字节',
            }

        from .utils import upload_file_path
        upload_path, filename = upload_file_path('upload', f)
        f.save(upload_path)
        return {'code': 'ok', 'url': f'/admin/static/upload/{filename}'}
