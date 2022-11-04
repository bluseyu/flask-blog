import os
from RealProject.settings import BASE_DIR
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 实例化SQLAlchemy对象，不用甚至任何参数,操作数据库
db = SQLAlchemy()
# 实例化Migrate对象
migrate = Migrate()


# 工厂函数
def create_app(test_config=None):
    # instance_relative_config设置为true，代表开启从文件加载配置，默认为Flase
    app = Flask(__name__, instance_relative_config=True)

    # app.config其实调用的是flask类的config属性，该属性被设置了一个config的类
    # from_mapping则是该config类下的一个方法，用来更新默认配置，返回值为True
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    # 这里判断是否运行时传入了测试配置
    if test_config is None:
        # 数据库配置绝对路径
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        # 如果没有传入，则从py文件加载配置，slilent=True代表文件，文件加载成功返回True
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # 和最开始的配置一致
        app.config.from_mapping(test_config)

    # 在工厂函数内延后注册SQLAlchemy、Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # 递归创建目录，确保项目文件存在
    # 这一段可以去掉，可是使用配置来寻找根目录
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # 注册视图：路由和视图可以正常访问，后面可以将视图放在蓝图文件，然后把蓝图在这里注册一下即可
    # @app.route("/hello")
    # def hello_world():
    #     return "<p>Hello, World!</p>"

    # 引入blog的视图文件
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    # 引入用户视图文件
    from app.auth import views as auth
    app.register_blueprint(auth.bp)
    # 引入后台管理视图
    from app.admin import views as admin
    app.register_blueprint(admin.bp)

    # url引入 首页注册
    app.add_url_rule('/', endpoint='index', view_func=blog.index)

    #注册数据库模型，之后可以同步创建数据库
    from app.blog import models
    from app.auth import models
    from app.admin import models

    # 引入上下文, 传值后，可以在模板中引用inject_category函数的变量
    app.context_processor(inject_category)

    return app


def inject_category():
    # 上下文处理器回调函数
    """
    context_processor上下文处理器在呈现模板之前运行，并且能够将新值注入模板上下文。上下文处理器是返回字典的函数。
    然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并：
    """
    from app.blog.models import Category
    # limit 返回几条数据
    categorys = Category.query.limit(6).all()
    return dict(categorys=categorys)