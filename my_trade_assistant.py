import os
import sys
import time
import configparser
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QDesktopWidget,
                             QLineEdit, QToolTip, QPushButton, QRadioButton,
                             QCheckBox, QComboBox, QLabel, qApp, QLCDNumber,
                             QMessageBox, QDialog)


class CWind(QMainWindow):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.init_timer()

        rec_text = cur_time() + ' 开启交易助手！'
        self.statusBar().showMessage(rec_text)
        my_operating_record(rec_text)

    def initUI(self):
        self.setFixedSize(300, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.center()
        self.setWindowTitle('交易助手')
        self.setWindowIcon(QIcon('myIcon.ico'))
        QToolTip.setFont(QFont('微软雅黑', 10))

        # 以下设置菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('设置')

        self.settingAct = QAction(QIcon('setting.png'), '设置交易环境', self)
        self.settingAct.setShortcut('Ctrl+P')

        aboutAct = QAction(QIcon('contact.png'), '联系我们', self)
        aboutAct.setShortcut('Ctrl+A')
        aboutAct.triggered.connect(self.about)

        exitAct = QAction(QIcon('exit.png'), '退出', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)

        fileMenu.addAction(self.settingAct)
        fileMenu.addAction(aboutAct)
        fileMenu.addAction(exitAct)

        # LCD时钟
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(5)
        self.lcd.setMode(QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%X", time.localtime()))
        self.lcd.resize(200, 66)
        self.lcd.move(50, 170)

        # 以下布局窗口各个控件

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
        self.combo2.setCurrentText(symbols[1])
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


class CDialog(QDialog):
    """
    配置文件对话框窗口
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.center()

    def initUI(self):
        self.setFixedSize(360, 220)
        self.setWindowTitle('设置交易环境相关变量')
        self.setWindowIcon(QIcon('myIcon.ico'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        lbl1 = QLabel('您的MT4账号：', self)
        lbl1.move(30, 30)

        self.qle_number = QLineEdit(self)
        self.qle_number.resize(90, 25)
        self.qle_number.move(140, 25)

        self.rb11 = QRadioButton('在本地交易', self)
        self.rb11.move(30, 70)
        self.rb11.setChecked(True)
        self.rb11.toggled.connect(self.rb_toggled)

        self.rb12 = QRadioButton('在服务器上交易', self)
        self.rb12.move(160, 70)
        self.rb12.toggled.connect(self.rb_toggled)

        self.lbl2 = QLabel('在下面输入MT4的Files文件夹路径：', self)
        self.lbl2.move(30, 105)

        self.qle_directory = QLineEdit(self)
        self.qle_directory.resize(300, 25)
        self.qle_directory.move(30, 140)

        btn_save = QPushButton('保存', self)
        btn_save.move(60, 180)
        btn_save.clicked.connect(self.save_environment)

        btn_cancel = QPushButton('取消', self)
        btn_cancel.move(180, 180)
        btn_cancel.clicked.connect(self.close)

    def rb_toggled(self):
        if self.rb11.isChecked():
            self.lbl2.setText('在下面输入MT4的Files文件夹路径：')
        elif self.rb12.isChecked():
            self.lbl2.setText('在下面输入服务器的IP地址和端口：')

    def save_environment(self):
        """
        设置交易环境，可以是本地的MT4的Files文件夹路径，也可以是服务器IP地址加端口
        """
        if len(self.qle_number.text()) > 0 and len(self.qle_directory.text()) > 0:
            config = configparser.ConfigParser()

            config['MT4'] = {'account_number': self.qle_number.text()}

            if self.rb11.isChecked():
                cur_mode = 'Local'
            elif self.rb12.isChecked():
                cur_mode = 'Network'
            config['Pathway'] = {'mode': cur_mode}

            dir_str = self.qle_directory.text()

            if cur_mode == 'Local':
                config['Local'] = {'directory': dir_str}

            elif cur_mode == 'Network':
                host = dir_str[: dir_str.find(':')]
                port = dir_str[dir_str.find(':') + 1:]
                config['Network'] = {'host': host,
                                     'port': port}

            with open('setting.cfg', 'w') as file_object:
                config.write(file_object)

        self.close()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + 85,
                  (screen.height() - size.height()) - 180)


def cur_time():
    """
    获取当前时间，返回字符串
    """
    now = time.localtime()
    cur_time = time.strftime('%H:%M:%S', now)
    return cur_time


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
    # 从配置文件setting.cfg中读取MT4路径
    symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']
    for symbol in symbols:
        if inp_text.find(symbol) >= 0:
            trade_symbol = symbol

    config = configparser.ConfigParser()
    config.read('setting.cfg')
    res_config = read_config()
    mode = res_config[1]

    if mode == 'Local':
        file_path = res_config[2]
        # 检查交易品种的子文件夹是否存在，不存在就新建相应的子文件夹
        if os.path.exists(file_path + '\\' + trade_symbol) == False:
            os.mkdir(file_path + '\\' + trade_symbol)

        file_path = file_path + '\\' + trade_symbol + '\\'

        # 将指令存到对应的子文件夹里
        file_name = file_path + 'trade_signal.txt'

        with open(file_name, 'w') as file_object:
            file_object.write(inp_text)

    elif mode == 'Network':
        # account_number = res_config[0]
        # host = res_config[2]
        # port = res_config[3]

        # 将交易指令发送到服务器上
        pass


def read_config():
    """
    启动主程序时，读取交易环境的配置文件,返回MT4账户和IP地址或文件夹
    """
    config = configparser.ConfigParser()
    config.read('setting.cfg')

    account_number = config.get('MT4', 'account_number')
    mode = config.get('Pathway', 'mode')

    if config.get('Pathway', 'mode') == 'Local':
        directory = config.get('Local', 'directory')
        return account_number, mode, directory

    elif config.get('Pathway', 'mode') == 'Network':
        host = config.get('Network', 'host')
        port = config.get('Network', 'port')
        return account_number, mode, host, port


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = CWind()
    d = CDialog()

    sub_menu = w.settingAct
    # 打开交易环境配置窗口
    sub_menu.triggered.connect(d.show)

    if os.path.isfile('setting.cfg') == False:
        d.show()

    sys.exit(app.exec_())

