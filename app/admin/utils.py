import os
import uuid
from RealProject.settings import BASE_DIR
from werkzeug.utils import secure_filename


# 判断图片上传路径是否存在
def _file_path(directory_name):
    # BASE_DIR 可以直接获取每个文件夹的路径是否存在
    file_path = BASE_DIR / f'app/admin/static/{directory_name}'

    # 如果图片上传路径不存在则返回路径
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path


# 修改文件名称
def update_filename(f):
    # 处理文件名中的中文
    # secure_filename 会剔除文件中的中文
    # splitext 将文件名拆分成一个列表，如 ['imgname', '.jpg']
    names = list(os.path.splitext(secure_filename(f.filename)))
    # 获取文件名后生成一个UUID，去掉‘-’后重新拼接
    names[0] = ''.join(str(uuid.uuid4()).split('-'))
    # 将重新拼接后的文件名返回
    return ''.join(names)


# 上传文件API接口
# directory_name：文件名称  f：文件对象
def upload_file_path(directory_name, f):
    # 处理过的图片保存路径
    file_path = _file_path(directory_name)
    filename = update_filename(f)
    # file_path / filename：拼接的文件路径
    return file_path / filename, filename