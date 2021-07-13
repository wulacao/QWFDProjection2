import re
import sys
import time
import os
import shutil
import matplotlib.pyplot as plt
from pylab import *
import pymysql
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider, QDialog, QPushButton
from PyQt5.QtCore import QDir, Qt, pyqtSlot
from concurrent.futures import ThreadPoolExecutor
from tools.danshexiangtou import Ui_MainWindow
from tools.whole_video import QmyelseWindow
# from renshujiankong import QmycountWindow
from tools.erro import QmyotherWindow
# from last import judge
mpl.rcParams['font.sans-serif'] = ['SimHei']
class QmythirdWindow(QMainWindow):
   def __init__(self, parent=None):
      super().__init__(parent)   #调用父类构 造函数，创建窗体
      self.ui=Ui_MainWindow()    #创建UI对象
      self.ui.setupUi(self)      #构造UI界面
      self.ui.comboBox.addItem('All')
      pic = QPixmap('pic_txt/biankaung.png')
      self.ui.label_22.setPixmap(pic)
      self.ui.label_22.setScaledContents(True)
      pic = QPixmap('pic_txt/biao_4.png')
      self.ui.label_5.setPixmap(pic)
      self.ui.label_5.setScaledContents(True)
      pic = QPixmap('pic_txt/zhenshu.png')
      self.ui.label_11.setPixmap(pic)
      pic = QPixmap('pic_txt/renshu.png')
      self.ui.label_17.setPixmap(pic)
      pic = QPixmap('pic_txt/zhixinsu.png')
      self.ui.label_10.setPixmap(pic)
      pic = QPixmap('pic_txt/jindu.png')
      self.ui.label_18.setPixmap(pic)
      pic = QPixmap('pic_txt/zhixindutiaozheng.png')
      self.ui.label_19.setPixmap(pic)
      pic = QPixmap('pic_txt/xiaoren.png')
      self.ui.label_20.setPixmap(pic)
      pic = QPixmap('pic_txt/weizhi.png')
      self.ui.label_21.setPixmap(pic)
      # pic = QPixmap('./pic_txt/camera_3.png')
      # self.ui.label_8.setPixmap(pic)
      # self.ui.label_8.setScaledContents(True)
      self.ui.comboBox.setEditable(True)
      self.ui.progressBar.setValue(0)
      self.ui.progressBar.setRange(0,100)
      # self.ui.textEdit.setText("0.5")
      self.ui.slider_1.setMinimum(1)
      self.ui.slider_1.setMaximum(9)
      self.ui.slider_1.setSingleStep(1)
      self.ui.slider_1.setValue(5)
      self.ui.slider_1.setTickPosition(QSlider.TicksAbove)
      self.ui.slider_1.setTickInterval(1)
      self.ui.slider_1.valueChanged.connect(self.change)
      self.ui.btnOpen.clicked.connect(self.btnOpenclicked)
      self.ui.btnPlay_2.clicked.connect(self.exit)
      self.ui.btnPlay.clicked.connect(self.videoplay)
      self.ui.btnOpen_2.clicked.connect(self.camera)
      self.ui.btnPlay_3.clicked.connect(self.pic_detection)
      # self.ui.pushButton.clicked.connect(self.process)
      self.ui.btnPlay_4.clicked.connect(self.picccc)
      self.ui.btnPlay_5.clicked.connect(self.move_pic)
   def move_pic(self):
       x = []
       y = []
       with open('pic_txt/all_frame', 'r') as f:
           x_aix = f.read()
       for i in range(int(x_aix)):
           x.append(i+1)
       with open('pic_txt/pic_cou.txt', 'r') as f:
           pic_count = f.read()
       pic_counts = re.findall(r'\d*',pic_count)
       # print(pic_counts)
       for i in range(len(pic_counts)):
           if pic_counts[i] !='':
               y.append(int(pic_counts[i]))
       # print(x,y)
       # plt.plot(x, y, 'ro-', color='#4169E1', alpha=0.8, linewidth=1, label='人数监控')
       # 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
       fig = plt.figure(figsize=(10, 5))
       # plt.style.use(['ggplot','dark_background'])
       plt.bar(x,y,label="人数监控", color="#87CEFA")
       for i in range(len(y)):
           plt.text(x[i],y[i],str(y[i]),ha='center')
       plt.legend(loc="upper right")
       plt.xlabel('frame')
       plt.ylabel('count')
       plt.show()
   def picccc(self):
       id = self.ui.comboBox.currentText()
       with open('pic_txt/pic_id.txt', 'w') as f:
           f.write(str(id))
       self.ui.label_8.setText('加载中请稍候......')
       QtWidgets.QApplication.processEvents()
       os.system('python ./img_detecte.py')
       pic = QPixmap(
           "./frame/" + str(1).zfill(5) + '.jpg') # str(n).zfill(5)设置保存图片文件名格式（5位）00001~ by XTX cv2.waitKey(1)
       self.ui.label_2.setPixmap(pic)
       self.ui.label_2.setScaledContents(True)
       QtWidgets.QApplication.processEvents()
       self.qssq(id)
   def qssq(self,id):
       with open('pic_txt/password.txt', 'r') as f:
           passworder = f.read()
       db = pymysql.connect(host='localhost',
                            user='root',
                            password=passworder,
                            database='test',
                            )
       cur = db.cursor()
       try:
           sql1 = 'select x_left from single_data where id=' + str(id) + ';'
           cur.execute(sql1)
           x_min = cur.fetchall()
           x_min = str(x_min)
           x_min = re.sub('\D', '', x_min)
           print('2')
           sql2 = 'select x_right from single_data where id=' + str(id) + ';'
           cur.execute(sql2)
           x_max = cur.fetchall()
           x_max = str(x_max)
           x_max = re.sub('\D', '', x_max)
           sql3 = 'select y_left from single_data where id=' + str(id) + ';'
           cur.execute(sql3)
           y_min = cur.fetchall()
           y_min = str(y_min)
           y_min = re.sub('\D', '', y_min)
           sql4 = 'select y_right from single_data where id=' + str(id) + ';'
           cur.execute(sql4)
           y_max = cur.fetchall()
           y_max = str(y_max)
           y_max = re.sub('\D', '', y_max)
           sql = 'select conf from single_data where id=' + str(id) + ';'
           cur.execute(sql)
           conf = cur.fetchall()
           conf = str(conf)
           conf = re.findall(r'\d+.?\d*', conf)[0]
           print(x_max, x_min, y_max, y_min, conf)
           self.ui.textEdit.setText(str(conf))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_3.setText(str(x_max))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_5.setText(str(y_max))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_6.setText(str(x_min))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_7.setText(str(y_min))
           QtWidgets.QApplication.processEvents()
       except:
           x_min = 0
           y_min = 0
           x_max = 0
           y_max = 0
           conf = 0.5
           self.ui.textEdit.setText(str(conf))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_3.setText(str(x_max))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_5.setText(str(y_max))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_6.setText(str(x_min))
           QtWidgets.QApplication.processEvents()
           self.ui.lineEdit_7.setText(str(y_min))
           QtWidgets.QApplication.processEvents()
       db.close()
   def process(self):
       print('start~')
       with open('pic_txt/all_frame', 'r') as f:
           all = f.read()
       all = int(all)
       print(all)
       # while True:
       with open('pic_txt/fraame.txt', 'r') as f:
           a = f.read()
       a = int(a)
       print(a)
       v = int((a/all)*100)
       if v == 0:
           v = 1
       for i in range(v):
           self.ui.progressBar.setValue(i)
   def pic_detection(self):
       self.ui.comboBox.clear()
       self.ui.comboBox.addItem('All')
       curPath = QDir.currentPath()  # 获取系统当前目录
       title = "选择图片文件"
       filt = "图片文件(*.png *.jpg *.jpeg);;所有文件(*.*)"
       fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
       if (fileName == ""):
           return
       self.ui.else_2.setText("wait")
       self.ui.label_8.setText('加载中请稍候......')
       QtWidgets.QApplication.processEvents()
       with open('pic_txt/pic_road', 'w') as f:
           f.write(fileName)
       id = self.ui.comboBox.currentText()
       with open('pic_txt/pic_id.txt', 'w') as f:
           f.write(str(id))
       os.system('python ./img_detecte.py')
       with open('pic_txt/flag.txt', 'r') as f:
           signal = f.read()
       print(signal)
       if signal == '0':
           # print('1')
           self.dialog()
       with open('pic_txt/flag.txt', 'w') as f:
           f.write('1')
       with open('pic_txt/count.txt', 'r') as f:
           count = f.read()
       self.ui.textEdit_2.setText(count)
       QtWidgets.QApplication.processEvents()
       pic = QPixmap(
           "./frame/" + str(1).zfill(5) + '.jpg')  # str(n).zfill(5)设置保存图片文件名格式（5位）00001~ by XTX cv2.waitKey(1)
       self.ui.label_2.setPixmap(pic)
       self.ui.label_2.setScaledContents(True)
       QtWidgets.QApplication.processEvents()
       with open('pic_txt/single_id.txt', 'r') as f:
           single_id = f.read()
       id = int(single_id)
       for i in range(id):
           self.ui.comboBox.addItem(str(i+1))
   def dialog(self):
       formTable = QmyotherWindow(self)
       formTable.setAttribute(Qt.WA_DeleteOnClose)
       formTable.setWindowTitle('警告')
       formTable.show()
   def change(self):
       data = self.ui.slider_1.value()
       data = data/10
       data = str(data)
       with open('pic_txt/confidence.txt', 'w') as f:
           f.write(data)
       self.ui.label_7.setText(data)
   def exit(self):
        sys.exit()
   def camera(self):
       with open('pic_txt/multiple_road.txt', 'w') as f:
           f.write('')
       os.system("start /B python ./mainz1_.py &")
       self.ui.else_2.setText("wait")
       self.ui.label_8.setText('加载中请稍候......')
       QtWidgets.QApplication.processEvents()
       time.sleep(2)
       print('ok')
       while True:
           time.sleep(0.08)
           with open("pic_txt/fraame.txt", "r") as f:  # 打开文件
               frame1 = f.read()  # 读取文件
           frame1 = str(frame1)
           with open('pic_txt/count.txt', 'r') as f:
               count = f.read()
           self.ui.textEdit_2.setText(count)
           pic = QPixmap(
               "./frame/" + str(frame1).zfill(5) + '.jpg')  # str(n).zfill(5)设置保存图片文件名格式（5位）00001~ by XTX cv2.waitKey(1)
           self.ui.label_2.setPixmap(pic)
           self.ui.label_2.setScaledContents(True)
           QtWidgets.QApplication.processEvents()
           self.ui.else_2.setText("第" + frame1 + "帧")
           print('over')
   def videoplay(self):
      formTable = QmyelseWindow(self)
      formTable.setAttribute(Qt.WA_DeleteOnClose)
      formTable.setWindowTitle('完整视频')
      formTable.show()
   def btnOpenclicked(self):
      curPath = QDir.currentPath()  # 获取系统当前目录
      title = "选择视频文件"
      filt = "视频文件(*.wmv *.avi *.mp4 *.webm);;所有文件(*.*)"
      fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
      if (fileName == ""):
         return
      file = 'pic_txt/multiple_road.txt'
      with open(file, 'w') as file_object:
         file_object.write(str(fileName))
      os.system('start /B python ./mainz1_.py')
      self.ui.else_2.setText("wait")
      self.ui.label_8.setText('加载中请稍候......')
      QtWidgets.QApplication.processEvents()
      time.sleep(5)
      print('ok')
      flag = 1
      while True:
        time.sleep(0.08)
        with open("pic_txt/fraame.txt", "r") as f:  # 打开文件
            frame1 = f.read()  # 读取文件
        # if int(frame1) != frame_pic[-1]:
        #     frame_pic.append(int(frame1))
        # v = int(frame1)/all
        # self.ui.progressBar.setValue(v)
        # frame1 = str(frame1)
        if frame1 == 'a':
            self.ui.else_2.setText("检测完毕")
            for i in range(1,101):
                self.ui.progressBar.setValue(i)
            break
        with open('pic_txt/count.txt', 'r') as f:
            count = f.read()
        # if int(count) != count_pic[-1]:
        #     count_pic.append(int(count))
        self.ui.textEdit_2.setText(count)
        pic = QPixmap("./frame/" + str(frame1).zfill(5) + '.jpg')  # str(n).zfill(5)设置保存图片文件名格式（5位）00001~ by XTX cv2.waitKey(1)
        self.ui.label_2.setPixmap(pic)
        self.ui.label_2.setScaledContents(True)
        QtWidgets.QApplication.processEvents()
        self.ui.else_2.setText("第"+frame1+"帧")
        print(count)
        if flag == 1:
            for j in range(1,int(count)+1):
                self.ui.comboBox.addItem(str(j))
        print('over')
        flag = 2
        id1 = self.ui.comboBox.currentText()
        print('1')
        with open('pic_txt/flag.txt', 'r') as f:
            signal = f.read()
        # print(signal)
        if signal == '0':
            # print('1')
            self.dialog()
        with open('pic_txt/flag.txt', 'w') as f:
            f.write('1')
        # print(frame_pic,count_pic)
        self.sqqs(id1,frame1)
        self.process()
      with open('pic_txt/fraame.txt', 'w') as f:
          f.write('1')
      with open('pic_txt/confidence.txt', 'w') as f:
          f.write('0.5')
      with open('pic_txt/multiple_road.txt', 'w') as f:
          f.write('')
      # with open('list.txt','w') as f:
      #     f.write(count_pic)

      # judge()
      
      shutil.rmtree('frame')
      os.mkdir('frame')
      print('ll')
   def sqqs(self,id1,frame1):
        with open('pic_txt/password.txt', 'r') as f:
            passworder = f.read()
        # try:
        db = pymysql.connect(host='localhost',
                            user='root',
                            password=passworder,
                            database='test',
                            )
        cur = db.cursor()

        try:
            sql1 = 'select x_left from person_data where id=' + id1 + ' and frame=' + frame1 + ';'
            cur.execute(sql1)
            x_min = cur.fetchall()
            x_min = str(x_min)
            x_min = re.sub('\D', '', x_min)
            print('2')
            sql2 = 'select x_right from person_data where id=' + id1 + ' and frame=' + frame1 + ';'
            cur.execute(sql2)
            x_max = cur.fetchall()
            x_max = str(x_max)
            x_max = re.sub('\D', '', x_max)
            # print('1')
            sql3 = 'select y_left from person_data where id=' + id1 + ' and frame=' + frame1 + ';'
            cur.execute(sql3)
            y_min = cur.fetchall()
            y_min = str(y_min)
            y_min = re.sub('\D', '', y_min)
            # print('2')
            sql4 = 'select x_right from person_data where id=' + id1 + ' and frame=' + frame1 + ';'
            cur.execute(sql4)
            y_max = cur.fetchall()
            y_max = str(y_max)
            y_max = re.sub('\D', '', y_max)
            # print('3')
            sql = 'select conf from person_data where id=' + id1 + ' and frame=' + frame1 + ';'
            cur.execute(sql)
            conf = cur.fetchall()
            conf = str(conf)
            # print("4")
            conf = re.findall(r'\d+.?\d*',conf)[0]
            # print('4')
            print(x_max,x_min,y_max,y_min,conf)
            # print('3')
            self.ui.textEdit.setText(str(conf))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_3.setText(str(x_max))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_5.setText(str(y_max))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_6.setText(str(x_min))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_7.setText(str(y_min))
            QtWidgets.QApplication.processEvents()
            # print('4')
        except:
            x_min = 0
            x_max = 0
            y_min = 0
            y_max = 0
            conf = 0.5
            self.ui.textEdit.setText(str(conf))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_3.setText(str(x_max))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_5.setText(str(y_max))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_6.setText(str(x_min))
            QtWidgets.QApplication.processEvents()
            self.ui.lineEdit_7.setText(str(y_min))
            QtWidgets.QApplication.processEvents()
        db.close()




if  __name__ == "__main__":        #用于当前窗体测试
   app = QApplication(sys.argv)    #创建GUI应用程序
   form=QmythirdWindow()            #创建窗体
   form.show()
   sys.exit(app.exec_())
