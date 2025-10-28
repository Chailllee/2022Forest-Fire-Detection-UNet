from osgeo import gdal
from PIL import Image
import os
import numpy as np
import cv2 as cv
# from numpy import np
import matplotlib.pyplot as plt

# ///////////DEFINITION///////////

# /////img_Sliding
def img_slide(cols, rows, wz):
    if wz > rows or wz > cols:
        print('WindowSize ge imageSize')
        return 0
    else:
        # row_num = ((rows - wz) / step) + 1  # step
        col_num = (cols - wz) + 1  # #x_axit
        row_num = (rows - wz) + 1  # #y_axit
        all_step = col_num * row_num
        # 记录窗口的数量
        # # col_num = int(cols / wz) + 1

        # 行列方向的窗口个数
        # slide_data = np.zeros(shape=(4, col_num, row_num))  # #edited
        # # slide_data = np.zeros(shape=(4, all_step))
        slide_data = np.zeros(shape=(4, row_num, col_num))
        # 用于存放滑动窗口在影像的左上右下列行坐标

        num = 0
        # 计数器
        # 逐行写入数组
        # 沿列方向进行滑动, 列之间的窗口无重叠  -1是为了防止i溢出列数
        for j in range(0, row_num):  # #edited
            for i in range(0, col_num):  # #edited
                # 左上列坐标
                slide_data[0, j, i] = i  # #x-L
                slide_data[1, j, i] = j  # #y-L
                # 右下列坐标
                slide_data[2, j, i] = i + wz - 1  # #x-R
                slide_data[3, j, i] = j + wz - 1  # #y-R

                # max_col = i + wz - 1  # x_max
                # max_row = j + wz - 1  # y_max

        return slide_data.astype(int)  # 由浮点型转换为整型


# ////Judge eqution////
def judge(b1_pix, b5_pix, b6_pix, b7_pix, b5_roi, b7_roi):

    equ1 = (b7_pix / b5_pix > 2.5) & ((b7_pix - b5_pix) > 0.3) & (b7_pix > 0.5)  #  UINT16负数溢出.FLOUT就不会
    equ3 = (b7_pix / b5_pix > 1.8) & ((b7_pix - b5_pix) > 0.17)
    equ2 = (b6_pix > 0.8) & (b1_pix < 0.2) & ((b5_pix > 0.4) | (b7_pix < 0.7))
    equ6 = b7_pix / b6_pix > 1.6

    equ4 = b7_pix / b5_pix > (np.mean(b7_roi / b5_roi) + max(3 * np.std(b7_roi / b5_roi), 0.8))
    equ5 = b7_pix > (np.mean(b7_roi) + max(3 * np.std(b7_roi), 0.08))

    if (equ1 | equ2) | (equ3 & equ4 & equ5 & equ6):
        return 1
    else:
        return 0
#  //////////////////////END/////////////////////////


# ///////Import the modules and open the file//////////////
# dataset = gdal.Open(r'F:/Files auto-update/0 Graduation Paper/2Model/Database/20181108_20181116_01_T1/process/3.24roi band567.tif')
dataset = gdal.Open(r'20171024_411bands-2.tif')
#  Database/TO-LC08_L1TP_045033_20171011_20171024_01_T1/process/20171024_411bands-2.tif

# dataset = gdal.Open('3.24roi band567.tif')

if not dataset:
    print('dataset is null')
    os.system("pause")
#  //////////////////////END/////////////////////////

# //////////Count the number of bands/////////
print(dataset.RasterCount)
if dataset.RasterCount != 7:
    print('channels != 7')
    os.system("pause")

width = dataset.RasterXSize
height = dataset.RasterYSize
print('width & height =', width, height)
#  //////////////////////END/////////////////////////

# ///////////func Sliding 61*61/////////////
wz = 61   # size of windows
subs = img_slide(width, height, wz)
print('shape of subs is:', subs.shape)
col = subs.shape[2]
row = subs.shape[1]
#  //////////////////////END/////////////////////////


# /////////////Fetch each band,the value of int we pass will always start from 1
band = []
for i in range(0, 8):
    b_rust = dataset.GetRasterBand(i)
    if i == 0:
        b_arr = np.zeros(shape=(row, col))
        # b_arr = b_arr.astype(np.int32)  # not succeed. it's still uint16
    else:
        b_arr = b_rust.ReadAsArray()
        # b_arr = b_arr.astype(np.int32)  # not succeed
    band.append(b_arr)
bands = np.array(band)  # stack as 3D array
print('type of bands: ', bands.dtype)  # show nothing

b1 = bands[1]
b6 = bands[6]
b5 = bands[5]
b7 = bands[7]
b1 = b1.astype(np.float32)
b6 = b6.astype(np.float32)
b5 = b5.astype(np.float32)
b7 = b7.astype(np.float32)
# b7 = b7.astype(np.int32)    # not succeed
# print(b7.dtype)

binary = np.zeros(shape=(row, col))  # no Margin
# binary = np.zeros(shape=(height, width))  # with Margin
print(binary.dtype)


# //////////each Pixel///////////
count1 = 0

for i in range(0, col):
    for j in range(0, row):
        sub = subs[:, j, i]
        b1_pix = b1[sub[1] + 30, sub[0] + 30]  # absolute coordinate
        b6_pix = b6[sub[1] + 30, sub[0] + 30]

        b5_pix = b5[sub[1] + 30, sub[0] + 30]
        b5_roi = b5[sub[1]:(sub[3] + 1), sub[0]:(sub[2] + 1)]

        b7_pix = b7[sub[1] + 30, sub[0] + 30]
        b7_roi = b7[sub[1]:(sub[3] + 1), sub[0]:(sub[2] + 1)]

        binary[j, i] = judge(b1_pix, b5_pix, b6_pix, b7_pix, b5_roi, b7_roi)  # no Margin
        if binary[j, i] == 1:
        # binary[j+30, i+30] = judge(b1_pix, b5_pix, b6_pix, b7_pix, b5_roi, b7_roi)   # with Margin
        # if binary[j+30, i+30] == 1:
            count1 += 1

propor = count1/(col*row)
print('numbers of fire pixel:', count1)
print('proportion of pix in all pic', count1/(col*row))

# binary = binary.astype(np.int32)
print('type of binary:', binary.dtype)

# 0-1
new_map = Image.fromarray(binary)
if new_map.mode == 'F':
    new_map = new_map.convert('L')  # 8位像素，黑白
new_map.save('20171024_411bands-2_binary0-1.png')

# # Method1
# print(binary.dtype)  # float64
binary *= 255
print('binary.dtype', binary.dtype)  # float64

new_map = Image.fromarray(binary)
if new_map.mode == 'F':
    new_map = new_map.convert('RGB')
# new_map.show()
new_map.save('20171024_411bands-2_rgb.png')  # √ in same location of this code


