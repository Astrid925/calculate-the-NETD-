import tkinter as tk
from tkinter import filedialog, ttk
from NEdtClass import NEdt

class GUI():

    def __init__(self) ->None:
        self.root=tk.Tk()
        self.root.geometry('850x500')
        self.root.title('NEdt计算软件')
        # 水印
        label=ttk.Label(self.root, text='版权：上海技术物理研究所航空组2023', font=1,foreground='crimson')
        label.place(x=20,y=450)

    def filePath1(self):
        self.filePath1 = filedialog.askopenfilename()
        if self.filePath1 is not None:
            self.v1.set(self.filePath1)
           # return self.filePath1   #不返回也是可以的，毕竟self.v1是想要的

    def filePath2(self):
        self.filePath2 = filedialog.askopenfilename()
        if self.filePath2 is not None:
            self.v2.set(self.filePath2)
          #  return self.filePath2

    def run(self):
        inputOption = tk.LabelFrame(self.root, font=10,text='输入参数和文件路径', padx=10, pady=10)
        inputOption.place(x=20, y=20)
        # 图像宽和高参数
        self.entryW_var = tk.IntVar()
        ttk.Label(inputOption, text='图像宽度',font=4).grid(row=0,column=0,pady=5,sticky="E")
        tk.Entry(inputOption,bg="pink",width=10, textvariable=self.entryW_var).grid(row=0,column=1,pady=5,ipady=4,sticky="W")
        self.entryH_var = tk.IntVar()
        ttk.Label(inputOption, text='图像高度',font=4).grid(row=1,column=0,pady=5,sticky="E")
        tk.Entry(inputOption,bg="pink",width=10, textvariable=self.entryH_var).grid(row=1,column=1,pady=5,ipady=4,sticky="W")
        # 温度参数
        self.entryT1_var = tk.IntVar()
        ttk.Label(inputOption, text='温度1',font=4).grid(row=0,column=3,pady=5,sticky="E")
        tk.Entry(inputOption, width=10, bg="pink",textvariable=self.entryT1_var).grid(row=0,column=4,pady=5,ipady=4,sticky="W")
        ttk.Label(inputOption, text='K',font=4).place(x=361,y=8, anchor="nw")
        # ttk.Label(inputOption, text='K',font=4).grid(row=0,column=5,pady=5,ipady=4,sticky="E")
        self.entryT2_var = tk.IntVar()
        ttk.Label(inputOption, text='温度2',font=4).grid(row=1,column=3,pady=5,sticky="E")
        tk.Entry(inputOption, width=10, bg="pink",textvariable=self.entryT2_var, state='normal').grid(row=1,column=4,pady=5,ipady=4,sticky="W")
        ttk.Label(inputOption, text='K',font=4).place(x=361,y=48, anchor="nw")
        #叠加帧数
        self.entryFrameNum_var = tk.IntVar()
        ttk.Label(inputOption, text='叠加帧数', font=4).grid(row=0, column=5, pady=5, sticky="E")
        tk.Entry(inputOption, width=10, bg="pink", textvariable=self.entryFrameNum_var, state='normal').grid(row=0, column=6,pady=5, ipady=4,sticky="W")
        #计算半径
        self.entryRadius_var = tk.IntVar()
        ttk.Label(inputOption, text='图像半径', font=4).grid(row=1, column=5, pady=5, sticky="E")
        tk.Entry(inputOption, width=10, bg="pink", textvariable=self.entryRadius_var, state='normal').grid(row=1, column=6,pady=5,ipady=4,sticky="W")
        # 是否有辅助数据
        self.entryFlag_var=tk.IntVar()
        tk.Checkbutton(inputOption,text="有无辅助数据",font=4,bg="pink",variable=self.entryFlag_var).grid(row=1,column=8,columnspan=1,pady=5)
        # 输入文件路径
        self.v1 = tk.StringVar()
        ttk.Label(inputOption, text='温度1数据文件',font=4).grid(row=3,column=0, pady=5)
        tk.Entry(inputOption, width=65, bg="pink",textvariable=self.v1).grid(row=3,column=1,columnspan=6,pady=5,ipady=4)
        tk.Button(inputOption, text='...',width=4, bg="plum",command=lambda: self.filePath1()).grid(row=3,column=7,sticky="W")
        self.v2 = tk.StringVar()
        ttk.Label(inputOption, text='温度2数据文件',font=4).grid( row=4,column=0)
        tk.Entry(inputOption, width=65, bg="pink",textvariable=self.v2).grid( row=4,column=1,columnspan=6,ipady=4)
        tk.Button(inputOption, text='...', width=4,bg="plum", command=lambda: self.filePath2()).grid(row=4,column=7,sticky="W")
        # 输出
        processOption = tk.LabelFrame(self.root, text='输出NEdt结果',font=10, padx=5, pady=5)
        processOption.place(x=20, y=225)

        # self.btn= tk.Button(processOption, text='计算NEdt', font=4,width=8, bg="lightcoral",command=lambda: self.start())
        self.btn= tk.Button(processOption, text='计算NEdt', font=4,width=12,bg="lightcoral")
        self.btn.grid(row=1,column=0, padx=140,pady=10,sticky=tk.W)
        ttk.Label(processOption, text='平均NEdt',font=4).grid(row=0,column=1)
        self.averLabel= ttk.Label(processOption,width=8,background="pink")
        self.averLabel.grid(row=0,column=2,ipady=3,pady=5)
        ttk.Label(processOption, text='mK',font=4).grid(row=0,column=3)

        ttk.Label(processOption, text='NEdt标准差',font=4).grid(row=1, column=1)
        self.stdLabel = ttk.Label(processOption, width=8,background="pink")
        self.stdLabel.grid(row=1, column=2, ipady=3,pady=5)
        ttk.Label(processOption, text='mK',font=4).grid(row=1, column=3)

        ttk.Label(processOption, text='NEdt最大值',font=4).grid(row=2, column=1)
        self.maxLabel = ttk.Label(processOption, width=8,background="pink")
        self.maxLabel.grid(row=2, column=2, ipady=3,pady=5)
        ttk.Label(processOption, text='mK',font=4).grid(row=2, column=3)

        ttk.Label(processOption, text='NEdt最小值',font=4).grid(row=3, column=1)
        self.minLabel = ttk.Label(processOption, width=8,background="pink")
        self.minLabel.grid(row=3, column=2, ipady=3,pady=5)
        ttk.Label(processOption, text='mK',font=4).grid(row=3, column=3)
        self.btn.bind("<Button-1>",self.callback)
        ttk.Label(processOption).grid(row=1, column=4,padx=95)
        self.root.mainloop()



    def callback(self,event):
        self.dataModel = NEdt(self.filePath1, self.filePath2, self.entryW_var.get(), self.entryH_var.get(),self.entryT1_var.get(), self.entryT2_var.get(), self.entryFrameNum_var.get(), self.entryRadius_var.get(),self.entryFlag_var.get())
        # print(self.entryRadius_var.get(),self.entryFlag_var.get())
        self.dataModel.openFile()
        self.dataModel.dataProcessing()
        (self.averValue, self.stdValue, self.maxValue, self.minValue) = self.dataModel.resultReturn()
        self.dataModel.closeFile()
        self.averLabel.config(text=str(round(self.averValue,2)))
        self.stdLabel.config(text=str(round(self.stdValue,2)))
        self.maxLabel.config(text=str(round(self.maxValue,2)))
        self.minLabel.config(text=str(round(self.minValue,2)))

if __name__ =="__main__":
    myGUI=GUI()
    myGUI.run()