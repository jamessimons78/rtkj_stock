import os
import sys
import time
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication,
                             QInputDialog, QToolTip, QPushButton, QMessageBox,
                             QCheckBox, QComboBox, QLabel, QDesktopWidget, qApp,
                             QLCDNumber, QRadioButton)


class Wind(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_timer()

        rec_text = cur_time() + ' 开启交易助手！'
        self.statusBar().showMessage(rec_text)
        my_operating_record(rec_text)
        if os.path.isfile('setting.ini') == False:
            self.setting_environment()

    def initUI(self):
        self.setFixedSize(300, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.center()
        self.setWindowTitle('交易助手')
        self.setWindowIcon(QIcon('myIcon.ico'))
        QToolTip.setFont(QFont('微软雅黑', 10))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('设置')

        settingAct = QAction(QIcon('setting.png'), '设置交易环境', self)
        settingAct.setShortcut('Ctrl+P')
        settingAct.triggered.connect(self.setting_environment)

        aboutAct = QAction(QIcon('contact.png'), '联系我们', self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.triggered.connect(self.about)

        exitAct = QAction(QIcon('exit.png'), '退出', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        fileMenu.addAction(settingAct)
        fileMenu.addAction(aboutAct)
        fileMenu.addAction(exitAct)

        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(5)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%X", time.localtime()))
        self.lcd.resize(200, 66)
        self.lcd.move(50, 170)

        symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']

        lab1 = QLabel('交易品种 (1)', self)
        lab1.move(20, 72)

        self.combo1 = QComboBox(self)
        for symbol in symbols:
            self.combo1.addItem(symbol)
        self.combo1.move(20, 102)

        self.cb_buy1 = QCheckBox('做多', self)
        self.cb_buy1.move(140, 75)
        self.cb_buy1.toggle()
        self.cb_buy1.setChecked(False)

        self.cb_sell1 = QCheckBox('做空', self)
        self.cb_sell1.move(140, 105)
        self.cb_sell1.toggle()
        self.cb_sell1.setChecked(False)

        btn_open1 = QPushButton('挂单/直开', self)
        btn_open1.setToolTip('挂单或者当前市价开仓')
        btn_open1.resize(85, 25)
        btn_open1.move(200, 75)
        btn_open1.clicked.connect(self.btn_open1_Clicked)

        btn_close1 = QPushButton('撤单/平仓', self)
        btn_close1.setToolTip('撤销挂单或平掉已有仓位')
        btn_close1.resize(85, 25)
        btn_close1.move(200, 105)
        btn_close1.clicked.connect(self.btn_close1_Clicked)

        lab2 = QLabel('交易品种 (2)', self)
        lab2.move(20, 257)

        self.combo2 = QComboBox(self)
        for symbol in symbols:
            self.combo2.addItem(symbol)
        self.combo2.setCurrentText(self.combo2.itemText(1))
        self.combo2.move(20, 287)

        self.cb_buy2 = QCheckBox('做多', self)
        self.cb_buy2.move(140, 260)
        self.cb_buy2.toggle()
        self.cb_buy2.setChecked(False)

        self.cb_sell2 = QCheckBox('做空', self)
        self.cb_sell2.move(140, 290)
        self.cb_sell2.toggle()
        self.cb_sell2.setChecked(False)

        btn_open2 = QPushButton('挂单/直开', self)
        btn_open2.setToolTip('挂单或者当前市价开仓')
        btn_open2.resize(85, 25)
        btn_open2.move(200, 260)
        btn_open2.clicked.connect(self.btn_open2_Clicked)

        btn_close2 = QPushButton('撤单/平仓', self)
        btn_close2.setToolTip('撤销挂单或平掉已有仓位')
        btn_close2.resize(85, 25)
        btn_close2.move(200, 290)
        btn_close2.clicked.connect(self.btn_close2_Clicked)

        lbl3 = QLabel('单笔止损：%', self)
        lbl3.move(20, 335)
        self.rb11 = QRadioButton('0.5', self)
        self.rb11.move(115, 335)
        self.rb11.setChecked(True)
        self.rb12 = QRadioButton('1.0', self)
        self.rb12.move(175, 335)
        self.rb13 = QRadioButton('2.0', self)
        self.rb13.move(235, 335)

        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + 90,
                  (screen.height() - size.height() - 90))

    def init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.update_time)

    def update_time(self):
        self.lcd.display(time.strftime("%X", time.localtime()))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '操作提示！',
                                     '您确定要关闭“交易助手”？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            rec_text = cur_time() + ' 关闭交易助手！'
            my_operating_record(rec_text)
            event.accept()
        else:
            event.ignore()

    def about(self):
        """
        关于菜单
        """
        QMessageBox.information(self, '联系我们!',
                                self.tr('微信：zyhj518，手机：13770675275。'))

    def setting_environment(self):
        """
        设置交易环境，可以是本地的MT4的Files文件夹路径，也可以是服务器IP地址加端口
        """
        result, ok = QInputDialog.getText(self, '配置环境',
                                        '输入MT4的Files文件夹路径，或IP地址和端口')
        result = str(result)

        if ok:
            if result.find('MetaQuotes') >= 0 or result.find(':') >= 0:
                with open('setting.ini', 'w') as file_object:
                    file_object.write(result)
                rec_text = cur_time() + ' 交易环境已经设置成功！'
                self.statusBar().showMessage(rec_text)
                my_operating_record(rec_text)
            else:
                QMessageBox.information(self, '错误提示!',
                                        self.tr('输入的文件夹不对，或IP地址和端口格式不对!'))
                rec_text = cur_time() + ' 输入的文件夹不对，或IP地址和端口格式不对!！'
                self.statusBar().showMessage(rec_text)
                my_operating_record(rec_text)


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.showMinimized()

    def btn_open1_Clicked(self):
        """
        挂单或直接市价开仓操作
        """
        if self.cb_buy1.isChecked() or self.cb_sell1.isChecked():
            signal_text = self.combo1.currentText()
            if self.cb_buy1.isChecked():
                signal_text += 'BUY'
            if self.cb_sell1.isChecked():
                signal_text += 'SELL'
            if self.rb12.isChecked():
                signal_text += '1'
            elif self.rb13.isChecked():
                signal_text += '2'

            my_send_signal(signal_text)

            rec_text = cur_time() + ' 执行' + signal_text + '操作'
            self.statusBar().showMessage(rec_text)
            my_operating_record(rec_text)
        else:
            QMessageBox.information(self, '错误提示!',
                                    self.tr('请勾选交易方向后，再开仓!'))


    def btn_close1_Clicked(self):
        """
        撤销挂单，或平掉已有仓位
        """
        signal_text = self.combo1.currentText() + 'CLOSE'

        my_send_signal(signal_text)
        rec_text = cur_time() + ' 执行' + signal_text + '操作'
        self.statusBar().showMessage(rec_text)
        my_operating_record(rec_text)


    def btn_open2_Clicked(self):
        """
        挂单或直接市价开仓操作
        """
        if self.cb_buy2.isChecked() or self.cb_sell2.isChecked():
            signal_text = self.combo2.currentText()
            if self.cb_buy2.isChecked():
                signal_text += 'BUY'
            if self.cb_sell2.isChecked():
                signal_text += 'SELL'
            if self.rb12.isChecked():
                signal_text += '1'
            elif self.rb13.isChecked():
                signal_text += '2'

            my_send_signal(signal_text)

            rec_text = cur_time() + ' 执行' + signal_text + '操作'
            self.statusBar().showMessage(rec_text)
            my_operating_record(rec_text)
        else:
            QMessageBox.information(self, '错误提示!',
                                    self.tr('请勾选交易方向后，再开仓!'))


    def btn_close2_Clicked(self):
        """
        撤销挂单，或平掉已有仓位
        """
        signal_text = self.combo2.currentText() + 'CLOSE'

        my_send_signal(signal_text)
        rec_text = cur_time() + ' 执行' + signal_text + '操作'
        self.statusBar().showMessage(rec_text)
        my_operating_record(rec_text)


def my_operating_record(inp_text):
    """
    记录操作日志
    """
    now = time.localtime()
    file_name = time.strftime('%Y-%m-%d', now) + '.txt'
    rec_text = time.strftime('%Y-%m-%d', now) + ' ' + inp_text + '\n'

    with open(file_name, 'a+', encoding='UTF-8') as file_object:
        file_object.write(rec_text)


def my_send_signal(inp_text):
    # 从配置文件setting.ini中读取MT4路径
    with open('setting.ini', 'r') as file_object:
        file_path = file_object.read()

    symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']
    for symbol in symbols:
        if inp_text.find(symbol) >= 0:
            trade_symbol = symbol

    # 检查交易品种的子文件夹是否存在，不存在就新建相应的子文件夹
    if os.path.exists(file_path + '\\' + trade_symbol) == False:
        os.mkdir(file_path + '\\' + trade_symbol)

    file_path = file_path + '\\' + trade_symbol + '\\'

    # 将指令存到对应的子文件夹里
    file_name = file_path + 'trade_signal.txt'

    with open(file_name, 'w') as file_object:
        file_object.write(inp_text)


def cur_time():
    """
    获取当前时间，返回字符串
    """
    now = time.localtime()
    cur_time = time.strftime('%H:%M:%S', now)
    return cur_time


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = Wind()

    sys.exit(app.exec_())

