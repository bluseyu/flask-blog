import functools
from flask import Blueprint, flash, render_template, request, redirect, url_for, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db
from ..models import User
from ..forms import LoginForm, RegisterForm

# 蓝图实例化，也需要在工厂函数里注册
bp = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
    static_folder='../static',  # 定义静态文件夹，相对路径
    template_folder='../templates')  # 定义模板文件夹


# 在模板中获取用户信息 g是全局对象
@bp.before_app_request
def load_logged_in_user():
    # 每个请求之前都回去session中查看user_id来获取用户
    user_id = session.get('user_id')

    # 注册用户允许登录后查看的url, 无法查看管理页
    urls = ['/auth/']

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(int(user_id))

        # 权限判断
        # 1: 允许访问，0：不允许访问
        if g.user.is_super_user and g.user.is_active:
            # 如果是超级用户&活跃用户,则权限标识为1
            g.user.has_perm = 1
        elif not g.user.is_super_user and g.user.is_active and not g.user.is_staff and request.path in urls:
            # 如果不是超级用户&是活跃用户&没有被锁定&在urls中，则权限标识为1
            g.user.has_perm = 1
        else:
            g.user.has_perm = 0


# 实现login_required装饰器 登录权限
def login_required(view):
    # 限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            redirect_to = f"{url_for('auth.login')}?redirect_to={request.path}"
            return redirect(redirect_to)
            # return redirect(url_for('auth.login'))

        # 登录成功后对权限进行判断处理
        if not g.user.has_perm:
            return '<h1>无权限查看当前页面！</h1>'

        return view(**kwargs)

    return wrapped_view


# 创建登录视图
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录
    redirect_to = request.args.get('redirect_to')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        session.clear()
        session['user_id'] = user.id
        # 判断用是否没有登录就直接进入用户中心
        if redirect_to is not None:
            return redirect(redirect_to)
        return redirect('/')
    return render_template('login.html', form=form)


# 创建注册视图
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        session.clear()
        session['user_id'] = user.id
        return redirect('/')
    return render_template('register.html', form=form)


# 退出登录
@bp.route('/logout')
def logout():
    # 注销
    session.clear()
    return redirect('/')


# 用户中心视图
@bp.route('/')
@login_required
def userinfo():
    return render_template('userinfo.html')