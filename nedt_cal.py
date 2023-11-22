import os
import numpy as np
import pandas as pd
#取圆形mask

def generate_mask(img_height, img_width, radius, center_x, center_y):
    y, x = np.ogrid[0:img_height, 0:img_width]
    # circle mask
    mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
    return mask
# 计算NEDT函数
def NEdt_cal(NDT1,NDT2,T1,T2,mask):
    averNDT1=np.mean(NDT1,axis=2)
    diffDNT2=NDT2-np.expand_dims(averNDT1,2).repeat(NDT2.shape[2],axis=2)
    std_diffDNT2=np.std(diffDNT2,axis=2)
    aver_diffDNT2=np.mean(diffDNT2,axis=2)
    NEdt=((T2-T1)*1000.*std_diffDNT2)/(aver_diffDNT2+0.00000001)
    rNEdt=mask*NEdt
    averNEdt=np.mean(NEdt)
    stdNEdt=np.std(NEdt)
    maxNEdt=np.max(NEdt)
    minNEdt=np.min(NEdt)
    return NEdt, averNEdt, stdNEdt, maxNEdt, minNEdt,rNEdt

# 输入信息
imgW=320   #列数
imgH=256  #行数
T1=27
T2=42
filePath1=r"D:\cxy\Data\NEdt\20221208105657_1_150_d27.dat"
filePath2=r"D:\cxy\Data\NEdt\20221208110748_1_150d42.dat"
auxData_flag=1
# 建立输出路径
(file, ext) = os.path.splitext(filePath1)
(Path, filename) = os.path.split(file)
if not os.path.exists(Path + '\\' + "NEdtResult_"+filename):
    os.mkdir(Path + '\\' + "NEdtResult_"+filename)  # 创建一个文件夹
outPath = Path + '\\' + "NEdtResult_"+filename
rPath = os.path.join(outPath, 'NEdt_result.raw')
rHeadPath = os.path.join(outPath, 'NEdt_result.hdr')
rFile = open(rPath, mode='wb')
rHeadFile = open(rHeadPath, mode='w', encoding='utf-8')
xlsFile=os.path.join(outPath, 'NEdt_result.xlsx')
xlsWrite=pd.ExcelWriter(xlsFile)

#生成圆形mask
mask=generate_mask(imgH,imgW,20, imgW/2, imgH/2)
# 读文件
fileT1=open(filePath1, mode="rb")
fileT2=open(filePath2,mode="rb")
fileSize1 = os.path.getsize(filePath1)
fileSize2=os.path.getsize(filePath2)
if auxData_flag==1:
    nFrame1=int(fileSize1/((7+imgW+1)*(1+imgH)*2))
    nFrame2=int(fileSize2/((7+imgW+1)*(1+imgH)*2))
    if nFrame1>=nFrame2:
        nFrame=nFrame2
    else:
        nFrame = nFrame1
    NDT1=np.zeros((imgH,imgW,nFrame),dtype=np.uint16,order="C")
    NDT2 =np.zeros((imgH, imgW, nFrame), dtype=np.uint16, order="C")
    for i in range (0,nFrame):
        temp1=np.frombuffer(fileT1.read((7+imgW+1)*(1+imgH)*2), dtype=np.uint16).reshape(1+imgH,7+imgW+1)
        temp2=np.frombuffer(fileT2.read((7+imgW+1)*(1+imgH)*2), dtype=np.uint16).reshape(1+imgH,7+imgW+1)
        NDT1[:,:,i]=temp1[1:,7:-1]
        NDT2[:, :, i] = temp2[1:,7:-1]
else:
    nFrame1 = fileSize1 / (imgW * imgH*2)
    nFrame2 = fileSize2 / (imgW * imgH*2)
    if nFrame1 >= nFrame2:
        nFrame = nFrame2
    else:
        nFrame = nFrame1
    NDT1=np.zeros((imgH,imgW,nFrame),dtype=np.uint16,order="C")
    NDT2 =np.zeros((imgH, imgW, nFrame), dtype=np.uint16, order="C")
    for i in range (0,nFrame):
        NDT1[:, :, i] = np.frombuffer(fileT1.read(imgW * imgH*2), dtype=np.uint16).reshape(imgH,imgW)
        NDT2[:, :, i] = np.frombuffer(fileT2.read(imgW * imgH*2), dtype=np.uint16).reshape(imgH,imgW)

# 计算NEdt
(NEdt, averNEdt, stdNEdt, maxNEdt, minNEdt,rNEdt)= NEdt_cal(NDT1, NDT2, T1, T2,mask)

 # 写文件
text = "ENVI\n" + "samples = "+str(imgW)+"\n" + "lines = " +str(imgH)+"\n"\
       + "bands = 1\n"+ "header offset = 0\n" + "file type = ENVI Standard\n" + "data type = 5\n" + "interleave = bsq\n" + "byte order = 0"
rFile.write(NEdt.astype('<f2'))
rHeadFile.write(text)
data = pd.DataFrame(NEdt)
data.to_excel(xlsWrite,"Sheet1",float_format="%.4f",header=False,index=False)

# 关闭文件
rFile.close()
rHeadFile.close()
xlsWrite.close()