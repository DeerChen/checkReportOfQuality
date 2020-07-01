'''
@Description: 文件选择界面
@Author: Senkita
@Date: 2020-06-30 16:05:44
@LastEditors: Senkita
@LastEditTime: 2020-07-01 17:06:54
'''
import PySimpleGUI as sg
from utils.utils import resource_path
from pathlib import Path


class UI:
    def warning_popup(self, cue_word):
        '''
        @description: 警告框
        @param {str} [cue_word] - 提示词
        @return: {function}
        @author: Senkita
        '''
        warningPopup = sg.Popup(
            '警告!', cue_word, icon=resource_path(Path('./assets/ico').joinpath('sn.ico'))
        )
        if warningPopup in (None, 'OK'):
            return self.user_interface()

    def user_interface(self):
        '''
        @description: 文件选择界面
        @param {type}
        @return: {str}
        @author: Senkita
        '''
        layout = [
            [sg.T('模板pdf路径:')],
            [
                sg.I(
                    default_text='./template/template.pdf',
                    size=(40, None),
                    disabled=True,
                ),
                sg.FileBrowse(button_text='打开', file_types=(('pdf文件', '*.pdf'),)),
            ],
            [sg.T('SN文件路径:')],
            [
                sg.I(
                    default_text='./template/sn.xlsx', size=(40, None), disabled=True,
                ),
                sg.FileBrowse(button_text='打开', file_types=(('Excel文件', '*.xlsx'),)),
            ],
            [sg.Submit('确定'), sg.Cancel('取消')],
        ]
        window = sg.Window('批量生成质检报告', layout)
        window.SetIcon(icon=resource_path(Path('./assets/ico').joinpath('sn.ico')))
        event, value = window.Read()
        if event == '确定':
            window.Close()
            if '' == value[0] or '' == value[1]:
                self.warning_popup('存在漏填项!')
            else:
                return value[0], value[1]
        elif event in (None, '取消'):
            window.Close()

    @staticmethod
    def progress_bar(length):
        '''
        @description: 进度条
        @param {int} [length] - 任务总数
        @return: {obj} [pb_window] - 进度条界面,
                 {obj} [pb] - 进度条
        @author: Senkita
        '''
        layout = [
            [sg.ProgressBar(length, orientation='h', size=(40, 20), key='progressbar')],
        ]

        pb_window = sg.Window('任务完成进度', layout)
        pb_window.SetIcon(icon=resource_path(Path('./assets/ico').joinpath('sn.ico')))
        pb = pb_window['progressbar']
        return pb_window, pb

    @staticmethod
    def popup(status, cue_word):
        '''
        @description: 弹框
        @param {string} [status] - 状态,
               {string} [cue_word] - 提示词
        @return: {Popup}
        @author: Senkita
        '''
        return sg.Popup(
            status,
            cue_word,
            icon=resource_path(Path('./assets/ico').joinpath('sn.ico')),
        )
