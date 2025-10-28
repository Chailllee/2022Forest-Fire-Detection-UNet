from PIL import Image
import numpy as np

#  //////convert: png 8d -- tif 24d
img = Image.open(r"Active0-1_20181108.png") # 用PIL中的Image.open打开图像
img_arr = np.array(img) # 转化成numpy数组
w = img.width
h = img.height
w_h = w*h
# r,g,b = img_arr[:,:,0], img_arr[:,:,1], img_arr[:,:,2]
print('width height', w, h)
print('num of fire pix:', np.sum(img_arr == 1))
print('sum of pic pix:', w_h)
print('proportion - fire pix:', np.sum(img_arr == 1)/(w_h))
new_map = Image.fromarray(img_arr)
# if new_map.mode == 'F':
new_map = new_map.convert('RGB')
# new_map.show()
new_map.save('Active_0-1_20181108.tiff')  # √ in same location of this code