from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = '1%3ya7fn3moipdpcltj(tdfcv5^@lj=t5d&72levvls+y*@_4^'

SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/flaskblog'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
''' 引用路径
要引用路径可以通过BASE_DIR来实现，BASE_DIR指向根目录，如:

BASE_DIR / 'app' # 寻找app目录
'''
