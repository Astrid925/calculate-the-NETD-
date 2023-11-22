import tkinter as tk
from tkinter import filedialog, ttk
from NEdtClass import NEdt

class GUI():

    def __init__(self) ->None:
        self.root=tk.Tk()
        self.root.geometry('800x600')
        self.root.title('NEdt计算软件')

    def filePath1(self):
        self.filePath1 = filedialog.askopenfilename()
        if self.filePath1 is not None:
            self.v1.set(self.filePath1)
            return self.filePath1

    def filePath2(self):
        self.filePath2 = filedialog.askopenfilename()
        if self.filePath2 is not None:
            self.v2.set(self.filePath2)
            return self.filePath2

    def run(self):
        inputOption = tk.LabelFrame(self.root, font=10,text='输入参数和文件路径', padx=10, pady=10)
        inputOption.place(x=20, y=20)
        # 图像宽和高参数
        self.entryW_var = tk.StringVar()
        ttk.Label(inputOption, text='图像宽度',font=4).grid(column=0,row=0)
        tk.Entry(inputOption, width=10,bg="pink", textvariable=self.entryW_var, state='normal').place(x=90,y=0, anchor="nw")
        self.entryH_var = tk.StringVar()
        ttk.Label(inputOption, text='图像高度',font=4).grid(column=0,row=1,pady=5)
        tk.Entry(inputOption, width=10,bg="pink", textvariable=self.entryH_var, state='normal').place(x=90,y=30, anchor="nw")
        # 温度参数
        self.entryT1_var = tk.StringVar()
        ttk.Label(inputOption, text='温度1',font=4).place(x=230,y=0, anchor="nw")
        tk.Entry(inputOption, width=10, bg="pink",textvariable=self.entryT1_var, state='normal').place(x=280,y=-5, anchor="nw")
        ttk.Label(inputOption, text='K',font=4).place(x=360,y=0, anchor="nw")
        self.entryT2_var = tk.StringVar()
        ttk.Label(inputOption, text='温度2',font=4).place(x=230,y=30, anchor="nw")
        tk.Entry(inputOption, width=10, bg="pink",textvariable=self.entryT2_var, state='normal').place(x=280,y=25, anchor="nw")
        ttk.Label(inputOption, text='K',font=4).place(x=360,y=30, anchor="nw")
        # 是否有辅助数据
        self.entryFlag_var=tk.IntVar()
        tk.Checkbutton(inputOption,text="有无辅助数据",font=4,bg="pink",variable=self.entryFlag_var).place(x=400,y=20, anchor="nw")
        # 输入文件路径
        self.v1 = tk.StringVar()
        ttk.Label(inputOption, text='温度1数据文件',font=4).grid(column=0, row=3,pady=5)
        tk.Entry(inputOption, width=50, bg="pink",textvariable=self.v1).grid(column=1, row=3,pady=5)
        tk.Button(inputOption, text='...',width=4, bg="plum",command=lambda: self.filePath1()).grid(column=2, row=3, padx=5, pady=5,stick=tk.E)
        self.v2 = tk.StringVar()
        ttk.Label(inputOption, text='温度2数据文件',font=4).grid(column=0, row=4),
        tk.Entry(inputOption, width=50, bg="pink",textvariable=self.v2).grid(column=1, row=4)
        tk.Button(inputOption, text='...', width=4,bg="plum", command=lambda: self.filePath2()).grid(column=2, row=4, padx=5, stick=tk.E)
        # 输出
        processOption = tk.LabelFrame(self.root, text='输出NEdt结果', padx=10, pady=10)
        processOption.place(x=20, y=300)
        tk.Button(processOption, text='计算NEdt', width=8, bg="lightcoral",command=lambda: self.start()).grid(column=0, row=0, padx=5,sticky=tk.W)

        self.averNEdt= tk.StringVar()
        ttk.Label(processOption, text='平均NEdt').grid(column=1, row=0)
        tk.Entry(processOption, width=10, bg="pink", textvariable=self.averNEdt, state='normal').grid(column=2, row=0)
        ttk.Label(processOption, text='mK').grid(column=3, row=0)

        self.stdNEdt = tk.StringVar()
        ttk.Label(processOption, text='NEdt标准差').grid(column=1, row=1)
        tk.Entry(processOption, width=10, bg="pink", textvariable=self.stdNEdt, state='normal').grid(column=2, row=1)
        ttk.Label(processOption, text='mK').grid(column=3, row=1)

        self.maxNEdt = tk.StringVar()
        ttk.Label(processOption, text='NEdt最大值').grid(column=1, row=2)
        tk.Entry(processOption, width=10, bg="pink", textvariable=self.maxNEdt, state='normal').grid(column=2, row=2)
        ttk.Label(processOption, text='mK').grid(column=3, row=2)

        self.minNEdt = tk.StringVar()
        ttk.Label(processOption, text='NEdt最小值').grid(column=1, row=3)
        tk.Entry(processOption, width=10, bg="pink", textvariable=self.minNEdt, state='normal').grid(column=2, row=3)
        ttk.Label(processOption, text='mK').grid(column=3, row=3)
        self.root.mainloop()

    def start(self):
        self.dataModel = NEdt(self.filepath1, self.filepath2, self.entryW_var.get(), self.entryH_var.get(), self.entryT1_var.get(), self.entryT2_var.get(), self.entryFlag_var.get())
        self.dataModel.openFile()
        self.dataModel.dataProcessing()
        (self.averNEdt, self.stdNEdt, self.maxNEdt, self.minNEdt)=self.dataModel.resultReturn()

        self.dataModel.closeFile()

if __name__ =="__main__":
    myGUI=GUI()
    myGUI.run()