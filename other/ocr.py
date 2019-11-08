#!/usr/bin/env python3
# Auther: sunjb

from aip import AipOcr
from PIL import Image
import xlwt, xlrd
from xlutils import copy
import os, time
import key
'''
本脚本用于读取表格图片的内容，并生成数据输入到对应的excel
'''
client = AipOcr(key.APP_ID, key.API_KEY, key.SECRET_KEY)

class img_to_str(object):
    '''
    通过调用百度ocr api，将图片中的文字转化为文字
    '''
    def __init__(self, image_path):
        self.image = self.get_file_content(image_path)

    def get_file_content(self,filePath):
        """ 读取图片 """
        with open(filePath, 'rb') as fp:
            return fp.read()

    def basicAccurate(self):
        # 高精度识别
        result = client.basicAccurate(self.image)
        print(result)
        if 'words_result' in result:
            data = []
            for w in result['words_result']:
                data.append(w['words'])
            row_content = data[0]
            col_content = data[1:]
            # print(row_content,col_content)
            return row_content, col_content
        return '识别错误'

    def accurate(self):
        # 带位置参数的高精度识别
        """ 如果有可选参数 """
        options = {}
        options["recognize_granularity"] = "big"
        options["detect_direction"] = "true"
        options["vertexes_location"] = "true"
        options["probability"] = "true"
        result = client.accurate(self.image)
        print(result)

    def basicGeneral(self):
        # 基础识别
        result = client.basicGeneral(self.image)
        print(result)

'''
    def tableRecognitionAsync(self):
        # 表格识别,注意表格识别是异步的，需要把request_id传递给get_result方法再次生成excel
        result = client.tableRecognitionAsync(self.image)
        print(result)
        request_id = result['result'][0]['request_id']
        print(request_id)
        return request_id

    def get_result(request_id):
        requestId = request_id

        """ 调用表格识别结果 """
        file = client.getTableRecognitionResult(requestId)
        print(file)
        # """ 如果有可选参数 """
        # options = {}
        # options["result_type"] = "json"
        #
        # """ 带参数调用表格识别结果 """
        # client.getTableRecognitionResult(requestId, options)
'''

class cut_img(object):
    '''用于裁剪图片,需要裁剪的像素点可以用画图软件打开图片,然后鼠标悬念的位置就会显示图片位置信息
    批量处理相同的表格时，要保证表格的位置都一致，这样才能基于像素截取到指定的单元格内容'''
    def __init__(self, points, img_dir,excel_name='自动生成.xls'):
        self.points = points
        self.cut_img_name = 'tmp.jpg'
        self.img_dir = img_dir
        self.excel_name=excel_name

    def cut(self, point):
        '''
        裁剪：传入一个元组作为参数
        元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片右边界距离，距离图片下边界距离）
        需提供两个坐标，左上角一个坐标，右下角一个坐标
        '''
        img = Image.open(self.img_path)
        region = img.crop(point)
        region.save(self.cut_img_name)
        #img_size = img.size
        # print("图片宽度和高度分别是{}".format(img_size))
        # 截取图片中一块宽和高都是250的
        # x = 832
        # y = 65
        # w = 965
        # h = 225
        # region = img.crop((x, y, w, h))

class handler(cut_img):
    def pre_cut(self):
        '''根据point来将图片截取为多张图片，并识别生成excel'''
        ins_col = 0
        for point in self.points:
            time.sleep(2)
            ins_col = ins_col + 1
            #裁剪图片
            self.cut(point)
            #将裁剪的图片识别成文字
            trans_img = img_to_str(self.cut_img_name)
            row_content, col_content = trans_img.basicAccurate()
            #将识别的文字写入excel
            excel_obj = excel_class(row_content, col_content, ins_col, self.start_row,excel_name=self.excel_name)
            excel_obj.change_excel()

    def handler_img(self):
        '''读取文件夹里面的图片，并交给pre_cut()处理'''
        images = os.listdir(self.img_dir)
        #首先创建excel
        excel_class.create_excel(self.excel_name)
        for image in images:
            self.img_path = os.path.join(self.img_dir, image)
            #读取excel里面的内容，获取到已有的文本行数，作为下次追加内容的起点
            row, col = excel_class(excel_name=self.excel_name).read_excel()
            self.start_row = row
            #print(self.start_row)
            self.pre_cut()
        os.remove(self.cut_img_name)    #删除临时生成的图片文件

