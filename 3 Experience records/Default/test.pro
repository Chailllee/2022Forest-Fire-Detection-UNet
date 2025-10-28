pro test
   e=ENVI()
   ;导入栅格数据（文件地址示例
   file='F:\Files auto-update\0 Graduation Paper\2Model\Database\20181108_20181116_01_T1\process\3.12roi chip'
   raster=e.OpenRaster(file)
   ;获取视图对象
   view1 = e.GetView()
   ;在视图中显示栅格数据
   layer1=view1.CreateLayer(raster)
 
end