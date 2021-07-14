import re
import shutil
import sys
import time
import os

import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QSlider
from PyQt5.QtCore import QDir, Qt, pyqtSlot
from concurrent.futures import ThreadPoolExecutor
from tools.duoshexiangtou import Ui_MainWindow
from tools.whole_video import QmyelseWindow
class QmyforthWindow(QMainWindow):
   def __init__(self, parent=None):
      super().__init__(parent)   #调用父类构 造函数，创建窗体
      self.ui=Ui_MainWindow()    #创建UI对象
      self.ui.setupUi(self)      #构造UI界面
      self.ui.comboBox_2.addItem('选择')
      self.ui.comboBox_2.addItem('Path1')
      self.ui.comboBox_2.addItem('Path2')
      self.ui.comboBox_2.addItem('Path3')
      self.ui.comboBox_2.addItem('Path4')
      self.ui.comboBox_2.addItem('Path5')
      self.ui.comboBox_2.addItem('Path6')
      self.ui.comboBox_2.addItem('Path7')
      self.ui.comboBox.addItem('All')
      self.ui.comboBox_2.currentIndexChanged.connect(self.writeline_by_line)
      self.ui.slider_1.setMinimum(1)
      self.ui.slider_1.setMaximum(9)
      self.ui.slider_1.setSingleStep(1)
      self.ui.slider_1.setValue(5)
      self.ui.slider_1.setTickPosition(QSlider.TicksAbove)
      self.ui.slider_1.setTickInterval(1)
      self.ui.slider_1.valueChanged.connect(self.change)
      self.ui.progressBar.setValue(0)
      self.ui.progressBar.setRange(0,100)
      pic = QPixmap('pic_txt/biankaung.png')
      self.ui.label_22.setPixmap(pic)
      self.ui.label_22.setScaledContents(True)
      pic = QPixmap('pic_txt/biao_4.png')
      self.ui.label_8.setPixmap(pic)
      self.ui.label_8.setScaledContents(True)
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
      self.ui.comboBox.setEditable(True)
      self.ui.btnOpen_2.clicked.connect(self.btnOpenclicked)
      self.ui.btnPlay_2.clicked.connect(self.exit)
      self.ui.btnPlay.clicked.connect(self.videoplay)
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
       for i in range(v):
           self.ui.progressBar.setValue(i)
   def change(self):
       data = self.ui.slider_1.value()
       data = data / 10
       data = str(data)
       with open('pic_txt/confidence.txt', 'w') as f:
           f.write(data)
       self.ui.label_7.setText(data)
   def exit(self):
       sys.exit()
   def writeline_by_line(self,count):
       curPath = QDir.currentPath()  # 获取系统当前目录
       title = "选择视频文件"
       filt = "视频文件(*.wmv *.avi *.mp4 *.webm);;所有文件(*.*)"
       fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
       if (fileName == ""):
           return
       filename = 'pic_txt/multiple_road.txt'
       with open(filename,'a') as f:
           f.write(fileName+'\n')

   def videoplay(self):
      formTable = QmyelseWindow(self)
      formTable.setAttribute(Qt.WA_DeleteOnClose)
      formTable.setWindowTitle('完整视频')
      formTable.show()
   def writefile(self):
      data = self.ui.zxdedit.text()
      filename = 'pic_txt/confidence.txt'
      with open(filename, 'w') as file_object:
         file_object.write(str(data))
      with open("pic_txt/confidence.txt", "r") as f:  # 打开文件
         data = f.read()  # 读取文件
      self.ui.textEdit.setText("["+str(data)+",1.0)")

   def btnOpenclicked(self):
      os.system("start /B python ./mainz1_.py")
      self.ui.else_2.setText("wait")
      self.ui.label_88.setText('加载中请稍候......')
      QtWidgets.QApplication.processEvents()
      time.sleep(2)
      print('ok')
      flag = 1
      while True:
        time.sleep(0.08)
        with open("pic_txt/fraame.txt", "r") as f:  # 打开文件
            frame1 = f.read()  # 读取文件
        if frame1 == 'a':
            self.ui.else_2.setText("检测完毕")
            break
        with open('pic_txt/count.txt', 'r') as f:
            count = f.read()
        self.ui.textEdit_2.setText(count)
        pic = QPixmap("./frame/" + str(frame1).zfill(5) + '.jpg')  # str(n).zfill(5)设置保存图片文件名格式（5位）00001~ by XTX cv2.waitKey(1)
        self.ui.label_2.setPixmap(pic)
        self.ui.label_2.setScaledContents(True)
        QtWidgets.QApplication.processEvents()
        self.ui.else_2.setText("第"+frame1+"帧")
        if flag == 1:
            for j in range(1,int(count)+1):
                self.ui.comboBox.addItem(str(j))
        flag = 2
        id1 = self.ui.comboBox.currentText()
        self.sqqs(id1,frame1)
        self.process()
        print('over')
      print('ll')
      with open('pic_txt/fraame.txt', 'w') as f:
          f.write('1')
      with open("pic_txt/multiple_road.txt", 'w') as f:
          f.write('')
      with open('pic_txt/confidence.txt', 'w') as f:
          f.write('0.5')
      with open('pic_txt/count.txt', 'w') as f:
          f.write('0')
      # shutil.rmtree('frame')
      # os.mkdir('frame')
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
           conf = re.findall(r'\d+.?\d*', conf)[0]
           # print('4')
           print(x_max, x_min, y_max, y_min, conf)
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
   form=QmyforthWindow()            #创建窗体
   form.show()
   sys.exit(app.exec_())

