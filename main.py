'''
@Description: 主函数入口
@Author: Senkita
@Date: 2020-06-25 23:07:41
@LastEditors: Senkita
@LastEditTime: 2020-07-01 17:40:34
'''
from src.processor import ExcelProcessing, PDFProcessing
from src.ui import UI
from utils.utils import mkDir, Error
from pathlib import Path
import sys


def main():
    ui = UI()
    try:
        template_file_path, sn_file_path = ui.user_interface()

        e = ExcelProcessing(sn_file_path)
        # 使用zip要避免生成器耗尽
        machine_list = list(e.get_machine_list())

        if machine_list == []:
            raise Error('SN.xlsx内未填写内容!')

        # 生成结果文件夹
        mkDir(Path('./result'))
        length = len(machine_list)
        n = 0
        pb_window, pb = ui.progress_bar(length)
        event, value = pb_window.Read(timeout=0)

        for model, sn in machine_list:
            p = PDFProcessing(template_file_path, model, sn)
            p.process()
            n += 1
            pb.UpdateBar(n)

        pb_window.Close()
        ui.popup('完成!', '任务已完成，请在result文件夹中查看!')
    except PermissionError:
        ui.popup('错误!', '文件夹被占用!')
    except FileNotFoundError:
        ui.popup('错误!', '文件不存在!')
    except Error as e:
        ui.popup('错误!', e)
    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
