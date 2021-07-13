import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtCore import pyqtSlot,Qt
from danshexiang import QmythirdWindow
from duoshexiang import QmyforthWindow
from tools.zhujiemian import Ui_MainWindow
from tools.guanyuruan import QmytreeWindow
class QmyMainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        pic = QPixmap('pic_txt/ppfj.jpg')
        self.ui.label.setPixmap(pic)
        self.ui.label.setScaledContents(True)
        pic = QPixmap('pic_txt/dz.jpg')
        self.ui.label_2.setPixmap(pic)
        self.ui.label_2.setScaledContents(True)
        self.ui.pushButton.clicked.connect(self.password)
    def password(self):
        password = self.ui.lineEdit.text()
        with open('pic_txt/password.txt', 'w') as f:
            f.write(password)
        self.ui.lineEdit.setText('输入成功')
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        formTable = QmythirdWindow(self)
        formTable.setAttribute(Qt.WA_DeleteOnClose)
        formTable.setWindowTitle('单镜头')
        formTable.show()
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        formTable = QmyforthWindow(self)
        formTable.setAttribute(Qt.WA_DeleteOnClose)
        formTable.setWindowTitle('多镜头')
        formTable.show()
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        formTable = QmytreeWindow(self)
        formTable.setAttribute(Qt.WA_DeleteOnClose)
        formTable.setWindowTitle('关于软件')
        formTable.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = QmyMainWindow()
    m.show()
    sys.exit(app.exec_())

