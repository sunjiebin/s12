#!/usr/bin/env python3
# Auther: sunjb

from aip import AipOcr
from PIL import Image
import xlwt, xlrd
from xlutils import copy
import os, time
import key

client = AipOcr(key.APP_ID, key.API_KEY, key.SECRET_KEY)



class img_to_str(object):
    '''
    通过调用百度ocr api，将图片中的文字转化为文字
    '''
    def __init__(self, image_path):
        """ 如果有可选参数 """

        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        self.image = self.get_file_content(image_path)

    def get_file_content(filePath):
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
            row = data[0]
            col = data[1:]
            # print(row,col)
            return row, col
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

    def tableRecognitionAsync(self):
        # 表格识别
        result = client.tableRecognitionAsync(self.image)
        print(result)
        rst = result['result'][0]['request_id']
        print(rst)
        return rst

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


class cut_img(object):
    '''用于裁剪图片,需要裁剪的像素点可以用画图软件打开图片,然后鼠标悬念的位置就会显示图片位置信息'''

    def __init__(self, points, save_path, img_dir):
        self.points = points
        self.save_path = save_path
        self.img_dir = img_dir

    def cut(self, point):
        '''
        裁剪：传入一个元组作为参数
        元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片右边界距离，距离图片下边界距离）
        需提供两个坐标，左上角一个坐标，右下角一个坐标
        '''
        img = Image.open(self.img_path)
        region = img.crop(point)
        region.save(self.save_path)
        #img_size = img.size
        # print("图片宽度和高度分别是{}".format(img_size))
        # 截取图片中一块宽和高都是250的
        # x = 832
        # y = 65
        # w = 965
        # h = 225
        # region = img.crop((x, y, w, h))


    def pre_cut(self):
        ins_col = 0
        for point in self.points:
            time.sleep(2)
            ins_col = ins_col + 1
            self.cut(point)
            trans_img = img_to_str(self.save_path)
            row, col = trans_img.basicAccurate()
            excel_obj = excel_class(row, col, ins_col, self.start_row)
            # if ins_col == 1:
            #     excel_obj.write_excel()
            # else:
            excel_obj.change_excel()

    def read_img(self):
        images = os.listdir(self.img_dir)
        # num=0
        for image in images:
            # num=num+1
            self.img_path = os.path.join(self.img_dir, image)
            excel_obj = excel_class()
            row, col = excel_obj.read_excel()
            self.start_row = row
            self.pre_cut()


class excel_class(object):
    '''用于读取/新建/修改excel表格'''
    def __init__(self, row=None, col=None, ins_col=None, start_row=0, start_col=0):
        self.row = row
        self.col = col
        self.ins_col = ins_col
        self.start_row = start_row  #起始行
        self.start_col = start_col
        # print(self.row,self.col)

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
        book = xlrd.open_workbook('test.xls')
        #读取表格里面第一个sheet标签的内容
        sheet = book.sheet_by_index(0)  # 根据sheet编号来
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

    # 写Excel
    def write_excel(self):
        f = xlwt.Workbook()
        #写入excel，标签名称为"测试"
        sheet1 = f.add_sheet('测试', cell_overwrite_ok=True)
        row0 = [self.row]
        colum0 = self.col

        # 在第一行里面写入多列数据
        for i in range(0, len(row0)):
            #（行，列，数据，参数）
            sheet1.write(0, self.ins_col, row0[i], self.set_style('Times New Roman', 220, True))
        # 在i+1行的self.ins_col列写入数据
        for i in range(0, len(colum0)):
            sheet1.write(i + 1, self.ins_col, colum0[i], self.set_style('Times New Roman', 220, True))
        f.save('test.xls')

        # sheet1.write(1,3,'2006/12/12')
        # sheet1.write_merge(6,6,1,3,'未知')#合并行单元格
        # sheet1.write_merge(1,2,3,3,'打游戏')#合并列单元格
        # sheet1.write_merge(4,5,3,3,'打篮球')


    # 修改excel
    def change_excel(self):
        f = xlrd.open_workbook('test.xls')
        new_book = copy.copy(f)
        sheet1 = new_book.get_sheet(0)
        row0 = [self.row]
        colum0 = self.col
        if self.start_row == 0:
            # 写第一行
            for i in range(0, len(row0)):
                sheet1.write(0, self.ins_col, row0[i], self.set_style('Times New Roman', 220, True))
        # 写列
        for i in range(0, len(colum0)):
            sheet1.write(self.start_row + i + 1, self.ins_col, colum0[i], self.set_style('Times New Roman', 220, True))
        new_book.save('test.xls')


points = [(99, 492, 336, 868), (343, 490, 457, 870), (883, 490, 1006, 870)]
# cut_obj=cut_img(points,img_path='img/3.jpg',save_path='./test5.jpg')
cut_obj = cut_img(points, img_dir='img', save_path='./test5.jpg')
cut_obj.read_img()

# trans_img=img_to_str('test5.jpg')
# trans_img.basicAccurate()

# img_str=img_to_str('test4.jpg')
# get_result('17721178_1211621')

# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"
#
# """ 带参数调用通用文字识别, 图片参数为本地图片 """
# client.basicGeneral(image, options)
#
# url = "https//www.x.com/sample.jpg"
#
# """ 调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url);
#
# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"
#
# """ 带参数调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url, options)