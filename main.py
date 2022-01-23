import csv
import sys

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from PyQt5 import sip
from PyQt5.QtCore import *
# 导入图形组件库
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC

plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
# 导入做好的界面库
from untitled import Ui_MainWindow  # 管理员登录
from untitled0 import Ui_MainWindow0  # 普通用户登录
from untitled1 import Ui_MainWindow1  # 登录
from untitled2 import Ui_MainWindow2  # 注册
import os
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.stats.weightstats as sw
from sklearn.model_selection import train_test_split  # 这里是引用了交叉验证
from sklearn.linear_model import LinearRegression  # 线性回归

from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

"""
使用python和pyqt5（tkinter也可）搭建一个数据分析可视化的平台目标：
基于已有的数据搭建一个可视化的数据分析系统数据分析的对象：2020年12个牌号数据功能模块：
1、登录模块（账号密码，具有注册、登录等功能）登陆后，可以使用数据分析可视化的相应功能模块

2、功能模块（以下功能均分牌号查询）
2.1 查询功能，可以分牌号查询某一组（某一日/某一月/全年所有）的具体数据。根据给定的标准，
可以选择输出某一指标的合格率以及出现不合格数据的数据行
2.2 剔除异常数据功能，可以剔除不符合给定标准范围及不符合3σ原则的数据（2.3到2.5的内容最好可以分别选择不剔除异常数据进行处理以及
剔除异常数据后进行处理）

2.3 组内数据分析：
① 一些简单指标的可视化，选择不同的因素指标，
可以查询该因素在某一组（某一日/某一月/全年所有）的均值、方差、偏度、峰度、
变异系数、极差、最小值、最大值、下四分位数、上四分位数、中位数指标。
可以选择绘制箱线图、散点图、直方图。
② 正态性检验，使用ks检验的方法，
用户可以选择不同的因素指标，可以进行组内正态性检验，判断该因素数据是否符合正态分布并输出结果。
③ t检验，用户可以选择不同因素指标，根据输入的值，判断该因素数据的稳定性。0.05p值判断显不显著
2.4 组间数据分析
① 使用z检验的方法，计算用户指定范围内（日、月或年）各组数据的p值，输出，绘制折线图
② 计算用户指定范围内（日、月或年）各组数据的平均值、中位数，输出，绘制折线图
③ 计算用户指定范围内（日、月或年）各组数据的CV变异系数，输出，绘制折线图
2.5 多因素分析模块由用户选择数据范围（每一组，每一天，每一月，全年）
① 以PD为因变量，分析每个物理指标与PD的关系显著性
② 筛除不显著自变量
③ 建立剩余自变量与PD的多元线性回归方程（输出系数，拟合图像）

备注：1、数据描述：数据为txt文件，月份、日子可能不全，每个txt（即每一天的数据）中数据组数不一定，每一组中可能有少数数据不是30个，
不影响结果。
2、部分因素指标没有给出标准，这些没有标准的指标不用做正态检验、t检验、z检验等涉及到标准的分析了。

"""

"""
    定义文件类，继承界面程序Ui_MainWindow
"""


# 登录
class MainWindow1(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        # 继承(QMainWindow,Ui_MainWindow)父类的属性
        super(MainWindow1, self).__init__()
        # 初始化界面组件
        self.setupUi(self)
        self.i = 0
        self.init_()
        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.ppp)

    def ppp(self):
        self.p = MainWindow2()
        self.p.show()
        self.close()

    def init_(self):
        self.a = []
        with open("pic_show/account.csv", "r") as f:
            f = csv.reader(f)
            for i in f:
                self.a.append(i)
        self.a1 = [i[0] for i in self.a]  # 账号
        self.a2 = [i[1] for i in self.a]  # 密码
        self.a3 = [i[2] for i in self.a]  # 权限

    def login(self):
        # 账号
        self.account = self.lineEdit.text()
        # 密码
        self.code = self.lineEdit_2.text()
        print(self.account, self.code)
        # 判断账号和密码是否正确
        for i in self.a:
            if i[0:2] == [self.account, self.code]:
                print("登录成功")
                if i[2] == '1':
                    # 实例化主窗口
                    self.w = MainWindow()
                    # 展示主窗口
                    self.w.show()
                    # 当前登录窗口关闭
                    self.close()
                    self.i += 1
                elif i[2] == '0':
                    # 实例化主窗口
                    self.w = MainWindow0()
                    # 展示主窗口
                    self.w.show()
                    # 当前登录窗口关闭
                    self.close()
                    self.i += 1
        if self.i == 0:
            # 如果账号密码不正确，发出警告
            print(QMessageBox.warning(self, "警告", "账号或者密码不正确！", QMessageBox.Yes))


# 注册
class MainWindow2(QMainWindow, Ui_MainWindow2):
    def __init__(self):
        # 继承(QMainWindow,Ui_MainWindow)父类的属性
        super(MainWindow2, self).__init__()
        # 初始化界面组件
        self.setupUi(self)
        self.init_()
        self.pushButton_2.clicked.connect(self.ppp)
        self.pushButton.clicked.connect(self.back)

    def init_(self):
        self.a = []
        with open("pic_show/account.csv", "r") as f:
            f = csv.reader(f)
            for i in f:
                self.a.append(i)
        self.a1 = [i[0] for i in self.a]  # 账号
        self.a2 = [i[1] for i in self.a]  # 密码

    def ppp(self):
        account = self.lineEdit.text()
        mima = self.lineEdit_2.text()
        mima2 = self.lineEdit_3.text()
        if account not in self.a1:
            if mima == mima2:
                with open("pic_show/account.csv", "w", newline="") as f:
                    if self.radioButton.isChecked():
                        grade = '1'
                    else:
                        grade = '0'
                    f = csv.writer(f)
                    self.a.append([account, mima2,grade])
                    f.writerows(self.a)
                print(QMessageBox.warning(self, "提示", "注册成功", QMessageBox.Yes))
                self.w1 = MainWindow1()
                self.w1.show()
                self.close()
            else:
                print(QMessageBox.warning(self, "警告", "输入的两次密码不一致", QMessageBox.Yes))
        else:
            print(QMessageBox.warning(self, "警告", "账号已经存在", QMessageBox.Yes))

    def back(self):
        self.p1 = MainWindow1()
        self.p1.show()
        self.close()


# 2、功能模块（以下功能均分牌号查询）
# 2.1 查询功能，可以分牌号查询某一组（某一日/某一月/全年所有）的具体数据。根据给定的标准，
# 可以选择输出某一指标的合格率以及出现不合格数据的数据行
# 2.2 剔除异常数据功能，可以剔除不符合给定标准范围及不符合3σ原则的数据（2.3到2.5的内容最好可以分别选择不剔除异常数据进行处理以及
# 剔除异常数据后进行处理）

