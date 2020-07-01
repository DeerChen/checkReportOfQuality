'''
@Description: 文件处理函数
@Author: Senkita
@Date: 2020-06-30 15:04:44
@LastEditors: Senkita
@LastEditTime: 2020-07-01 17:19:14
'''
import fitz
from pathlib import Path
from PIL import ImageFont, Image, ImageDraw
import pandas as pd
from utils.utils import mkDir, deleteDir, resource_path


class ExcelProcessing:
    def __init__(self, file_path):
        '''
        @description: 初始化Excel处理类
        @param {string} [file_path] - S/N号文件路径
        @return: None
        @author: Senkita
        '''
        self.df = pd.read_excel(file_path)

    def get_machine_list(self):
        '''
        @description: 获取S/N号
        @param {type}
        @return: {list} [model_list]  - 型号列表,
                 {list} [sn_list] - S/N号列表
        @author: Senkita
        '''
        return zip(self.df['型号'].values.tolist(), self.df['SN号'].values.tolist())


class PDFProcessing:
    def __init__(self, template_file_path, model, sn):
        '''
        @description: 初始化pdf处理类
        @param {string} [template_file_path] - 缓存文件夹路径,
               {string | int} [model] - 型号
               {int} [sn] - SN号
        @return: None
        @author: Senkita
        '''
        self.temp_dir = Path('./temp')
        self.result_dir = Path('./result')
        self.template_file_path = template_file_path
        self.model = str(model)
        self.sn = str(sn)

    def __pdf2png(self):
        '''
        @description: pdf转图片
        @param {type}
        @return: None
        @author: Senkita
        '''
        template = fitz.open(self.template_file_path)
        page = template[0]
        # 清晰度
        zoom_x = 10
        zoom_y = 10
        rotate = 0

        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        pix.writePNG('./temp/preprocess.png')

    def __addText(self, model, sn):
        '''
        @description: 添加S/N号
        @param {str} [model] - 型号,
               {str} [sn] - S/N号
        @return: None
        @author: Senkita
        '''
        img = Image.open(self.temp_dir.joinpath('preprocess.png'))
        draw = ImageDraw.Draw(img)
        ttf_font = str(resource_path(Path('./assets/font').joinpath('times.ttf')))
        model_font = ImageFont.truetype(font=ttf_font, size=119)
        sn_font = ImageFont.truetype(font=ttf_font, size=100)
        # 添加型号
        draw.text((1866, 1117), model, (0, 0, 0), font=model_font)
        # 添加S/N号
        draw.text((4516, 1127), sn, (0, 0, 0), font=sn_font)

        img.save(self.temp_dir.joinpath('postprocess.png'))

    # 图片转pdf
    def __png2pdf(self, model, file_name):
        '''
        @description: 图片转pdf
        @param {string} [file_name] - 文件名
        @return: None
        @author: Senkita
        '''
        doc = fitz.open()
        newImg = fitz.open(self.temp_dir.joinpath('postprocess.png'))
        pdfBytes = newImg.convertToPDF()
        imgpdf = fitz.open('pdf', pdfBytes)
        doc.insertPDF(imgpdf)
        doc.save('./result/{} {}.pdf'.format(model, file_name))

    def process(self):
        '''
        @description: 整合处理
        @param {type}
        @return: None
        @author: Senkita
        '''
        # 新建缓存文件夹
        mkDir(self.temp_dir)
        self.__pdf2png()
        self.__addText(self.model, self.sn)
        self.__png2pdf(self.model, self.sn)
        # 删除缓存文件夹
        deleteDir(self.temp_dir)
