import cv2
img = cv2.imread("Database/TO-LC08_L1TP_045033_20171011_20171024_01_T1/process/manmade/20171024-2_ps_band765.png")

wz = int((61-1)/2)  # margin size of slice, wz=30
print(img.shape)
if len(img.shape) == 3:
    height, width = img.shape[0], img.shape[1]
    crop = img[wz: -wz, wz: -wz, :]
else:
    print('input correct 3d img')
# cv2.imshow("cropped", crop)
    # if crop.shape == img.shape-wz:
    #     print('right')
cv2.imwrite("Database/TO-LC08_L1TP_045033_20171011_20171024_01_T1/process/manmade/20171024-2_ps_band765_nomg.png", crop)
print(crop.shape)


# label = img[:, :, -1]
# roi = label[29:741, 29:1325]
# roi = roi * 255

# cv2.imwrite("20181108-1-255-NDBR08.png", roi)

# cv2.imshow("cropped", roi)
# cv2.waitKey(1000)