#普通用户功能模块
class MainWindow0(QMainWindow, Ui_MainWindow0):
        def __init__(self):
            # 继承(QMainWindow,Ui_MainWindow)父类的属性
            super(MainWindow0, self).__init__()
            # 初始化界面组件
            self.setupUi(self)
            self.tabWidget.setCurrentIndex(0)
            self.init_()
            # 查询
            self.pushButton_15.clicked.connect(self.chaxun)
            # 统计合格率
            self.pushButton.clicked.connect(self.tongji)
            # 画图
            self.pushButton_2.clicked.connect(self.huatu)
            # 正态性
            self.pushButton_3.clicked.connect(self.t_z)
            # t检验
            self.pushButton_4.clicked.connect(self.t)
            # 月度分析#3
            self.pushButton_14.clicked.connect(self.fenxi3)
            # 4
            #        self.pushButton_13.clicked.connect(self.fenxi4)
            # 5月度综合分析
            self.pushButton_16.clicked.connect(self.fenxi5)
            self.pushButton_5.clicked.connect(self.fenxi6)
            # 6年度数据分析
            self.pushButton_6.clicked.connect(self.fenxi7)
            # pingpai#1
            self.comboBox.currentIndexChanged.connect(self.selectionchange)
            # year
            self.comboBox_2.currentIndexChanged.connect(self.selectionchange1)
            # 月
            self.comboBox_3.currentIndexChanged.connect(self.selectionchange2)
            # 日
            self.comboBox_4.currentIndexChanged.connect(self.selectionchange3)

            # pingpai#2
            self.comboBox_13.currentIndexChanged.connect(self.selectionchange0)
            # year
            self.comboBox_11.currentIndexChanged.connect(self.selectionchange11)
            # 月
            self.comboBox_12.currentIndexChanged.connect(self.selectionchange22)
            # 日
            self.comboBox_14.currentIndexChanged.connect(self.selectionchange33)

            # pingpai#3
            self.comboBox_23.currentIndexChanged.connect(self.selectionchange00)
            # year
            self.comboBox_22.currentIndexChanged.connect(self.selectionchange111)

            # pingpai#4

            # pingpai#5
            self.comboBox_62.currentIndexChanged.connect(self.selectionchange0000)
            # year
            self.comboBox_64.currentIndexChanged.connect(self.selectionchange11111)

            # pingpai#5  左边的
            self.comboBox_67.currentIndexChanged.connect(self.selectionchange00000)
            # year
            self.comboBox_65.currentIndexChanged.connect(self.selectionchange111111)

            # pingpai#5  右边的
            self.comboBox_70.currentIndexChanged.connect(self.selectionchange000000)
            # year
            self.comboBox_69.currentIndexChanged.connect(self.selectionchange1111111)

            # 年度数据
            self.comboBox_71.currentIndexChanged.connect(self.selectionchange0000000)
            self.comboBox_72.currentIndexChanged.connect(self.selectionchange11111111)
            # 年度数据分析

        def fenxi7(self):

            zhuangtai = False
            if self.radioButton_13.isChecked():
                zhuangtai = True
            # 左边的数据
            pingpai = self.comboBox_71.currentText()
            nian = self.comboBox_72.currentText()
            # yue = self.comboBox_66.currentText()

            text = pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            # 根据所选的年获取月的数据
            yues = []
            for key, value in self.data2.items():
                nians = os.path.split(key)[-1]
                yues.append(nians)
            total_data = {}
            for yue in yues:
                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
                data3 = self.data[path1][path2][path3]  # 到txt
                last_result = []
                label = []

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            if len(lines[i].split()) == 10:
                                try:
                                    total["wt"].append(float(lines[i].split()[1].strip("*")))
                                    total["circ"].append(float(lines[i].split()[2].strip("*")))
                                    total["PD"].append(float(lines[i].split()[3].strip("*")))
                                    total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                    total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                    total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                    total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                    total["Len"].append(float(lines[i].split()[8].strip("*")))
                                    total["DD"].append(float(lines[i].split()[9].strip("*")))
                                except:
                                    pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                for path in data3:
                    # all txt组
                    data = load_data(path)
                    # 【】1
                    p = 0
                    for i in data:
                        p += 1
                        last_result.append(i)  # [[],[]]
                        label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

                total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                         "DD": []}
                for da in last_result:
                    print(da)
                    for i in da["wt"]:
                        total["wt"].append(i)
                    for i in da["circ"]:
                        total["circ"].append(i)
                    for i in da["PD"]:
                        total["PD"].append(i)
                    for i in da["CPD"]:
                        total["CPD"].append(i)
                    for i in da["Vent"]:
                        total["Vent"].append(i)
                    for i in da["PVnt"]:
                        total["PVnt"].append(i)
                    for i in da["TotV"]:
                        total["TotV"].append(i)
                    for i in da["Len"]:
                        total["Len"].append(i)
                    for i in da["DD"]:
                        total["DD"].append(i)

                if zhuangtai:
                    def contrast(pingpaiming, canshu, num):
                        # 初始化标准
                        standard = []
                        with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                            f = csv.reader(f)
                            for i in f:
                                standard.append(i)
                            del standard[0]

                        # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                        for i in standard:
                            if i[1] == pingpaiming:
                                if canshu == "wt":
                                    sp = float(i[2].split("±")[0])
                                    sp1 = float(i[2].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "PD":
                                    sp = float(i[3].split("±")[0]) / 1000
                                    sp1 = float(i[3].split("±")[1]) / 1000
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "TotV":
                                    sp = float(i[4].split("±")[0])
                                    sp1 = float(i[4].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "DD":
                                    sp = float(i[5].split("±")[0])
                                    sp1 = float(i[5].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "circ":
                                    sp = float(i[6].split("±")[0])
                                    sp1 = float(i[6].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"

                    # TODO:字典数据total
                    # TODO:字典数据total
                    def try_(pingpai, total):

                        wt = total["wt"]  #
                        circ = total["circ"]  #
                        PD = total["PD"]  #
                        cpd = total["CPD"]
                        vent = total["Vent"]
                        pvnt = total["PVnt"]
                        totv = total["TotV"]  #
                        Len = total["Len"]
                        DD = total["DD"]  #
                        # 去除不符合标准的contrast
                        for i in range(len(wt)):
                            if contrast(pingpai, "wt", wt[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(circ)):
                            if contrast(pingpai, "circ", circ[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(PD)):
                            if contrast(pingpai, "PD", PD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(totv)):
                            if contrast(pingpai, "TotV", totv[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(DD)):
                            if contrast(pingpai, "DD", DD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        # todo:不符合3σ
                        # wt
                        # np.std(a,ddof=1)
                        left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                        right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                        left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                        right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                        left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                        right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                        left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                        right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                        left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                        right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                        left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                        right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                        left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                        right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                        left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                        right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                        left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                        right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                        nums = []
                        for i in range(len(wt)):
                            if left < wt[i] < right:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        nums = []
                        # circ
                        for i in range(len(circ)):
                            if left1 < circ[i] < right1:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]
                        # PD
                        nums = []
                        for i in range(len(PD)):
                            if left2 < PD[i] < right2:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # cpd
                        nums = []
                        for i in range(len(cpd)):
                            if left3 < cpd[i] < right3:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # vent
                        nums = []

                        for i in range(len(vent)):
                            if left4 < vent[i] < right4:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # pvnt
                        nums = []

                        for i in range(len(pvnt)):
                            if left5 < pvnt[i] < right5:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # totv
                        nums = []
                        for i in range(len(totv)):
                            if left6 < totv[i] < right6:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # Len
                        nums = []
                        for i in range(len(Len)):
                            if left7 < Len[i] < right7:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # DD
                        nums = []
                        for i in range(len(DD)):
                            if left8 < DD[i] < right8:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                                "Len": Len, "DD": DD}

                    data5 = try_(pingpai, total)
                    # {"wt":"","",""}
                else:
                    data5 = total
                total_data[yue] = data5
            ####------- total_data ------->根据年得到月的所有数据
            chooseItem = self.comboBox_27.currentText()
            if self.comboBox_26.currentText() == "质量":
                zhibiao = "wt"
            elif self.comboBox_26.currentText() == "圆周":
                zhibiao = "circ"
            elif self.comboBox_26.currentText() == "吸阻":
                zhibiao = "PD"
            elif self.comboBox_26.currentText() == "封闭吸阻":
                zhibiao = "CPD"
            elif self.comboBox_26.currentText() == "滤嘴通风":
                zhibiao = "Vent"
            elif self.comboBox_26.currentText() == "纸通风":
                zhibiao = "PVnt"
            elif self.comboBox_26.currentText() == "总通风":
                zhibiao = "TotV"
            elif self.comboBox_26.currentText() == "长度":
                zhibiao = "Len"
            elif self.comboBox_26.currentText() == "硬度":
                zhibiao = "DD"
            # "分指标质量控制图", "分指标年度z检验p值折线图","分指标年度变异系数折线图","分指标年度中位数折线图",
            if chooseItem == "年度分指标质量控制图":

                # 均值图
                label = []
                data_get = []
                for key, item in total_data.items():
                    label.append(key)
                    data_get.append(item[zhibiao])
                try:
                    sip.delete(self.canvasv)
                    sip.delete(self.layoutv)
                except:
                    pass
                self.figv = plt.Figure()
                self.canvasv = FC(self.figv)
                self.layoutv = QVBoxLayout()
                self.layoutv.addWidget(self.canvasv)
                self.widget_5.setLayout(self.layoutv)
                ax = self.figv.add_subplot(111)
                ######z
                all = []
                for i in data_get:
                    all.append(np.mean(i))
                ax.plot(label, [np.mean(i) for i in data_get])
                ax.scatter(label, [np.mean(i) for i in data_get])
                ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
                ax.set_title("年度x图（均值图）")
                self.canvasv.draw_idle()
                self.canvasv.draw()  # TODO:这里开始绘制

                # S图（标准差图）
                try:
                    sip.delete(self.canvasp)
                    sip.delete(self.layoutp)
                except:
                    pass

                self.figp = plt.Figure()
                self.canvasp = FC(self.figp)
                self.layoutp = QVBoxLayout()
                self.layoutp.addWidget(self.canvasp)
                self.widget_6.setLayout(self.layoutp)
                ax = self.figp.add_subplot(111)
                ######z
                all = []
                for i in data_get:
                    all.append(np.std(i))
                ax.plot(label, [np.std(i) for i in data_get])
                ax.scatter(label, [np.std(i) for i in data_get])
                ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
                ax.set_title("年度S图（标准差图）")
                self.canvasp.draw_idle()
                self.canvasp.draw()  # TODO:这里开始绘制

                # R图（极差图）

                try:
                    sip.delete(self.canvaso)
                    sip.delete(self.layouto)
                except:
                    pass

                self.figo = plt.Figure()
                self.canvaso = FC(self.figo)
                self.layouto = QVBoxLayout()
                self.layouto.addWidget(self.canvaso)
                self.widget_7.setLayout(self.layouto)
                ax = self.figo.add_subplot(111)
                ######z
                all = []
                for i in data_get:
                    all.append(max(i) - min(i))
                ax.plot(label, [max(i) - min(i) for i in data_get])
                ax.scatter(label, [max(i) - min(i) for i in data_get])

                ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
                ax.set_title("年度R图（极差图）")
                self.canvaso.draw_idle()
                self.canvaso.draw()  # TODO:这里开始绘制
            elif chooseItem == "分指标年度z检验p值折线图":

                label = []
                data_get = []
                for key, item in total_data.items():
                    label.append(key)
                    data_get.append(item[zhibiao])
                try:
                    sip.delete(self.canvasv)
                    sip.delete(self.layoutv)
                except:
                    pass
                self.figv = plt.Figure()
                self.canvasv = FC(self.figv)
                self.layoutv = QVBoxLayout()
                self.layoutv.addWidget(self.canvasv)
                self.widget_5.setLayout(self.layoutv)
                ax = self.figv.add_subplot(111)
                ######z
                ax.plot(label, [sw.ztest(i, value=float(self.lineEdit_6.text()))[1] for i in data_get])
                ax.set_title("分指标年度z检验p值折线图")
                self.canvasv.draw_idle()
                self.canvasv.draw()  # TODO:这里开始绘制
            elif chooseItem == "分指标年度变异系数折线图":  #

                label = []
                data_get = []
                for key, item in total_data.items():
                    label.append(key)
                    data_get.append(item[zhibiao])
                try:
                    sip.delete(self.canvasv)
                    sip.delete(self.layoutv)
                except:
                    pass
                self.figv = plt.Figure()
                self.canvasv = FC(self.figv)
                self.layoutv = QVBoxLayout()
                self.layoutv.addWidget(self.canvasv)
                self.widget_5.setLayout(self.layoutv)
                ax = self.figv.add_subplot(111)
                ax.plot(label, [np.std(i) / np.mean(i) for i in data_get])

                ax.plot(label, [0.01 for i in range(len(label))], linestyle="--")
                ax.plot(label, [0.02 for i in range(len(label))], linestyle="--")
                ax.plot(label, [0.03 for i in range(len(label))], linestyle="--")
                ax.plot(label, [0.04 for i in range(len(label))], linestyle="--")
                ax.plot(label, [0.1 for i in range(len(label))], linestyle="--")

                ax.set_title("分指标年度变异系数折线图")
                self.canvasv.draw_idle()
                self.canvasv.draw()  # TODO:这里开始绘制
            elif chooseItem == "分指标年度中位数折线图":
                label = []
                data_get = []
                for key, item in total_data.items():
                    label.append(key)
                    data_get.append(item[zhibiao])
                try:
                    sip.delete(self.canvasv)
                    sip.delete(self.layoutv)
                except:
                    pass
                self.figv = plt.Figure()
                self.canvasv = FC(self.figv)
                self.layoutv = QVBoxLayout()
                self.layoutv.addWidget(self.canvasv)
                self.widget_5.setLayout(self.layoutv)
                ax = self.figv.add_subplot(111)

                # 中位数
                def get_median(data):
                    data.sort()
                    half = len(data) // 2
                    return (data[half] + data[~half]) / 2

                ax.plot(label, [get_median(i) for i in data_get])

                ax.set_title("年度中位数折线图")
                self.canvasv.draw_idle()
                self.canvasv.draw()  # TODO:这里开始绘制
            elif chooseItem == "月度分指标质量控制图":
                zhuangtai = False
                if self.radioButton_13.isChecked():
                    zhuangtai = True
                pingpai = self.comboBox_71.currentText()
                nian = self.comboBox_72.currentText()
                yue = self.comboBox_73.currentText()
                if self.comboBox_26.currentText() == "质量":
                    zhibiao = "wt"
                elif self.comboBox_26.currentText() == "圆周":
                    zhibiao = "circ"
                elif self.comboBox_26.currentText() == "吸阻":
                    zhibiao = "PD"
                elif self.comboBox_26.currentText() == "封闭吸阻":
                    zhibiao = "CPD"
                elif self.comboBox_26.currentText() == "滤嘴通风":
                    zhibiao = "Vent"
                elif self.comboBox_26.currentText() == "纸通风":
                    zhibiao = "PVnt"
                elif self.comboBox_26.currentText() == "总通风":
                    zhibiao = "TotV"
                elif self.comboBox_26.currentText() == "长度":
                    zhibiao = "Len"
                elif self.comboBox_26.currentText() == "硬度":
                    zhibiao = "DD"
                text = pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
                data3 = self.data[path1][path2][path3]  # 到txt

                last_result = []
                label = []

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []

                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                # print(float(lines[i].split()[1].strip("*")))
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                for path in data3:
                    # all txt组
                    data = load_data(path)
                    # 【】1
                    p = 0
                    for i in data:
                        p += 1
                        last_result.append(i)  # [[],[]]
                        label.append(str(p))  # ["txt"]

                if zhuangtai:
                    def contrast(pingpaiming, canshu, num):
                        # 初始化标准
                        standard = []
                        with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                            f = csv.reader(f)
                            for i in f:
                                standard.append(i)
                            del standard[0]

                        # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                        for i in standard:
                            if i[1] == pingpaiming:
                                if canshu == "wt":
                                    sp = float(i[2].split("±")[0])
                                    sp1 = float(i[2].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "PD":
                                    sp = float(i[3].split("±")[0]) / 1000
                                    sp1 = float(i[3].split("±")[1]) / 1000
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "TotV":
                                    sp = float(i[4].split("±")[0])
                                    sp1 = float(i[4].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "DD":
                                    sp = float(i[5].split("±")[0])
                                    sp1 = float(i[5].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "circ":
                                    sp = float(i[6].split("±")[0])
                                    sp1 = float(i[6].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"

                    # TODO:字典数据total
                    # TODO:字典数据total
                    def try_(pingpai, total):

                        wt = total["wt"]  #
                        circ = total["circ"]  #
                        PD = total["PD"]  #
                        cpd = total["CPD"]
                        vent = total["Vent"]
                        pvnt = total["PVnt"]
                        totv = total["TotV"]  #
                        Len = total["Len"]
                        DD = total["DD"]  #
                        # 去除不符合标准的contrast
                        for i in range(len(wt)):
                            if contrast(pingpai, "wt", wt[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(circ)):
                            if contrast(pingpai, "circ", circ[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(PD)):
                            if contrast(pingpai, "PD", PD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(totv)):
                            if contrast(pingpai, "TotV", totv[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(DD)):
                            if contrast(pingpai, "DD", DD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        # todo:不符合3σ
                        # wt
                        # np.std(a,ddof=1)
                        left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                        right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                        left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                        right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                        left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                        right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                        left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                        right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                        left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                        right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                        left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                        right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                        left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                        right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                        left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                        right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                        left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                        right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                        nums = []
                        for i in range(len(wt)):
                            if left < wt[i] < right:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        nums = []
                        # circ
                        for i in range(len(circ)):
                            if left1 < circ[i] < right1:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]
                        # PD
                        nums = []
                        for i in range(len(PD)):
                            if left2 < PD[i] < right2:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # cpd
                        nums = []
                        for i in range(len(cpd)):
                            if left3 < cpd[i] < right3:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # vent
                        nums = []

                        for i in range(len(vent)):
                            if left4 < vent[i] < right4:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # pvnt
                        nums = []

                        for i in range(len(pvnt)):
                            if left5 < pvnt[i] < right5:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # totv
                        nums = []
                        for i in range(len(totv)):
                            if left6 < totv[i] < right6:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # Len
                        nums = []
                        for i in range(len(Len)):
                            if left7 < Len[i] < right7:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # DD
                        nums = []
                        for i in range(len(DD)):
                            if left8 < DD[i] < right8:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                                "Len": Len, "DD": DD}

                    data5 = [try_(pingpai, i) for i in last_result]
                    data5 = [i[zhibiao] for i in data5]

                else:
                    data5 = [i[zhibiao] for i in last_result]
                label = [i + 1 for i in range(len(label))]

                try:
                    sip.delete(self.canvasv)
                    sip.delete(self.layoutv)
                except:
                    pass
                self.figv = plt.Figure()
                self.canvasv = FC(self.figv)
                self.layoutv = QVBoxLayout()
                self.layoutv.addWidget(self.canvasv)
                self.widget_5.setLayout(self.layoutv)
                ax = self.figv.add_subplot(111)
                ######z
                all = []
                for i in data5:
                    all.append(np.mean(i))
                ax.plot(label, [np.mean(i) for i in data5])
                ax.scatter(label, [np.mean(i) for i in data5])
                ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
                ax.set_title("月度x图（均值图）")
                self.canvasv.draw_idle()
                self.canvasv.draw()  # TODO:这里开始绘制

                # S图（标准差图）
                try:
                    sip.delete(self.canvasp)
                    sip.delete(self.layoutp)
                except:
                    pass

                self.figp = plt.Figure()
                self.canvasp = FC(self.figp)
                self.layoutp = QVBoxLayout()
                self.layoutp.addWidget(self.canvasp)
                self.widget_6.setLayout(self.layoutp)
                ax = self.figp.add_subplot(111)
                ######z
                all = []
                for i in data5:
                    all.append(np.std(i))
                ax.plot(label, [np.std(i) for i in data5])
                ax.scatter(label, [np.std(i) for i in data5])
                ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
                ax.set_title("月度S图（标准差图）")
                self.canvasp.draw_idle()
                self.canvasp.draw()  # TODO:这里开始绘制

                # R图（极差图）

                try:
                    sip.delete(self.canvaso)
                    sip.delete(self.layouto)
                except:
                    pass

                self.figo = plt.Figure()
                self.canvaso = FC(self.figo)
                self.layouto = QVBoxLayout()
                self.layouto.addWidget(self.canvaso)
                self.widget_7.setLayout(self.layouto)
                ax = self.figo.add_subplot(111)
                ######z
                all = []
                for i in data5:
                    all.append(max(i) - min(i))
                ax.plot(label, [max(i) - min(i) for i in data5])
                ax.scatter(label, [max(i) - min(i) for i in data5])

                ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
                ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
                ax.set_title("月度R图（极差图）")
                self.canvaso.draw_idle()
                self.canvaso.draw()  # TODO:这里开始绘制

        def fenxi6(self):

            zhuangtai = False
            if self.radioButton_12.isChecked():
                zhuangtai = True
            # 左边的数据
            pingpai = self.comboBox_67.currentText()
            nian = self.comboBox_65.currentText()
            yue = self.comboBox_66.currentText()
            text = pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]  # 到txt
            last_result = []
            label = []

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        if len(lines[i].split()) == 10:
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                    group.append(total)  # 提取的全在group里面了
                return group

            for path in data3:
                # all txt组
                data = load_data(path)
                # 【】1
                p = 0
                for i in data:
                    p += 1
                    last_result.append(i)  # [[],[]]
                    label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

            total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [], "DD": []}
            for da in last_result:

                for i in da["wt"]:
                    total["wt"].append(i)
                for i in da["circ"]:
                    total["circ"].append(i)
                for i in da["PD"]:
                    total["PD"].append(i)
                for i in da["CPD"]:
                    total["CPD"].append(i)
                for i in da["Vent"]:
                    total["Vent"].append(i)
                for i in da["PVnt"]:
                    total["PVnt"].append(i)
                for i in da["TotV"]:
                    total["TotV"].append(i)
                for i in da["Len"]:
                    total["Len"].append(i)
                for i in da["DD"]:
                    total["DD"].append(i)

            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = try_(pingpai, total)

            else:
                data5 = total
            # 右边的数据
            try:
                pingpai = self.comboBox_70.currentText()
                nian = self.comboBox_69.currentText()
                yue = self.comboBox_68.currentText()
                text = pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
                data3 = self.data[path1][path2][path3]  # 到txt
                last_result = []
                label = []

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            if len(lines[i].split()) == 10:
                                try:
                                    total["wt"].append(float(lines[i].split()[1].strip("*")))
                                    total["circ"].append(float(lines[i].split()[2].strip("*")))
                                    total["PD"].append(float(lines[i].split()[3].strip("*")))
                                    total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                    total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                    total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                    total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                    total["Len"].append(float(lines[i].split()[8].strip("*")))
                                    total["DD"].append(float(lines[i].split()[9].strip("*")))
                                except:
                                    pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                for path in data3:
                    # all txt组
                    data = load_data(path)
                    # 【】1
                    p = 0
                    for i in data:
                        p += 1
                        last_result.append(i)  # [[],[]]
                        label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

                total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                         "DD": []}
                for da in last_result:

                    for i in da["wt"]:
                        total["wt"].append(i)
                    for i in da["circ"]:
                        total["circ"].append(i)
                    for i in da["PD"]:
                        total["PD"].append(i)
                    for i in da["CPD"]:
                        total["CPD"].append(i)
                    for i in da["Vent"]:
                        total["Vent"].append(i)
                    for i in da["PVnt"]:
                        total["PVnt"].append(i)
                    for i in da["TotV"]:
                        total["TotV"].append(i)
                    for i in da["Len"]:
                        total["Len"].append(i)
                    for i in da["DD"]:
                        total["DD"].append(i)

                if zhuangtai:
                    def contrast(pingpaiming, canshu, num):
                        # 初始化标准
                        standard = []
                        with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                            f = csv.reader(f)
                            for i in f:
                                standard.append(i)
                            del standard[0]

                        # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                        for i in standard:
                            if i[1] == pingpaiming:
                                if canshu == "wt":
                                    sp = float(i[2].split("±")[0])
                                    sp1 = float(i[2].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "PD":
                                    sp = float(i[3].split("±")[0]) / 1000
                                    sp1 = float(i[3].split("±")[1]) / 1000
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "TotV":
                                    sp = float(i[4].split("±")[0])
                                    sp1 = float(i[4].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "DD":
                                    sp = float(i[5].split("±")[0])
                                    sp1 = float(i[5].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "circ":
                                    sp = float(i[6].split("±")[0])
                                    sp1 = float(i[6].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"

                    # TODO:字典数据total
                    # TODO:字典数据total
                    def try_(pingpai, total):

                        wt = total["wt"]  #
                        circ = total["circ"]  #
                        PD = total["PD"]  #
                        cpd = total["CPD"]
                        vent = total["Vent"]
                        pvnt = total["PVnt"]
                        totv = total["TotV"]  #
                        Len = total["Len"]
                        DD = total["DD"]  #
                        # 去除不符合标准的contrast
                        for i in range(len(wt)):
                            if contrast(pingpai, "wt", wt[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(circ)):
                            if contrast(pingpai, "circ", circ[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(PD)):
                            if contrast(pingpai, "PD", PD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(totv)):
                            if contrast(pingpai, "TotV", totv[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(DD)):
                            if contrast(pingpai, "DD", DD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        # todo:不符合3σ
                        # wt
                        # np.std(a,ddof=1)
                        left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                        right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                        left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                        right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                        left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                        right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                        left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                        right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                        left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                        right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                        left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                        right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                        left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                        right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                        left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                        right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                        left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                        right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                        nums = []
                        for i in range(len(wt)):
                            if left < wt[i] < right:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        nums = []
                        # circ
                        for i in range(len(circ)):
                            if left1 < circ[i] < right1:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]
                        # PD
                        nums = []
                        for i in range(len(PD)):
                            if left2 < PD[i] < right2:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # cpd
                        nums = []
                        for i in range(len(cpd)):
                            if left3 < cpd[i] < right3:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # vent
                        nums = []

                        for i in range(len(vent)):
                            if left4 < vent[i] < right4:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # pvnt
                        nums = []

                        for i in range(len(pvnt)):
                            if left5 < pvnt[i] < right5:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # totv
                        nums = []
                        for i in range(len(totv)):
                            if left6 < totv[i] < right6:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # Len
                        nums = []
                        for i in range(len(Len)):
                            if left7 < Len[i] < right7:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # DD
                        nums = []
                        for i in range(len(DD)):
                            if left8 < DD[i] < right8:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                                "Len": Len, "DD": DD}

                    data55 = try_(pingpai, total)

                else:
                    data55 = total
            except:
                pass
            num = self.comboBox_25.currentText()
            if self.comboBox_24.currentText() == "质量":
                zhibiao = "wt"
            elif self.comboBox_24.currentText() == "圆周":
                zhibiao = "circ"
            elif self.comboBox_24.currentText() == "吸阻":
                zhibiao = "PD"
            elif self.comboBox_24.currentText() == "封闭吸阻":
                zhibiao = "CPD"
            elif self.comboBox_24.currentText() == "滤嘴通风":
                zhibiao = "Vent"
            elif self.comboBox_24.currentText() == "纸通风":
                zhibiao = "PVnt"
            elif self.comboBox_24.currentText() == "总通风":
                zhibiao = "TotV"
            elif self.comboBox_24.currentText() == "长度":
                zhibiao = "Len"
            elif self.comboBox_24.currentText() == "硬度":
                zhibiao = "DD"
            if num == "独立样本t检验":
                # 初始化删除数据
                self.textEdit_8.clear()
                # 1、查询每月数据_____________________________________
                for key, item in data55.items():
                    # t

                    sample = np.asarray(data5[key])
                    sample1 = np.asarray(data55[key])

                    r = stats.ttest_ind(sample, sample1)
                    self.textEdit_8.append(f"{key}" + "pvalue:" + str(r.__getattribute__("pvalue")))
                    self.textEdit_8.append("_____________________________________")
                    self.textEdit_8.append("_____________________________________")
            # 分指标单样本t检验
            elif num == "分指标单样本t检验":
                # 初始化删除数据
                self.textEdit_8.clear()
                # 1、查询每月数据_____________________________________
                bt = float(self.lineEdit_5.text())
                sample = np.asarray(np.array(data5[zhibiao]))
                # 单样本检验用stats.ttest_1samp
                r = stats.ttest_1samp(sample, bt, axis=0)
                self.textEdit_8.append(
                    "pvalue:" + str(
                        r.__getattribute__("pvalue")) + '\n' + "ks检验p值：" + str(
                        stats.kstest(data5[zhibiao], 'norm', (np.mean(data5[zhibiao]), np.std(data5[zhibiao])))))


            elif num == "分指标散点图":

                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                print(sp, sp1)
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                data = data5[zhibiao]

                num = len(data)  # 总数
                p = 0
                sp = []

                for i in range(len(data)):

                    if contrast(self.comboBox_67.currentText(), zhibiao, data[i]) == "合格":
                        p += 1
                    else:
                        # 不合格
                        sp.append(i)

                per = (p / num) * 100

                # 合格率
                self.textEdit_8.setText("总数为 " + str(num) + '\n' + "合格数为 " + str(p) + '\n' + "合格率为 " + str(per) + "%")

                def contrast1(pingpaiming, canshu):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:

                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])

                                return sp, sp1
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                return sp, sp1

                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                return sp, sp1
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                return sp, sp1
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                return sp, sp1

                sp, sp1 = contrast1(self.comboBox_67.currentText(), zhibiao)

                try:
                    sip.delete(self.canvasa)
                    sip.delete(self.layouta)
                except:
                    pass
                self.figa = plt.Figure()
                self.canvasa = FC(self.figa)
                self.layouta = QVBoxLayout()
                self.layouta.addWidget(self.canvasa)
                self.widget_8.setLayout(self.layouta)
                ax = self.figa.add_subplot(111)
                # x的个数决定了样本量
                ax.scatter(np.arange(len(data5[zhibiao])), data5[zhibiao])
                ax.plot(np.arange(len(data5[zhibiao])), [sp - sp1 for i in range(len(data5[zhibiao]))], linestyle="-")
                ax.plot(np.arange(len(data5[zhibiao])), [sp1 + sp for i in range(len(data5[zhibiao]))], linestyle="-")
                ax.legend()
                ax.set_title("散点图")
                self.canvasa.draw_idle()
                self.canvasa.draw()  # TODO:这里开始绘制
            elif num == "分指标直方图":
                self.textEdit_8.clear()
                try:
                    sip.delete(self.canvasa)
                    sip.delete(self.layouta)
                except:
                    pass
                self.figa = plt.Figure()
                self.canvasa = FC(self.figa)
                self.layouta = QVBoxLayout()
                self.layouta.addWidget(self.canvasa)
                self.widget_8.setLayout(self.layouta)
                ax = self.figa.add_subplot(111)
                # x的个数决定了样本量
                ax.hist(data5[zhibiao])
                ax.legend()
                ax.set_title("直方图")
                self.canvasa.draw_idle()
                self.canvasa.draw()  # TODO:这里开始绘制
                self.textEdit_8.append("ks检验p值：" + str(
                    stats.kstest(data5[zhibiao], 'norm', (np.mean(data5[zhibiao]), np.std(data5[zhibiao])))))

        def fenxi5(self):
            # 1、查询每月数据
            # 2、显示每月数据的均值、方差、偏度、峰度、变异系数、极差、最小值、最大值、下四分位数、上四分位数、中位数指标
            # try:
            # 初始化删除数据
            self.textEdit_8.clear()
            zhuangtai = False
            if self.radioButton_11.isChecked():
                zhuangtai = True

            pingpai = self.comboBox_62.currentText()
            nian = self.comboBox_64.currentText()
            yue = self.comboBox_63.currentText()
            text = pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]  # 到txt

            last_result = []
            label = []

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        if len(lines[i].split()) == 10:
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                    group.append(total)  # 提取的全在group里面了
                return group

            for path in data3:
                # all txt组
                data = load_data(path)
                # 【】1
                p = 0
                for i in data:
                    p += 1
                    last_result.append(i)  # [[],[]]
                    label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

            total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [], "DD": []}
            for da in last_result:

                for i in da["wt"]:
                    total["wt"].append(i)
                for i in da["circ"]:
                    total["circ"].append(i)
                for i in da["PD"]:
                    total["PD"].append(i)
                for i in da["CPD"]:
                    total["CPD"].append(i)
                for i in da["Vent"]:
                    total["Vent"].append(i)
                for i in da["PVnt"]:
                    total["PVnt"].append(i)
                for i in da["TotV"]:
                    total["TotV"].append(i)
                for i in da["Len"]:
                    total["Len"].append(i)
                for i in da["DD"]:
                    total["DD"].append(i)

            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = try_(pingpai, total)

            else:
                data5 = total

            def foundation(data):
                # 均值
                aver = np.mean(data)
                # 方差
                std = np.var(data)
                # 偏度
                s = pd.Series(data)
                piandu = s.skew()
                # 峰度
                fengdu = s.kurt()  # <class 'numpy.float64'>
                # 变异系数
                cv = np.std(data) / np.mean(data)
                # 最大
                Max = max(data)
                # 最小
                Min = min(data)
                # 极差
                jicha = Max - Min

                # 中位数
                def get_median(data):
                    data.sort()
                    half = len(data) // 2
                    return (data[half] + data[~half]) / 2

                median = get_median(data)
                # 下四分位数
                xia = np.percentile(data, (75))
                # 上四分位数
                shang = np.percentile(data, (25))
                RSD = round((np.sqrt(std) / aver) * 100, 2)
                return aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang, RSD

            # 1、查询每月数据_____________________________________
            for key, item in data5.items():
                self.textEdit_8.append(str(key) + str(data5[key]))
                # 2、显示每月数据的均值、方差、偏度、峰度、变异系数、极差、最小值、最大值、下四分位数、上四分位数、中位数指标
                aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang, RSD = foundation(data5[key])
                # t
                bt = 2.0
                # bt = float(self.lineEdit_5.text())
                sample = np.asarray(data5[key])
                # 单样本检验用stats.ttest_1samp
                r = stats.ttest_1samp(sample, bt, axis=0)
                self.textEdit_8.append(f"{key}均值 {str(aver)}")
                self.textEdit_8.append(f"{key}方差 {str(std)}")
                self.textEdit_8.append(f"{key}偏度 {str(piandu)}")
                self.textEdit_8.append(f"{key}峰度 {str(fengdu)}")
                self.textEdit_8.append(f"{key}变异系数 {str(cv)}")
                self.textEdit_8.append(f"{key}最大值 {str(Max)}")
                self.textEdit_8.append(f"{key}最小值 {str(Min)}")
                self.textEdit_8.append(f"{key}极差 {str(jicha)}")
                self.textEdit_8.append(f"{key}中位数 {str(median)}")
                self.textEdit_8.append(f"{key}下四分位数 {str(shang)}")
                self.textEdit_8.append(f"{key}上四分位数 {str(xia)}")
                self.textEdit_8.append(f"{key}相对标准偏差RSd为{str(RSD)}%")
                self.textEdit_8.append(
                    f"{key} t检验 statistic:" + str(r.__getattribute__("statistic")) + "  " + "pvalue:" + str(
                        r.__getattribute__("pvalue")))
                self.textEdit_8.append("_____________________________________")
                self.textEdit_8.append("_____________________________________")

        def fenxi3(self):
            try:
                zhuangtai = False
                if self.radioButton_3.isChecked():
                    zhuangtai = True
                z = self.lineEdit.text()
                pingpai = self.comboBox_23.currentText()
                nian = self.comboBox_22.currentText()
                yue = self.comboBox_19.currentText()
                if self.comboBox_21.currentText() == "质量":
                    zhibiao = "wt"
                elif self.comboBox_21.currentText() == "圆周":
                    zhibiao = "circ"
                elif self.comboBox_21.currentText() == "吸阻":
                    zhibiao = "PD"
                elif self.comboBox_21.currentText() == "封闭吸阻":
                    zhibiao = "CPD"
                elif self.comboBox_21.currentText() == "滤嘴通风":
                    zhibiao = "Vent"
                elif self.comboBox_21.currentText() == "纸通风":
                    zhibiao = "PVnt"
                elif self.comboBox_21.currentText() == "总通风":
                    zhibiao = "TotV"
                elif self.comboBox_21.currentText() == "长度":
                    zhibiao = "Len"
                elif self.comboBox_21.currentText() == "硬度":
                    zhibiao = "DD"
                text = pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
                data3 = self.data[path1][path2][path3]  # 到txt
                # ① 使用z检验的方法，计算用户指定范围内（日、月或年）各组数据的p值，输出，绘制折线图
                # ② 计算用户指定范围内（日、月或年）各组数据的平均值、中位数，输出，绘制折线图
                # ③ 计算用户指定范围内（日、月或年）各组数据的CV变异系数，输出，绘制折线图
                last_result = []
                label = []

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []

                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                # print(float(lines[i].split()[1].strip("*")))
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                for path in data3:
                    # all txt组
                    data = load_data(path)
                    # 【】1
                    p = 0
                    for i in data:
                        p += 1
                        last_result.append(i)  # [[],[]]
                        label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]
                print(last_result)
                if zhuangtai:
                    def contrast(pingpaiming, canshu, num):
                        # 初始化标准
                        standard = []
                        with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                            f = csv.reader(f)
                            for i in f:
                                standard.append(i)
                            del standard[0]

                        # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                        for i in standard:
                            if i[1] == pingpaiming:
                                if canshu == "wt":
                                    sp = float(i[2].split("±")[0])
                                    sp1 = float(i[2].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "PD":
                                    sp = float(i[3].split("±")[0]) / 1000
                                    sp1 = float(i[3].split("±")[1]) / 1000
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "TotV":
                                    sp = float(i[4].split("±")[0])
                                    sp1 = float(i[4].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "DD":
                                    sp = float(i[5].split("±")[0])
                                    sp1 = float(i[5].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "circ":
                                    sp = float(i[6].split("±")[0])
                                    sp1 = float(i[6].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"

                    # TODO:字典数据total
                    # TODO:字典数据total
                    def try_(pingpai, total):

                        wt = total["wt"]  #
                        circ = total["circ"]  #
                        PD = total["PD"]  #
                        cpd = total["CPD"]
                        vent = total["Vent"]
                        pvnt = total["PVnt"]
                        totv = total["TotV"]  #
                        Len = total["Len"]
                        DD = total["DD"]  #
                        # 去除不符合标准的contrast
                        for i in range(len(wt)):
                            if contrast(pingpai, "wt", wt[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(circ)):
                            if contrast(pingpai, "circ", circ[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(PD)):
                            if contrast(pingpai, "PD", PD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(totv)):
                            if contrast(pingpai, "TotV", totv[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(DD)):
                            if contrast(pingpai, "DD", DD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        # todo:不符合3σ
                        # wt
                        # np.std(a,ddof=1)
                        left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                        right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                        left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                        right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                        left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                        right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                        left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                        right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                        left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                        right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                        left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                        right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                        left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                        right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                        left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                        right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                        left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                        right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                        nums = []
                        for i in range(len(wt)):
                            if left < wt[i] < right:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        nums = []
                        # circ
                        for i in range(len(circ)):
                            if left1 < circ[i] < right1:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]
                        # PD
                        nums = []
                        for i in range(len(PD)):
                            if left2 < PD[i] < right2:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # cpd
                        nums = []
                        for i in range(len(cpd)):
                            if left3 < cpd[i] < right3:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # vent
                        nums = []

                        for i in range(len(vent)):
                            if left4 < vent[i] < right4:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # pvnt
                        nums = []

                        for i in range(len(pvnt)):
                            if left5 < pvnt[i] < right5:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # totv
                        nums = []
                        for i in range(len(totv)):
                            if left6 < totv[i] < right6:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # Len
                        nums = []
                        for i in range(len(Len)):
                            if left7 < Len[i] < right7:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # DD
                        nums = []
                        for i in range(len(DD)):
                            if left8 < DD[i] < right8:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                                "Len": Len, "DD": DD}

                    data5 = [try_(pingpai, i) for i in last_result]
                    data5 = [i[zhibiao] for i in data5]

                else:
                    data5 = [i[zhibiao] for i in last_result]
                # z检验
                p = []
                for i in data5:
                    p.append(sw.ztest(i, value=float(z))[1])  # p
                self.textEdit_2.clear()
                for i in range(len(p)):
                    self.textEdit_2.append(str(label[i] + "p值" + str(p[i])))
                try:
                    sip.delete(self.canvas)
                    sip.delete(self.layout)
                except:
                    pass
                self.fig = plt.Figure()
                self.canvas = FC(self.fig)
                self.layout = QVBoxLayout()
                self.layout.addWidget(self.canvas)
                self.widget_2.setLayout(self.layout)
                ax = self.fig.add_subplot(111)
                x = [i for i in range(len(p))]
                ax.plot(x, p)
                ax.set_title("z检验")
                self.canvas.draw_idle()
                self.canvas.draw()  # TODO:这里开始绘制

                # 平均值、中位数
                mean = []
                zhong = []
                for i in data5:
                    mean.append(np.mean(i))
                    zhong.append(np.median(i))
                for i in range(len(mean)):
                    self.textEdit_2.append(str(label[i] + "平均值" + str(mean[i]) + "中位数" + str(zhong[i])))
                try:
                    sip.delete(self.canvas2)
                    sip.delete(self.layout2)
                except:
                    pass
                self.fig2 = plt.Figure()
                self.canvas2 = FC(self.fig2)
                self.layout2 = QVBoxLayout()
                self.layout2.addWidget(self.canvas2)
                self.widget_3.setLayout(self.layout2)
                ax = self.fig2.add_subplot(111)
                x = [i for i in range(len(mean))]
                ax.plot(x, mean, label="平均值")
                ax.plot(x, zhong, label="中位数")
                ax.legend()
                ax.set_title("平均值 中位数")
                self.canvas2.draw_idle()
                self.canvas2.draw()  # TODO:这里开始绘制

                # cv
                cv = []

                for i in data5:
                    cv.append(np.std(i) / np.mean(i))

                for i in range(len(cv)):
                    self.textEdit_2.append(str(label[i] + "变异系数" + str(cv[i])))
                try:
                    sip.delete(self.canvas3)
                    sip.delete(self.layout3)
                except:
                    pass
                self.fig3 = plt.Figure()
                self.canvas3 = FC(self.fig3)
                self.layout3 = QVBoxLayout()
                self.layout3.addWidget(self.canvas3)
                self.widget_4.setLayout(self.layout3)
                ax = self.fig3.add_subplot(111)
                x = [i for i in range(len(mean))]
                ax.plot(x, cv)
                ax.axhline(y=0.01, color='green', linestyle='--')
                ax.axhline(y=0.02, color='green', linestyle='--')
                ax.axhline(y=0.03, color='green', linestyle='--')
                ax.axhline(y=0.04, color='green', linestyle='--')
                ax.axhline(y=0.1, color='green', linestyle='--')

                ax.set_title("变异系数")
                self.canvas3.draw_idle()
                self.canvas3.draw()  # TODO:这里开始绘制
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

        def huatu(self):
            try:

                zhuangtai = False
                if self.radioButton_2.isChecked():
                    zhuangtai = True

                pingpai = self.comboBox_13.currentText()
                nian = self.comboBox_11.currentText()
                yue = self.comboBox_12.currentText()
                ri = self.comboBox_14.currentText()
                zu = int(self.comboBox_15.currentText()) - 1
                # tablewidget
                path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
                if self.comboBox_16.currentText() == "质量":
                    zhibiao = "wt"
                elif self.comboBox_16.currentText() == "圆周":
                    zhibiao = "circ"
                elif self.comboBox_16.currentText() == "吸阻":
                    zhibiao = "PD"
                elif self.comboBox_16.currentText() == "封闭吸阻":
                    zhibiao = "CPD"
                elif self.comboBox_16.currentText() == "滤嘴通风":
                    zhibiao = "Vent"
                elif self.comboBox_16.currentText() == "纸通风":
                    zhibiao = "PVnt"
                elif self.comboBox_16.currentText() == "总通风":
                    zhibiao = "TotV"
                elif self.comboBox_16.currentText() == "长度":
                    zhibiao = "Len"
                elif self.comboBox_16.currentText() == "硬度":
                    zhibiao = "DD"

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                data = load_data(path)[zu]
                if zhuangtai:
                    def contrast(pingpaiming, canshu, num):
                        # 初始化标准
                        standard = []
                        with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                            f = csv.reader(f)
                            for i in f:
                                standard.append(i)
                            del standard[0]

                        # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                        for i in standard:
                            if i[1] == pingpaiming:
                                if canshu == "wt":
                                    sp = float(i[2].split("±")[0])
                                    sp1 = float(i[2].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "PD":
                                    sp = float(i[3].split("±")[0]) / 1000
                                    sp1 = float(i[3].split("±")[1]) / 1000
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "TotV":
                                    sp = float(i[4].split("±")[0])
                                    sp1 = float(i[4].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "DD":
                                    sp = float(i[5].split("±")[0])
                                    sp1 = float(i[5].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "circ":
                                    sp = float(i[6].split("±")[0])
                                    sp1 = float(i[6].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"

                    # TODO:字典数据total
                    # TODO:字典数据total
                    def try_(pingpai, total):

                        wt = total["wt"]  #
                        circ = total["circ"]  #
                        PD = total["PD"]  #
                        cpd = total["CPD"]
                        vent = total["Vent"]
                        pvnt = total["PVnt"]
                        totv = total["TotV"]  #
                        Len = total["Len"]
                        DD = total["DD"]  #
                        # 去除不符合标准的contrast
                        for i in range(len(wt)):
                            if contrast(pingpai, "wt", wt[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(circ)):
                            if contrast(pingpai, "circ", circ[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(PD)):
                            if contrast(pingpai, "PD", PD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(totv)):
                            if contrast(pingpai, "TotV", totv[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(DD)):
                            if contrast(pingpai, "DD", DD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        # todo:不符合3σ
                        # wt
                        # np.std(a,ddof=1)
                        left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                        right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                        left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                        right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                        left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                        right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                        left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                        right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                        left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                        right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                        left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                        right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                        left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                        right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                        left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                        right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                        left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                        right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                        nums = []
                        for i in range(len(wt)):
                            if left < wt[i] < right:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        nums = []
                        # circ
                        for i in range(len(circ)):
                            if left1 < circ[i] < right1:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]
                        # PD
                        nums = []
                        for i in range(len(PD)):
                            if left2 < PD[i] < right2:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # cpd
                        nums = []
                        for i in range(len(cpd)):
                            if left3 < cpd[i] < right3:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # vent
                        nums = []

                        for i in range(len(vent)):
                            if left4 < vent[i] < right4:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # pvnt
                        nums = []

                        for i in range(len(pvnt)):
                            if left5 < pvnt[i] < right5:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # totv
                        nums = []
                        for i in range(len(totv)):
                            if left6 < totv[i] < right6:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # Len
                        nums = []
                        for i in range(len(Len)):
                            if left7 < Len[i] < right7:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # DD
                        nums = []
                        for i in range(len(DD)):
                            if left8 < DD[i] < right8:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                                "Len": Len, "DD": DD}

                    data5 = try_(pingpai, data)
                    data5 = data5[zhibiao]

                else:
                    data5 = data[zhibiao]
                # print(data5)
                # huatu
                tu = self.comboBox_17.currentText()
                # 箱线图","散点图","直方图
                if tu == "直方图":
                    try:
                        sip.delete(self.canvas1)
                        sip.delete(self.layout1)
                    except:
                        pass
                    self.fig1 = plt.Figure()
                    self.canvas1 = FC(self.fig1)
                    self.layout1 = QVBoxLayout()
                    self.layout1.addWidget(self.canvas1)
                    self.widget.setLayout(self.layout1)
                    ax = self.fig1.add_subplot(111)
                    # x的个数决定了样本量
                    bins = np.linspace(min(data5), max(data5), 20)
                    ax.hist(data5, bins)
                    ax.set_title("直方图")
                    self.canvas1.draw_idle()
                    self.canvas1.draw()  # TODO:这里开始绘制
                elif tu == "箱线图":
                    try:
                        sip.delete(self.canvas1)
                        sip.delete(self.layout1)
                    except:
                        pass
                    self.fig1 = plt.Figure()
                    self.canvas1 = FC(self.fig1)
                    self.layout1 = QVBoxLayout()
                    self.layout1.addWidget(self.canvas1)
                    self.widget.setLayout(self.layout1)
                    ax = self.fig1.add_subplot(111)
                    ax.boxplot(data5)
                    ax.set_title("箱线图")
                    self.canvas1.draw_idle()
                    self.canvas1.draw()  # TODO:这里开始绘制
                elif tu == "散点图":
                    try:
                        sip.delete(self.canvas1)
                        sip.delete(self.layout1)
                    except:
                        pass
                    self.fig1 = plt.Figure()
                    self.canvas1 = FC(self.fig1)
                    self.layout1 = QVBoxLayout()
                    self.layout1.addWidget(self.canvas1)
                    self.widget.setLayout(self.layout1)
                    ax = self.fig1.add_subplot(111)
                    # x的个数决定了样本量
                    num = [i for i in range(len(data5))]
                    print(num)
                    print(data5)
                    ax.scatter(num, data5)
                    ax.set_title("散点图")
                    self.canvas1.draw_idle()
                    self.canvas1.draw()  # TODO:这里开始绘制

                def foundation(data):
                    # 均值
                    aver = np.mean(data)
                    # 方差
                    std = np.var(data)
                    # 偏度
                    s = pd.Series(data)
                    piandu = s.skew()
                    # 峰度
                    fengdu = s.kurt()  # <class 'numpy.float64'>
                    # 变异系数
                    cv = np.std(data) / np.mean(data)
                    # 最大
                    Max = max(data)
                    # 最小
                    Min = min(data)
                    # 极差
                    jicha = Max - Min

                    # 中位数
                    def get_median(data):
                        data.sort()
                        half = len(data) // 2
                        return (data[half] + data[~half]) / 2

                    median = get_median(data)
                    # 下四分位数
                    xia = np.percentile(data, (75))
                    # 上四分位数
                    shang = np.percentile(data, (25))
                    return aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang

                aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang = foundation(data5)
                self.textEdit.clear()
                self.textEdit.append(f"均值 {str(aver)}")
                self.textEdit.append(f"方差 {str(std)}")
                self.textEdit.append(f"偏度 {str(piandu)}")
                self.textEdit.append(f"峰度 {str(fengdu)}")
                self.textEdit.append(f"变异系数 {str(cv)}")
                self.textEdit.append(f"最大值 {str(Max)}")
                self.textEdit.append(f"最小值 {str(Min)}")
                self.textEdit.append(f"极差 {str(jicha)}")
                self.textEdit.append(f"中位数 {str(median)}")
                self.textEdit.append(f"下四分位数 {str(shang)}")
                self.textEdit.append(f"上四分位数 {str(xia)}")
            except:
                QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

        def t_z(self):
            # 正态
            try:
                zhuangtai = False
                if self.radioButton_2.isChecked():
                    zhuangtai = True

                pingpai = self.comboBox_13.currentText()
                nian = self.comboBox_11.currentText()
                yue = self.comboBox_12.currentText()
                ri = self.comboBox_14.currentText()
                zu = int(self.comboBox_15.currentText()) - 1
                # tablewidget
                path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
                if self.comboBox_18.currentText() == "质量":
                    zhibiao = "wt"
                elif self.comboBox_18.currentText() == "圆周":
                    zhibiao = "circ"
                elif self.comboBox_18.currentText() == "吸阻":
                    zhibiao = "PD"
                elif self.comboBox_18.currentText() == "封闭吸阻":
                    zhibiao = "CPD"
                elif self.comboBox_18.currentText() == "滤嘴通风":
                    zhibiao = "Vent"
                elif self.comboBox_18.currentText() == "纸通风":
                    zhibiao = "PVnt"
                elif self.comboBox_18.currentText() == "总通风":
                    zhibiao = "TotV"
                elif self.comboBox_18.currentText() == "长度":
                    zhibiao = "Len"
                elif self.comboBox_18.currentText() == "硬度":
                    zhibiao = "DD"

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                data = load_data(path)[zu]
                if zhuangtai:
                    def contrast(pingpaiming, canshu, num):
                        # 初始化标准
                        standard = []
                        with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                            f = csv.reader(f)
                            for i in f:
                                standard.append(i)
                            del standard[0]

                        # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                        for i in standard:
                            if i[1] == pingpaiming:
                                if canshu == "wt":
                                    sp = float(i[2].split("±")[0])
                                    sp1 = float(i[2].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "PD":
                                    sp = float(i[3].split("±")[0]) / 1000
                                    sp1 = float(i[3].split("±")[1]) / 1000
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "TotV":
                                    sp = float(i[4].split("±")[0])
                                    sp1 = float(i[4].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "DD":
                                    sp = float(i[5].split("±")[0])
                                    sp1 = float(i[5].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "circ":
                                    sp = float(i[6].split("±")[0])
                                    sp1 = float(i[6].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"

                    # TODO:字典数据total
                    # TODO:字典数据total
                    def try_(pingpai, total):

                        wt = total["wt"]  #
                        circ = total["circ"]  #
                        PD = total["PD"]  #
                        cpd = total["CPD"]
                        vent = total["Vent"]
                        pvnt = total["PVnt"]
                        totv = total["TotV"]  #
                        Len = total["Len"]
                        DD = total["DD"]  #
                        # 去除不符合标准的contrast
                        for i in range(len(wt)):
                            if contrast(pingpai, "wt", wt[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(circ)):
                            if contrast(pingpai, "circ", circ[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(PD)):
                            if contrast(pingpai, "PD", PD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(totv)):
                            if contrast(pingpai, "TotV", totv[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(DD)):
                            if contrast(pingpai, "DD", DD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        # todo:不符合3σ
                        # wt
                        # np.std(a,ddof=1)
                        left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                        right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                        left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                        right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                        left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                        right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                        left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                        right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                        left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                        right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                        left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                        right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                        left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                        right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                        left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                        right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                        left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                        right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                        nums = []
                        for i in range(len(wt)):
                            if left < wt[i] < right:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        nums = []
                        # circ
                        for i in range(len(circ)):
                            if left1 < circ[i] < right1:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]
                        # PD
                        nums = []
                        for i in range(len(PD)):
                            if left2 < PD[i] < right2:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # cpd
                        nums = []
                        for i in range(len(cpd)):
                            if left3 < cpd[i] < right3:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # vent
                        nums = []

                        for i in range(len(vent)):
                            if left4 < vent[i] < right4:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # pvnt
                        nums = []

                        for i in range(len(pvnt)):
                            if left5 < pvnt[i] < right5:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # totv
                        nums = []
                        for i in range(len(totv)):
                            if left6 < totv[i] < right6:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # Len
                        nums = []
                        for i in range(len(Len)):
                            if left7 < Len[i] < right7:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # DD
                        nums = []
                        for i in range(len(DD)):
                            if left8 < DD[i] < right8:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                                "Len": Len, "DD": DD}

                    data5 = try_(pingpai, data)
                    data5 = data5[zhibiao]

                else:
                    data5 = data[zhibiao]

                # ks
                self.lineEdit_3.setText(str(stats.kstest(data5, 'norm', (np.mean(data5), np.std(data5)))))
            except:
                QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

        def t(self):
            # t
            try:
                zhuangtai = False
                if self.radioButton_2.isChecked():
                    zhuangtai = True

                pingpai = self.comboBox_13.currentText()
                nian = self.comboBox_11.currentText()
                yue = self.comboBox_12.currentText()
                ri = self.comboBox_14.currentText()
                zu = int(self.comboBox_15.currentText()) - 1
                # tablewidget
                path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
                if self.comboBox_18.currentText() == "质量":
                    zhibiao = "wt"
                elif self.comboBox_18.currentText() == "圆周":
                    zhibiao = "circ"
                elif self.comboBox_18.currentText() == "吸阻":
                    zhibiao = "PD"
                elif self.comboBox_18.currentText() == "封闭吸阻":
                    zhibiao = "CPD"
                elif self.comboBox_18.currentText() == "滤嘴通风":
                    zhibiao = "Vent"
                elif self.comboBox_18.currentText() == "纸通风":
                    zhibiao = "PVnt"
                elif self.comboBox_18.currentText() == "总通风":
                    zhibiao = "TotV"
                elif self.comboBox_18.currentText() == "长度":
                    zhibiao = "Len"
                elif self.comboBox_18.currentText() == "硬度":
                    zhibiao = "DD"

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                data = load_data(path)[zu]
                if zhuangtai:
                    def contrast(pingpaiming, canshu, num):
                        # 初始化标准
                        standard = []
                        with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                            f = csv.reader(f)
                            for i in f:
                                standard.append(i)
                            del standard[0]

                        # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                        for i in standard:
                            if i[1] == pingpaiming:
                                if canshu == "wt":
                                    sp = float(i[2].split("±")[0])
                                    sp1 = float(i[2].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "PD":
                                    sp = float(i[3].split("±")[0]) / 1000
                                    sp1 = float(i[3].split("±")[1]) / 1000
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "TotV":
                                    sp = float(i[4].split("±")[0])
                                    sp1 = float(i[4].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "DD":
                                    sp = float(i[5].split("±")[0])
                                    sp1 = float(i[5].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"
                                elif canshu == "circ":
                                    sp = float(i[6].split("±")[0])
                                    sp1 = float(i[6].split("±")[1])
                                    if (sp - sp1) <= num <= (sp + sp1):
                                        return "合格"
                                    else:
                                        return "不合格"

                    # TODO:字典数据total
                    # TODO:字典数据total
                    def try_(pingpai, total):

                        wt = total["wt"]  #
                        circ = total["circ"]  #
                        PD = total["PD"]  #
                        cpd = total["CPD"]
                        vent = total["Vent"]
                        pvnt = total["PVnt"]
                        totv = total["TotV"]  #
                        Len = total["Len"]
                        DD = total["DD"]  #
                        # 去除不符合标准的contrast
                        for i in range(len(wt)):
                            if contrast(pingpai, "wt", wt[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(circ)):
                            if contrast(pingpai, "circ", circ[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(PD)):
                            if contrast(pingpai, "PD", PD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(totv)):
                            if contrast(pingpai, "TotV", totv[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        for i in range(len(DD)):
                            if contrast(pingpai, "DD", DD[i]) == "不合格":
                                wt.remove(wt[i])
                                circ.remove(circ[i])
                                PD.remove(PD[i])
                                cpd.remove(cpd[i])
                                vent.remove(vent[i])
                                pvnt.remove(pvnt[i])
                                totv.remove(totv[i])
                                Len.remove(Len[i])
                                DD.remove(DD[i])
                        # todo:不符合3σ
                        # wt
                        # np.std(a,ddof=1)
                        left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                        right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                        left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                        right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                        left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                        right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                        left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                        right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                        left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                        right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                        left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                        right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                        left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                        right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                        left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                        right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                        left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                        right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                        nums = []
                        for i in range(len(wt)):
                            if left < wt[i] < right:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        nums = []
                        # circ
                        for i in range(len(circ)):
                            if left1 < circ[i] < right1:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]
                        # PD
                        nums = []
                        for i in range(len(PD)):
                            if left2 < PD[i] < right2:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # cpd
                        nums = []
                        for i in range(len(cpd)):
                            if left3 < cpd[i] < right3:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # vent
                        nums = []

                        for i in range(len(vent)):
                            if left4 < vent[i] < right4:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # pvnt
                        nums = []

                        for i in range(len(pvnt)):
                            if left5 < pvnt[i] < right5:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # totv
                        nums = []
                        for i in range(len(totv)):
                            if left6 < totv[i] < right6:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # Len
                        nums = []
                        for i in range(len(Len)):
                            if left7 < Len[i] < right7:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        # DD
                        nums = []
                        for i in range(len(DD)):
                            if left8 < DD[i] < right8:
                                nums.append(i)
                        wt = [wt[i] for i in nums]
                        circ = [circ[i] for i in nums]
                        PD = [PD[i] for i in nums]
                        cpd = [cpd[i] for i in nums]
                        vent = [vent[i] for i in nums]
                        pvnt = [pvnt[i] for i in nums]
                        totv = [totv[i] for i in nums]
                        Len = [Len[i] for i in nums]
                        DD = [DD[i] for i in nums]

                        return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                                "Len": Len, "DD": DD}

                    data5 = try_(pingpai, data)
                    data5 = data5[zhibiao]

                else:
                    data5 = data[zhibiao]

                bt = float(self.lineEdit_2.text())
                sample = np.asarray(data5)
                # 单样本检验用stats.ttest_1samp
                r = stats.ttest_1samp(sample, bt, axis=0)
                self.lineEdit_4.setText("statistic:" + str(r.__getattribute__("statistic")) + "  " + "pvalue:" + str(
                    r.__getattribute__("pvalue")))
            except:
                QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

        def tongji(self):
            try:
                pingpai = self.comboBox.currentText()
                nian = self.comboBox_2.currentText()
                yue = self.comboBox_3.currentText()
                ri = self.comboBox_4.currentText()
                zu = int(self.comboBox_9.currentText()) - 1
                # tablewidget
                path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
                if self.comboBox_10.currentText() == "质量":
                    zhibiao = "wt"
                elif self.comboBox_10.currentText() == "圆周":
                    zhibiao = "circ"
                elif self.comboBox_10.currentText() == "吸阻":
                    zhibiao = "PD"
                elif self.comboBox_10.currentText() == "封闭吸阻":
                    zhibiao = "CPD"
                elif self.comboBox_10.currentText() == "滤嘴通风":
                    zhibiao = "Vent"
                elif self.comboBox_10.currentText() == "纸通风":
                    zhibiao = "PVnt"
                elif self.comboBox_10.currentText() == "总通风":
                    zhibiao = "TotV"
                elif self.comboBox_10.currentText() == "长度":
                    zhibiao = "Len"
                elif self.comboBox_10.currentText() == "硬度":
                    zhibiao = "DD"

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]
                        print(standard)
                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                data1 = load_data(path)[zu]
                data_wt = data1["wt"]
                data_circ = data1["circ"]
                data_PD = data1["PD"]
                data_CPD = data1["CPD"]
                data_Vent = data1["Vent"]
                data_PVnt = data1["PVnt"]
                data_TotV = data1["TotV"]
                data_Len = data1["Len"]
                data_DD = data1["DD"]
                # 获取一个列表
                data = load_data(path)[zu][zhibiao]
                num = len(data)  # 总数
                p = 0
                sp = []
                for i in range(len(data)):
                    if contrast(pingpai, zhibiao, data[i]) == "合格":
                        p += 1
                    else:
                        # 不合格
                        sp.append(i)
                per = round((p / num) * 100, 2)
                # 合格率
                self.label_13.setText(str(per) + "%")
                print(per)
                data2 = []
                for i in sp:
                    data3 = []
                    data3.append(data_wt[i])
                    data3.append(data_circ[i])
                    data3.append(data_PD[i])
                    data3.append(data_CPD[i])
                    data3.append(data_Vent[i])
                    data3.append(data_PVnt[i])
                    data3.append(data_TotV[i])
                    data3.append(data_Len[i])
                    data3.append(data_DD[i])
                    data2.append(data3)
                # 不合格数据所在行
                self.tableWidget_3.setRowCount(len(data2))  # 设置表格的行数
                self.tableWidget_3.setColumnCount(9)  # 设置表格的列数
                self.tableWidget_3.setHorizontalHeaderLabels(
                    ["wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"])
                self.tableWidget_3.setHorizontalHeaderLabels(
                    ["质量", "圆周", "吸阻", "封闭吸阻", "滤嘴通风", "纸通风", "总通风", "长度", "硬度"])
                self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                for i in range(len(data2)):
                    newItem = QTableWidgetItem(str(data2[i][0]))
                    newItem1 = QTableWidgetItem(str(data2[i][1]))
                    newItem2 = QTableWidgetItem(str(data2[i][2]))
                    newItem3 = QTableWidgetItem(str(data2[i][3]))
                    newItem4 = QTableWidgetItem(str(data2[i][4]))
                    newItem5 = QTableWidgetItem(str(data2[i][5]))
                    newItem6 = QTableWidgetItem(str(data2[i][6]))
                    newItem7 = QTableWidgetItem(str(data2[i][7]))
                    newItem8 = QTableWidgetItem(str(data2[i][8]))

                    self.tableWidget_3.setItem(i, 0, newItem)
                    self.tableWidget_3.setItem(i, 1, newItem1)
                    self.tableWidget_3.setItem(i, 2, newItem2)
                    self.tableWidget_3.setItem(i, 3, newItem3)
                    self.tableWidget_3.setItem(i, 4, newItem4)
                    self.tableWidget_3.setItem(i, 5, newItem5)
                    self.tableWidget_3.setItem(i, 6, newItem6)
                    self.tableWidget_3.setItem(i, 7, newItem7)
                    self.tableWidget_3.setItem(i, 8, newItem8)
            except:
                QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

        def chaxun(self):
            try:
                # 获取 品牌，年， 月， 日， 组
                pingpai = self.comboBox.currentText()
                nian = self.comboBox_2.currentText()
                yue = self.comboBox_3.currentText()
                ri = self.comboBox_4.currentText()
                zu = int(self.comboBox_9.currentText()) - 1
                # tablewidget
                path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                data = load_data(path)[zu]
                self.tableWidget.setRowCount(len(data["wt"]))  # 设置表格的行数
                self.tableWidget.setColumnCount(len(data))  # 设置表格的列数
                self.tableWidget.setHorizontalHeaderLabels(
                    ["wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"])
                self.tableWidget.setHorizontalHeaderLabels(["质量", "圆周", "吸阻", "封闭吸阻", "滤嘴通风", "纸通风", "总通风", "长度", "硬度"])
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                for i in range(len(data["wt"])):
                    newItem = QTableWidgetItem(str(data["wt"][i]))
                    newItem1 = QTableWidgetItem(str(data["circ"][i]))
                    newItem2 = QTableWidgetItem(str(data["PD"][i]))
                    newItem3 = QTableWidgetItem(str(data["CPD"][i]))
                    newItem4 = QTableWidgetItem(str(data["Vent"][i]))
                    newItem5 = QTableWidgetItem(str(data["PVnt"][i]))
                    newItem6 = QTableWidgetItem(str(data["TotV"][i]))
                    newItem7 = QTableWidgetItem(str(data["Len"][i]))
                    newItem8 = QTableWidgetItem(str(data["DD"][i]))

                    self.tableWidget.setItem(i, 0, newItem)
                    self.tableWidget.setItem(i, 1, newItem1)
                    self.tableWidget.setItem(i, 2, newItem2)
                    self.tableWidget.setItem(i, 3, newItem3)
                    self.tableWidget.setItem(i, 4, newItem4)
                    self.tableWidget.setItem(i, 5, newItem5)
                    self.tableWidget.setItem(i, 6, newItem6)
                    self.tableWidget.setItem(i, 7, newItem7)
                    self.tableWidget.setItem(i, 8, newItem8)
            except:
                QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

        def init_(self):
            init_com1 = ['质量', '圆周', '吸阻', '封闭吸阻', '滤嘴通风', '纸通风', '总通风', '长度', '硬度']
            # ('名称', '07221黄鹤楼（硬生态）'), ('烟支质量Wt（g/支）', '0.520±0.050'), ('烟支吸阻PD（Pa）', '1850±250'),
            # ('总通风率TotV（％）', '25.0±10.0'), ('烟支硬度DD（％）', '53.0±12.0'), ('圆周Circ （mm）', '17.1±0.2')
            # init_com1 = ['wt', 'circ', 'PD', 'TotV', 'DD']
            self.comboBox_10.addItems([""])
            self.comboBox_10.addItems(init_com1)
            self.comboBox_16.addItems([""])
            self.comboBox_16.addItems(init_com1)
            self.comboBox_21.addItems([""])
            self.comboBox_21.addItems(init_com1)
            self.comboBox_18.addItems([""])
            self.comboBox_18.addItems(init_com1)

            # 图种类
            self.comboBox_17.addItems([""])
            self.comboBox_17.addItems(["箱线图", "散点图", "直方图"])
            # 加载月数据分析 指标
            self.comboBox_24.addItems([""])
            self.comboBox_24.addItems(init_com1)
            # 加载年度数据分析 指标
            self.comboBox_26.addItems([""])
            self.comboBox_26.addItems(init_com1)
            # 5、分指标独立样本t检验（任意选择不同两月数据比较分析）
            # 6、分指标散点图（加两条线，分别是标准的上下限），出个合格率
            # 7、分指标直方图、质量控制图（X-R）
            # 8、分指标年度z检验p值折线图、变异系数折线图、中位数及平均数折线图（就是横坐标为月，每月一个值的折线图）
            # 年度数据分析
            self.comboBox_25.addItems([""])
            self.comboBox_25.addItems(["分指标单样本t检验", "独立样本t检验", "分指标散点图", "分指标直方图"])

            self.comboBox_27.addItems([""])
            self.comboBox_27.addItems(["年度分指标质量控制图", "月度分指标质量控制图", "分指标年度z检验p值折线图", "分指标年度变异系数折线图", "分指标年度中位数折线图"])

            def look_for(path):
                list_all = []
                for file in os.listdir(path):
                    files = os.path.join(path, file)
                    list_all.append(files)
                total = {}
                for file in list_all:
                    total[file] = {}
                    for i in os.listdir(file):  # 2019
                        files = os.path.join(file, i)  # /2019
                        total[file][files] = {}
                        for m in os.listdir(files):  #
                            m = os.path.join(files, m)  # /2019/01/
                            total[file][files][m] = []
                            for k in os.listdir(m):
                                sp = os.path.join(m, k)
                                total[file][files][m].append(sp)
                return total

            self.path = r"数据及标准\数据"
            self.data = look_for(self.path)
            print("__" * 60)
            print(self.data)
            pingpai = []
            for key, value in self.data.items():
                pingpai.append(os.path.split(key)[-1])
            self.comboBox.addItems([""])
            self.comboBox.addItems(pingpai)
            self.comboBox_13.addItems([""])
            self.comboBox_13.addItems(pingpai)
            self.comboBox_23.addItems([""])
            self.comboBox_23.addItems(pingpai)
            #        self.comboBox_61.addItems([""])
            #        self.comboBox_61.addItems(pingpai)
            # 62 4
            self.comboBox_62.addItems([""])
            self.comboBox_62.addItems(pingpai)
            # 月数据分析左1
            self.comboBox_67.addItems([""])
            self.comboBox_67.addItems(pingpai)
            # 月数据分析左2
            self.comboBox_70.addItems([""])
            self.comboBox_70.addItems(pingpai)
            # 年度数据分析左2
            self.comboBox_71.addItems([""])
            self.comboBox_71.addItems(pingpai)

            print("初始化完毕")

        # pingpai 动#1
        def selectionchange(self, i):

            print("sd")
            try:
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_2.clear()
                self.comboBox_2.addItems([""])
                text = self.comboBox.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_2.addItems(nian1)
            except Exception as e:
                print(e)
                pass

        # 年动
        def selectionchange1(self, i):
            print("sdd")
            try:
                self.comboBox_3.clear()
                self.comboBox_3.addItems([""])
                pingpai = self.comboBox.currentText()
                nian = self.comboBox_2.currentText()
                text = self.comboBox.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_3.addItems(yue)
            except Exception as e:
                print(e)
                pass

        # 月动
        def selectionchange2(self, i):
            print("sddd")
            try:
                self.comboBox_4.clear()
                self.comboBox_4.addItems([""])
                pingpai = self.comboBox.currentText()
                nian = self.comboBox_2.currentText()
                text = self.comboBox.currentText()  # pingpai
                yue = self.comboBox_3.currentText()
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
                data3 = self.data[path1][path2][path3]
                ri = [os.path.split(i)[-1] for i in data3]
                self.comboBox_4.addItems(ri)
            except Exception as e:
                print(e)
                pass

        # ri动
        def selectionchange3(self, i):
            print("sdddd")
            try:
                self.comboBox_9.clear()
                self.comboBox_9.addItems([""])
                pingpai = self.comboBox.currentText()
                nian = self.comboBox_2.currentText()
                text = self.comboBox.currentText()  # pingpai
                yue = self.comboBox_3.currentText()
                ri = self.comboBox_4.currentText()

                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                num = len(load_data(path3))
                self.comboBox_9.addItems([str(i) for i in range(1, num + 1)])
            except Exception as e:
                print(e)
                pass

        # pingpai 动#2

        def selectionchange0(self, i):
            print("sd")
            try:
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_11.clear()
                self.comboBox_11.addItems([""])
                text = self.comboBox_13.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_11.addItems(nian1)
            except Exception as e:
                print(e)
                pass
            # 年动

        def selectionchange11(self, i):
            print("sdd")
            try:
                self.comboBox_12.clear()
                self.comboBox_12.addItems([""])
                pingpai = self.comboBox_13.currentText()
                nian = self.comboBox_11.currentText()
                text = self.comboBox_13.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_12.addItems(yue)
            except Exception as e:
                print(e)
                pass
            # 月动

        def selectionchange22(self, i):
            print("sddd")
            try:
                self.comboBox_14.clear()
                self.comboBox_14.addItems([""])
                pingpai = self.comboBox_13.currentText()
                nian = self.comboBox_11.currentText()
                text = self.comboBox_13.currentText()  # pingpai
                yue = self.comboBox_12.currentText()
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
                data3 = self.data[path1][path2][path3]
                ri = [os.path.split(i)[-1] for i in data3]
                self.comboBox_14.addItems(ri)
            except Exception as e:
                print(e)
                pass
            # ri动

        def selectionchange33(self, i):
            print("sdddd")
            try:
                self.comboBox_15.clear()
                self.comboBox_15.addItems([""])
                pingpai = self.comboBox_13.currentText()
                nian = self.comboBox_11.currentText()
                text = self.comboBox_13.currentText()  # pingpai
                yue = self.comboBox_12.currentText()
                ri = self.comboBox_14.currentText()

                path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri

                def load_data(file_path):
                    lines = []
                    with open(file_path, "r", encoding="gbk") as f:
                        for i in f.readlines():
                            line = i.strip()
                            lines.append(line)

                    index = []
                    last = []
                    for i in range(len(lines)):
                        if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                            index.append(i)
                        try:
                            if lines[i][0] == "N":
                                last.append(i)
                        except:
                            pass
                    p = list(zip(index, last))
                    group = []
                    for indexs in p:
                        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [],
                                 "Len": [],
                                 "DD": []}
                        for i in range(indexs[0] + 1, indexs[1]):
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                        group.append(total)  # 提取的全在group里面了
                    return group

                num = len(load_data(path3))
                self.comboBox_15.addItems([str(i) for i in range(1, num + 1)])
            except Exception as e:
                print(e)
                pass

            # pingpai 动#3

        def selectionchange00(self, i):
            print("sd")
            try:
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_22.clear()
                self.comboBox_22.addItems([""])
                text = self.comboBox_23.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_22.addItems(nian1)
            except Exception as e:
                print(e)
                pass
            # 年动

        def selectionchange111(self, i):
            print("sdd")
            try:
                self.comboBox_19.clear()
                self.comboBox_19.addItems([""])
                pingpai = self.comboBox_23.currentText()
                nian = self.comboBox_22.currentText()
                text = self.comboBox_23.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_19.addItems(yue)
            except Exception as e:
                print(e)
                pass
            # 月动

        # pingpai 动#4

        def selectionchange000(self, i):
            print("sd")
            try:
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_59.clear()
                self.comboBox_59.addItems([""])
                text = self.comboBox_61.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_59.addItems(nian1)
            except Exception as e:
                print(e)
                pass
            # 年动

        def selectionchange1111(self, i):
            print("sdd")
            try:
                self.comboBox_60.clear()
                self.comboBox_60.addItems([""])
                pingpai = self.comboBox_61.currentText()
                nian = self.comboBox_59.currentText()
                text = self.comboBox_61.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_60.addItems(yue)
            except Exception as e:
                print(e)
                pass
            # 月动

        # pingpai 动#5

        def selectionchange0000(self, i):
            print("sd")
            try:
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_64.clear()
                self.comboBox_64.addItems([""])
                text = self.comboBox_62.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_64.addItems(nian1)
            except Exception as e:
                print(e)
                pass
            # 年动

        def selectionchange11111(self, i):
            print("sdd")
            try:
                self.comboBox_63.clear()
                self.comboBox_63.addItems([""])
                pingpai = self.comboBox_62.currentText()
                nian = self.comboBox_64.currentText()
                text = self.comboBox_62.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_63.addItems(yue)
            except Exception as e:
                print(e)
                pass
            # 月动

        # pingpai 动#5左边

        def selectionchange00000(self, i):
            print("sd")
            try:
                print(self.data)
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_65.clear()
                self.comboBox_65.addItems([""])
                text = self.comboBox_67.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_65.addItems(nian1)
            except Exception as e:
                print(e)
                pass
            # 年动

        def selectionchange111111(self, i):
            print("sdd")
            try:
                self.comboBox_66.clear()
                self.comboBox_66.addItems([""])
                pingpai = self.comboBox_67.currentText()
                nian = self.comboBox_65.currentText()
                text = self.comboBox_67.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_66.addItems(yue)
            except Exception as e:
                print(e)
                pass
            # 月动

        # pingpai 动#5右边

        def selectionchange000000(self, i):
            print("sd")
            try:
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_69.clear()
                self.comboBox_69.addItems([""])
                text = self.comboBox_70.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_69.addItems(nian1)
            except Exception as e:
                print(e)
                pass
            # 年动

        def selectionchange1111111(self, i):
            print("sdd")
            try:
                self.comboBox_68.clear()
                self.comboBox_68.addItems([""])
                pingpai = self.comboBox_70.currentText()
                nian = self.comboBox_69.currentText()
                text = self.comboBox_70.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_68.addItems(yue)
            except Exception as e:
                print(e)
                pass
            # 月动

        def selectionchange0000000(self, i):
            print("sd")
            try:
                # 标签用来显示选中的文本
                # currentText()：返回选中选项的文本
                self.comboBox_72.clear()
                self.comboBox_72.addItems([""])
                text = self.comboBox_71.currentText()  # pingpai
                path1 = self.path + "\\" + text
                data1 = self.data[path1]
                self.data1 = data1
                nian1 = []
                for key, value in data1.items():
                    nian = os.path.split(key)[-1]
                    nian1.append(nian)
                self.comboBox_72.addItems(nian1)
            except Exception as e:
                print(e)
                pass
            # 年动

        def selectionchange11111111(self, i):
            print("sdd")
            try:
                self.comboBox_73.clear()
                self.comboBox_73.addItems([""])
                pingpai = self.comboBox_71.currentText()
                nian = self.comboBox_72.currentText()
                text = self.comboBox_71.currentText()  # pingpai
                path1 = self.path + "\\" + text
                path2 = self.path + "\\" + pingpai + "\\" + nian
                self.data2 = self.data[path1][path2]
                yue = []
                for key, value in self.data2.items():
                    nian = os.path.split(key)[-1]
                    yue.append(nian)
                self.comboBox_73.addItems(yue)
            except Exception as e:
                print(e)
                pass
            # 月动

#管理员功能模块
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 继承(QMainWindow,Ui_MainWindow)父类的属性
        super(MainWindow, self).__init__()
        # 初始化界面组件
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.init_()
        # 查询
        self.pushButton_15.clicked.connect(self.chaxun)
        # 统计合格率
        self.pushButton.clicked.connect(self.tongji)
        # 画图
        self.pushButton_2.clicked.connect(self.huatu)
        # 正态性
        self.pushButton_3.clicked.connect(self.t_z)
        # t检验
        self.pushButton_4.clicked.connect(self.t)
        # 月度分析#3
        self.pushButton_14.clicked.connect(self.fenxi3)
        # 4
        self.pushButton_13.clicked.connect(self.fenxi4)
        # 5月度综合分析
        self.pushButton_16.clicked.connect(self.fenxi5)
        self.pushButton_5.clicked.connect(self.fenxi6)
        # 6年度数据分析
        self.pushButton_6.clicked.connect(self.fenxi7)
        # 7预测
        #self.pushButton_58.clicked.connect(self.forecast)
        # 预测补充信号与槽
        self.pushButton_57.clicked.connect(self.clickreturn)
        #self.pushButton_57.clicked.connect(self.checkBox.setChecked(False))
        self.pushButton_57.clicked.connect(self.spinBox.setEnabled)
        self.pushButton_57.clicked.connect(self.spinBox_2.setEnabled)
        self.pushButton_57.clicked.connect(self.spinBox_3.setEnabled)
        self.pushButton_57.clicked.connect(self.lineEdit_7.setEnabled)
        self.pushButton_57.clicked.connect(self.lineEdit_15.setEnabled)
        self.pushButton_57.clicked.connect(self.lineEdit_16.setEnabled)
        self.pushButton_57.clicked.connect(self.lineEdit_17.setEnabled)
        self.pushButton_57.clicked.connect(self.lineEdit_18.setEnabled)
        self.pushButton_57.clicked.connect(self.lineEdit_19.setEnabled)
        self.checkBox.clicked['bool'].connect(self.spinBox.setEnabled)
        self.checkBox.clicked['bool'].connect(self.spinBox_2.setEnabled)
        self.checkBox.clicked['bool'].connect(self.spinBox_3.setEnabled)
        self.checkBox.clicked['bool'].connect(self.lineEdit_15.setEnabled)
        self.checkBox.clicked['bool'].connect(self.lineEdit_17.setEnabled)
        self.checkBox.clicked['bool'].connect(self.lineEdit_19.setEnabled)
        self.checkBox.clicked['bool'].connect(self.lineEdit_7.setEnabled)
        self.checkBox.clicked['bool'].connect(self.lineEdit_16.setEnabled)
        self.checkBox.clicked['bool'].connect(self.lineEdit_18.setEnabled)
        self.checkBox.clicked.connect(self.clickreturn)
        # pingpai#1
        self.comboBox.currentIndexChanged.connect(self.selectionchange)
        # year
        self.comboBox_2.currentIndexChanged.connect(self.selectionchange1)
        # 月
        self.comboBox_3.currentIndexChanged.connect(self.selectionchange2)
        # 日
        self.comboBox_4.currentIndexChanged.connect(self.selectionchange3)

        # pingpai#2
        self.comboBox_13.currentIndexChanged.connect(self.selectionchange0)
        # year
        self.comboBox_11.currentIndexChanged.connect(self.selectionchange11)
        # 月
        self.comboBox_12.currentIndexChanged.connect(self.selectionchange22)
        # 日
        self.comboBox_14.currentIndexChanged.connect(self.selectionchange33)

        # pingpai#3
        self.comboBox_23.currentIndexChanged.connect(self.selectionchange00)
        # year
        self.comboBox_22.currentIndexChanged.connect(self.selectionchange111)

        # pingpai#4
        self.comboBox_61.currentIndexChanged.connect(self.selectionchange000)
        # year
        self.comboBox_59.currentIndexChanged.connect(self.selectionchange1111)

        # pingpai#5
        self.comboBox_62.currentIndexChanged.connect(self.selectionchange0000)
        # year
        self.comboBox_64.currentIndexChanged.connect(self.selectionchange11111)

        # pingpai#5  左边的
        self.comboBox_67.currentIndexChanged.connect(self.selectionchange00000)
        # year
        self.comboBox_65.currentIndexChanged.connect(self.selectionchange111111)

        # pingpai#5  右边的
        self.comboBox_70.currentIndexChanged.connect(self.selectionchange000000)
        # year
        self.comboBox_69.currentIndexChanged.connect(self.selectionchange1111111)

        # 年度数据
        self.comboBox_71.currentIndexChanged.connect(self.selectionchange0000000)
        self.comboBox_72.currentIndexChanged.connect(self.selectionchange11111111)
        # 年度数据分析

        # 卷烟纸纸单因素分析表格输出
        self.radioButton.clicked.connect(self.shuchu1)
        # 接装纸单因素分析表格输出
        self.radioButton_4.clicked.connect(self.shuchu2)
        # 滤棒单因素分析表格输出
        self.radioButton_5.clicked.connect(self.shuchu3)

        # 卷烟纸纸单因素分析表格输出
        self.radioButton_6.clicked.connect(self.shuchu6)
        # 接装纸单因素分析表格输出
        self.radioButton_7.clicked.connect(self.shuchu4)
        # 滤棒单因素分析表格输出
        self.radioButton_8.clicked.connect(self.shuchu5)

        # 展示热力图
        self.pushButton_7.clicked.connect(self.rlt)
        # 展示热力图
        self.pushButton_25.clicked.connect(self.rlt1)

        # 打开文件夹
        self.pushButton_12.clicked.connect(self.getfiles)
        # 确认查询
        self.pushButton_17.clicked.connect(self.schaxun)

        # 方差分析
        self.pushButton_19.clicked.connect(self.fcfx)

        # 方差分析
        self.pushButton_22.clicked.connect(self.fcfx1)

        # 极差分析1
        self.pushButton_18.clicked.connect(self.jcfx1)
        # 极差分析2
        self.pushButton_20.clicked.connect(self.jcfx2)
        # 极差分析3
        self.pushButton_21.clicked.connect(self.jcfx3)
        # 卷烟纸主效应图
        self.pushButton_8.clicked.connect(self.zxyt1)
        # 滤棒吸阻主效应图
        self.pushButton_9.clicked.connect(self.zxyt2)
        # 接装纸主效应图
        self.pushButton_10.clicked.connect(self.zxyt3)

        # 极差分析1
        self.pushButton_26.clicked.connect(self.jcfx10)
        # 极差分析2
        self.pushButton_27.clicked.connect(self.jcfx20)
        # 极差分析3
        self.pushButton_39.clicked.connect(self.jcfx30)
        # 卷烟纸主效应图
        self.pushButton_11.clicked.connect(self.zxyt10)
        # 滤棒吸阻主效应图
        self.pushButton_28.clicked.connect(self.zxyt20)
        # 接装纸主效应图
        self.pushButton_40.clicked.connect(self.zxyt30)

    # 补充的槽
    def clickreturn(self):
        self.lineEdit_15.setText("500")
        self.lineEdit_16.setText("380")
        self.lineEdit_17.setText("600")
        self.lineEdit_18.setText("30")
        self.lineEdit_19.setText("80")
        self.lineEdit_7.setText("100")
        self.spinBox.setProperty("value", 50)
        self.spinBox_2.setProperty("value", 10)
        self.spinBox_3.setProperty("value", 10)
    #        self.pushButton_18.clicked.connect(self.jcfx)

    def zxyt30(self):
        try:
            jc = self.comboBox_37.currentText()
            if jc == "吸阻":
                try:
                    y1 = [1.946, 1.941, 1.835, 1.843, 1.8, 1.76, 1.728, 1.686]
                    x1 = [100, 150, 250, 300, 350, 400, 450, 500]
                    y2 = [1.943, 1.825, 1.725]
                    x2 = [1, 2, 3]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('吸阻 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    #                    plt.savefig('jzzxz')
                    png = QPixmap("./jzzxz.png").scaled(360, 270)
                    self.label_32.setPixmap(QPixmap(''))
                    self.label_32.setPixmap(png)
                #                    plt.show()

                except:
                    pass
            if jc == "总通风率":
                try:
                    y1 = [22.05, 23.95, 28.15, 28.85, 30.95, 34.35, 35.7, 34.95]
                    x1 = [100, 150, 250, 300, 350, 400, 450, 500]
                    y2 = [23, 29.32, 35]
                    x2 = [1, 2, 3]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('总通风 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    #                    plt.savefig('jzzztf')
                    png = QPixmap("./jzzztf.png").scaled(360, 270)
                    self.label_32.setPixmap(QPixmap(''))
                    self.label_32.setPixmap(png)
                except:
                    pass
        except:
            pass

    def zxyt20(self):
        try:
            jc = self.comboBox_31.currentText()
            if jc == "吸阻":
                try:
                    y1 = [1.402, 1.493, 1.553, 1.645, 1.696]
                    x1 = [380, 410, 460, 500, 560]
                    y2 = [1.696, 1.599, 1.447]
                    x2 = [6, 7.5, 8]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('吸阻 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    #                    plt.savefig('lbxz')
                    png = QPixmap("./lbxz.png").scaled(360, 270)
                    self.label_8.setPixmap(QPixmap(''))

                    self.label_8.setPixmap(png)
                except:
                    pass
            if jc == "总通风率":
                try:
                    y1 = [29.95, 30.25, 28.30, 28.45, 28.35]
                    x1 = [380, 410, 460, 500, 560]
                    y2 = [28.35, 28.38, 30.10]
                    x2 = [6, 7.5, 8]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('总通风 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    #                    plt.savefig('lbztf')
                    png = QPixmap("./lbztf.png").scaled(360, 270)

                    self.label_8.setPixmap(QPixmap(''))

                    self.label_8.setPixmap(png)
                except:
                    pass
        except:
            pass

    def zxyt10(self):
        try:
            jc = self.comboBox_30.currentText()
            if jc == "吸阻":
                try:
                    y1 = [1.766, 1.817, 1.775, 1.834, 1.878]
                    x1 = [40, 50, 60, 70, 80]
                    y2 = [1.802, 1.826, 1.812, 1.825, 1.804]
                    x2 = [26, 28, 30, 32, 34]
                    y3 = [1.802, 1.836, 1.816, 1.810, 1.794]
                    x3 = [0.9, 1.2, 1.5, 1.8, 2.1]

                    plt.subplot(2, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('吸阻 主效应图')

                    plt.subplot(2, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.subplot(2, 2, 3)
                    plt.plot(x3, y3, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x3, y3, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('助溶剂含量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    #                    plt.savefig('jyzxz')
                    png = QPixmap("./jyzxz.png").scaled(360, 270)
                    self.label_7.setPixmap(QPixmap(''))
                    self.label_7.setPixmap(png)

                except:
                    pass
            if jc == "总通风率":
                try:
                    y1 = [23.33, 25.12, 27.10, 30.41, 29.58]
                    x1 = [40, 50, 60, 70, 80]
                    y2 = [28.06, 27.29, 26.72, 26.97, 26.5]
                    x2 = [26, 28, 30, 32, 34]
                    y3 = [26.45, 28.5, 27.12, 26.86, 25.975]
                    x3 = [0.9, 1.2, 1.5, 1.8, 2.1]

                    plt.subplot(2, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('总通风 主效应图')

                    plt.subplot(2, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.subplot(2, 2, 3)
                    plt.plot(x3, y3, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x3, y3, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('助溶剂含量')
                    plt.ylabel('均值')

                    plt.tight_layout()

                    #                    plt.savefig('jyzztf')
                    png = QPixmap("./jyzztf.png").scaled(360, 270)
                    self.label_7.setPixmap(QPixmap(''))
                    self.label_7.setPixmap(png)



                except:
                    pass
        except:
            pass

    def jcfx30(self):
        try:
            jc = self.comboBox_37.currentText()
            if jc == "吸阻":
                try:
                    self.tableWidget_19.setRowCount(11)  # 设置表格的行数
                    self.tableWidget_19.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_19.setHorizontalHeaderLabels(["接装纸透气度", "排数"])  # 设置表格的列名
                    self.tableWidget_19.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "6", "7", "8", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('1.946')
                    self.tableWidget_19.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('1.943')
                    self.tableWidget_19.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('1.941')
                    self.tableWidget_19.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('1.825')
                    self.tableWidget_19.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('1.835')
                    self.tableWidget_19.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('1.725')
                    self.tableWidget_19.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('1.843')
                    self.tableWidget_19.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('1.8')
                    self.tableWidget_19.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('1.76')
                    self.tableWidget_19.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('1.728')
                    self.tableWidget_19.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('1.686')
                    self.tableWidget_19.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('0.261')
                    self.tableWidget_19.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('0.219')
                    self.tableWidget_19.setItem(8, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_19.setItem(9, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_19.setItem(9, 1, newItem)

                    newItem = QTableWidgetItem('0.027')
                    self.tableWidget_19.setItem(10, 0, newItem)
                    newItem = QTableWidgetItem('0.073')
                    self.tableWidget_19.setItem(10, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

            if jc == "总通风率":
                try:
                    self.tableWidget_19.setRowCount(11)  # 设置表格的行数
                    self.tableWidget_19.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_19.setHorizontalHeaderLabels(["接装纸透气度", "排数"])  # 设置表格的列名
                    self.tableWidget_19.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "6", "7", "8", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('22.05')
                    self.tableWidget_19.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('23')
                    self.tableWidget_19.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('23.95')
                    self.tableWidget_19.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('29.32')
                    self.tableWidget_19.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('28.15')
                    self.tableWidget_19.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('35')
                    self.tableWidget_19.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('28.85')
                    self.tableWidget_19.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('30.95')
                    self.tableWidget_19.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('34.35')
                    self.tableWidget_19.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('35.70')
                    self.tableWidget_19.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('34.95')
                    self.tableWidget_19.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_19.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('13.65')
                    self.tableWidget_19.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('12')
                    self.tableWidget_19.setItem(8, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_19.setItem(9, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_19.setItem(9, 1, newItem)

                    newItem = QTableWidgetItem('1.70625')
                    self.tableWidget_19.setItem(10, 0, newItem)
                    newItem = QTableWidgetItem('4')
                    self.tableWidget_19.setItem(10, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def jcfx20(self):
        try:
            jc = self.comboBox_31.currentText()
            if jc == "吸阻":
                try:
                    self.tableWidget_13.setRowCount(8)  # 设置表格的行数
                    self.tableWidget_13.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_13.setHorizontalHeaderLabels(["滤棒吸阻", "丝束"])  # 设置表格的列名
                    self.tableWidget_13.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('1.402')
                    self.tableWidget_13.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('1.696')
                    self.tableWidget_13.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('1.493')
                    self.tableWidget_13.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('1.599')
                    self.tableWidget_13.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('1.553')
                    self.tableWidget_13.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('1.447')
                    self.tableWidget_13.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('1.645')
                    self.tableWidget_13.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_13.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('1.696')
                    self.tableWidget_13.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_13.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('0.293')
                    self.tableWidget_13.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('0.248')
                    self.tableWidget_13.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_13.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_13.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_13.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_13.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('0.0586')
                    self.tableWidget_13.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('0.0826')
                    self.tableWidget_13.setItem(8, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

            if jc == "总通风率":
                try:
                    self.tableWidget_13.setRowCount(8)  # 设置表格的行数
                    self.tableWidget_13.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_13.setHorizontalHeaderLabels(["滤棒吸阻", "丝束"])  # 设置表格的列名
                    self.tableWidget_13.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('29.95')
                    self.tableWidget_13.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('28.35')
                    self.tableWidget_13.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('30.25')
                    self.tableWidget_13.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('28.38')
                    self.tableWidget_13.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('28.30')
                    self.tableWidget_13.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('30.10')
                    self.tableWidget_13.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('28.45')
                    self.tableWidget_13.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_13.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('28.35')
                    self.tableWidget_13.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_13.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('1.95')
                    self.tableWidget_13.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('1.75')
                    self.tableWidget_13.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_13.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_13.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_13.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_13.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('0.39')
                    self.tableWidget_13.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('0.583')
                    self.tableWidget_13.setItem(8, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def jcfx10(self):
        try:
            jc = self.comboBox_30.currentText()
            if jc == "吸阻":
                try:
                    self.tableWidget_12.setRowCount(7)  # 设置表格的行数
                    self.tableWidget_12.setColumnCount(3)  # 设置表格的列数
                    self.tableWidget_12.setHorizontalHeaderLabels(["卷烟纸透气度", "定量", "助溶剂含量"])  # 设置表格的列名
                    self.tableWidget_12.setVerticalHeaderLabels(["1", "2", "3", "4", "5", "极差值", "排序"])  # 设置表格的行名

                    newItem = QTableWidgetItem('1.766')
                    self.tableWidget_12.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('1.802')
                    self.tableWidget_12.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem('1.802')
                    self.tableWidget_12.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem('1.817')
                    self.tableWidget_12.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('1.826')
                    self.tableWidget_12.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem('1.836')
                    self.tableWidget_12.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem('1.775')
                    self.tableWidget_12.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('1.812')
                    self.tableWidget_12.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem('1.816')
                    self.tableWidget_12.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem('1.834')
                    self.tableWidget_12.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('1.825')
                    self.tableWidget_12.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem('1.810')
                    self.tableWidget_12.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem('1.878')
                    self.tableWidget_12.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('1.804')
                    self.tableWidget_12.setItem(4, 1, newItem)
                    newItem = QTableWidgetItem('1.794')
                    self.tableWidget_12.setItem(4, 2, newItem)
                    newItem = QTableWidgetItem('0.112')
                    self.tableWidget_12.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('0.023')
                    self.tableWidget_12.setItem(5, 1, newItem)
                    newItem = QTableWidgetItem('0.042')
                    self.tableWidget_12.setItem(5, 2, newItem)
                    newItem = QTableWidgetItem('1')
                    self.tableWidget_12.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_12.setItem(6, 1, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_12.setItem(6, 2, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

            if jc == "总通风率":
                try:
                    self.tableWidget_12.setRowCount(7)  # 设置表格的行数
                    self.tableWidget_12.setColumnCount(3)  # 设置表格的列数
                    self.tableWidget_12.setHorizontalHeaderLabels(["卷烟纸透气度", "定量", "助溶剂含量"])  # 设置表格的列名
                    self.tableWidget_12.setVerticalHeaderLabels(["1", "2", "3", "4", "5", "极差值", "排序"])  # 设置表格的行名

                    newItem = QTableWidgetItem('23.33')
                    self.tableWidget_12.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('28.06')
                    self.tableWidget_12.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem('27.29')
                    self.tableWidget_12.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem('25.12')
                    self.tableWidget_12.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('27.29')
                    self.tableWidget_12.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem('28.5')
                    self.tableWidget_12.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem('27.10')
                    self.tableWidget_12.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('26.72')
                    self.tableWidget_12.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem('27.12')
                    self.tableWidget_12.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem('30.41')
                    self.tableWidget_12.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('26.97')
                    self.tableWidget_12.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem('26.86')
                    self.tableWidget_12.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem('29.58')
                    self.tableWidget_12.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('26.5')
                    self.tableWidget_12.setItem(4, 1, newItem)
                    newItem = QTableWidgetItem('25.975')
                    self.tableWidget_12.setItem(4, 2, newItem)
                    newItem = QTableWidgetItem('7.08')
                    self.tableWidget_12.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('1.56')
                    self.tableWidget_12.setItem(5, 1, newItem)
                    newItem = QTableWidgetItem('2.525')
                    self.tableWidget_12.setItem(5, 2, newItem)
                    newItem = QTableWidgetItem('1')
                    self.tableWidget_12.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_12.setItem(6, 1, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_12.setItem(6, 2, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def fcfx1(self):
        try:
            fc = self.comboBox_32.currentText()
            if fc == "吸阻":
                try:
                    db = pd.read_csv('xz.csv')
                    db = db[['jyztqd', 'dl', 'zrjhl', 'xz']]
                    data = np.array(db.loc[:, :])
                    data = pd.DataFrame(data, columns=['jyztqd', 'dl', 'zrjhl', 'xz'])
                    print(data)
                    formula = 'xz~ C(jyztqd) + C(dl)+C(zrjhl)'
                    anova_results = anova_lm(ols(formula, data).fit())
                    print(anova_results)

                    self._data = anova_results
                    self.tableWidget_10.setRowCount(self._data.shape[0])  # 设置表格的行数
                    self.tableWidget_10.setColumnCount(self._data.shape[1])  # 设置表格的列数
                    self.tableWidget_10.setHorizontalHeaderLabels(self._data.columns.tolist())  # 设置表格的列名
                    self.tableWidget_10.setVerticalHeaderLabels(self._data.index.tolist())  # 设置表格的行名

                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'df']))
                    self.tableWidget_10.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'sum_sq']))
                    self.tableWidget_10.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'mean_sq']))
                    self.tableWidget_10.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'F']))
                    self.tableWidget_10.setItem(0, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'PR(>F)']))
                    self.tableWidget_10.setItem(0, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'df']))
                    self.tableWidget_10.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'sum_sq']))
                    self.tableWidget_10.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'mean_sq']))
                    self.tableWidget_10.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'F']))
                    self.tableWidget_10.setItem(1, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'PR(>F)']))
                    self.tableWidget_10.setItem(1, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'df']))
                    self.tableWidget_10.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'sum_sq']))
                    self.tableWidget_10.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'mean_sq']))
                    self.tableWidget_10.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'F']))
                    self.tableWidget_10.setItem(2, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'PR(>F)']))
                    self.tableWidget_10.setItem(2, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'df']))
                    self.tableWidget_10.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'sum_sq']))
                    self.tableWidget_10.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'mean_sq']))
                    self.tableWidget_10.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'F']))
                    self.tableWidget_10.setItem(3, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'PR(>F)']))
                    self.tableWidget_10.setItem(3, 4, newItem)
                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
            if fc == "总通风率":
                try:
                    db = pd.read_csv('ztf.csv')
                    db = db[['jyztqd', 'dl', 'zrjhl', 'ztf']]
                    data = np.array(db.loc[:, :])
                    data = pd.DataFrame(data, columns=['jyztqd', 'dl', 'zrjhl', 'ztf'])
                    print(data)
                    formula = 'ztf~ C(jyztqd) + C(dl)+C(zrjhl)'
                    anova_results = anova_lm(ols(formula, data).fit())
                    print(anova_results)

                    self._data = anova_results
                    self.tableWidget_10.setRowCount(self._data.shape[0])  # 设置表格的行数
                    self.tableWidget_10.setColumnCount(self._data.shape[1])  # 设置表格的列数
                    self.tableWidget_10.setHorizontalHeaderLabels(self._data.columns.tolist())  # 设置表格的列名
                    self.tableWidget_10.setVerticalHeaderLabels(self._data.index.tolist())  # 设置表格的行名

                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'df']))
                    self.tableWidget_10.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'sum_sq']))
                    self.tableWidget_10.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'mean_sq']))
                    self.tableWidget_10.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'F']))
                    self.tableWidget_10.setItem(0, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'PR(>F)']))
                    self.tableWidget_10.setItem(0, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'df']))
                    self.tableWidget_10.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'sum_sq']))
                    self.tableWidget_10.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'mean_sq']))
                    self.tableWidget_10.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'F']))
                    self.tableWidget_10.setItem(1, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'PR(>F)']))
                    self.tableWidget_10.setItem(1, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'df']))
                    self.tableWidget_10.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'sum_sq']))
                    self.tableWidget_10.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'mean_sq']))
                    self.tableWidget_10.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'F']))
                    self.tableWidget_10.setItem(2, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'PR(>F)']))
                    self.tableWidget_10.setItem(2, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'df']))
                    self.tableWidget_10.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'sum_sq']))
                    self.tableWidget_10.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'mean_sq']))
                    self.tableWidget_10.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'F']))
                    self.tableWidget_10.setItem(3, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'PR(>F)']))
                    self.tableWidget_10.setItem(3, 4, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def rlt1(self):
        try:
            rlt = self.comboBox_33.currentText()
            if rlt == "总通风":
                png = QPixmap("./ztfrlt.png").scaled(630, 485)

                self.label_37.setPixmap(QPixmap(''))
                self.label_37.setPixmap(png)

            if rlt == "纸通风":
                png = QPixmap("./zztfrlt.png").scaled(630, 485)
                self.label_37.setPixmap(QPixmap(''))
                self.label_37.setPixmap(png)

            if rlt == "滤嘴通风":
                png = QPixmap("./lztfrlt.png").scaled(630, 485)
                self.label_37.setPixmap(QPixmap(''))
                self.label_37.setPixmap(png)

            #                  plt.savefig('lztf.png')#保存
            if rlt == "吸阻":
                png = QPixmap("./xzrlt.png").scaled(630, 485)
                self.label_37.setPixmap(QPixmap(''))
                self.label_37.setPixmap(png)

            if rlt == "封闭吸阻":
                png = QPixmap("./fbxzrlt.png").scaled(630, 485)
                self.label_37.setPixmap(QPixmap(''))
                self.label_37.setPixmap(png)

        except:
            pass

    def shuchu4(self):
        self.tableWidget_9.setRowCount(25)  # 设置表格的行数
        self.tableWidget_9.setColumnCount(2)  # 设置表格的列数
        self.tableWidget_9.setHorizontalHeaderLabels(["样品序号", "卷烟纸规格"])
        self.tableWidget_9.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        Item0 = QTableWidgetItem("0#纸")
        Item1 = QTableWidgetItem("1#纸")
        Item2 = QTableWidgetItem("2#纸")
        Item3 = QTableWidgetItem("3#纸")
        Item4 = QTableWidgetItem("4#纸")
        Item5 = QTableWidgetItem("5#纸")
        Item6 = QTableWidgetItem("6#纸")
        Item7 = QTableWidgetItem("7#纸")
        Item8 = QTableWidgetItem("8#纸")
        Item9 = QTableWidgetItem("9#纸")
        Item10 = QTableWidgetItem("10#纸")
        Item11 = QTableWidgetItem("11#纸")
        Item12 = QTableWidgetItem("12#纸")
        Item13 = QTableWidgetItem("13#纸")
        Item14 = QTableWidgetItem("14#纸")
        Item15 = QTableWidgetItem("15#纸")
        Item16 = QTableWidgetItem("16#纸")
        Item17 = QTableWidgetItem("17#纸")
        Item18 = QTableWidgetItem("18#纸")
        Item19 = QTableWidgetItem("19#纸")
        Item20 = QTableWidgetItem("20#纸")
        Item21 = QTableWidgetItem("21#纸")
        Item22 = QTableWidgetItem("22#纸")
        Item23 = QTableWidgetItem("23#纸")
        Item24 = QTableWidgetItem("24#纸")
        Item25 = QTableWidgetItem("25#纸")

        self.tableWidget_9.setItem(0, 0, Item0)
        self.tableWidget_9.setItem(1, 0, Item1)
        self.tableWidget_9.setItem(2, 0, Item2)
        self.tableWidget_9.setItem(3, 0, Item3)
        self.tableWidget_9.setItem(4, 0, Item4)
        self.tableWidget_9.setItem(5, 0, Item5)
        self.tableWidget_9.setItem(6, 0, Item6)
        self.tableWidget_9.setItem(7, 0, Item7)
        self.tableWidget_9.setItem(8, 0, Item8)
        self.tableWidget_9.setItem(9, 0, Item9)
        self.tableWidget_9.setItem(10, 0, Item10)
        self.tableWidget_9.setItem(11, 0, Item11)
        self.tableWidget_9.setItem(12, 0, Item12)
        self.tableWidget_9.setItem(13, 0, Item13)
        self.tableWidget_9.setItem(14, 0, Item14)
        self.tableWidget_9.setItem(15, 0, Item15)
        self.tableWidget_9.setItem(16, 0, Item16)
        self.tableWidget_9.setItem(17, 0, Item17)
        self.tableWidget_9.setItem(18, 0, Item18)
        self.tableWidget_9.setItem(19, 0, Item19)
        self.tableWidget_9.setItem(20, 0, Item20)
        self.tableWidget_9.setItem(21, 0, Item21)
        self.tableWidget_9.setItem(22, 0, Item22)
        self.tableWidget_9.setItem(23, 0, Item23)
        self.tableWidget_9.setItem(24, 0, Item24)
        self.tableWidget_9.setItem(25, 0, Item25)

        LItem0 = QTableWidgetItem("70-32-1.8")
        LItem1 = QTableWidgetItem("40-26-0.9")
        LItem2 = QTableWidgetItem("40-28-1.2")
        LItem3 = QTableWidgetItem("40-30-1.5")
        LItem4 = QTableWidgetItem("40-32-1.8")
        LItem5 = QTableWidgetItem("40-34-2.1")
        LItem6 = QTableWidgetItem("50-26-1.5")
        LItem7 = QTableWidgetItem("50-28-1.8")
        LItem8 = QTableWidgetItem("50-30-2.21")
        LItem9 = QTableWidgetItem("50-32-0.9")
        LItem10 = QTableWidgetItem("50-34-1.2")
        LItem11 = QTableWidgetItem("60-26-2.1")
        LItem12 = QTableWidgetItem("60-28-0.9")
        LItem13 = QTableWidgetItem("60-30-1.2")
        LItem14 = QTableWidgetItem("60-32-1.5")
        LItem15 = QTableWidgetItem("60-34-1.8")
        LItem16 = QTableWidgetItem("70-26-1.2")
        LItem17 = QTableWidgetItem("70-28-1.5")
        LItem18 = QTableWidgetItem("70-30-1.8")
        LItem19 = QTableWidgetItem("70-32-2.1")
        LItem20 = QTableWidgetItem("70-34-0.9")
        LItem21 = QTableWidgetItem("80-26-1.8")
        LItem22 = QTableWidgetItem("80-28-2.1")
        LItem23 = QTableWidgetItem("80-30-0.9")
        LItem24 = QTableWidgetItem("80-32-1.2")
        LItem25 = QTableWidgetItem("80-34-1.5")

        self.tableWidget_9.setItem(0, 1, LItem0)
        self.tableWidget_9.setItem(1, 1, LItem1)
        self.tableWidget_9.setItem(2, 1, LItem2)
        self.tableWidget_9.setItem(3, 1, LItem3)
        self.tableWidget_9.setItem(4, 1, LItem4)
        self.tableWidget_9.setItem(5, 1, LItem5)
        self.tableWidget_9.setItem(6, 1, LItem6)
        self.tableWidget_9.setItem(7, 1, LItem7)
        self.tableWidget_9.setItem(8, 1, LItem8)
        self.tableWidget_9.setItem(9, 1, LItem9)
        self.tableWidget_9.setItem(10, 1, LItem10)
        self.tableWidget_9.setItem(11, 1, LItem11)
        self.tableWidget_9.setItem(12, 1, LItem12)
        self.tableWidget_9.setItem(13, 1, LItem13)
        self.tableWidget_9.setItem(14, 1, LItem14)
        self.tableWidget_9.setItem(15, 1, LItem15)
        self.tableWidget_9.setItem(16, 1, LItem16)
        self.tableWidget_9.setItem(17, 1, LItem17)
        self.tableWidget_9.setItem(18, 1, LItem18)
        self.tableWidget_9.setItem(19, 1, LItem19)
        self.tableWidget_9.setItem(20, 1, LItem20)
        self.tableWidget_9.setItem(21, 1, LItem21)
        self.tableWidget_9.setItem(22, 1, LItem22)
        self.tableWidget_9.setItem(23, 1, LItem23)
        self.tableWidget_9.setItem(24, 1, LItem24)
        self.tableWidget_9.setItem(25, 1, LItem25)

    def shuchu5(self):
        self.tableWidget_8.setRowCount(9)  # 设置表格的行数
        self.tableWidget_8.setColumnCount(2)  # 设置表格的列数
        self.tableWidget_8.setHorizontalHeaderLabels(["样品序号", "接装纸规格"])
        self.tableWidget_8.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        Item_J0 = QTableWidgetItem("1#接装纸")
        self.tableWidget_8.setItem(0, 0, Item_J0)
        LItem_J0 = QTableWidgetItem("100单排")
        self.tableWidget_8.setItem(0, 1, LItem_J0)

        Item_J1 = QTableWidgetItem("2#接装纸")
        self.tableWidget_8.setItem(1, 0, Item_J1)
        LItem_J1 = QTableWidgetItem("150单排")
        self.tableWidget_8.setItem(1, 1, LItem_J1)

        Item_J2 = QTableWidgetItem("3产品")
        self.tableWidget_8.setItem(2, 0, Item_J2)
        LItem_J2 = QTableWidgetItem("200双排")
        self.tableWidget_8.setItem(2, 1, LItem_J2)

        Item_J3 = QTableWidgetItem("4#接装纸")
        self.tableWidget_8.setItem(3, 0, Item_J3)
        LItem_J3 = QTableWidgetItem("250双排")
        self.tableWidget_8.setItem(3, 1, LItem_J3)

        Item_J4 = QTableWidgetItem("5#接装纸")
        self.tableWidget_8.setItem(4, 0, Item_J4)
        LItem_J4 = QTableWidgetItem("300双排")
        self.tableWidget_8.setItem(4, 1, LItem_J4)

        Item_J5 = QTableWidgetItem("6#接装纸")
        self.tableWidget_8.setItem(5, 0, Item_J5)
        LItem_J5 = QTableWidgetItem("350双排")
        self.tableWidget_8.setItem(5, 1, LItem_J5)

        Item_J6 = QTableWidgetItem("7#接装纸")
        self.tableWidget_8.setItem(6, 0, Item_J6)
        LItem_J6 = QTableWidgetItem("400三排")
        self.tableWidget_8.setItem(6, 1, LItem_J6)

        Item_J7 = QTableWidgetItem("8#接装纸")
        self.tableWidget_8.setItem(7, 0, Item_J7)
        LItem_J7 = QTableWidgetItem("450三排")
        self.tableWidget_8.setItem(7, 1, LItem_J7)

        Item_J8 = QTableWidgetItem("9#接装纸")
        self.tableWidget_8.setItem(8, 0, Item_J8)
        LItem_J8 = QTableWidgetItem("500三排")
        self.tableWidget_8.setItem(8, 1, LItem_J8)

    def shuchu6(self):
        self.tableWidget_8.setRowCount(6)  # 设置表格的行数
        self.tableWidget_8.setColumnCount(2)  # 设置表格的列数
        self.tableWidget_8.setHorizontalHeaderLabels(["样品序号", "滤棒规格"])
        self.tableWidget_8.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        Item_B0 = QTableWidgetItem("1#棒")
        self.tableWidget_8.setItem(0, 0, Item_B0)
        LItem_B0 = QTableWidgetItem("6.0丝束560吸阻")
        self.tableWidget_8.setItem(0, 1, LItem_B0)

        Item_B1 = QTableWidgetItem("2产品")
        self.tableWidget_8.setItem(1, 0, Item_B1)
        LItem_B1 = QTableWidgetItem("6.0丝束600吸阻")
        self.tableWidget_8.setItem(1, 1, LItem_B1)

        Item_B2 = QTableWidgetItem("3#棒")
        self.tableWidget_8.setItem(2, 0, Item_B2)
        LItem_B2 = QTableWidgetItem("7.5丝束460吸阻")
        self.tableWidget_8.setItem(2, 1, LItem_B2)

        Item_B3 = QTableWidgetItem("4#棒")
        self.tableWidget_8.setItem(3, 0, Item_B3)
        LItem_B3 = QTableWidgetItem("7.5丝束500吸阻")
        self.tableWidget_8.setItem(3, 1, LItem_B3)

        Item_B4 = QTableWidgetItem("5#棒")
        self.tableWidget_8.setItem(4, 0, Item_B4)
        LItem_B4 = QTableWidgetItem("8.0丝束380吸阻")
        self.tableWidget_8.setItem(4, 1, LItem_B4)

        Item_B5 = QTableWidgetItem("6#棒")
        self.tableWidget_8.setItem(5, 0, Item_B5)
        LItem_B5 = QTableWidgetItem("8.0丝束410吸阻")
        self.tableWidget_8.setItem(5, 1, LItem_B5)

    def zxyt1(self):
        try:
            jc = self.comboBox_8.currentText()
            if jc == "吸阻":
                try:
                    y1 = [1.766, 1.817, 1.775, 1.834, 1.878]
                    x1 = [40, 50, 60, 70, 80]
                    y2 = [1.802, 1.826, 1.812, 1.825, 1.804]
                    x2 = [26, 28, 30, 32, 34]
                    y3 = [1.802, 1.836, 1.816, 1.810, 1.794]
                    x3 = [0.9, 1.2, 1.5, 1.8, 2.1]

                    plt.subplot(2, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('吸阻 主效应图')

                    plt.subplot(2, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.subplot(2, 2, 3)
                    plt.plot(x3, y3, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x3, y3, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('助溶剂含量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    plt.show()
                except:
                    pass
            if jc == "总通风率":
                try:
                    y1 = [23.33, 25.12, 27.10, 30.41, 29.58]
                    x1 = [40, 50, 60, 70, 80]
                    y2 = [28.06, 27.29, 26.72, 26.97, 26.5]
                    x2 = [26, 28, 30, 32, 34]
                    y3 = [26.45, 28.5, 27.12, 26.86, 25.975]
                    x3 = [0.9, 1.2, 1.5, 1.8, 2.1]

                    plt.subplot(2, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('总通风 主效应图')

                    plt.subplot(2, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.subplot(2, 2, 3)
                    plt.plot(x3, y3, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x3, y3, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('助溶剂含量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    plt.show()
                except:
                    pass
        except:
            pass

    def jcfx1(self):
        try:
            jc = self.comboBox_8.currentText()
            if jc == "吸阻":
                try:
                    self.tableWidget_5.setRowCount(7)  # 设置表格的行数
                    self.tableWidget_5.setColumnCount(3)  # 设置表格的列数
                    self.tableWidget_5.setHorizontalHeaderLabels(["卷烟纸透气度", "定量", "助溶剂含量"])  # 设置表格的列名
                    self.tableWidget_5.setVerticalHeaderLabels(["1", "2", "3", "4", "5", "极差值", "排序"])  # 设置表格的行名

                    newItem = QTableWidgetItem('1.766')
                    self.tableWidget_5.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('1.802')
                    self.tableWidget_5.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem('1.802')
                    self.tableWidget_5.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem('1.817')
                    self.tableWidget_5.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('1.826')
                    self.tableWidget_5.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem('1.836')
                    self.tableWidget_5.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem('1.775')
                    self.tableWidget_5.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('1.812')
                    self.tableWidget_5.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem('1.816')
                    self.tableWidget_5.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem('1.834')
                    self.tableWidget_5.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('1.825')
                    self.tableWidget_5.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem('1.810')
                    self.tableWidget_5.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem('1.878')
                    self.tableWidget_5.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('1.804')
                    self.tableWidget_5.setItem(4, 1, newItem)
                    newItem = QTableWidgetItem('1.794')
                    self.tableWidget_5.setItem(4, 2, newItem)
                    newItem = QTableWidgetItem('0.112')
                    self.tableWidget_5.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('0.023')
                    self.tableWidget_5.setItem(5, 1, newItem)
                    newItem = QTableWidgetItem('0.042')
                    self.tableWidget_5.setItem(5, 2, newItem)
                    newItem = QTableWidgetItem('1')
                    self.tableWidget_5.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_5.setItem(6, 1, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_5.setItem(6, 2, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

            if jc == "总通风率":
                try:
                    self.tableWidget_5.setRowCount(7)  # 设置表格的行数
                    self.tableWidget_5.setColumnCount(3)  # 设置表格的列数
                    self.tableWidget_5.setHorizontalHeaderLabels(["卷烟纸透气度", "定量", "助溶剂含量"])  # 设置表格的列名
                    self.tableWidget_5.setVerticalHeaderLabels(["1", "2", "3", "4", "5", "极差值", "排序"])  # 设置表格的行名

                    newItem = QTableWidgetItem('23.33')
                    self.tableWidget_5.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('28.06')
                    self.tableWidget_5.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem('27.29')
                    self.tableWidget_5.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem('25.12')
                    self.tableWidget_5.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('27.29')
                    self.tableWidget_5.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem('28.5')
                    self.tableWidget_5.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem('27.10')
                    self.tableWidget_5.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('26.72')
                    self.tableWidget_5.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem('27.12')
                    self.tableWidget_5.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem('30.41')
                    self.tableWidget_5.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('26.97')
                    self.tableWidget_5.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem('26.86')
                    self.tableWidget_5.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem('29.58')
                    self.tableWidget_5.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('26.5')
                    self.tableWidget_5.setItem(4, 1, newItem)
                    newItem = QTableWidgetItem('25.975')
                    self.tableWidget_5.setItem(4, 2, newItem)
                    newItem = QTableWidgetItem('7.08')
                    self.tableWidget_5.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('1.56')
                    self.tableWidget_5.setItem(5, 1, newItem)
                    newItem = QTableWidgetItem('2.525')
                    self.tableWidget_5.setItem(5, 2, newItem)
                    newItem = QTableWidgetItem('1')
                    self.tableWidget_5.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_5.setItem(6, 1, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_5.setItem(6, 2, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def zxyt2(self):
        try:
            jc = self.comboBox_20.currentText()
            if jc == "吸阻":
                try:
                    y1 = [1.402, 1.493, 1.553, 1.645, 1.696]
                    x1 = [380, 410, 460, 500, 560]
                    y2 = [1.696, 1.599, 1.447]
                    x2 = [6, 7.5, 8]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('吸阻 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    plt.show()
                except:
                    pass
            if jc == "总通风率":
                try:
                    y1 = [29.95, 30.25, 28.30, 28.45, 28.35]
                    x1 = [380, 410, 460, 500, 560]
                    y2 = [28.35, 28.38, 30.10]
                    x2 = [6, 7.5, 8]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('总通风 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    plt.show()
                except:
                    pass
        except:
            pass

    def jcfx2(self):
        try:
            jc = self.comboBox_20.currentText()
            if jc == "吸阻":
                try:
                    self.tableWidget_6.setRowCount(8)  # 设置表格的行数
                    self.tableWidget_6.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_6.setHorizontalHeaderLabels(["滤棒吸阻", "丝束"])  # 设置表格的列名
                    self.tableWidget_6.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('1.402')
                    self.tableWidget_6.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('1.696')
                    self.tableWidget_6.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('1.493')
                    self.tableWidget_6.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('1.599')
                    self.tableWidget_6.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('1.553')
                    self.tableWidget_6.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('1.447')
                    self.tableWidget_6.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('1.645')
                    self.tableWidget_6.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_6.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('1.696')
                    self.tableWidget_6.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_6.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('0.293')
                    self.tableWidget_6.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('0.248')
                    self.tableWidget_6.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_6.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_6.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_6.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_6.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('0.0586')
                    self.tableWidget_6.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('0.0826')
                    self.tableWidget_6.setItem(8, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

            if jc == "总通风率":
                try:
                    self.tableWidget_6.setRowCount(8)  # 设置表格的行数
                    self.tableWidget_6.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_6.setHorizontalHeaderLabels(["滤棒吸阻", "丝束"])  # 设置表格的列名
                    self.tableWidget_6.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('29.95')
                    self.tableWidget_6.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('28.35')
                    self.tableWidget_6.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('30.25')
                    self.tableWidget_6.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('28.38')
                    self.tableWidget_6.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('28.30')
                    self.tableWidget_6.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('30.10')
                    self.tableWidget_6.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('28.45')
                    self.tableWidget_6.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_6.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('28.35')
                    self.tableWidget_6.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_6.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('1.95')
                    self.tableWidget_6.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('1.75')
                    self.tableWidget_6.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_6.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_6.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_6.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('3')
                    self.tableWidget_6.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('0.39')
                    self.tableWidget_6.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('0.583')
                    self.tableWidget_6.setItem(8, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def zxyt3(self):
        try:
            jc = self.comboBox_28.currentText()
            if jc == "吸阻":
                try:
                    y1 = [1.946, 1.941, 1.835, 1.843, 1.8, 1.76, 1.728, 1.686]
                    x1 = [100, 150, 250, 300, 350, 400, 450, 500]
                    y2 = [1.943, 1.825, 1.725]
                    x2 = [1, 2, 3]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('吸阻 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    plt.show()
                except:
                    pass
            if jc == "总通风率":
                try:
                    y1 = [22.05, 23.95, 28.15, 28.85, 30.95, 34.35, 35.7, 34.95]
                    x1 = [100, 150, 250, 300, 350, 400, 450, 500]
                    y2 = [23, 29.32, 35]
                    x2 = [1, 2, 3]

                    plt.subplot(1, 2, 1)
                    plt.plot(x1, y1, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x1, y1, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('卷烟纸透气度')
                    plt.ylabel('均值')
                    plt.title('总通风 主效应图')

                    plt.subplot(1, 2, 2)
                    plt.plot(x2, y2, 'b', lw=1.5)  # 蓝色的线
                    plt.plot(x2, y2, 'ro')
                    plt.grid(True)
                    plt.axis('tight')
                    plt.xlabel('定量')
                    plt.ylabel('均值')

                    plt.tight_layout()
                    plt.show()
                except:
                    pass
        except:
            pass

    def jcfx3(self):
        try:
            jc = self.comboBox_28.currentText()
            if jc == "吸阻":
                try:
                    self.tableWidget_7.setRowCount(11)  # 设置表格的行数
                    self.tableWidget_7.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_7.setHorizontalHeaderLabels(["接装纸透气度", "排数"])  # 设置表格的列名
                    self.tableWidget_7.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "6", "7", "8", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('1.946')
                    self.tableWidget_7.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('1.943')
                    self.tableWidget_7.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('1.941')
                    self.tableWidget_7.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('1.825')
                    self.tableWidget_7.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('1.835')
                    self.tableWidget_7.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('1.725')
                    self.tableWidget_7.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('1.843')
                    self.tableWidget_7.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('1.8')
                    self.tableWidget_7.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('1.76')
                    self.tableWidget_7.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('1.728')
                    self.tableWidget_7.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('1.686')
                    self.tableWidget_7.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('0.261')
                    self.tableWidget_7.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('0.219')
                    self.tableWidget_7.setItem(8, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_7.setItem(9, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_7.setItem(9, 1, newItem)

                    newItem = QTableWidgetItem('0.027')
                    self.tableWidget_7.setItem(10, 0, newItem)
                    newItem = QTableWidgetItem('0.073')
                    self.tableWidget_7.setItem(10, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

            if jc == "总通风率":
                try:
                    self.tableWidget_7.setRowCount(11)  # 设置表格的行数
                    self.tableWidget_7.setColumnCount(2)  # 设置表格的列数
                    self.tableWidget_7.setHorizontalHeaderLabels(["接装纸透气度", "排数"])  # 设置表格的列名
                    self.tableWidget_7.setVerticalHeaderLabels(
                        ["1", "2", "3", "4", "5", "6", "7", "8", "极差值", "排序", "平均极差"])  # 设置表格的行名

                    newItem = QTableWidgetItem('22.05')
                    self.tableWidget_7.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem('23')
                    self.tableWidget_7.setItem(0, 1, newItem)

                    newItem = QTableWidgetItem('23.95')
                    self.tableWidget_7.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem('29.32')
                    self.tableWidget_7.setItem(1, 1, newItem)

                    newItem = QTableWidgetItem('28.15')
                    self.tableWidget_7.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem('35')
                    self.tableWidget_7.setItem(2, 1, newItem)

                    newItem = QTableWidgetItem('28.85')
                    self.tableWidget_7.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(3, 1, newItem)

                    newItem = QTableWidgetItem('30.95')
                    self.tableWidget_7.setItem(4, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(4, 1, newItem)

                    newItem = QTableWidgetItem('34.35')
                    self.tableWidget_7.setItem(5, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(5, 1, newItem)

                    newItem = QTableWidgetItem('35.70')
                    self.tableWidget_7.setItem(6, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(6, 1, newItem)

                    newItem = QTableWidgetItem('34.95')
                    self.tableWidget_7.setItem(7, 0, newItem)
                    newItem = QTableWidgetItem('')
                    self.tableWidget_7.setItem(7, 1, newItem)

                    newItem = QTableWidgetItem('13.65')
                    self.tableWidget_7.setItem(8, 0, newItem)
                    newItem = QTableWidgetItem('12')
                    self.tableWidget_7.setItem(8, 1, newItem)

                    newItem = QTableWidgetItem('1')
                    self.tableWidget_7.setItem(9, 0, newItem)
                    newItem = QTableWidgetItem('2')
                    self.tableWidget_7.setItem(9, 1, newItem)

                    newItem = QTableWidgetItem('1.70625')
                    self.tableWidget_7.setItem(10, 0, newItem)
                    newItem = QTableWidgetItem('4')
                    self.tableWidget_7.setItem(10, 1, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def fcfx(self):
        try:
            fc = self.comboBox_7.currentText()
            if fc == "吸阻":
                try:
                    db = pd.read_csv('xz.csv')
                    db = db[['jyztqd', 'dl', 'zrjhl', 'xz']]
                    data = np.array(db.loc[:, :])
                    data = pd.DataFrame(data, columns=['jyztqd', 'dl', 'zrjhl', 'xz'])
                    print(data)
                    formula = 'xz~ C(jyztqd) + C(dl)+C(zrjhl)'
                    anova_results = anova_lm(ols(formula, data).fit())
                    print(anova_results)

                    self._data = anova_results
                    self.tableWidget_4.setRowCount(self._data.shape[0])  # 设置表格的行数
                    self.tableWidget_4.setColumnCount(self._data.shape[1])  # 设置表格的列数
                    self.tableWidget_4.setHorizontalHeaderLabels(self._data.columns.tolist())  # 设置表格的列名
                    self.tableWidget_4.setVerticalHeaderLabels(self._data.index.tolist())  # 设置表格的行名

                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'df']))
                    self.tableWidget_4.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'sum_sq']))
                    self.tableWidget_4.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'mean_sq']))
                    self.tableWidget_4.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'F']))
                    self.tableWidget_4.setItem(0, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'PR(>F)']))
                    self.tableWidget_4.setItem(0, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'df']))
                    self.tableWidget_4.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'sum_sq']))
                    self.tableWidget_4.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'mean_sq']))
                    self.tableWidget_4.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'F']))
                    self.tableWidget_4.setItem(1, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'PR(>F)']))
                    self.tableWidget_4.setItem(1, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'df']))
                    self.tableWidget_4.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'sum_sq']))
                    self.tableWidget_4.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'mean_sq']))
                    self.tableWidget_4.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'F']))
                    self.tableWidget_4.setItem(2, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'PR(>F)']))
                    self.tableWidget_4.setItem(2, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'df']))
                    self.tableWidget_4.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'sum_sq']))
                    self.tableWidget_4.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'mean_sq']))
                    self.tableWidget_4.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'F']))
                    self.tableWidget_4.setItem(3, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'PR(>F)']))
                    self.tableWidget_4.setItem(3, 4, newItem)
                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
            if fc == "总通风率":
                try:
                    db = pd.read_csv('ztf.csv')
                    db = db[['jyztqd', 'dl', 'zrjhl', 'ztf']]
                    data = np.array(db.loc[:, :])
                    data = pd.DataFrame(data, columns=['jyztqd', 'dl', 'zrjhl', 'ztf'])
                    print(data)
                    formula = 'ztf~ C(jyztqd) + C(dl)+C(zrjhl)'
                    anova_results = anova_lm(ols(formula, data).fit())
                    print(anova_results)

                    self._data = anova_results
                    self.tableWidget_4.setRowCount(self._data.shape[0])  # 设置表格的行数
                    self.tableWidget_4.setColumnCount(self._data.shape[1])  # 设置表格的列数
                    self.tableWidget_4.setHorizontalHeaderLabels(self._data.columns.tolist())  # 设置表格的列名
                    self.tableWidget_4.setVerticalHeaderLabels(self._data.index.tolist())  # 设置表格的行名

                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'df']))
                    self.tableWidget_4.setItem(0, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'sum_sq']))
                    self.tableWidget_4.setItem(0, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'mean_sq']))
                    self.tableWidget_4.setItem(0, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'F']))
                    self.tableWidget_4.setItem(0, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(jyztqd)', 'PR(>F)']))
                    self.tableWidget_4.setItem(0, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'df']))
                    self.tableWidget_4.setItem(1, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'sum_sq']))
                    self.tableWidget_4.setItem(1, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'mean_sq']))
                    self.tableWidget_4.setItem(1, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'F']))
                    self.tableWidget_4.setItem(1, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(dl)', 'PR(>F)']))
                    self.tableWidget_4.setItem(1, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'df']))
                    self.tableWidget_4.setItem(2, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'sum_sq']))
                    self.tableWidget_4.setItem(2, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'mean_sq']))
                    self.tableWidget_4.setItem(2, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'F']))
                    self.tableWidget_4.setItem(2, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['C(zrjhl)', 'PR(>F)']))
                    self.tableWidget_4.setItem(2, 4, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'df']))
                    self.tableWidget_4.setItem(3, 0, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'sum_sq']))
                    self.tableWidget_4.setItem(3, 1, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'mean_sq']))
                    self.tableWidget_4.setItem(3, 2, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'F']))
                    self.tableWidget_4.setItem(3, 3, newItem)
                    newItem = QTableWidgetItem(str(self._data.loc['Residual', 'PR(>F)']))
                    self.tableWidget_4.setItem(3, 4, newItem)

                except Exception as e:
                    print(e)
                    QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误！", QMessageBox.Yes, QMessageBox.Yes)

    def rlt(self):
        try:
            rlt = self.comboBox_29.currentText()
            if rlt == "总通风":
                data = pd.read_csv('ztf.csv')
            if rlt == "纸通风":
                data = pd.read_csv('zt.csv')
            if rlt == "滤嘴通风":
                data = pd.read_csv('lztf.csv')
            #                  plt.savefig('lztf.png')#保存
            if rlt == "吸阻":
                data = pd.read_csv('xz.csv')
            if rlt == "封闭吸阻":
                data = pd.read_csv('fbxz.csv')

            a = data.corr()  # 得到这个dataframe的相关系数矩阵
            plt.subplots(figsize=(9, 9))  # 设置画面大小，而不是格数
            sns.heatmap(a, annot=True, vmax=1, square=True, cmap="Oranges")
            plt.rcParams['font.sans-serif'] = ['FangSong']
            plt.show()
        except:
            pass

    def shuchu1(self):
        self.tableWidget_2.setRowCount(25)  # 设置表格的行数
        self.tableWidget_2.setColumnCount(2)  # 设置表格的列数
        self.tableWidget_2.setHorizontalHeaderLabels(["样品序号", "卷烟纸规格"])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        Item0 = QTableWidgetItem("0#纸")
        Item1 = QTableWidgetItem("1#纸")
        Item2 = QTableWidgetItem("2#纸")
        Item3 = QTableWidgetItem("3#纸")
        Item4 = QTableWidgetItem("4#纸")
        Item5 = QTableWidgetItem("5#纸")
        Item6 = QTableWidgetItem("6#纸")
        Item7 = QTableWidgetItem("7#纸")
        Item8 = QTableWidgetItem("8#纸")
        Item9 = QTableWidgetItem("9#纸")
        Item10 = QTableWidgetItem("10#纸")
        Item11 = QTableWidgetItem("11#纸")
        Item12 = QTableWidgetItem("12#纸")
        Item13 = QTableWidgetItem("13#纸")
        Item14 = QTableWidgetItem("14#纸")
        Item15 = QTableWidgetItem("15#纸")
        Item16 = QTableWidgetItem("16#纸")
        Item17 = QTableWidgetItem("17#纸")
        Item18 = QTableWidgetItem("18#纸")
        Item19 = QTableWidgetItem("19#纸")
        Item20 = QTableWidgetItem("20#纸")
        Item21 = QTableWidgetItem("21#纸")
        Item22 = QTableWidgetItem("22#纸")
        Item23 = QTableWidgetItem("23#纸")
        Item24 = QTableWidgetItem("24#纸")
        Item25 = QTableWidgetItem("25#纸")

        self.tableWidget_2.setItem(0, 0, Item0)
        self.tableWidget_2.setItem(1, 0, Item1)
        self.tableWidget_2.setItem(2, 0, Item2)
        self.tableWidget_2.setItem(3, 0, Item3)
        self.tableWidget_2.setItem(4, 0, Item4)
        self.tableWidget_2.setItem(5, 0, Item5)
        self.tableWidget_2.setItem(6, 0, Item6)
        self.tableWidget_2.setItem(7, 0, Item7)
        self.tableWidget_2.setItem(8, 0, Item8)
        self.tableWidget_2.setItem(9, 0, Item9)
        self.tableWidget_2.setItem(10, 0, Item10)
        self.tableWidget_2.setItem(11, 0, Item11)
        self.tableWidget_2.setItem(12, 0, Item12)
        self.tableWidget_2.setItem(13, 0, Item13)
        self.tableWidget_2.setItem(14, 0, Item14)
        self.tableWidget_2.setItem(15, 0, Item15)
        self.tableWidget_2.setItem(16, 0, Item16)
        self.tableWidget_2.setItem(17, 0, Item17)
        self.tableWidget_2.setItem(18, 0, Item18)
        self.tableWidget_2.setItem(19, 0, Item19)
        self.tableWidget_2.setItem(20, 0, Item20)
        self.tableWidget_2.setItem(21, 0, Item21)
        self.tableWidget_2.setItem(22, 0, Item22)
        self.tableWidget_2.setItem(23, 0, Item23)
        self.tableWidget_2.setItem(24, 0, Item24)
        self.tableWidget_2.setItem(25, 0, Item25)

        LItem0 = QTableWidgetItem("70-32-1.8")
        LItem1 = QTableWidgetItem("40-26-0.9")
        LItem2 = QTableWidgetItem("40-28-1.2")
        LItem3 = QTableWidgetItem("40-30-1.5")
        LItem4 = QTableWidgetItem("40-32-1.8")
        LItem5 = QTableWidgetItem("40-34-2.1")
        LItem6 = QTableWidgetItem("50-26-1.5")
        LItem7 = QTableWidgetItem("50-28-1.8")
        LItem8 = QTableWidgetItem("50-30-2.21")
        LItem9 = QTableWidgetItem("50-32-0.9")
        LItem10 = QTableWidgetItem("50-34-1.2")
        LItem11 = QTableWidgetItem("60-26-2.1")
        LItem12 = QTableWidgetItem("60-28-0.9")
        LItem13 = QTableWidgetItem("60-30-1.2")
        LItem14 = QTableWidgetItem("60-32-1.5")
        LItem15 = QTableWidgetItem("60-34-1.8")
        LItem16 = QTableWidgetItem("70-26-1.2")
        LItem17 = QTableWidgetItem("70-28-1.5")
        LItem18 = QTableWidgetItem("70-30-1.8")
        LItem19 = QTableWidgetItem("70-32-2.1")
        LItem20 = QTableWidgetItem("70-34-0.9")
        LItem21 = QTableWidgetItem("80-26-1.8")
        LItem22 = QTableWidgetItem("80-28-2.1")
        LItem23 = QTableWidgetItem("80-30-0.9")
        LItem24 = QTableWidgetItem("80-32-1.2")
        LItem25 = QTableWidgetItem("80-34-1.5")

        self.tableWidget_2.setItem(0, 1, LItem0)
        self.tableWidget_2.setItem(1, 1, LItem1)
        self.tableWidget_2.setItem(2, 1, LItem2)
        self.tableWidget_2.setItem(3, 1, LItem3)
        self.tableWidget_2.setItem(4, 1, LItem4)
        self.tableWidget_2.setItem(5, 1, LItem5)
        self.tableWidget_2.setItem(6, 1, LItem6)
        self.tableWidget_2.setItem(7, 1, LItem7)
        self.tableWidget_2.setItem(8, 1, LItem8)
        self.tableWidget_2.setItem(9, 1, LItem9)
        self.tableWidget_2.setItem(10, 1, LItem10)
        self.tableWidget_2.setItem(11, 1, LItem11)
        self.tableWidget_2.setItem(12, 1, LItem12)
        self.tableWidget_2.setItem(13, 1, LItem13)
        self.tableWidget_2.setItem(14, 1, LItem14)
        self.tableWidget_2.setItem(15, 1, LItem15)
        self.tableWidget_2.setItem(16, 1, LItem16)
        self.tableWidget_2.setItem(17, 1, LItem17)
        self.tableWidget_2.setItem(18, 1, LItem18)
        self.tableWidget_2.setItem(19, 1, LItem19)
        self.tableWidget_2.setItem(20, 1, LItem20)
        self.tableWidget_2.setItem(21, 1, LItem21)
        self.tableWidget_2.setItem(22, 1, LItem22)
        self.tableWidget_2.setItem(23, 1, LItem23)
        self.tableWidget_2.setItem(24, 1, LItem24)
        self.tableWidget_2.setItem(25, 1, LItem25)

    def shuchu2(self):
        self.tableWidget_2.setRowCount(9)  # 设置表格的行数
        self.tableWidget_2.setColumnCount(2)  # 设置表格的列数
        self.tableWidget_2.setHorizontalHeaderLabels(["样品序号", "接装纸规格"])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        Item_J0 = QTableWidgetItem("1#接装纸")
        self.tableWidget_2.setItem(0, 0, Item_J0)
        LItem_J0 = QTableWidgetItem("100单排")
        self.tableWidget_2.setItem(0, 1, LItem_J0)

        Item_J1 = QTableWidgetItem("2#接装纸")
        self.tableWidget_2.setItem(1, 0, Item_J1)
        LItem_J1 = QTableWidgetItem("150单排")
        self.tableWidget_2.setItem(1, 1, LItem_J1)

        Item_J2 = QTableWidgetItem("3产品")
        self.tableWidget_2.setItem(2, 0, Item_J2)
        LItem_J2 = QTableWidgetItem("200双排")
        self.tableWidget_2.setItem(2, 1, LItem_J2)

        Item_J3 = QTableWidgetItem("4#接装纸")
        self.tableWidget_2.setItem(3, 0, Item_J3)
        LItem_J3 = QTableWidgetItem("250双排")
        self.tableWidget_2.setItem(3, 1, LItem_J3)

        Item_J4 = QTableWidgetItem("5#接装纸")
        self.tableWidget_2.setItem(4, 0, Item_J4)
        LItem_J4 = QTableWidgetItem("300双排")
        self.tableWidget_2.setItem(4, 1, LItem_J4)

        Item_J5 = QTableWidgetItem("6#接装纸")
        self.tableWidget_2.setItem(5, 0, Item_J5)
        LItem_J5 = QTableWidgetItem("350双排")
        self.tableWidget_2.setItem(5, 1, LItem_J5)

        Item_J6 = QTableWidgetItem("7#接装纸")
        self.tableWidget_2.setItem(6, 0, Item_J6)
        LItem_J6 = QTableWidgetItem("400三排")
        self.tableWidget_2.setItem(6, 1, LItem_J6)

        Item_J7 = QTableWidgetItem("8#接装纸")
        self.tableWidget_2.setItem(7, 0, Item_J7)
        LItem_J7 = QTableWidgetItem("450三排")
        self.tableWidget_2.setItem(7, 1, LItem_J7)

        Item_J8 = QTableWidgetItem("9#接装纸")
        self.tableWidget_2.setItem(8, 0, Item_J8)
        LItem_J8 = QTableWidgetItem("500三排")
        self.tableWidget_2.setItem(8, 1, LItem_J8)

    def shuchu3(self):
        self.tableWidget_2.setRowCount(6)  # 设置表格的行数
        self.tableWidget_2.setColumnCount(2)  # 设置表格的列数
        self.tableWidget_2.setHorizontalHeaderLabels(["样品序号", "滤棒规格"])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        Item_B0 = QTableWidgetItem("1#棒")
        self.tableWidget_2.setItem(0, 0, Item_B0)
        LItem_B0 = QTableWidgetItem("6.0丝束560吸阻")
        self.tableWidget_2.setItem(0, 1, LItem_B0)

        Item_B1 = QTableWidgetItem("2产品")
        self.tableWidget_2.setItem(1, 0, Item_B1)
        LItem_B1 = QTableWidgetItem("6.0丝束600吸阻")
        self.tableWidget_2.setItem(1, 1, LItem_B1)

        Item_B2 = QTableWidgetItem("3#棒")
        self.tableWidget_2.setItem(2, 0, Item_B2)
        LItem_B2 = QTableWidgetItem("7.5丝束460吸阻")
        self.tableWidget_2.setItem(2, 1, LItem_B2)

        Item_B3 = QTableWidgetItem("4#棒")
        self.tableWidget_2.setItem(3, 0, Item_B3)
        LItem_B3 = QTableWidgetItem("7.5丝束500吸阻")
        self.tableWidget_2.setItem(3, 1, LItem_B3)

        Item_B4 = QTableWidgetItem("5#棒")
        self.tableWidget_2.setItem(4, 0, Item_B4)
        LItem_B4 = QTableWidgetItem("8.0丝束380吸阻")
        self.tableWidget_2.setItem(4, 1, LItem_B4)

        Item_B5 = QTableWidgetItem("6#棒")
        self.tableWidget_2.setItem(5, 0, Item_B5)
        LItem_B5 = QTableWidgetItem("8.0丝束410吸阻")
        self.tableWidget_2.setItem(5, 1, LItem_B5)

    def getfiles(self):
        self.comboBox_6.clear()
        self.comboBox_6.addItems([""])
        dig = QFileDialog()
        dig.setFileMode(QFileDialog.AnyFile)
        dig.setFilter(QDir.Files)

        if dig.exec_():
            filenames = dig.selectedFiles()
            self.comboBox_5.clear()
            self.comboBox_5.addItems([""])
            self.comboBox_5.addItems(filenames)
            print(filenames)

            def load_data(file_path):
                lines = []
                f = open(file_path[0], 'r', encoding="gbk")
                with f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            load_data(filenames)
            num = len(load_data(filenames))
            self.comboBox_6.addItems([str(i) for i in range(1, num + 1)])

    def schaxun(self):
        mulu = self.comboBox_5.currentText()
        zu = int(self.comboBox_6.currentText()) - 1

        def load_data(file_path):
            lines = []
            f = open(file_path, 'r', encoding="gbk")
            with f:
                for i in f.readlines():
                    line = i.strip()
                    lines.append(line)

            index = []
            last = []
            for i in range(len(lines)):
                if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                    index.append(i)
                try:
                    if lines[i][0] == "N":
                        last.append(i)
                except:
                    pass
            p = list(zip(index, last))
            group = []
            for indexs in p:
                total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                         "DD": []}
                for i in range(indexs[0] + 1, indexs[1]):
                    try:
                        total["wt"].append(float(lines[i].split()[1].strip("*")))
                        total["circ"].append(float(lines[i].split()[2].strip("*")))
                        total["PD"].append(float(lines[i].split()[3].strip("*")))
                        total["CPD"].append(float(lines[i].split()[4].strip("*")))
                        total["Vent"].append(float(lines[i].split()[5].strip("*")))
                        total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                        total["TotV"].append(float(lines[i].split()[7].strip("*")))
                        total["Len"].append(float(lines[i].split()[8].strip("*")))
                        total["DD"].append(float(lines[i].split()[9].strip("*")))
                    except:
                        pass
                group.append(total)  # 提取的全在group里面了
            return group

        data = load_data(mulu)[zu]
        self.tableWidget.setRowCount(len(data["wt"]))  # 设置表格的行数
        self.tableWidget.setColumnCount(len(data))  # 设置表格的列数
        self.tableWidget.setHorizontalHeaderLabels(["wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(data["wt"])):
            newItem = QTableWidgetItem(str(data["wt"][i]))
            newItem1 = QTableWidgetItem(str(data["circ"][i]))
            newItem2 = QTableWidgetItem(str(data["PD"][i]))
            newItem3 = QTableWidgetItem(str(data["CPD"][i]))
            newItem4 = QTableWidgetItem(str(data["Vent"][i]))
            newItem5 = QTableWidgetItem(str(data["PVnt"][i]))
            newItem6 = QTableWidgetItem(str(data["TotV"][i]))
            newItem7 = QTableWidgetItem(str(data["Len"][i]))
            newItem8 = QTableWidgetItem(str(data["DD"][i]))

            self.tableWidget.setItem(i, 0, newItem)
            self.tableWidget.setItem(i, 1, newItem1)
            self.tableWidget.setItem(i, 2, newItem2)
            self.tableWidget.setItem(i, 3, newItem3)
            self.tableWidget.setItem(i, 4, newItem4)
            self.tableWidget.setItem(i, 5, newItem5)
            self.tableWidget.setItem(i, 6, newItem6)
            self.tableWidget.setItem(i, 7, newItem7)
            self.tableWidget.setItem(i, 8, newItem8)

    def fenxi7(self):

        zhuangtai = False
        if self.radioButton_13.isChecked():
            zhuangtai = True
        # 左边的数据
        pingpai = self.comboBox_71.currentText()
        nian = self.comboBox_72.currentText()
        # yue = self.comboBox_66.currentText()

        text = pingpai
        path1 = self.path + "\\" + text
        path2 = self.path + "\\" + pingpai + "\\" + nian
        self.data2 = self.data[path1][path2]
        # 根据所选的年获取月的数据
        yues = []
        for key, value in self.data2.items():
            nians = os.path.split(key)[-1]
            yues.append(nians)
        total_data = {}
        for yue in yues:
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]  # 到txt
            last_result = []
            label = []

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        if len(lines[i].split()) == 10:
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                    group.append(total)  # 提取的全在group里面了
                return group

            for path in data3:
                # all txt组
                data = load_data(path)
                # 【】1
                p = 0
                for i in data:
                    p += 1
                    last_result.append(i)  # [[],[]]
                    label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

            total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [], "DD": []}
            for da in last_result:
                print(da)
                for i in da["wt"]:
                    total["wt"].append(i)
                for i in da["circ"]:
                    total["circ"].append(i)
                for i in da["PD"]:
                    total["PD"].append(i)
                for i in da["CPD"]:
                    total["CPD"].append(i)
                for i in da["Vent"]:
                    total["Vent"].append(i)
                for i in da["PVnt"]:
                    total["PVnt"].append(i)
                for i in da["TotV"]:
                    total["TotV"].append(i)
                for i in da["Len"]:
                    total["Len"].append(i)
                for i in da["DD"]:
                    total["DD"].append(i)

            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = try_(pingpai, total)
                # {"wt":"","",""}
            else:
                data5 = total
            total_data[yue] = data5
        ####------- total_data ------->根据年得到月的所有数据
        chooseItem = self.comboBox_27.currentText()
        zhibiao = self.comboBox_26.currentText()
        # "分指标质量控制图", "分指标年度z检验p值折线图","分指标年度变异系数折线图","分指标年度中位数折线图",
        if chooseItem == "年度分指标质量控制图":

            # 均值图
            label = []
            data_get = []
            for key, item in total_data.items():
                label.append(key)
                data_get.append(item[zhibiao])
            try:
                sip.delete(self.canvasv)
                sip.delete(self.layoutv)
            except:
                pass
            self.figv = plt.Figure()
            self.canvasv = FC(self.figv)
            self.layoutv = QVBoxLayout()
            self.layoutv.addWidget(self.canvasv)
            self.widget_5.setLayout(self.layoutv)
            ax = self.figv.add_subplot(111)
            ######z
            all = []
            for i in data_get:
                all.append(np.mean(i))
            ax.plot(label, [np.mean(i) for i in data_get])
            ax.scatter(label, [np.mean(i) for i in data_get])
            ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
            ax.set_title("年度x图（均值图）")
            self.canvasv.draw_idle()
            self.canvasv.draw()  # TODO:这里开始绘制

            # S图（标准差图）
            try:
                sip.delete(self.canvasp)
                sip.delete(self.layoutp)
            except:
                pass

            self.figp = plt.Figure()
            self.canvasp = FC(self.figp)
            self.layoutp = QVBoxLayout()
            self.layoutp.addWidget(self.canvasp)
            self.widget_6.setLayout(self.layoutp)
            ax = self.figp.add_subplot(111)
            ######z
            all = []
            for i in data_get:
                all.append(np.std(i))
            ax.plot(label, [np.std(i) for i in data_get])
            ax.scatter(label, [np.std(i) for i in data_get])
            ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
            ax.set_title("年度S图（标准差图）")
            self.canvasp.draw_idle()
            self.canvasp.draw()  # TODO:这里开始绘制

            # R图（极差图）

            try:
                sip.delete(self.canvaso)
                sip.delete(self.layouto)
            except:
                pass

            self.figo = plt.Figure()
            self.canvaso = FC(self.figo)
            self.layouto = QVBoxLayout()
            self.layouto.addWidget(self.canvaso)
            self.widget_7.setLayout(self.layouto)
            ax = self.figo.add_subplot(111)
            ######z
            all = []
            for i in data_get:
                all.append(max(i) - min(i))
            ax.plot(label, [max(i) - min(i) for i in data_get])
            ax.scatter(label, [max(i) - min(i) for i in data_get])

            ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
            ax.set_title("年度R图（极差图）")
            self.canvaso.draw_idle()
            self.canvaso.draw()  # TODO:这里开始绘制
        elif chooseItem == "分指标年度z检验p值折线图":

            label = []
            data_get = []
            for key, item in total_data.items():
                label.append(key)
                data_get.append(item[zhibiao])
            try:
                sip.delete(self.canvasv)
                sip.delete(self.layoutv)
            except:
                pass
            self.figv = plt.Figure()
            self.canvasv = FC(self.figv)
            self.layoutv = QVBoxLayout()
            self.layoutv.addWidget(self.canvasv)
            self.widget_5.setLayout(self.layoutv)
            ax = self.figv.add_subplot(111)
            ######z
            ax.plot(label, [sw.ztest(i, value=float(self.lineEdit_6.text()))[1] for i in data_get])
            ax.set_title("分指标年度z检验p值折线图")
            self.canvasv.draw_idle()
            self.canvasv.draw()  # TODO:这里开始绘制
        elif chooseItem == "分指标年度变异系数折线图":  #

            label = []
            data_get = []
            for key, item in total_data.items():
                label.append(key)
                data_get.append(item[zhibiao])
            try:
                sip.delete(self.canvasv)
                sip.delete(self.layoutv)
            except:
                pass
            self.figv = plt.Figure()
            self.canvasv = FC(self.figv)
            self.layoutv = QVBoxLayout()
            self.layoutv.addWidget(self.canvasv)
            self.widget_5.setLayout(self.layoutv)
            ax = self.figv.add_subplot(111)
            ax.plot(label, [np.std(i) / np.mean(i) for i in data_get])

            ax.plot(label, [0.01 for i in range(len(label))], linestyle="--")
            ax.plot(label, [0.02 for i in range(len(label))], linestyle="--")
            ax.plot(label, [0.03 for i in range(len(label))], linestyle="--")
            ax.plot(label, [0.04 for i in range(len(label))], linestyle="--")
            ax.plot(label, [0.1 for i in range(len(label))], linestyle="--")

            ax.set_title("分指标年度变异系数折线图")
            self.canvasv.draw_idle()
            self.canvasv.draw()  # TODO:这里开始绘制
        elif chooseItem == "分指标年度中位数折线图":
            label = []
            data_get = []
            for key, item in total_data.items():
                label.append(key)
                data_get.append(item[zhibiao])
            try:
                sip.delete(self.canvasv)
                sip.delete(self.layoutv)
            except:
                pass
            self.figv = plt.Figure()
            self.canvasv = FC(self.figv)
            self.layoutv = QVBoxLayout()
            self.layoutv.addWidget(self.canvasv)
            self.widget_5.setLayout(self.layoutv)
            ax = self.figv.add_subplot(111)

            # 中位数
            def get_median(data):
                data.sort()
                half = len(data) // 2
                return (data[half] + data[~half]) / 2

            ax.plot(label, [get_median(i) for i in data_get])

            ax.set_title("年度中位数折线图")
            self.canvasv.draw_idle()
            self.canvasv.draw()  # TODO:这里开始绘制
        elif chooseItem == "月度分指标质量控制图":
            zhuangtai = False
            if self.radioButton_13.isChecked():
                zhuangtai = True
            pingpai = self.comboBox_71.currentText()
            nian = self.comboBox_72.currentText()
            yue = self.comboBox_73.currentText()
            zhibiao = self.comboBox_26.currentText()
            text = pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]  # 到txt

            last_result = []
            label = []

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []

                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            # print(float(lines[i].split()[1].strip("*")))
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            for path in data3:
                # all txt组
                data = load_data(path)
                # 【】1
                p = 0
                for i in data:
                    p += 1
                    last_result.append(i)  # [[],[]]
                    label.append(str(p))  # ["txt"]

            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = [try_(pingpai, i) for i in last_result]
                data5 = [i[zhibiao] for i in data5]

            else:
                data5 = [i[zhibiao] for i in last_result]
            label = [i + 1 for i in range(len(label))]

            try:
                sip.delete(self.canvasv)
                sip.delete(self.layoutv)
            except:
                pass
            self.figv = plt.Figure()
            self.canvasv = FC(self.figv)
            self.layoutv = QVBoxLayout()
            self.layoutv.addWidget(self.canvasv)
            self.widget_5.setLayout(self.layoutv)
            ax = self.figv.add_subplot(111)
            ######z
            all = []
            for i in data5:
                all.append(np.mean(i))
            ax.plot(label, [np.mean(i) for i in data5])
            ax.scatter(label, [np.mean(i) for i in data5])
            ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
            ax.set_title("月度x图（均值图）")
            self.canvasv.draw_idle()
            self.canvasv.draw()  # TODO:这里开始绘制

            # S图（标准差图）
            try:
                sip.delete(self.canvasp)
                sip.delete(self.layoutp)
            except:
                pass

            self.figp = plt.Figure()
            self.canvasp = FC(self.figp)
            self.layoutp = QVBoxLayout()
            self.layoutp.addWidget(self.canvasp)
            self.widget_6.setLayout(self.layoutp)
            ax = self.figp.add_subplot(111)
            ######z
            all = []
            for i in data5:
                all.append(np.std(i))
            ax.plot(label, [np.std(i) for i in data5])
            ax.scatter(label, [np.std(i) for i in data5])
            ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
            ax.set_title("月度S图（标准差图）")
            self.canvasp.draw_idle()
            self.canvasp.draw()  # TODO:这里开始绘制

            # R图（极差图）

            try:
                sip.delete(self.canvaso)
                sip.delete(self.layouto)
            except:
                pass

            self.figo = plt.Figure()
            self.canvaso = FC(self.figo)
            self.layouto = QVBoxLayout()
            self.layouto.addWidget(self.canvaso)
            self.widget_7.setLayout(self.layouto)
            ax = self.figo.add_subplot(111)
            ######z
            all = []
            for i in data5:
                all.append(max(i) - min(i))
            ax.plot(label, [max(i) - min(i) for i in data5])
            ax.scatter(label, [max(i) - min(i) for i in data5])

            ax.plot(label, [np.mean(all) + 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) - 3 * np.std(all) for i in range(len(label))], color="r")
            ax.plot(label, [np.mean(all) for i in range(len(label))], color="g")
            ax.set_title("月度R图（极差图）")
            self.canvaso.draw_idle()
            self.canvaso.draw()  # TODO:这里开始绘制

    def fenxi6(self):

        zhuangtai = False
        if self.radioButton_12.isChecked():
            zhuangtai = True
        # 左边的数据
        pingpai = self.comboBox_67.currentText()
        nian = self.comboBox_65.currentText()
        yue = self.comboBox_66.currentText()
        text = pingpai
        path1 = self.path + "\\" + text
        path2 = self.path + "\\" + pingpai + "\\" + nian
        path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
        data3 = self.data[path1][path2][path3]  # 到txt
        last_result = []
        label = []

        def load_data(file_path):
            lines = []
            with open(file_path, "r", encoding="gbk") as f:
                for i in f.readlines():
                    line = i.strip()
                    lines.append(line)

            index = []
            last = []
            for i in range(len(lines)):
                if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                    index.append(i)
                try:
                    if lines[i][0] == "N":
                        last.append(i)
                except:
                    pass
            p = list(zip(index, last))
            group = []
            for indexs in p:
                total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                         "DD": []}
                for i in range(indexs[0] + 1, indexs[1]):
                    if len(lines[i].split()) == 10:
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                group.append(total)  # 提取的全在group里面了
            return group

        for path in data3:
            # all txt组
            data = load_data(path)
            # 【】1
            p = 0
            for i in data:
                p += 1
                last_result.append(i)  # [[],[]]
                label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [], "DD": []}
        for da in last_result:

            for i in da["wt"]:
                total["wt"].append(i)
            for i in da["circ"]:
                total["circ"].append(i)
            for i in da["PD"]:
                total["PD"].append(i)
            for i in da["CPD"]:
                total["CPD"].append(i)
            for i in da["Vent"]:
                total["Vent"].append(i)
            for i in da["PVnt"]:
                total["PVnt"].append(i)
            for i in da["TotV"]:
                total["TotV"].append(i)
            for i in da["Len"]:
                total["Len"].append(i)
            for i in da["DD"]:
                total["DD"].append(i)

        if zhuangtai:
            def contrast(pingpaiming, canshu, num):
                # 初始化标准
                standard = []
                with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                    f = csv.reader(f)
                    for i in f:
                        standard.append(i)
                    del standard[0]

                # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                for i in standard:
                    if i[1] == pingpaiming:
                        if canshu == "wt":
                            sp = float(i[2].split("±")[0])
                            sp1 = float(i[2].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "PD":
                            sp = float(i[3].split("±")[0]) / 1000
                            sp1 = float(i[3].split("±")[1]) / 1000
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "TotV":
                            sp = float(i[4].split("±")[0])
                            sp1 = float(i[4].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "DD":
                            sp = float(i[5].split("±")[0])
                            sp1 = float(i[5].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "circ":
                            sp = float(i[6].split("±")[0])
                            sp1 = float(i[6].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"

            # TODO:字典数据total
            # TODO:字典数据total
            def try_(pingpai, total):

                wt = total["wt"]  #
                circ = total["circ"]  #
                PD = total["PD"]  #
                cpd = total["CPD"]
                vent = total["Vent"]
                pvnt = total["PVnt"]
                totv = total["TotV"]  #
                Len = total["Len"]
                DD = total["DD"]  #
                # 去除不符合标准的contrast
                for i in range(len(wt)):
                    if contrast(pingpai, "wt", wt[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(circ)):
                    if contrast(pingpai, "circ", circ[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(PD)):
                    if contrast(pingpai, "PD", PD[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(totv)):
                    if contrast(pingpai, "TotV", totv[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(DD)):
                    if contrast(pingpai, "DD", DD[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                # todo:不符合3σ
                # wt
                # np.std(a,ddof=1)
                left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                nums = []
                for i in range(len(wt)):
                    if left < wt[i] < right:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                nums = []
                # circ
                for i in range(len(circ)):
                    if left1 < circ[i] < right1:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]
                # PD
                nums = []
                for i in range(len(PD)):
                    if left2 < PD[i] < right2:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # cpd
                nums = []
                for i in range(len(cpd)):
                    if left3 < cpd[i] < right3:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # vent
                nums = []

                for i in range(len(vent)):
                    if left4 < vent[i] < right4:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # pvnt
                nums = []

                for i in range(len(pvnt)):
                    if left5 < pvnt[i] < right5:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # totv
                nums = []
                for i in range(len(totv)):
                    if left6 < totv[i] < right6:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # Len
                nums = []
                for i in range(len(Len)):
                    if left7 < Len[i] < right7:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # DD
                nums = []
                for i in range(len(DD)):
                    if left8 < DD[i] < right8:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                        "Len": Len, "DD": DD}

            data5 = try_(pingpai, total)

        else:
            data5 = total
        # 右边的数据
        try:
            pingpai = self.comboBox_70.currentText()
            nian = self.comboBox_69.currentText()
            yue = self.comboBox_68.currentText()
            text = pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]  # 到txt
            last_result = []
            label = []

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        if len(lines[i].split()) == 10:
                            try:
                                total["wt"].append(float(lines[i].split()[1].strip("*")))
                                total["circ"].append(float(lines[i].split()[2].strip("*")))
                                total["PD"].append(float(lines[i].split()[3].strip("*")))
                                total["CPD"].append(float(lines[i].split()[4].strip("*")))
                                total["Vent"].append(float(lines[i].split()[5].strip("*")))
                                total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                                total["TotV"].append(float(lines[i].split()[7].strip("*")))
                                total["Len"].append(float(lines[i].split()[8].strip("*")))
                                total["DD"].append(float(lines[i].split()[9].strip("*")))
                            except:
                                pass
                    group.append(total)  # 提取的全在group里面了
                return group

            for path in data3:
                # all txt组
                data = load_data(path)
                # 【】1
                p = 0
                for i in data:
                    p += 1
                    last_result.append(i)  # [[],[]]
                    label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

            total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [], "DD": []}
            for da in last_result:

                for i in da["wt"]:
                    total["wt"].append(i)
                for i in da["circ"]:
                    total["circ"].append(i)
                for i in da["PD"]:
                    total["PD"].append(i)
                for i in da["CPD"]:
                    total["CPD"].append(i)
                for i in da["Vent"]:
                    total["Vent"].append(i)
                for i in da["PVnt"]:
                    total["PVnt"].append(i)
                for i in da["TotV"]:
                    total["TotV"].append(i)
                for i in da["Len"]:
                    total["Len"].append(i)
                for i in da["DD"]:
                    total["DD"].append(i)

            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data55 = try_(pingpai, total)

            else:
                data55 = total
        except:
            pass
        num = self.comboBox_25.currentText()
        zhibiao = self.comboBox_24.currentText()
        if num == "独立样本t检验":
            # 初始化删除数据
            self.textEdit_8.clear()
            # 1、查询每月数据_____________________________________
            for key, item in data55.items():
                # t

                sample = np.asarray(data5[key])
                sample1 = np.asarray(data55[key])

                r = stats.ttest_ind(sample, sample1)
                self.textEdit_8.append(f"{key}" + "pvalue:" + str(r.__getattribute__("pvalue")))
                self.textEdit_8.append("_____________________________________")
                self.textEdit_8.append("_____________________________________")
        # 分指标单样本t检验
        elif num == "分指标单样本t检验":
            # 初始化删除数据
            self.textEdit_8.clear()
            # 1、查询每月数据_____________________________________
            bt = float(self.lineEdit_5.text())
            sample = np.asarray(np.array(data5[zhibiao]))
            # 单样本检验用stats.ttest_1samp
            r = stats.ttest_1samp(sample, bt, axis=0)
            self.textEdit_8.append(
                "pvalue:" + str(
                    r.__getattribute__("pvalue")) + '\n' + "ks检验p值：" + str(
                    stats.kstest(data5[zhibiao], 'norm', (np.mean(data5[zhibiao]), np.std(data5[zhibiao])))))


        elif num == "分指标散点图":

            def contrast(pingpaiming, canshu, num):
                # 初始化标准
                standard = []
                with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                    f = csv.reader(f)
                    for i in f:
                        standard.append(i)
                    del standard[0]

                # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                for i in standard:
                    if i[1] == pingpaiming:
                        if canshu == "wt":
                            sp = float(i[2].split("±")[0])
                            sp1 = float(i[2].split("±")[1])
                            print(sp, sp1)
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "PD":
                            sp = float(i[3].split("±")[0]) / 1000
                            sp1 = float(i[3].split("±")[1]) / 1000
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "TotV":
                            sp = float(i[4].split("±")[0])
                            sp1 = float(i[4].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "DD":
                            sp = float(i[5].split("±")[0])
                            sp1 = float(i[5].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "circ":
                            sp = float(i[6].split("±")[0])
                            sp1 = float(i[6].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"

            data = data5[zhibiao]

            num = len(data)  # 总数
            p = 0
            sp = []

            for i in range(len(data)):

                if contrast(self.comboBox_67.currentText(), zhibiao, data[i]) == "合格":
                    p += 1
                else:
                    # 不合格
                    sp.append(i)

            per = (p / num) * 100

            # 合格率
            self.textEdit_8.setText("总数为 " + str(num) + '\n' + "合格数为 " + str(p) + '\n' + "合格率为 " + str(per) + "%")

            def contrast1(pingpaiming, canshu):
                # 初始化标准
                standard = []
                with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                    f = csv.reader(f)
                    for i in f:
                        standard.append(i)
                    del standard[0]

                # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                for i in standard:

                    if i[1] == pingpaiming:
                        if canshu == "wt":
                            sp = float(i[2].split("±")[0])
                            sp1 = float(i[2].split("±")[1])

                            return sp, sp1
                        elif canshu == "PD":
                            sp = float(i[3].split("±")[0]) / 1000
                            sp1 = float(i[3].split("±")[1]) / 1000
                            return sp, sp1

                        elif canshu == "TotV":
                            sp = float(i[4].split("±")[0])
                            sp1 = float(i[4].split("±")[1])
                            return sp, sp1
                        elif canshu == "DD":
                            sp = float(i[5].split("±")[0])
                            sp1 = float(i[5].split("±")[1])
                            return sp, sp1
                        elif canshu == "circ":
                            sp = float(i[6].split("±")[0])
                            sp1 = float(i[6].split("±")[1])
                            return sp, sp1

            sp, sp1 = contrast1(self.comboBox_67.currentText(), zhibiao)

            try:
                sip.delete(self.canvasa)
                sip.delete(self.layouta)
            except:
                pass
            self.figa = plt.Figure()
            self.canvasa = FC(self.figa)
            self.layouta = QVBoxLayout()
            self.layouta.addWidget(self.canvasa)
            self.widget_8.setLayout(self.layouta)
            ax = self.figa.add_subplot(111)
            # x的个数决定了样本量
            ax.scatter(np.arange(len(data5[zhibiao])), data5[zhibiao])
            ax.plot(np.arange(len(data5[zhibiao])), [sp - sp1 for i in range(len(data5[zhibiao]))], linestyle="-")
            ax.plot(np.arange(len(data5[zhibiao])), [sp1 + sp for i in range(len(data5[zhibiao]))], linestyle="-")
            ax.legend()
            ax.set_title("散点图")
            self.canvasa.draw_idle()
            self.canvasa.draw()  # TODO:这里开始绘制
        elif num == "分指标直方图":
            self.textEdit_8.clear()
            try:
                sip.delete(self.canvasa)
                sip.delete(self.layouta)
            except:
                pass
            self.figa = plt.Figure()
            self.canvasa = FC(self.figa)
            self.layouta = QVBoxLayout()
            self.layouta.addWidget(self.canvasa)
            self.widget_8.setLayout(self.layouta)
            ax = self.figa.add_subplot(111)
            # x的个数决定了样本量
            ax.hist(data5[zhibiao])
            ax.legend()
            ax.set_title("直方图")
            self.canvasa.draw_idle()
            self.canvasa.draw()  # TODO:这里开始绘制
            self.textEdit_8.append("ks检验p值：" + str(
                stats.kstest(data5[zhibiao], 'norm', (np.mean(data5[zhibiao]), np.std(data5[zhibiao])))))

    def fenxi5(self):
        # 1、查询每月数据
        # 2、显示每月数据的均值、方差、偏度、峰度、变异系数、极差、最小值、最大值、下四分位数、上四分位数、中位数指标
        # try:
        # 初始化删除数据
        self.textEdit_8.clear()
        zhuangtai = False
        if self.radioButton_11.isChecked():
            zhuangtai = True

        pingpai = self.comboBox_62.currentText()
        nian = self.comboBox_64.currentText()
        yue = self.comboBox_63.currentText()
        text = pingpai
        path1 = self.path + "\\" + text
        path2 = self.path + "\\" + pingpai + "\\" + nian
        path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
        data3 = self.data[path1][path2][path3]  # 到txt

        last_result = []
        label = []

        def load_data(file_path):
            lines = []
            with open(file_path, "r", encoding="gbk") as f:
                for i in f.readlines():
                    line = i.strip()
                    lines.append(line)

            index = []
            last = []
            for i in range(len(lines)):
                if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                    index.append(i)
                try:
                    if lines[i][0] == "N":
                        last.append(i)
                except:
                    pass
            p = list(zip(index, last))
            group = []
            for indexs in p:
                total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                         "DD": []}
                for i in range(indexs[0] + 1, indexs[1]):
                    if len(lines[i].split()) == 10:
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                group.append(total)  # 提取的全在group里面了
            return group

        for path in data3:
            # all txt组
            data = load_data(path)
            # 【】1
            p = 0
            for i in data:
                p += 1
                last_result.append(i)  # [[],[]]
                label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [], "DD": []}
        for da in last_result:

            for i in da["wt"]:
                total["wt"].append(i)
            for i in da["circ"]:
                total["circ"].append(i)
            for i in da["PD"]:
                total["PD"].append(i)
            for i in da["CPD"]:
                total["CPD"].append(i)
            for i in da["Vent"]:
                total["Vent"].append(i)
            for i in da["PVnt"]:
                total["PVnt"].append(i)
            for i in da["TotV"]:
                total["TotV"].append(i)
            for i in da["Len"]:
                total["Len"].append(i)
            for i in da["DD"]:
                total["DD"].append(i)

        if zhuangtai:
            def contrast(pingpaiming, canshu, num):
                # 初始化标准
                standard = []
                with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                    f = csv.reader(f)
                    for i in f:
                        standard.append(i)
                    del standard[0]

                # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                for i in standard:
                    if i[1] == pingpaiming:
                        if canshu == "wt":
                            sp = float(i[2].split("±")[0])
                            sp1 = float(i[2].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "PD":
                            sp = float(i[3].split("±")[0]) / 1000
                            sp1 = float(i[3].split("±")[1]) / 1000
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "TotV":
                            sp = float(i[4].split("±")[0])
                            sp1 = float(i[4].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "DD":
                            sp = float(i[5].split("±")[0])
                            sp1 = float(i[5].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "circ":
                            sp = float(i[6].split("±")[0])
                            sp1 = float(i[6].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"

            # TODO:字典数据total
            # TODO:字典数据total
            def try_(pingpai, total):

                wt = total["wt"]  #
                circ = total["circ"]  #
                PD = total["PD"]  #
                cpd = total["CPD"]
                vent = total["Vent"]
                pvnt = total["PVnt"]
                totv = total["TotV"]  #
                Len = total["Len"]
                DD = total["DD"]  #
                # 去除不符合标准的contrast
                for i in range(len(wt)):
                    if contrast(pingpai, "wt", wt[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(circ)):
                    if contrast(pingpai, "circ", circ[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(PD)):
                    if contrast(pingpai, "PD", PD[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(totv)):
                    if contrast(pingpai, "TotV", totv[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(DD)):
                    if contrast(pingpai, "DD", DD[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                # todo:不符合3σ
                # wt
                # np.std(a,ddof=1)
                left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                nums = []
                for i in range(len(wt)):
                    if left < wt[i] < right:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                nums = []
                # circ
                for i in range(len(circ)):
                    if left1 < circ[i] < right1:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]
                # PD
                nums = []
                for i in range(len(PD)):
                    if left2 < PD[i] < right2:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # cpd
                nums = []
                for i in range(len(cpd)):
                    if left3 < cpd[i] < right3:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # vent
                nums = []

                for i in range(len(vent)):
                    if left4 < vent[i] < right4:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # pvnt
                nums = []

                for i in range(len(pvnt)):
                    if left5 < pvnt[i] < right5:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # totv
                nums = []
                for i in range(len(totv)):
                    if left6 < totv[i] < right6:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # Len
                nums = []
                for i in range(len(Len)):
                    if left7 < Len[i] < right7:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # DD
                nums = []
                for i in range(len(DD)):
                    if left8 < DD[i] < right8:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                        "Len": Len, "DD": DD}

            data5 = try_(pingpai, total)

        else:
            data5 = total

        def foundation(data):
            # 均值
            aver = np.mean(data)
            # 方差
            std = np.var(data)
            # 偏度
            s = pd.Series(data)
            piandu = s.skew()
            # 峰度
            fengdu = s.kurt()  # <class 'numpy.float64'>
            # 变异系数
            cv = np.std(data) / np.mean(data)
            # 最大
            Max = max(data)
            # 最小
            Min = min(data)
            # 极差
            jicha = Max - Min

            # 中位数
            def get_median(data):
                data.sort()
                half = len(data) // 2
                return (data[half] + data[~half]) / 2

            median = get_median(data)
            # 下四分位数
            xia = np.percentile(data, (75))
            # 上四分位数
            shang = np.percentile(data, (25))
            RSD = round((np.sqrt(std) / aver) * 100, 2)
            return aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang, RSD

        # 1、查询每月数据_____________________________________
        for key, item in data5.items():
            self.textEdit_8.append(str(key) + str(data5[key]))
            # 2、显示每月数据的均值、方差、偏度、峰度、变异系数、极差、最小值、最大值、下四分位数、上四分位数、中位数指标
            aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang, RSD = foundation(data5[key])
            # t
            bt = 2.0
            # bt = float(self.lineEdit_5.text())
            sample = np.asarray(data5[key])
            # 单样本检验用stats.ttest_1samp
            r = stats.ttest_1samp(sample, bt, axis=0)
            self.textEdit_8.append(f"{key}均值 {str(aver)}")
            self.textEdit_8.append(f"{key}方差 {str(std)}")
            self.textEdit_8.append(f"{key}偏度 {str(piandu)}")
            self.textEdit_8.append(f"{key}峰度 {str(fengdu)}")
            self.textEdit_8.append(f"{key}变异系数 {str(cv)}")
            self.textEdit_8.append(f"{key}最大值 {str(Max)}")
            self.textEdit_8.append(f"{key}最小值 {str(Min)}")
            self.textEdit_8.append(f"{key}极差 {str(jicha)}")
            self.textEdit_8.append(f"{key}中位数 {str(median)}")
            self.textEdit_8.append(f"{key}下四分位数 {str(shang)}")
            self.textEdit_8.append(f"{key}上四分位数 {str(xia)}")
            self.textEdit_8.append(f"{key}相对标准偏差RSd为{str(RSD)}%")
            self.textEdit_8.append(
                f"{key} t检验 statistic:" + str(r.__getattribute__("statistic")) + "  " + "pvalue:" + str(
                    r.__getattribute__("pvalue")))
            self.textEdit_8.append("_____________________________________")
            self.textEdit_8.append("_____________________________________")

    def fenxi4(self):
        # try:
        zhuangtai = False
        if self.radioButton_10.isChecked():
            zhuangtai = True

        pingpai = self.comboBox_61.currentText()
        nian = self.comboBox_59.currentText()
        yue = self.comboBox_60.currentText()
        text = pingpai
        path1 = self.path + "\\" + text
        path2 = self.path + "\\" + pingpai + "\\" + nian
        path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
        data3 = self.data[path1][path2][path3]  # 到txt
        last_result = []
        label = []

        def load_data(file_path):
            lines = []
            with open(file_path, "r", encoding="gbk") as f:
                for i in f.readlines():
                    line = i.strip()
                    lines.append(line)

            index = []
            last = []
            for i in range(len(lines)):
                if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                    index.append(i)
                try:
                    if lines[i][0] == "N":
                        last.append(i)
                except:
                    pass
            p = list(zip(index, last))
            group = []
            for indexs in p:
                total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                         "DD": []}
                for i in range(indexs[0] + 1, indexs[1]):
                    if len(lines[i].split()) == 10:
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                group.append(total)  # 提取的全在group里面了
            return group

        for path in data3:
            # all txt组
            data = load_data(path)
            # 【】1
            p = 0
            for i in data:
                p += 1
                last_result.append(i)  # [[],[]]
                label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]

        total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [], "DD": []}
        for da in last_result:
            print(da)
            for i in da["wt"]:
                total["wt"].append(i)
            for i in da["circ"]:
                total["circ"].append(i)
            for i in da["PD"]:
                total["PD"].append(i)
            for i in da["CPD"]:
                total["CPD"].append(i)
            for i in da["Vent"]:
                total["Vent"].append(i)
            for i in da["PVnt"]:
                total["PVnt"].append(i)
            for i in da["TotV"]:
                total["TotV"].append(i)
            for i in da["Len"]:
                total["Len"].append(i)
            for i in da["DD"]:
                total["DD"].append(i)
        print(len(total["DD"]))
        if zhuangtai:
            def contrast(pingpaiming, canshu, num):
                # 初始化标准
                standard = []
                with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                    f = csv.reader(f)
                    for i in f:
                        standard.append(i)
                    del standard[0]

                # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                for i in standard:
                    if i[1] == pingpaiming:
                        if canshu == "wt":
                            sp = float(i[2].split("±")[0])
                            sp1 = float(i[2].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "PD":
                            sp = float(i[3].split("±")[0]) / 1000
                            sp1 = float(i[3].split("±")[1]) / 1000
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "TotV":
                            sp = float(i[4].split("±")[0])
                            sp1 = float(i[4].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "DD":
                            sp = float(i[5].split("±")[0])
                            sp1 = float(i[5].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "circ":
                            sp = float(i[6].split("±")[0])
                            sp1 = float(i[6].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"

            # TODO:字典数据total
            # TODO:字典数据total
            def try_(pingpai, total):

                wt = total["wt"]  #
                circ = total["circ"]  #
                PD = total["PD"]  #
                cpd = total["CPD"]
                vent = total["Vent"]
                pvnt = total["PVnt"]
                totv = total["TotV"]  #
                Len = total["Len"]
                DD = total["DD"]  #
                # 去除不符合标准的contrast
                for i in range(len(wt)):
                    if contrast(pingpai, "wt", wt[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(circ)):
                    if contrast(pingpai, "circ", circ[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(PD)):
                    if contrast(pingpai, "PD", PD[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(totv)):
                    if contrast(pingpai, "TotV", totv[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                for i in range(len(DD)):
                    if contrast(pingpai, "DD", DD[i]) == "不合格":
                        wt.remove(wt[i])
                        circ.remove(circ[i])
                        PD.remove(PD[i])
                        cpd.remove(cpd[i])
                        vent.remove(vent[i])
                        pvnt.remove(pvnt[i])
                        totv.remove(totv[i])
                        Len.remove(Len[i])
                        DD.remove(DD[i])
                # todo:不符合3σ
                # wt
                # np.std(a,ddof=1)
                left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                nums = []
                for i in range(len(wt)):
                    if left < wt[i] < right:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                nums = []
                # circ
                for i in range(len(circ)):
                    if left1 < circ[i] < right1:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]
                # PD
                nums = []
                for i in range(len(PD)):
                    if left2 < PD[i] < right2:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # cpd
                nums = []
                for i in range(len(cpd)):
                    if left3 < cpd[i] < right3:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # vent
                nums = []

                for i in range(len(vent)):
                    if left4 < vent[i] < right4:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # pvnt
                nums = []

                for i in range(len(pvnt)):
                    if left5 < pvnt[i] < right5:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # totv
                nums = []
                for i in range(len(totv)):
                    if left6 < totv[i] < right6:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # Len
                nums = []
                for i in range(len(Len)):
                    if left7 < Len[i] < right7:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                # DD
                nums = []
                for i in range(len(DD)):
                    if left8 < DD[i] < right8:
                        nums.append(i)
                wt = [wt[i] for i in nums]
                circ = [circ[i] for i in nums]
                PD = [PD[i] for i in nums]
                cpd = [cpd[i] for i in nums]
                vent = [vent[i] for i in nums]
                pvnt = [pvnt[i] for i in nums]
                totv = [totv[i] for i in nums]
                Len = [Len[i] for i in nums]
                DD = [DD[i] for i in nums]

                return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                        "Len": Len, "DD": DD}

            data5 = try_(pingpai, total)

        else:
            data5 = total
        print(data5)
        print(len(data5["DD"]))
        # 2.5
        # 多因素分析模块由用户选择数据范围（每一组，每一天，每一月，全年）
        # ① 以PD为因变量，分析每个物理指标与PD的关系显著性
        # ② 筛除不显著自变量
        # ③ 建立剩余自变量与PD的多元线性回归方程（输出系数，拟合图像）
        pdd = data5["PD"]
        sp = ["wt", "circ", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"]

        for i in sp:

            pp = stats.pearsonr(pdd, data5[i])[1]
            # 判断 p值
            if pp > 0.05:
                sp.remove(i)

        ddd = []
        for i in sp:
            ddd.append(pd.DataFrame({i: data5[i]}))

        pd_data = pd.DataFrame(data5)

        X = pd.concat(ddd, axis=1)
        y = pd_data.loc[:, 'PD']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
        linreg = LinearRegression()
        model = linreg.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        # 训练后模型截距
        self.textEdit_7.clear()
        self.textEdit_7.append(f"拟合自变量为{str(sp)}")
        self.textEdit_7.append(f"系数为{str(linreg.coef_)}")
        self.textEdit_7.append(f"截距为{str(linreg.intercept_)}")
        self.textEdit_7.append(f"拟合得分为{str(score)}")
        try:
            sip.delete(self.canvas7)
            sip.delete(self.layout7)
        except:
            pass
        self.fig7 = plt.Figure()
        self.canvas7 = FC(self.fig7)
        self.layout7 = QVBoxLayout()
        self.layout7.addWidget(self.canvas7)
        self.widget_13.setLayout(self.layout7)
        ax = self.fig7.add_subplot(111)
        # x的个数决定了样本量
        y_pred = linreg.predict(X_test)
        ax.plot(range(len(y_pred)), y_pred, 'b', label="predict")
        ax.plot(range(len(y_pred)), y_test, 'r', label="test")
        ax.legend()
        ax.set_title("拟合图")
        self.canvas7.draw_idle()
        self.canvas7.draw()  # TODO:这里开始绘制
        # except:
        #     QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

    def fenxi3(self):
        try:
            zhuangtai = False
            if self.radioButton_3.isChecked():
                zhuangtai = True
            z = self.lineEdit.text()
            pingpai = self.comboBox_23.currentText()
            nian = self.comboBox_22.currentText()
            yue = self.comboBox_19.currentText()
            zhibiao = self.comboBox_21.currentText()
            text = pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]  # 到txt
            # ① 使用z检验的方法，计算用户指定范围内（日、月或年）各组数据的p值，输出，绘制折线图
            # ② 计算用户指定范围内（日、月或年）各组数据的平均值、中位数，输出，绘制折线图
            # ③ 计算用户指定范围内（日、月或年）各组数据的CV变异系数，输出，绘制折线图
            last_result = []
            label = []

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []

                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            # print(float(lines[i].split()[1].strip("*")))
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            for path in data3:
                # all txt组
                data = load_data(path)
                # 【】1
                p = 0
                for i in data:
                    p += 1
                    last_result.append(i)  # [[],[]]
                    label.append(str(os.path.split(path)[-1] + "第" + str(p) + "组"))  # ["txt"]
            print(last_result)
            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = [try_(pingpai, i) for i in last_result]
                data5 = [i[zhibiao] for i in data5]

            else:
                data5 = [i[zhibiao] for i in last_result]
            # z检验
            p = []
            for i in data5:
                p.append(sw.ztest(i, value=float(z))[1])  # p
            self.textEdit_2.clear()
            for i in range(len(p)):
                self.textEdit_2.append(str(label[i] + "p值" + str(p[i])))
            try:
                sip.delete(self.canvas)
                sip.delete(self.layout)
            except:
                pass
            self.fig = plt.Figure()
            self.canvas = FC(self.fig)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.canvas)
            self.widget_2.setLayout(self.layout)
            ax = self.fig.add_subplot(111)
            x = [i for i in range(len(p))]
            ax.plot(x, p)
            ax.set_title("z检验")
            self.canvas.draw_idle()
            self.canvas.draw()  # TODO:这里开始绘制

            # 平均值、中位数
            mean = []
            zhong = []
            for i in data5:
                mean.append(np.mean(i))
                zhong.append(np.median(i))
            for i in range(len(mean)):
                self.textEdit_2.append(str(label[i] + "平均值" + str(mean[i]) + "中位数" + str(zhong[i])))
            try:
                sip.delete(self.canvas2)
                sip.delete(self.layout2)
            except:
                pass
            self.fig2 = plt.Figure()
            self.canvas2 = FC(self.fig2)
            self.layout2 = QVBoxLayout()
            self.layout2.addWidget(self.canvas2)
            self.widget_3.setLayout(self.layout2)
            ax = self.fig2.add_subplot(111)
            x = [i for i in range(len(mean))]
            ax.plot(x, mean, label="平均值")
            ax.plot(x, zhong, label="中位数")
            ax.legend()
            ax.set_title("平均值 中位数")
            self.canvas2.draw_idle()
            self.canvas2.draw()  # TODO:这里开始绘制

            # cv
            cv = []

            for i in data5:
                cv.append(np.std(i) / np.mean(i))

            for i in range(len(cv)):
                self.textEdit_2.append(str(label[i] + "变异系数" + str(cv[i])))
            try:
                sip.delete(self.canvas3)
                sip.delete(self.layout3)
            except:
                pass
            self.fig3 = plt.Figure()
            self.canvas3 = FC(self.fig3)
            self.layout3 = QVBoxLayout()
            self.layout3.addWidget(self.canvas3)
            self.widget_4.setLayout(self.layout3)
            ax = self.fig3.add_subplot(111)
            x = [i for i in range(len(mean))]
            ax.plot(x, cv)
            ax.axhline(y=0.01, color='green', linestyle='--')
            ax.axhline(y=0.02, color='green', linestyle='--')
            ax.axhline(y=0.03, color='green', linestyle='--')
            ax.axhline(y=0.04, color='green', linestyle='--')
            ax.axhline(y=0.1, color='green', linestyle='--')

            ax.set_title("变异系数")
            self.canvas3.draw_idle()
            self.canvas3.draw()  # TODO:这里开始绘制
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

    def huatu(self):
        try:

            zhuangtai = False
            if self.radioButton_2.isChecked():
                zhuangtai = True

            pingpai = self.comboBox_13.currentText()
            nian = self.comboBox_11.currentText()
            yue = self.comboBox_12.currentText()
            ri = self.comboBox_14.currentText()
            zu = int(self.comboBox_15.currentText()) - 1
            # tablewidget
            path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
            zhibiao = self.comboBox_16.currentText()

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            data = load_data(path)[zu]
            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = try_(pingpai, data)
                data5 = data5[zhibiao]

            else:
                data5 = data[zhibiao]
            # print(data5)
            # huatu
            tu = self.comboBox_17.currentText()
            # 箱线图","散点图","直方图
            if tu == "直方图":
                try:
                    sip.delete(self.canvas1)
                    sip.delete(self.layout1)
                except:
                    pass
                self.fig1 = plt.Figure()
                self.canvas1 = FC(self.fig1)
                self.layout1 = QVBoxLayout()
                self.layout1.addWidget(self.canvas1)
                self.widget.setLayout(self.layout1)

                ax = self.fig1.add_subplot(111)
                # x的个数决定了样本量
                bins = np.linspace(min(data5), max(data5), 20)
                ax.hist(data5, bins)
                ax.set_title("直方图")
                self.canvas1.draw_idle()
                self.canvas1.draw()  # TODO:这里开始绘制
            elif tu == "箱线图":
                try:
                    sip.delete(self.canvas1)
                    sip.delete(self.layout1)
                except:
                    pass
                self.fig1 = plt.Figure()
                self.canvas1 = FC(self.fig1)
                self.layout1 = QVBoxLayout()
                self.layout1.addWidget(self.canvas1)
                self.widget.setLayout(self.layout1)
                ax = self.fig1.add_subplot(111)
                ax.boxplot(data5)
                ax.set_title("箱线图")
                self.canvas1.draw_idle()
                self.canvas1.draw()  # TODO:这里开始绘制
            elif tu == "散点图":
                try:
                    sip.delete(self.canvas1)
                    sip.delete(self.layout1)
                except:
                    pass
                self.fig1 = plt.Figure()
                self.canvas1 = FC(self.fig1)
                self.layout1 = QVBoxLayout()
                self.layout1.addWidget(self.canvas1)
                self.widget.setLayout(self.layout1)
                ax = self.fig1.add_subplot(111)
                # x的个数决定了样本量
                num = [i for i in range(len(data5))]
                print(num)
                print(data5)
                ax.scatter(num, data5)
                ax.set_title("散点图")
                self.canvas1.draw_idle()
                self.canvas1.draw()  # TODO:这里开始绘制

            def foundation(data):
                # 均值
                aver = np.mean(data)
                # 方差
                std = np.var(data)
                # 偏度
                s = pd.Series(data)
                piandu = s.skew()
                # 峰度
                fengdu = s.kurt()  # <class 'numpy.float64'>
                # 变异系数
                cv = np.std(data) / np.mean(data)
                # 最大
                Max = max(data)
                # 最小
                Min = min(data)
                # 极差
                jicha = Max - Min

                # 中位数
                def get_median(data):
                    data.sort()
                    half = len(data) // 2
                    return (data[half] + data[~half]) / 2

                median = get_median(data)
                # 下四分位数
                xia = np.percentile(data, (75))
                # 上四分位数
                shang = np.percentile(data, (25))
                return aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang

            aver, std, piandu, fengdu, cv, Min, Max, jicha, median, xia, shang = foundation(data5)
            self.textEdit.clear()
            self.textEdit.append(f"均值 {str(aver)}")
            self.textEdit.append(f"方差 {str(std)}")
            self.textEdit.append(f"偏度 {str(piandu)}")
            self.textEdit.append(f"峰度 {str(fengdu)}")
            self.textEdit.append(f"变异系数 {str(cv)}")
            self.textEdit.append(f"最大值 {str(Max)}")
            self.textEdit.append(f"最小值 {str(Min)}")
            self.textEdit.append(f"极差 {str(jicha)}")
            self.textEdit.append(f"中位数 {str(median)}")
            self.textEdit.append(f"下四分位数 {str(shang)}")
            self.textEdit.append(f"上四分位数 {str(xia)}")
        except:
            QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

    def t_z(self):
        # 正态
        try:
            zhuangtai = False
            if self.radioButton_2.isChecked():
                zhuangtai = True

            pingpai = self.comboBox_13.currentText()
            nian = self.comboBox_11.currentText()
            yue = self.comboBox_12.currentText()
            ri = self.comboBox_14.currentText()
            zu = int(self.comboBox_15.currentText()) - 1
            # tablewidget
            path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
            zhibiao = self.comboBox_18.currentText()

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            data = load_data(path)[zu]
            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = try_(pingpai, data)
                data5 = data5[zhibiao]

            else:
                data5 = data[zhibiao]

            # ks
            self.lineEdit_3.setText(str(stats.kstest(data5, 'norm', (np.mean(data5), np.std(data5)))))
        except:
            QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

    def t(self):
        # t
        try:
            zhuangtai = False
            if self.radioButton_2.isChecked():
                zhuangtai = True

            pingpai = self.comboBox_13.currentText()
            nian = self.comboBox_11.currentText()
            yue = self.comboBox_12.currentText()
            ri = self.comboBox_14.currentText()
            zu = int(self.comboBox_15.currentText()) - 1
            # tablewidget
            path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
            zhibiao = self.comboBox_18.currentText()

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            data = load_data(path)[zu]
            if zhuangtai:
                def contrast(pingpaiming, canshu, num):
                    # 初始化标准
                    standard = []
                    with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                        f = csv.reader(f)
                        for i in f:
                            standard.append(i)
                        del standard[0]

                    # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                    for i in standard:
                        if i[1] == pingpaiming:
                            if canshu == "wt":
                                sp = float(i[2].split("±")[0])
                                sp1 = float(i[2].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "PD":
                                sp = float(i[3].split("±")[0]) / 1000
                                sp1 = float(i[3].split("±")[1]) / 1000
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "TotV":
                                sp = float(i[4].split("±")[0])
                                sp1 = float(i[4].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "DD":
                                sp = float(i[5].split("±")[0])
                                sp1 = float(i[5].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"
                            elif canshu == "circ":
                                sp = float(i[6].split("±")[0])
                                sp1 = float(i[6].split("±")[1])
                                if (sp - sp1) <= num <= (sp + sp1):
                                    return "合格"
                                else:
                                    return "不合格"

                # TODO:字典数据total
                # TODO:字典数据total
                def try_(pingpai, total):

                    wt = total["wt"]  #
                    circ = total["circ"]  #
                    PD = total["PD"]  #
                    cpd = total["CPD"]
                    vent = total["Vent"]
                    pvnt = total["PVnt"]
                    totv = total["TotV"]  #
                    Len = total["Len"]
                    DD = total["DD"]  #
                    # 去除不符合标准的contrast
                    for i in range(len(wt)):
                        if contrast(pingpai, "wt", wt[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(circ)):
                        if contrast(pingpai, "circ", circ[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(PD)):
                        if contrast(pingpai, "PD", PD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(totv)):
                        if contrast(pingpai, "TotV", totv[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    for i in range(len(DD)):
                        if contrast(pingpai, "DD", DD[i]) == "不合格":
                            wt.remove(wt[i])
                            circ.remove(circ[i])
                            PD.remove(PD[i])
                            cpd.remove(cpd[i])
                            vent.remove(vent[i])
                            pvnt.remove(pvnt[i])
                            totv.remove(totv[i])
                            Len.remove(Len[i])
                            DD.remove(DD[i])
                    # todo:不符合3σ
                    # wt
                    # np.std(a,ddof=1)
                    left = np.mean(wt) - 3 * np.std(wt, ddof=1)
                    right = np.mean(wt) + 3 * np.std(wt, ddof=1)

                    left1 = np.mean(circ) - 3 * np.std(circ, ddof=1)
                    right1 = np.mean(circ) + 3 * np.std(circ, ddof=1)

                    left2 = np.mean(PD) - 3 * np.std(PD, ddof=1)
                    right2 = np.mean(PD) + 3 * np.std(PD, ddof=1)

                    left3 = np.mean(cpd) - 3 * np.std(cpd, ddof=1)
                    right3 = np.mean(cpd) + 3 * np.std(cpd, ddof=1)

                    left4 = np.mean(vent) - 3 * np.std(vent, ddof=1)
                    right4 = np.mean(vent) + 3 * np.std(vent, ddof=1)

                    left5 = np.mean(pvnt) - 3 * np.std(pvnt, ddof=1)
                    right5 = np.mean(pvnt) + 3 * np.std(pvnt, ddof=1)

                    left6 = np.mean(totv) - 3 * np.std(totv, ddof=1)
                    right6 = np.mean(totv) + 3 * np.std(totv, ddof=1)

                    left7 = np.mean(Len) - 3 * np.std(Len, ddof=1)
                    right7 = np.mean(Len) + 3 * np.std(Len, ddof=1)

                    left8 = np.mean(DD) - 3 * np.std(DD, ddof=1)
                    right8 = np.mean(DD) + 3 * np.std(DD, ddof=1)

                    nums = []
                    for i in range(len(wt)):
                        if left < wt[i] < right:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    nums = []
                    # circ
                    for i in range(len(circ)):
                        if left1 < circ[i] < right1:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]
                    # PD
                    nums = []
                    for i in range(len(PD)):
                        if left2 < PD[i] < right2:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # cpd
                    nums = []
                    for i in range(len(cpd)):
                        if left3 < cpd[i] < right3:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # vent
                    nums = []

                    for i in range(len(vent)):
                        if left4 < vent[i] < right4:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # pvnt
                    nums = []

                    for i in range(len(pvnt)):
                        if left5 < pvnt[i] < right5:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # totv
                    nums = []
                    for i in range(len(totv)):
                        if left6 < totv[i] < right6:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # Len
                    nums = []
                    for i in range(len(Len)):
                        if left7 < Len[i] < right7:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    # DD
                    nums = []
                    for i in range(len(DD)):
                        if left8 < DD[i] < right8:
                            nums.append(i)
                    wt = [wt[i] for i in nums]
                    circ = [circ[i] for i in nums]
                    PD = [PD[i] for i in nums]
                    cpd = [cpd[i] for i in nums]
                    vent = [vent[i] for i in nums]
                    pvnt = [pvnt[i] for i in nums]
                    totv = [totv[i] for i in nums]
                    Len = [Len[i] for i in nums]
                    DD = [DD[i] for i in nums]

                    return {"wt": wt, "circ": circ, "PD": PD, "CPD": cpd, "Vent": vent, "PVnt": pvnt, "TotV": totv,
                            "Len": Len, "DD": DD}

                data5 = try_(pingpai, data)
                data5 = data5[zhibiao]

            else:
                data5 = data[zhibiao]

            bt = float(self.lineEdit_2.text())
            sample = np.asarray(data5)
            # 单样本检验用stats.ttest_1samp
            r = stats.ttest_1samp(sample, bt, axis=0)
            self.lineEdit_4.setText("statistic:" + str(r.__getattribute__("statistic")) + "  " + "pvalue:" + str(
                r.__getattribute__("pvalue")))
        except:
            QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

    def tongji(self):
        try:
            pingpai = self.comboBox.currentText()
            nian = self.comboBox_2.currentText()
            yue = self.comboBox_3.currentText()
            ri = self.comboBox_4.currentText()
            zu = int(self.comboBox_9.currentText()) - 1
            # tablewidget
            path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri
            zhibiao = self.comboBox_10.currentText()  # 指标

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            def contrast(pingpaiming, canshu, num):
                # 初始化标准
                standard = []
                with open("数据及标准\标准\细支烟物理指标标准.csv", "r") as f:
                    f = csv.reader(f)
                    for i in f:
                        standard.append(i)
                    del standard[0]
                    print(standard)
                # "wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"
                for i in standard:
                    if i[1] == pingpaiming:
                        if canshu == "wt":
                            sp = float(i[2].split("±")[0])
                            sp1 = float(i[2].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "PD":
                            sp = float(i[3].split("±")[0]) / 1000
                            sp1 = float(i[3].split("±")[1]) / 1000
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "TotV":
                            sp = float(i[4].split("±")[0])
                            sp1 = float(i[4].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "DD":
                            sp = float(i[5].split("±")[0])
                            sp1 = float(i[5].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"
                        elif canshu == "circ":
                            sp = float(i[6].split("±")[0])
                            sp1 = float(i[6].split("±")[1])
                            if (sp - sp1) <= num <= (sp + sp1):
                                return "合格"
                            else:
                                return "不合格"

            data1 = load_data(path)[zu]
            data_wt = data1["wt"]
            data_circ = data1["circ"]
            data_PD = data1["PD"]
            data_CPD = data1["CPD"]
            data_Vent = data1["Vent"]
            data_PVnt = data1["PVnt"]
            data_TotV = data1["TotV"]
            data_Len = data1["Len"]
            data_DD = data1["DD"]
            # 获取一个列表
            data = load_data(path)[zu][zhibiao]
            num = len(data)  # 总数
            p = 0
            sp = []
            for i in range(len(data)):
                if contrast(pingpai, zhibiao, data[i]) == "合格":
                    p += 1
                else:
                    # 不合格
                    sp.append(i)
            per = round((p / num) * 100, 2)
            # 合格率
            self.label_13.setText(str(per) + "%")
            print(per)
            data2 = []
            for i in sp:
                data3 = []
                data3.append(data_wt[i])
                data3.append(data_circ[i])
                data3.append(data_PD[i])
                data3.append(data_CPD[i])
                data3.append(data_Vent[i])
                data3.append(data_PVnt[i])
                data3.append(data_TotV[i])
                data3.append(data_Len[i])
                data3.append(data_DD[i])
                data2.append(data3)
            # 不合格数据所在行
            self.tableWidget_3.setRowCount(len(data2))  # 设置表格的行数
            self.tableWidget_3.setColumnCount(9)  # 设置表格的列数
            self.tableWidget_3.setHorizontalHeaderLabels(
                ["wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"])
            self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(data2)):
                newItem = QTableWidgetItem(str(data2[i][0]))
                newItem1 = QTableWidgetItem(str(data2[i][1]))
                newItem2 = QTableWidgetItem(str(data2[i][2]))
                newItem3 = QTableWidgetItem(str(data2[i][3]))
                newItem4 = QTableWidgetItem(str(data2[i][4]))
                newItem5 = QTableWidgetItem(str(data2[i][5]))
                newItem6 = QTableWidgetItem(str(data2[i][6]))
                newItem7 = QTableWidgetItem(str(data2[i][7]))
                newItem8 = QTableWidgetItem(str(data2[i][8]))

                self.tableWidget_3.setItem(i, 0, newItem)
                self.tableWidget_3.setItem(i, 1, newItem1)
                self.tableWidget_3.setItem(i, 2, newItem2)
                self.tableWidget_3.setItem(i, 3, newItem3)
                self.tableWidget_3.setItem(i, 4, newItem4)
                self.tableWidget_3.setItem(i, 5, newItem5)
                self.tableWidget_3.setItem(i, 6, newItem6)
                self.tableWidget_3.setItem(i, 7, newItem7)
                self.tableWidget_3.setItem(i, 8, newItem8)
        except:
            QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

    def chaxun(self):
        try:
            # 获取 品牌，年， 月， 日， 组
            pingpai = self.comboBox.currentText()
            nian = self.comboBox_2.currentText()
            yue = self.comboBox_3.currentText()
            ri = self.comboBox_4.currentText()
            zu = int(self.comboBox_9.currentText()) - 1
            # tablewidget
            path = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            data = load_data(path)[zu]
            self.tableWidget.setRowCount(len(data["wt"]))  # 设置表格的行数
            self.tableWidget.setColumnCount(len(data))  # 设置表格的列数
            self.tableWidget.setHorizontalHeaderLabels(["wt", "circ", "PD", "CPD", "Vent", "PVnt", "TotV", "Len", "DD"])
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(data["wt"])):
                newItem = QTableWidgetItem(str(data["wt"][i]))
                newItem1 = QTableWidgetItem(str(data["circ"][i]))
                newItem2 = QTableWidgetItem(str(data["PD"][i]))
                newItem3 = QTableWidgetItem(str(data["CPD"][i]))
                newItem4 = QTableWidgetItem(str(data["Vent"][i]))
                newItem5 = QTableWidgetItem(str(data["PVnt"][i]))
                newItem6 = QTableWidgetItem(str(data["TotV"][i]))
                newItem7 = QTableWidgetItem(str(data["Len"][i]))
                newItem8 = QTableWidgetItem(str(data["DD"][i]))

                self.tableWidget.setItem(i, 0, newItem)
                self.tableWidget.setItem(i, 1, newItem1)
                self.tableWidget.setItem(i, 2, newItem2)
                self.tableWidget.setItem(i, 3, newItem3)
                self.tableWidget.setItem(i, 4, newItem4)
                self.tableWidget.setItem(i, 5, newItem5)
                self.tableWidget.setItem(i, 6, newItem6)
                self.tableWidget.setItem(i, 7, newItem7)
                self.tableWidget.setItem(i, 8, newItem8)
        except:
            QMessageBox.warning(self, "警告", "数据有误，确认不为空再试！", QMessageBox.Yes, QMessageBox.Yes)

    def init_(self):
        init_com1 = ['wt', 'circ', 'PD', 'CPD', 'Vent', 'PVnt', 'TotV', 'Len', 'DD']
        # ('名称', '07221黄鹤楼（硬生态）'), ('烟支质量Wt（g/支）', '0.520±0.050'), ('烟支吸阻PD（Pa）', '1850±250'),
        # ('总通风率TotV（％）', '25.0±10.0'), ('烟支硬度DD（％）', '53.0±12.0'), ('圆周Circ （mm）', '17.1±0.2')
        # init_com1 = ['wt', 'circ', 'PD', 'TotV', 'DD']
        self.comboBox_10.addItems([""])
        self.comboBox_10.addItems(init_com1)
        self.comboBox_16.addItems([""])
        self.comboBox_16.addItems(init_com1)
        self.comboBox_21.addItems([""])
        self.comboBox_21.addItems(init_com1)
        self.comboBox_18.addItems([""])
        self.comboBox_18.addItems(init_com1)

        # 热力图分析
        self.comboBox_29.addItems([""])
        self.comboBox_29.addItems(["总通风", "纸通风", "滤嘴通风", "吸阻", "封闭吸阻"])
        # 热力图分析
        self.comboBox_33.addItems([""])
        self.comboBox_33.addItems(["总通风", "纸通风", "滤嘴通风", "吸阻", "封闭吸阻"])

        # 方差分析
        self.comboBox_7.addItems([""])
        self.comboBox_7.addItems(["吸阻", "总通风率"])
        # 方差分析
        self.comboBox_32.addItems([""])
        self.comboBox_32.addItems(["吸阻", "总通风率"])

        # 极差分析
        self.comboBox_8.addItems([""])
        self.comboBox_8.addItems(["吸阻", "总通风率"])
        self.comboBox_20.addItems([""])
        self.comboBox_20.addItems(["吸阻", "总通风率"])
        self.comboBox_28.addItems([""])
        self.comboBox_28.addItems(["吸阻", "总通风率"])

        self.comboBox_30.addItems([""])
        self.comboBox_30.addItems(["吸阻", "总通风率"])
        self.comboBox_31.addItems([""])
        self.comboBox_31.addItems(["吸阻", "总通风率"])
        self.comboBox_37.addItems([""])
        self.comboBox_37.addItems(["吸阻", "总通风率"])

        # 图种类
        self.comboBox_17.addItems([""])
        self.comboBox_17.addItems(["箱线图", "散点图", "直方图"])
        # 加载月数据分析 指标
        self.comboBox_24.addItems([""])
        self.comboBox_24.addItems(init_com1)
        # 加载年度数据分析 指标
        self.comboBox_26.addItems([""])
        self.comboBox_26.addItems(init_com1)
        # 5、分指标独立样本t检验（任意选择不同两月数据比较分析）
        # 6、分指标散点图（加两条线，分别是标准的上下限），出个合格率
        # 7、分指标直方图、质量控制图（X-R）
        # 8、分指标年度z检验p值折线图、变异系数折线图、中位数及平均数折线图（就是横坐标为月，每月一个值的折线图）
        # 年度数据分析
        self.comboBox_25.addItems([""])
        self.comboBox_25.addItems(["分指标单样本t检验", "独立样本t检验", "分指标散点图", "分指标直方图"])

        self.comboBox_27.addItems([""])
        self.comboBox_27.addItems(["年度分指标质量控制图", "月度分指标质量控制图", "分指标年度z检验p值折线图", "分指标年度变异系数折线图", "分指标年度中位数折线图"])

        def look_for(path):
            list_all = []
            for file in os.listdir(path):
                files = os.path.join(path, file)
                list_all.append(files)
            total = {}
            for file in list_all:
                total[file] = {}
                for i in os.listdir(file):  # 2019
                    files = os.path.join(file, i)  # /2019
                    total[file][files] = {}
                    for m in os.listdir(files):  #
                        m = os.path.join(files, m)  # /2019/01/
                        total[file][files][m] = []
                        for k in os.listdir(m):
                            sp = os.path.join(m, k)
                            total[file][files][m].append(sp)
            return total

        self.path = r"数据及标准\数据"
        self.data = look_for(self.path)
        print("__" * 60)
        print(self.data)
        pingpai = []
        for key, value in self.data.items():
            pingpai.append(os.path.split(key)[-1])
        self.comboBox.addItems([""])
        self.comboBox.addItems(pingpai)
        self.comboBox_13.addItems([""])
        self.comboBox_13.addItems(pingpai)
        self.comboBox_23.addItems([""])
        self.comboBox_23.addItems(pingpai)
        self.comboBox_61.addItems([""])
        self.comboBox_61.addItems(pingpai)
        # 62 4
        self.comboBox_62.addItems([""])
        self.comboBox_62.addItems(pingpai)
        # 月数据分析左1
        self.comboBox_67.addItems([""])
        self.comboBox_67.addItems(pingpai)
        # 月数据分析左2
        self.comboBox_70.addItems([""])
        self.comboBox_70.addItems(pingpai)
        # 年度数据分析左2
        self.comboBox_71.addItems([""])
        self.comboBox_71.addItems(pingpai)

        print("初始化完毕")

    # pingpai 动#1
    def selectionchange(self, i):
        print("sd")
        try:
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_2.clear()
            self.comboBox_2.addItems([""])
            text = self.comboBox.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_2.addItems(nian1)
        except Exception as e:
            print(e)
            pass

    # 年动
    def selectionchange1(self, i):
        print("sdd")
        try:
            self.comboBox_3.clear()
            self.comboBox_3.addItems([""])
            pingpai = self.comboBox.currentText()
            nian = self.comboBox_2.currentText()
            text = self.comboBox.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_3.addItems(yue)
        except Exception as e:
            print(e)
            pass

    # 月动
    def selectionchange2(self, i):
        print("sddd")
        try:
            self.comboBox_4.clear()
            self.comboBox_4.addItems([""])
            pingpai = self.comboBox.currentText()
            nian = self.comboBox_2.currentText()
            text = self.comboBox.currentText()  # pingpai
            yue = self.comboBox_3.currentText()
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]
            ri = [os.path.split(i)[-1] for i in data3]
            self.comboBox_4.addItems(ri)
        except Exception as e:
            print(e)
            pass

    # ri动
    def selectionchange3(self, i):
        print("sdddd")
        try:
            self.comboBox_9.clear()
            self.comboBox_9.addItems([""])
            pingpai = self.comboBox.currentText()
            nian = self.comboBox_2.currentText()
            text = self.comboBox.currentText()  # pingpai
            yue = self.comboBox_3.currentText()
            ri = self.comboBox_4.currentText()

            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            num = len(load_data(path3))
            self.comboBox_9.addItems([str(i) for i in range(1, num + 1)])
        except Exception as e:
            print(e)
            pass

    # pingpai 动#2

    def selectionchange0(self, i):
        print("sd")
        try:
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_11.clear()
            self.comboBox_11.addItems([""])
            text = self.comboBox_13.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_11.addItems(nian1)
        except Exception as e:
            print(e)
            pass
        # 年动

    def selectionchange11(self, i):
        print("sdd")
        try:
            self.comboBox_12.clear()
            self.comboBox_12.addItems([""])
            pingpai = self.comboBox_13.currentText()
            nian = self.comboBox_11.currentText()
            text = self.comboBox_13.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_12.addItems(yue)
        except Exception as e:
            print(e)
            pass
        # 月动

    def selectionchange22(self, i):
        print("sddd")
        try:
            self.comboBox_14.clear()
            self.comboBox_14.addItems([""])
            pingpai = self.comboBox_13.currentText()
            nian = self.comboBox_11.currentText()
            text = self.comboBox_13.currentText()  # pingpai
            yue = self.comboBox_12.currentText()
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue
            data3 = self.data[path1][path2][path3]
            ri = [os.path.split(i)[-1] for i in data3]
            self.comboBox_14.addItems(ri)
        except Exception as e:
            print(e)
            pass
        # ri动

    def selectionchange33(self, i):
        print("sdddd")
        try:
            self.comboBox_15.clear()
            self.comboBox_15.addItems([""])
            pingpai = self.comboBox_13.currentText()
            nian = self.comboBox_11.currentText()
            text = self.comboBox_13.currentText()  # pingpai
            yue = self.comboBox_12.currentText()
            ri = self.comboBox_14.currentText()

            path3 = self.path + "\\" + pingpai + "\\" + nian + "\\" + yue + "\\" + ri

            def load_data(file_path):
                lines = []
                with open(file_path, "r", encoding="gbk") as f:
                    for i in f.readlines():
                        line = i.strip()
                        lines.append(line)

                index = []
                last = []
                for i in range(len(lines)):
                    if lines[i] == "g        mm       kPa     kPa     %      %      %      mm      %":
                        index.append(i)
                    try:
                        if lines[i][0] == "N":
                            last.append(i)
                    except:
                        pass
                p = list(zip(index, last))
                group = []
                for indexs in p:
                    total = {"wt": [], "circ": [], "PD": [], "CPD": [], "Vent": [], "PVnt": [], "TotV": [], "Len": [],
                             "DD": []}
                    for i in range(indexs[0] + 1, indexs[1]):
                        try:
                            total["wt"].append(float(lines[i].split()[1].strip("*")))
                            total["circ"].append(float(lines[i].split()[2].strip("*")))
                            total["PD"].append(float(lines[i].split()[3].strip("*")))
                            total["CPD"].append(float(lines[i].split()[4].strip("*")))
                            total["Vent"].append(float(lines[i].split()[5].strip("*")))
                            total["PVnt"].append(float(lines[i].split()[6].strip("*")))
                            total["TotV"].append(float(lines[i].split()[7].strip("*")))
                            total["Len"].append(float(lines[i].split()[8].strip("*")))
                            total["DD"].append(float(lines[i].split()[9].strip("*")))
                        except:
                            pass
                    group.append(total)  # 提取的全在group里面了
                return group

            num = len(load_data(path3))
            self.comboBox_15.addItems([str(i) for i in range(1, num + 1)])
        except Exception as e:
            print(e)
            pass

        # pingpai 动#3

    def selectionchange00(self, i):
        print("sd")
        try:
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_22.clear()
            self.comboBox_22.addItems([""])
            text = self.comboBox_23.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_22.addItems(nian1)
        except Exception as e:
            print(e)
            pass
        # 年动

    def selectionchange111(self, i):
        print("sdd")
        try:
            self.comboBox_19.clear()
            self.comboBox_19.addItems([""])
            pingpai = self.comboBox_23.currentText()
            nian = self.comboBox_22.currentText()
            text = self.comboBox_23.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_19.addItems(yue)
        except Exception as e:
            print(e)
            pass
        # 月动

    # pingpai 动#4

    def selectionchange000(self, i):
        print("sd")
        try:
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_59.clear()
            self.comboBox_59.addItems([""])
            text = self.comboBox_61.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_59.addItems(nian1)
        except Exception as e:
            print(e)
            pass
        # 年动

    def selectionchange1111(self, i):
        print("sdd")
        try:
            self.comboBox_60.clear()
            self.comboBox_60.addItems([""])
            pingpai = self.comboBox_61.currentText()
            nian = self.comboBox_59.currentText()
            text = self.comboBox_61.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_60.addItems(yue)
        except Exception as e:
            print(e)
            pass
        # 月动

    # pingpai 动#5

    def selectionchange0000(self, i):
        print("sd")
        try:
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_64.clear()
            self.comboBox_64.addItems([""])
            text = self.comboBox_62.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_64.addItems(nian1)
        except Exception as e:
            print(e)
            pass
        # 年动

    def selectionchange11111(self, i):
        print("sdd")
        try:
            self.comboBox_63.clear()
            self.comboBox_63.addItems([""])
            pingpai = self.comboBox_62.currentText()
            nian = self.comboBox_64.currentText()
            text = self.comboBox_62.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_63.addItems(yue)
        except Exception as e:
            print(e)
            pass
        # 月动

    # pingpai 动#5左边

    def selectionchange00000(self, i):
        print("sd")
        try:
            print(self.data)
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_65.clear()
            self.comboBox_65.addItems([""])
            text = self.comboBox_67.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_65.addItems(nian1)
        except Exception as e:
            print(e)
            pass
        # 年动

    def selectionchange111111(self, i):
        print("sdd")
        try:
            self.comboBox_66.clear()
            self.comboBox_66.addItems([""])
            pingpai = self.comboBox_67.currentText()
            nian = self.comboBox_65.currentText()
            text = self.comboBox_67.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_66.addItems(yue)
        except Exception as e:
            print(e)
            pass
        # 月动

    # pingpai 动#5右边

    def selectionchange000000(self, i):
        print("sd")
        try:
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_69.clear()
            self.comboBox_69.addItems([""])
            text = self.comboBox_70.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_69.addItems(nian1)
        except Exception as e:
            print(e)
            pass
        # 年动

    def selectionchange1111111(self, i):
        print("sdd")
        try:
            self.comboBox_68.clear()
            self.comboBox_68.addItems([""])
            pingpai = self.comboBox_70.currentText()
            nian = self.comboBox_69.currentText()
            text = self.comboBox_70.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_68.addItems(yue)
        except Exception as e:
            print(e)
            pass
        # 月动

    def selectionchange0000000(self, i):
        print("sd")
        try:
            # 标签用来显示选中的文本
            # currentText()：返回选中选项的文本
            self.comboBox_72.clear()
            self.comboBox_72.addItems([""])
            text = self.comboBox_71.currentText()  # pingpai
            path1 = self.path + "\\" + text
            data1 = self.data[path1]
            self.data1 = data1
            nian1 = []
            for key, value in data1.items():
                nian = os.path.split(key)[-1]
                nian1.append(nian)
            self.comboBox_72.addItems(nian1)
        except Exception as e:
            print(e)
            pass
        # 年动

    def selectionchange11111111(self, i):
        print("sdd")
        try:
            self.comboBox_73.clear()
            self.comboBox_73.addItems([""])
            pingpai = self.comboBox_71.currentText()
            nian = self.comboBox_72.currentText()
            text = self.comboBox_71.currentText()  # pingpai
            path1 = self.path + "\\" + text
            path2 = self.path + "\\" + pingpai + "\\" + nian
            self.data2 = self.data[path1][path2]
            yue = []
            for key, value in self.data2.items():
                nian = os.path.split(key)[-1]
                yue.append(nian)
            self.comboBox_73.addItems(yue)
        except Exception as e:
            print(e)
            pass
        # 月动


if __name__ == "__main__":
    # 创建QApplication 固定写法
    app = QApplication(sys.argv)
    # 实例化界面
    window = MainWindow1()
    # 显示界面
    window.show()
    # 阻塞，固定写法
    sys.exit(app.exec_())