class excel_class(object):
    '''用于读取/新建/修改excel表格'''
    def __init__(self, row_content=None, col_content=None, ins_col=None, start_row=0, start_col=0,excel_name='test.xls'):
        self.row_content = row_content
        self.col_content = col_content
        self.ins_col = ins_col
        self.start_row_num = start_row  #起始行
        self.start_col_num = start_col
        self.excel_name = excel_name
        # print(self.start_row_num,self.start_col_num)

    # 设置表格样式
    def set_style(self, name, height, bold=False):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    # 读Excel
    def read_excel(self):
        book = xlrd.open_workbook(self.excel_name)
        #读取表格里面第一个sheet标签的内容
        sheet = book.sheet_by_index(0)  # 根据sheet编号来
        # print(sheet.nrows, sheet.ncols)
        #返回表格里面的行数和列数
        return sheet.nrows, sheet.ncols

        # sheet=book.sheet_by_name('sheet1')   #根据 sheet名称来
        # print(sheet.nrows)  # excel里面有多少行
        # print(sheet.ncols)  # excel里面有多少列
        # print(sheet.cell(0, 0).value)  # 获取第0行第0列的值
        # print(sheet.row_values(0))  # 获取到整行的内容
        # print(sheet.col_values(1))  # 获取到整列的内容
        #
        # for i in range(sheet.nrows):  # 循环获取每行的内容
        #     print(sheet.row_values(i))

    #创建Excel
    @staticmethod
    def create_excel(excel_name):
        f = xlwt.Workbook()
        sheet1 = f.add_sheet('测试',cell_overwrite_ok=True)
        f.save(excel_name)

    # 写Excel
    def write_excel(self):
        f = xlwt.Workbook()
        #写入excel，标签名称为"测试"
        sheet1 = f.add_sheet('测试', cell_overwrite_ok=True)
        row0 = [self.row_content]
        colum0 = self.col_content

        # 在第一行里面写入多列数据
        for i in range(0, len(row0)):
            #（行，列，数据，参数）
            sheet1.write(0, self.ins_col, row0[i], self.set_style('Times New Roman', 220, True))
        # 在i+1行的self.ins_col列写入数据
        for i in range(0, len(colum0)):
            sheet1.write(i + 1, self.ins_col, colum0[i], self.set_style('Times New Roman', 220, True))
        f.save(self.excel_name)

        # sheet1.write(1,3,'2006/12/12')
        # sheet1.write_merge(6,6,1,3,'未知')#合并行单元格
        # sheet1.write_merge(1,2,3,3,'打游戏')#合并列单元格
        # sheet1.write_merge(4,5,3,3,'打篮球')


    # 修改excel
    def change_excel(self):
        f = xlrd.open_workbook(self.excel_name)
        new_book = copy.copy(f)
        sheet1 = new_book.get_sheet(0)
        row_list = [self.row_content]
        col_list = self.col_content
        if self.start_row_num == 0: #如果第一次循环，则添加表头
            print('start_row_num为0')
            # 写第一行
            for i in range(0, len(row_list)):
                sheet1.write(0, self.ins_col, row_list[i], self.set_style('Times New Roman', 220, True))
            for i in range(0, len(col_list)):
                sheet1.write(i + 1, self.ins_col, col_list[i], self.set_style('Times New Roman', 220, True))
        else:   #如果不是第一次循环，则不添加表头，只追加内容
            # 写列
            for i in range(0, len(col_list)):
                sheet1.write(self.start_row_num + i, self.ins_col, col_list[i], self.set_style('Times New Roman', 220, True))
        new_book.save(self.excel_name)


points = [(99, 492, 336, 868), (343, 490, 457, 870), (883, 490, 1006, 870)]
handler_obj=handler(points,'img')
handler_obj.handler_img()