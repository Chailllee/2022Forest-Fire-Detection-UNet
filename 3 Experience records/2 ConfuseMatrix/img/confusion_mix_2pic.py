# 混淆矩阵
import cv2
import numpy as np
from sklearn.metrics import confusion_matrix
import os
# from pyExcelerator import *
import xlwt
from openpyxl import load_workbook
# import matplotlib.pyplot as plt

# /////build new excel
book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建Workbook，相当于创建Excel
# /////set a Style
# def set_style():
#     style = xlwt.XFStyle()  # 初始化样式
#
#     alignment = xlwt.Alignment() #设置字体在单元格中的位置
#     # alignment.horz =  xlwt.Alignment.HORZ_CENTER  #水平居左
#     alignment.vert = xlwt.Alignment.VERT_CENTER  #垂直居中
#     # alignment.horz = 1  # 居中
#
#     style.alignment = alignment

# //////文件夹
# dir_tag = os.listdir(r'Database/0confuse_matrix')  # 每组数据所在文件夹
# print(dir_tag)

# ///////所有文件名
for filepath, dirnames, filenames in os.walk(r'Database/0confuse_matrix'):
    img_r = []
    y_pred = []
    # print(filepath)
    # print(dirnames)
    #///new data for new sheet
    data = [
        ['img', 'precision', 'recall', 'F1', 'iou1', 'iou2', 'miou']
    ]

    if len(filenames) == 3:

        # /////add new sheet
        path_list = filepath.split("\\")
        cur_filename = path_list[-1]
        # book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet('%s' % cur_filename, cell_overwrite_ok=True)


        for filename in filenames:
            # print(os.path.join(filepath, filename))
            img_r.append(os.path.join(filepath, filename))
            # print(img_r)

        _y_true = cv2.imread(img_r[0])  # Active  .cv2.imread(filenames[0])
        y_true = _y_true.ravel()


        for j in range(1, 3):
            _y_pred = cv2.imread(img_r[j])  # Ocular band654 ~ 765
            y_pred.append(_y_pred.ravel())
            cm = confusion_matrix(y_true, y_pred[j-1])
            # _y_pred1 = cv2.imread(img_r[1])  # Ocular band654
            # y_pred1 = _y_pred1.ravel()
            # _y_pred2 = cv2.imread(img_r[2])  # Ocular band765
            # y_pred2 = _y_pred2.ravel()

        # cm1 = confusion_matrix(y_true, y_pred1)
        # cm2 = confusion_matrix(y_true, y_pred2)

            TP = np.diag(cm)[0]
            FP = np.sum(cm, axis=0)[0] - TP
            FN = np.sum(cm, axis=1)[0] - TP

            num_classes = 2
            TN1 = []
            for i in range(num_classes):
                temp = np.delete(cm, i, 0)  # delete ith row
                temp = np.delete(temp, i, 1)  # delete ith column
                TN1.append(sum(sum(temp)))
            TN = TN1[0]

            precision = TP / (TP + FP)
            recall = TP / (TP + FN)
            F1 = 2 * precision * recall / (precision + recall)

            iou1 = TP / (TP + FP + FN)  # 类别1交并比
            iou2 = TN / (TN + FP + FN)
            miou = (iou1 + iou2) / 2   # Mean IoU平均交并比

            # print("precision=", precision)
            # print("recall=", recall)
            # print("F1_score:", F1)
            # print(iou1, iou2, miou)

            curdata = [filenames[j], precision, recall, F1, iou1, iou2, miou]
            data.append(curdata)

        # sheet.column_dimensions['A':'G'].width = 20  # 列宽

        row = len(data)
        line = len(data[0])
        for k in range(row):
            for l in range(line):
                sheet.col(l).width = 255*20  # 列宽
                sheet.write(k, l, data[k][l])

            # sheet.append(k)
        # book.save('confusion_mix.xlsx')

        else:
            pass

book.save('Database/0confuse_matrix/confusion_mix.xlsx')

# # ///////////////ORIGINAL////////////////
# _y_true = cv2.imread("Database/20181108_20181116_01_T1/process_out/4.11rgb_no mg.png")  # Active
# y_true = _y_true.ravel()
# _y_pred = cv2.imread("Database/20181108_20181116_01_T1/process_out/4.19ps_765_Nomg.png")  # Ocular
# y_pred = _y_pred.ravel()
#
# cm = confusion_matrix(y_true, y_pred)
# print(cm)
#
# TP = np.diag(cm)[0]
# FP = np.sum(cm, axis=0)[0] - TP
# FN = np.sum(cm, axis=1)[0] - TP
#
# num_classes = 2
# TN1 = []
# for i in range(num_classes):
#     temp = np.delete(cm, i, 0)    # delete ith row
#     temp = np.delete(temp, i, 1)  # delete ith column
#     TN1.append(sum(sum(temp)))
# TN = TN1[0]
#
#
# precision = TP/(TP+FP)
# recall = TP/(TP+FN)
# F1 = 2 * precision * recall / (precision + recall)
#
# iou1 = TP/(TP + FP + FN)
# iou2 = TN/(TN + FP + FN)
# miou = (iou1 + iou2)/2
#
# print("precision=", precision)
# print("recall=", recall)
# print("F1_score:", F1)
#
# print(iou1, iou2, miou)
# # ///////////////END////////////////


