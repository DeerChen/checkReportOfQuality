'''
@Description: 资源目录
@Author: Senkita
@Date: 2020-06-30 16:15:51
@LastEditors: Senkita
@LastEditTime: 2020-07-01 16:08:09
'''
from pathlib import Path
import sys


class Error(Exception):
    def __init__(self, err):
        '''
        @description: 自定义错误类
        @param {str} [err] - 错误
        @return: None
        @author: Senkita
        '''
        self.err = err

    def __repr__(self):
        return self.err


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = Path(".").resolve()
    return Path(base_path).joinpath(relative_path)


def mkDir(dir_path):
    '''
    @description: 新建文件夹
    @param {Path} dir_path - 目录名
    @return: None
    @author: Senkita
    '''
    # 如果存在，则先删除
    if dir_path.exists():
        deleteDir(dir_path)
        dir_path.mkdir()
    else:
        dir_path.mkdir()


def deleteDir(file_path):
    '''
    @description: 删除文件夹
    @param {Path} file_path - 目录名
    @return: None
    @author: Senkita
    '''
    for sub_file_path in file_path.iterdir():
        # 递归删除
        if sub_file_path.is_dir():
            deleteDir(sub_file_path)
        else:
            sub_file_path.unlink()

    file_path.rmdir()
