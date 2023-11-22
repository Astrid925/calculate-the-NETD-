import os
import numpy as np
import pandas as pd

class NEdt():
    def __init__(self,filePath1,filePath2,imgW,imgH,T1,T2,nFrame,auxData_flag):
        self.filePath1=filePath1
        self.filePath2=filePath2
        self.imgW=imgW
        self.imgH=imgH
        self.T1=T1
        self.T2=T2
        self.auxData_flag=auxData_flag
        self.nFrame=nFrame

    def openFile(self):
        (file, ext) = os.path.splitext(self.filePath1)
        (Path, filename) = os.path.split(file)
        if not os.path.exists(Path + '\\' + "NEdtResult_" + filename):
            os.mkdir(Path + '\\' + "NEdtResult_" + filename)  # 创建一个文件夹
        outPath = Path + '\\' + "NEdtResult_" + filename
        rPath = os.path.join(outPath, 'NEdt_result.raw')
        rHeadPath = os.path.join(outPath, 'NEdt_result.hdr')
        self.rFile = open(rPath, mode='wb')
        self.rHeadFile = open(rHeadPath, mode='w', encoding='utf-8')
        xlsFile = os.path.join(outPath, 'NEdt_result.xlsx')
        self.xlsWrite = pd.ExcelWriter(xlsFile)

    def closeFile(self):
        text = "ENVI\n" + "samples = " + str(self.imgW) + "\n" + "lines = " + str(self.imgH) + "\n" \
               + "bands = 1\n" + "header offset = 0\n" + "file type = ENVI Standard\n" + "data type = 4\n" + "interleave = bsq\n" + "byte order = 0"
        self.rFile.write(self.NEdt.astype('<f'))
        self.rHeadFile.write(text)
        data = pd.DataFrame(self.NEdt)
        data.to_excel(self.xlsWrite, "Sheet1", float_format="%.4f", header=False, index=False)
        self.rFile.close()
        self.rHeadFile.close()
        self.xlsWrite.close()

    def generate_mask(self,img_height, img_width, radius, center_x, center_y):
        y, x = np.ogrid[0:img_height, 0:img_width]
        # circle mask
        mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
        return mask

    def NEdt_cal(self,NDT1,NDT2,T1,T2):
        averNDT1=np.mean(NDT1,axis=2)
        diffDNT2=NDT2-np.expand_dims(averNDT1,2).repeat(NDT2.shape[2],axis=2)
        std_diffDNT2=np.std(diffDNT2,axis=2)
        aver_diffDNT2=np.mean(diffDNT2,axis=2)
        NEdt=((T2-T1)*1000*std_diffDNT2)/(aver_diffDNT2+0.00000001)
        averNEdt=np.mean(NEdt)
        stdNEdt=np.std(NEdt)
        maxNEdt=np.max(NEdt)
        minNEdt=np.min(NEdt)
        return NEdt, averNEdt, stdNEdt, maxNEdt, minNEdt

    def dataProcessing(self):
        fileT1 = open(self.filePath1, mode="rb")
        fileT2 = open(self.filePath2, mode="rb")
        fileSize1 = os.path.getsize(self.filePath1)
        fileSize2 = os.path.getsize(self.filePath2)
        if self.auxData_flag == 1:
            nFrame1 = int(fileSize1 / (self.imgW*self.imgH * 2))
            nFrame2 = int(fileSize2 / (self.imgW*self.imgH * 2))
            if nFrame1 >= nFrame2:
                nFrame = nFrame2
            else:
                nFrame = nFrame1
            NDT1 = np.zeros((self.imgH-1, self.imgW-8, nFrame), dtype=np.uint16, order="C")
            NDT2 = np.zeros((self.imgH-1, self.imgW-8, nFrame), dtype=np.uint16, order="C")
            for i in range(0, nFrame):
                temp1 = np.frombuffer(fileT1.read(self.imgW*self.imgH * 2), dtype=np.uint16).reshape(self.imgH,self.imgW)
                temp2 = np.frombuffer(fileT2.read(self.imgW*self.imgH * 2), dtype=np.uint16).reshape(self.imgH,self.imgW)
                NDT1[:, :, i] = temp1[1:, 7:-1]
                NDT2[:, :, i] = temp2[1:, 7:-1]
        else:
            nFrame1 = fileSize1 / (self.imgW * self.imgH * 2)
            nFrame2 = fileSize2 / (self.imgW * self.imgH * 2)
            if nFrame1 >= nFrame2:
                nFrame = nFrame2
            else:
                nFrame = nFrame1
            NDT1 = np.zeros((self.imgH, self.imgW, nFrame), dtype=np.uint16, order="C")
            NDT2 = np.zeros((self.imgH, self.imgW, nFrame), dtype=np.uint16, order="C")
            for i in range(0, nFrame):
                NDT1[:, :, i] = np.frombuffer(fileT1.read(self.imgW * self.imgH * 2), dtype=np.uint16).reshape(self.imgH, self.imgW)
                NDT2[:, :, i] = np.frombuffer(fileT2.read(self.imgW * self.imgH * 2), dtype=np.uint16).reshape(self.imgH, self.imgW)
        # 计算NEdt
        (self.NEdt, self.averNEdt, self.stdNEdt, self.maxNEdt, self.minNEdt) = self.NEdt_cal(NDT1, NDT2, self.T1, self.T2)

    def resultReturn(self):
        return self.averNEdt, self.stdNEdt, self.maxNEdt, self.minNEdt

if __name__=="__main__":
    imgW = 328  # 列数
    imgH = 257  # 行数
    T1 = 300
    T2 = 315
    filePath1 = r"D:\cxy\Data\NEdt\20221208105657_1_150_d27.dat"
    filePath2 = r"D:\cxy\Data\NEdt\20221208110748_1_150d42.dat"
    auxData_flag = 1
    myTest=NEdt(filePath1,filePath2,imgW,imgH,T1,T2,auxData_flag)
    myTest.openFile()
    myTest.dataProcessing()
    (averVaule,stdValue,maxValue,minValue)=myTest.resultReturn()
    print(maxValue)
    print(stdValue)
    myTest.closeFile()