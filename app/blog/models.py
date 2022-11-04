from datetime import datetime, timedelta
from RealProject import db
from enum import IntEnum
from sqlalchemy.dialects.mysql import LONGTEXT


# 创建一个数据库基类模型
class BaseModel(db.Model):
    # __abstract__ 为 True 说明是基类模型
    __abstract__ = True

    china_time = datetime.utcnow() + timedelta(hours=8)

    add_date = db.Column(
        db.DateTime,
        nullable=False,
        default=china_time,
    )  # 创建时间，utcnow是国际标准时间，比北京时间慢8小时
    pub_date = db.Column(db.DateTime,
                         default=china_time,
                         onupdate=china_time,
                         nullable=False)  # 更新时间


class PostPublishType(IntEnum):
    """ 文章发布类型
    """
    draft = 1  # 草稿
    show = 2  # 发布


""" 注册一个模型类: 分类表
创建基类后，class Category(db.Model)调整为class Category(BaseModel)
Category类中的 add_date、pub_date 就可以删除了，
把BaseMOdel作为Category类的参数后，
会自动在该表引入 add_date 和 pub_date 字段
"""


# 创建一个Category：分类模型
class Category(BaseModel):

    #   db.Integer 定义了数据库类型
    id = db.Column(db.Integer, primary_key=True)
    #   nullable=False，该字段是必填的，不能为空，name的数据类型为 String长度128字节
    name = db.Column(db.String(128), nullable=False)
    #   nullable=True，该字段可以为空
    icon = db.Column(db.String(128), nullable=True)
    # 不同数据模型的关联, 反向关联查询（关联文章），不会进入数据库
    # post = db.relationship('Post', back_populates= 'category', )
    # post赋值后，不会在数据库产生记录，可用于查询数据
    post = db.relationship('Post', backref='category', lazy=True)

    # add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, )
    # pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


# 多对多关系帮助器表
tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id',
              db.Integer,
              db.ForeignKey('post.id'),
              primary_key=True))


# 创建文章模型
class Post(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    # LONGTEXT是MySQL独有的一个类型，用于长文本，需独立引入
    content = db.Column(LONGTEXT, nullable=False)
    has_type = db.Column(db.Enum(PostPublishType),
                         server_default='show',
                         nullable=False)
    #  ForeignKey('category.id')中的'category'就是上面 post里的backref='category'
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            nullable=False)
    # 多对多关系, secondary字段关联多对多关系器表
    tags = db.relationship('Tag',
                           secondary=tags,
                           lazy='subquery',
                           backref=db.backref('post', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title


# 创建文章标签模型
class Tag(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    #   unique=True, 不允许出现重复的值
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return self.name
