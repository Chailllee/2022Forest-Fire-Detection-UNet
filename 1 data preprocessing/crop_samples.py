from osgeo import gdal
from PIL import Image
import os
import numpy as np
import cv2 as cv
# from numpy import np
import matplotlib.pyplot as plt
#


import os
import gdal
import numpy as np


#  读取tif数据集
def readTif(fileName):
    dataset = gdal.Open(fileName)
    if dataset == None:
        print(fileName + "文件无法打开")
    return dataset


#  保存tif文件函数
def writeTiff(im_data, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
        im_bands, im_height, im_width = im_data.shape
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, int(im_width), int(im_height), int(im_bands), datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


'''
滑动窗口裁剪函数
TifPath 影像路径
SavePath 裁剪后保存目录
CropSize 裁剪尺寸
RepetitionRate 重复率
'''


def TifCrop(TifPath, SavePath, CropSize, RepetitionRate):
    dataset_img = readTif(TifPath)
    width = dataset_img.RasterXSize
    height = dataset_img.RasterYSize
    proj = dataset_img.GetProjection()
    geotrans = dataset_img.GetGeoTransform()
    img = dataset_img.ReadAsArray(0, 0, width, height)  # 获取数据

    #  获取当前文件夹的文件个数len,并以len+1命名即将裁剪得到的图像
    new_name = len(os.listdir(SavePath)) + 1
    file_name = os.path.basename(TifPath)
    tif_name = file_name.split('.')[0]      # added
    #  裁剪图片,重复率为RepetitionRate

    for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
        for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
            #  如果图像是单波段
            if (len(img.shape) == 2):
                cropped = img[
                          int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                          int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
            #  如果图像是多波段
            else:
                cropped = img[:,
                          int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                          int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
            #  写图像
            # writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
            writeTiff(cropped, geotrans, proj, SavePath + "/%s_%d.tif" %(tif_name, new_name))

            #  文件名 + 1
            new_name = new_name + 1
    #  向前裁剪最后一列
    for i in range(int((height - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
        if (len(img.shape) == 2):
            cropped = img[int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                      (width - CropSize): width]
        else:
            cropped = img[:,
                      int(i * CropSize * (1 - RepetitionRate)): int(i * CropSize * (1 - RepetitionRate)) + CropSize,
                      (width - CropSize): width]
        #  写图像
        # writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
        writeTiff(cropped, geotrans, proj, SavePath + "/%s_%d.tif" % (tif_name, new_name))
        new_name = new_name + 1
    #  向前裁剪最后一行
    for j in range(int((width - CropSize * RepetitionRate) / (CropSize * (1 - RepetitionRate)))):
        if (len(img.shape) == 2):
            cropped = img[(height - CropSize): height,
                      int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
        else:
            cropped = img[:,
                      (height - CropSize): height,
                      int(j * CropSize * (1 - RepetitionRate)): int(j * CropSize * (1 - RepetitionRate)) + CropSize]
        # writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
        writeTiff(cropped, geotrans, proj, SavePath + "/%s_%d.tif" % (tif_name, new_name))
        #  文件名 + 1
        new_name = new_name + 1
    #  裁剪右下角
    if (len(img.shape) == 2):
        cropped = img[(height - CropSize): height,
                  (width - CropSize): width]
    else:
        cropped = img[:,
                  (height - CropSize): height,
                  (width - CropSize): width]
    # writeTiff(cropped, geotrans, proj, SavePath + "/%d.tif" % new_name)
    writeTiff(cropped, geotrans, proj, SavePath + "/%s_%d.tif" % (tif_name, new_name))
    new_name = new_name + 1

#  将影像1裁剪为重复率为0.1的256×256的数据集
# TifCrop(r"Data\data2\label\label.tif",
#         r"data\train\label1", 256, 0.1)

# image.tiff
tifPath = "F:\Files auto-update\\0 Graduation Paper\\2Model\Database\\20181108_20181116_01_T1\\process_out\\active\\Active20181108cropped.tiff"
# "F:\Files auto-update\\0 Graduation Paper\\2Model\Database\\20181108_20181116_01_T1\process_out\\active"
savePath = "F:\Files auto-update\\0 Graduation Paper\\2Model\Database\\20181108_20181116_01_T1\\train_data\\0 crop_img"
TifCrop(tifPath, savePath, 512, 0)

# # label.tiff
# tifPath = "F:\Files auto-update\\0 Graduation Paper\\2Model\Database\\20181108_20181116_01_T1\process_out\\active\Active_0-1_20181108.tiff"
# savePath = "F:\Files auto-update\\0 Graduation Paper\\2Model\Database\\20181108_20181116_01_T1\\train_data\\0 crop_label"
# #  将影像1裁剪为重复率为0.1的256×256的数据集
# TifCrop(tifPath, savePath, 512, 0)


# # ///////////DEFINITION///////////
#
# # /////img_Sliding
# def img_slide(cols, rows, wz):
#     if wz > rows or wz > cols:
#         print('WindowSize ge imageSize')
#         return 0
#     else:
#         # row_num = ((rows - wz) / step) + 1  # step
#         col_num = (cols - wz) + 1  # #x_axit
#         row_num = (rows - wz) + 1  # #y_axit
#         all_step = col_num * row_num
#         # 记录窗口的数量
#         # # col_num = int(cols / wz) + 1
#
#         # 行列方向的窗口个数
#         # slide_data = np.zeros(shape=(4, col_num, row_num))  # #edited
#         # # slide_data = np.zeros(shape=(4, all_step))
#         slide_data = np.zeros(shape=(4, row_num, col_num))
#         # 用于存放滑动窗口在影像的左上右下列行坐标
#
#         num = 0
#         # 计数器
#         # 逐行写入数组
#         # 沿列方向进行滑动, 列之间的窗口无重叠  -1是为了防止i溢出列数
#         for j in range(0, row_num):  # #edited
#             for i in range(0, col_num):  # #edited
#                 # 左上列坐标
#                 slide_data[0, j, i] = i  # #x-L
#                 slide_data[1, j, i] = j  # #y-L
#                 # 右下列坐标
#                 slide_data[2, j, i] = i + wz - 1  # #x-R
#                 slide_data[3, j, i] = j + wz - 1  # #y-R
#
#                 # max_col = i + wz - 1  # x_max
#                 # max_row = j + wz - 1  # y_max
#
#         return slide_data.astype(int)  # 由浮点型转换为整型
# #  //////////////////////END/////////////////////////
#
# # # ////Judge eqution////
# # def judge(b1_pix, b5_pix, b6_pix, b7_pix, b5_roi, b7_roi):
# #
# #     equ1 = (b7_pix / b5_pix > 2.5) & ((b7_pix - b5_pix) > 0.3) & (b7_pix > 0.5)  #  UINT16负数溢出.FLOUT就不会
# #     equ3 = (b7_pix / b5_pix > 1.8) & ((b7_pix - b5_pix) > 0.17)
# #     equ2 = (b6_pix > 0.8) & (b1_pix < 0.2) & ((b5_pix > 0.4) | (b7_pix < 0.7))
# #     equ6 = b7_pix / b6_pix > 1.6
# #
# #     equ4 = b7_pix / b5_pix > (np.mean(b7_roi / b5_roi) + max(3 * np.std(b7_roi / b5_roi), 0.8))
# #     equ5 = b7_pix > (np.mean(b7_roi) + max(3 * np.std(b7_roi), 0.08))
# #
# #     if (equ1 | equ2) | (equ3 & equ4 & equ5 & equ6):
# #         return 1
# #     else:
# #         return 0
# # #  //////////////////////END/////////////////////////
#
#
# # ///////Import the modules and open the file//////////////
# # dataset = gdal.Open(r'F:/Files auto-update/0 Graduation Paper/2Model/Database/20181108_20181116_01_T1/process/3.24roi band567.tif')
# dataset = gdal.Open(r'F:\Files auto-update\0 Graduation Paper\2Model\Database\20181108_20181116_01_T1\process_out\active\Active20181108cropped.tiff')
#
# if not dataset:
#     print('dataset is null')
#     os.system("pause")
# #  //////////////////////END/////////////////////////
#
# # //////////Count the number of bands/////////
# '''
# print(dataset.RasterCount)
# if dataset.RasterCount != 7:
#     print('channels != 7')
#     os.system("pause")
# '''
# width = dataset.RasterXSize
# height = dataset.RasterYSize
# print('width & height =', width, height)
# #  //////////////////////END/////////////////////////
#
# # ///////////func Sliding 61*61/////////////
# wz = 512   # size of windows
# subs = img_slide(width, height, wz)
# print('shape of subs is:', subs.shape)
# col = subs.shape[2]
# row = subs.shape[1]
# #  //////////////////////END/////////////////////////
#
#
# # /////////////Fetch each band,the value of int we pass will always start from 1
# '''
# band = []
# for i in range(0, 8):
#     b_rust = dataset.GetRasterBand(i)
#     if i == 0:
#         b_arr = np.zeros(shape=(row, col))
#         # b_arr = b_arr.astype(np.int32)  # not succeed. it's still uint16
#     else:
#         b_arr = b_rust.ReadAsArray()
#         # b_arr = b_arr.astype(np.int32)  # not succeed
#     band.append(b_arr)
# bands = np.array(band)  # stack as 3D array
# print('type of bands: ', bands.dtype)  # show nothing
#
# b1 = bands[1]
# b6 = bands[6]
# b5 = bands[5]
# b7 = bands[7]
# b1 = b1.astype(np.float32)
# b6 = b6.astype(np.float32)
# b5 = b5.astype(np.float32)
# b7 = b7.astype(np.float32)
# # b7 = b7.astype(np.int32)    # not succeed
# # print(b7.dtype)
#
# binary = np.zeros(shape=(row, col))  # no Margin
# # binary = np.zeros(shape=(height, width))  # with Margin
# print(binary.dtype)
# '''
#
# # //////////each Pixel///////////
# '''
# count1 = 0
#
# for i in range(0, col):
#     for j in range(0, row):
#         sub = subs[:, j, i]
#         b1_pix = b1[sub[1] + 30, sub[0] + 30]  # absolute coordinate
#         b6_pix = b6[sub[1] + 30, sub[0] + 30]
#
#         b5_pix = b5[sub[1] + 30, sub[0] + 30]
#         b5_roi = b5[sub[1]:(sub[3] + 1), sub[0]:(sub[2] + 1)]
#
#         b7_pix = b7[sub[1] + 30, sub[0] + 30]
#         b7_roi = b7[sub[1]:(sub[3] + 1), sub[0]:(sub[2] + 1)]
#
#         binary[j, i] = judge(b1_pix, b5_pix, b6_pix, b7_pix, b5_roi, b7_roi)  # no Margin
#
#         # if binary[j, i] == 1:
#         #     binary[j+30, i+30] = judge(b1_pix, b5_pix, b6_pix, b7_pix, b5_roi, b7_roi)   # with Margin
#         # if binary[j+30, i+30] == 1:
#         #     count1 += 1
#
# # propor = count1/(col*row)
# print('numbers of fire pixel:', np.sum(binary==1))  # count1
# print('proportion of pix in all pic', np.sum(binary==1)/(col*row))  # count1/(col*row)
#
# # binary = binary.astype(np.int32)
# print('type of binary:', binary.dtype)
#
# '''
#
# # ///////  0 - 1  //////
# # new_map = Image.fromarray(binary)
# # if new_map.mode == 'F':
# #     new_map = new_map.convert('L')  # 8位像素，黑白
# # new_map.save('Active0-1_8d_20191122_2.png')
# # //////////////////////
#
# # # Method1
#
# binary *= 255
# print('binary.dtype', binary.dtype)  # float64
#
# new_map = Image.fromarray(binary)
# if new_map.mode == 'F':
#     new_map = new_map.convert('RGB')
# # new_map.show()
# new_map.save('Active_0-1rgb_20191122_2.tiff')  # √ in same location of this code
#
#

'''
def crop_img(img, cropsize, overlap):
    """
    裁剪图像为指定格式并保存成tiff
    输入为array形式的数组
    """
    num = 0
    height = img.shape[1]
    width = img.shape[2]
    print(height)
    print(width)

    # 从左上开始裁剪
    for i in range(int(height / (cropsize * (1 - overlap)))):  # 行裁剪次数
        for j in range(int(width / (cropsize * (1 - overlap)))):  # 列裁剪次数
            cropped = img[:,  # 通道不裁剪
                      int(i * cropsize * (1 - overlap)): int(i * cropsize * (1 - overlap) + cropsize),
                      int(j * cropsize * (1 - overlap)): int(j * cropsize * (1 - overlap) + cropsize),
                      ]  # max函数是为了防止i，j为0时索引为负数

            num = num + 1
            target = 'tiff_crop' + '/cropped{n}.tif'.format(n=num)
            gdal_array.SaveArray(cropped, target, format="GTiff")

    #  向前裁剪最后的列
    for i in range(int(height / (cropsize * (1 - overlap)))):
        cropped = img[:,  # 通道不裁剪
                  int(i * cropsize * (1 - overlap)): int(i * cropsize * (1 - overlap) + cropsize),  # 所有行
                  width - cropsize: width,  # 最后256列
                  ]

        num = num + 1
        target = 'tiff_crop' + '/cropped{n}.tif'.format(n=num)
        gdal_array.SaveArray(cropped, target, format="GTiff")

    # 向前裁剪最后的行
    for j in range(int(width / (cropsize * (1 - overlap)))):
        cropped = img[:,  # 通道不裁剪
                  height - cropsize: height,  # 最后256行
                  int(j * cropsize * (1 - overlap)): int(j * cropsize * (1 - overlap) + cropsize),  # 所有列
                  ]

        num = num + 1
        target = 'tiff_crop' + '/cropped{n}.tif'.format(n=num)
        gdal_array.SaveArray(cropped, target, format="GTiff")


    # 裁剪右下角
    cropped = img[:,  # 通道不裁剪
              height - cropsize: height,
              width - cropsize: width,
              ]

    num = num + 1
    target = 'tiff_crop' + '/cropped{n}.tif'.format(n=num)
    gdal_array.SaveArray(cropped, target, format="GTiff")

if __name__ == '__main__':
    base_path = 'data'
    img = get_img(base_path)
    cropsize = 256  # 裁剪尺寸
    overlap = 0.5 # 重叠率
    crop_img(img, cropsize, overlap)
    print('finish')
'''