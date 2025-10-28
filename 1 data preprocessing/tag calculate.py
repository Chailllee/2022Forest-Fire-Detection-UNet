from PIL import Image
import numpy as np

# # /// rgb calculate num of pix////

img = Image.open("4.19ps_765_Nomg.png") # 用PIL中的Image.open打开图像
img_arr = np.array(img) # 转化成numpy数组
w = img.width
h = img.height
w_h = w*h
r,g,b = img_arr[:,:,0], img_arr[:,:,1], img_arr[:,:,2]

print('num of fire pix:', np.sum(r == 255))
print('sum of pic pix:', w_h)
print('proportion - fire pix:', np.sum(r == 255)/(w_h))

print('succeed')

