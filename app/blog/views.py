from flask import Blueprint, render_template, request
from .models import Post, Category, Tag

# 蓝图实例化
bp = Blueprint(
    'blog',
    __name__,
    url_prefix='/blog',
    static_folder='static',  # 定义静态文件夹
    template_folder='templates')  # 定义模板文件夹
'''
用蓝图来绑定route，把URL定义在该应用当中
@bp.route('/')读取的地址是./blog，而不是/
'''

# @bp.route('/')
# def hello_world():
# return 'Hello world'


# 首页视图
# 在 RealProject/__init__.py 引入url后，index()指向127.0.0.1:8000
def index():
    # 获取文章数据
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(page,
                                                              per_page=15,
                                                              error_out=False)
    post_list = pagination.items
    # 文章预览图 随机获取网上图片
    import random
    imgs = [
        'blog/static/img/poster_01.jpg', 'blog/static/img/poster_02.jpg',
        'blog/static/img/poster_03.jpg', 'blog/static/img/poster_04.jpg',
        'blog/static/img/poster_05.jpg', 'blog/static/img/poster_06.jpg',
        'blog/static/img/poster_07.jpg', 'blog/static/img/poster_08.jpg',
        'blog/static/img/poster_09.jpg', 'blog/static/img/poster_10.jpg',
        'blog/static/img/poster_11.jpg', 'blog/static/img/poster_12.jpg',
        'blog/static/img/poster_13.jpg', 'blog/static/img/poster_14.jpg',
        'blog/static/img/poster_15.jpg', 'blog/static/img/poster_16.jpg'
    ]

    for post in post_list:
        post.img = random.sample(imgs, 1)[0]
        # post.img = random.choice(imgs)

    # posts = [1, 2, 3, 4, 5, 6]  # 模板首页显示6篇文章简介
    return render_template('index.html',
                           posts=post_list,
                           pagination=pagination)  # render_template函数用于读取模板文件


# 分类文章列表视图
@bp.route('/category/<int:cate_id>')
def cates(cate_id):
    cate = Category.query.get(cate_id)
    page = request.args.get('page', default=1, type=int)

    pagination = Post.query.filter(Post.category_id == cate_id).paginate(
        page, per_page=10, error_out=False)

    post_list = pagination.items

    return render_template('cate_list.html',
                           cate=cate,
                           cate_id=cate_id,
                           post_list=post_list,
                           pagination=pagination)


# 文章详情视图
@bp.route('/category/<int:cate_id>/<int:post_id>')
def detail(cate_id, post_id):
    cate = Category.query.get(cate_id)
    post = Post.query.get_or_404(post_id)

    # 上一篇 or 下一篇
    #  1)ID：读取当前ID相邻的上一个或下一个ID
    #  2)发布时间：读取当前文章相邻的之前或之后的发布时间
    prev_post = Post.query.filter(Post.id < post_id).order_by(-Post.id).first()
    next_post = Post.query.filter(Post.id > post_id).order_by(Post.id).first()

    return render_template('detail.html',
                           cate=cate,
                           post=post,
                           prev_post=prev_post,
                           next_post=next_post)


# 侧边栏
@bp.context_processor
def inject_archive():
    # 文章归档日期注入上下文
    posts = Post.query.order_by(-Post.add_date)
    dates = set([post.add_date.strftime("%Y年%m月") for post in posts])

    # 标签
    tags = Tag.query.all()
    for tag in tags:
        tag.style = [
            'is-success', 'is-danger', 'is-black', 'is-light', 'is-primary',
            'is-link', 'is-info', 'is-warning'
        ]

    # 最新文章
    new_posts = posts.limit(6)
    return dict(dates=dates, tags=tags, new_posts=new_posts)


# 文章归档详情视图
@bp.route('/category/<string:date>')
def archive(date):
    # 归档页
    import re
    # 正则匹配年月
    regex = re.compile(r'\d{4}|\d{2}')
    dates = regex.findall(date)

    from sqlalchemy import extract, and_, or_
    page = request.args.get('page', 1, type=int)
    # 根据年月获取数据
    archive_posts = Post.query.filter(
        and_(
            extract('year', Post.add_date) == int(dates[0]),
            extract('month', Post.add_date) == int(dates[1])))
    # 对数据进行分页
    pagination = archive_posts.paginate(page, per_page=15, error_out=False)
    return render_template('archive.html',
                           post_list=pagination.items,
                           pagination=pagination,
                           date=date)


# 标签详情视图
@bp.route('/tags/<int:tag_id>')
def tags(tag_id):
    # 标签页
    tag = Tag.query.get(tag_id)
    return render_template('tags.html', post_list=tag.post, tag=tag)


# 搜索视图
@bp.route('/search')
def search():
    # 获取表单输入的数据
    words = request.args.get("words")
    page = request.args.get('page', 1, type=int)
    # filter 查询出多条数据 title 搜索结果只匹配标题
    pagination = Post.query.filter(
        Post.title.like("%" + words + "%")).paginate(page,
                                                     per_page=10,
                                                     error_out=False)
    post_list = pagination.items

    return render_template('search.html',
                           words=words,
                           post_list=post_list,
                           pagination=pagination)
