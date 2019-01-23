import os
import re
import sys
import time
import configparser
from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtCore import (Qt, QTimer, QRegExp, QByteArray, QDataStream, QIODevice)
from PyQt5.QtGui import (QIcon, QFont, QRegExpValidator)
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QDesktopWidget,
                             QLineEdit, QToolTip, QPushButton, QRadioButton,
                             QCheckBox, QComboBox, QLabel, qApp, QLCDNumber,
                             QMessageBox, QDialog)

SIZEOF_UINT16 = 2

class CWind(QMainWindow):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()
        self._initUI()
        self.my_init_timer()

        self.socket = QTcpSocket()
        self.nextBlockSize = 0
        self.request = None

        self.socket.connected.connect(self.my_sendRequest)
        self.socket.readyRead.connect(self.my_readResponse)
        self.socket.disconnected.connect(self.my_serverHasStopped)
        self.socket.error.connect(self.my_serverHasError)

        # 若已有交易环境配置文件，则打开并读到self.config变量中
        self.config = ()
        if os.path.isfile('setting.cfg') == True:
            self.config = self.my_read_config()
            self.my_update_atr()

        # 状态栏显示启动信息，并存入日志文件
        rec_text = my_cur_time() + ' 开启交易助手！'
        self.statusBar().showMessage(rec_text)
        my_operating_record(rec_text)

    def _initUI(self):
        self.setFixedSize(300, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.my_center()
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
        aboutAct.triggered.connect(self._about)

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

        self.lab0 = QLabel('', self)
        font0 = QFont()
        font0.setFamily("微软雅黑")
        font0.setPointSize(9)
        font0.setBold(True)
        self.lab0.setFont(font0)
        self.lab0.setStyleSheet('color: rgb(0, 0, 127)')
        self.lab0.resize(288, 20)
        self.lab0.move(5, 36)

        symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']

        lab1 = QLabel('交易品种 (1)', self)
        lab1.move(20, 72)

        self.combo1 = QComboBox(self)
        for symbol in symbols:
            self.combo1.addItem(symbol)
        self.combo1.move(20, 102)
        font12 = QFont()
        font12.setBold(True)
        self.combo1.setFont(font12)

        self.cb_buy1 = QCheckBox('做多', self)
        self.cb_buy1.move(140, 75)
        self.cb_buy1.toggle()
        self.cb_buy1.setChecked(False)

        self.cb_sell1 = QCheckBox('做空', self)
        self.cb_sell1.move(140, 105)
        self.cb_sell1.toggle()
        self.cb_sell1.setChecked(False)

        self.btn_open1 = QPushButton('挂单/直开', self)
        self.btn_open1.setToolTip('挂单或者当前市价开仓')
        self.btn_open1.resize(85, 25)
        self.btn_open1.move(200, 75)
        self.btn_open1.clicked.connect(self.my_btn_open1_Clicked)

        self.btn_close1 = QPushButton('撤单/平仓', self)
        self.btn_close1.setToolTip('撤销挂单或平掉已有仓位')
        self.btn_close1.resize(85, 25)
        self.btn_close1.move(200, 105)
        self.btn_close1.clicked.connect(self.my_btn_close1_Clicked)

        lab2 = QLabel('交易品种 (2)', self)
        lab2.move(20, 257)

        self.combo2 = QComboBox(self)
        for symbol in symbols:
            self.combo2.addItem(symbol)
        self.combo2.setCurrentText(symbols[1])
        self.combo2.move(20, 287)
        self.combo2.setFont(font12)

        self.cb_buy2 = QCheckBox('做多', self)
        self.cb_buy2.move(140, 260)
        self.cb_buy2.toggle()
        self.cb_buy2.setChecked(False)

        self.cb_sell2 = QCheckBox('做空', self)
        self.cb_sell2.move(140, 290)
        self.cb_sell2.toggle()
        self.cb_sell2.setChecked(False)

        self.btn_open2 = QPushButton('挂单/直开', self)
        self.btn_open2.setToolTip('挂单或者当前市价开仓')
        self.btn_open2.resize(85, 25)
        self.btn_open2.move(200, 260)
        self.btn_open2.clicked.connect(self.my_btn_open2_Clicked)

        self.btn_close2 = QPushButton('撤单/平仓', self)
        self.btn_close2.setToolTip('撤销挂单或平掉已有仓位')
        self.btn_close2.resize(85, 25)
        self.btn_close2.move(200, 290)
        self.btn_close2.clicked.connect(self.my_btn_close2_Clicked)

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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '操作提示！',
                                     '您确定要关闭“交易助手”？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.socket.close()
            rec_text = my_cur_time() + ' 关闭交易助手！'
            my_operating_record(rec_text)
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.showMinimized()

    def my_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + 132,
                  (screen.height() - size.height() - 90))

    def my_init_timer(self):
        """
        定时器
        """
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.my_update_time)

    def my_update_time(self):
        # 定时刷新LCD时钟
        self.lcd.display(time.strftime("%X", time.localtime()))
        # 定时刷新各品种的ATR
        self.my_update_atr()

    def my_update_atr(self):
        """
        读取ATR文件并更新标签文本
        """
        if len(self.config) == 0:
            self.config = self.my_read_config()
        mode = self.config[1]
        # 从配置文件里找到看盘MT4的Files文件夹
        if mode == 'Local':
            atr_file_path = self.config[3]
        elif mode == 'Network':
            atr_file_path = self.config[4]

        # ATR文件存放在看盘MT4的Files文件夹里
        file_name = atr_file_path + '\\' + 'myatr.txt'
        if os.path.isfile(file_name):
            try:
                with open(file_name, 'r') as file_object:
                    atr = file_object.read()
                self.lab0.setText(atr[:38])
            except:
                pass
        else:
            self.lab0.setText('请打开MT4看盘软件并加载ATR_EA程序')

    def _about(self):
        """
        关于菜单
        """
        QMessageBox.information(self, '联系我们——瑞讯银行智能化交易系统',
                                self.tr('微信：zyhj518，手机：13770675275。'))

    def my_btn_open1_Clicked(self):
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

            self.my_send_signal(signal_text)
        else:
            QMessageBox.information(self, '错误提示!',
                                    self.tr('请勾选交易方向后，再开仓!'))

    def my_btn_close1_Clicked(self):
        """
        撤销挂单，或平掉已有仓位
        """
        signal_text = self.combo1.currentText() + 'CLOSE'

        self.my_send_signal(signal_text)

    def my_btn_open2_Clicked(self):
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

            self.my_send_signal(signal_text)
        else:
            QMessageBox.critical(self, '错误提示!',
                                 self.tr('请勾选交易方向后，再开仓!'))

    def my_btn_close2_Clicked(self):
        """
        撤销挂单，或平掉已有仓位
        """
        signal_text = self.combo2.currentText() + 'CLOSE'

        self.my_send_signal(signal_text)

    def my_updateUI(self):
        if self.request is not None:
            enabled = False
        else:
            enabled = True

        self.btn_open1.setEnabled(enabled)
        self.btn_close1.setEnabled(enabled)
        self.btn_open2.setEnabled(enabled)
        self.btn_close2.setEnabled(enabled)

    def my_read_config(self):
        """
        读取交易环境的配置文件,返回MT4账户和IP地址或文件夹
        """
        config = configparser.ConfigParser()
        config.read('setting.cfg')

        account_number = config.get('MT4', 'account_number')
        mode = config.get('Pathway', 'mode')
        atr = config.get('ATR', 'directory')

        if config.get('Pathway', 'mode') == 'Local':
            directory = config.get('Local', 'directory')
            return account_number, mode, directory, atr

        elif config.get('Pathway', 'mode') == 'Network':
            host = config.get('Network', 'host')
            port = config.get('Network', 'port')
            return account_number, mode, host, port, atr

    def my_send_signal(self, inp_text):
        """
        发送交易指令到MT4的Files文件夹，或发送到交易服务器
        """
        # 读取配置文件到字典变量
        if len(self.config) == 0:
            self.config = self.my_read_config()
        mode = self.config[1]

        if mode == 'Local':
            symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']
            for symbol in symbols:
                if inp_text.find(symbol) >= 0:
                    trade_symbol = symbol
            file_path = self.config[2]
            # 检查交易品种的子文件夹是否存在，不存在就新建相应的子文件夹
            if os.path.exists(file_path + '\\' + trade_symbol) == False:
                os.mkdir(file_path + '\\' + trade_symbol)

            file_path = file_path + '\\' + trade_symbol + '\\'

            # 将指令存到对应的子文件夹里
            file_name = file_path + 'trade_signal.txt'

            with open(file_name, 'w') as file_object:
                file_object.write(inp_text)

        # 将交易指令传到交易服务器上
        elif mode == 'Network':
            account_number = self.config[0]
            host = self.config[2]
            port = int(self.config[3])

            self.request = QByteArray()
            stream = QDataStream(self.request, QIODevice.WriteOnly)
            stream.writeUInt16(0)
            stream.writeQString(account_number)
            stream.writeQString(inp_text)
            stream.device().seek(0)
            stream.writeUInt16(self.request.size() - SIZEOF_UINT16)

            self.my_updateUI()

            if self.socket.isOpen():
                self.socket.close()
            self.socket.connectToHost(host, port)

            rec_text = my_cur_time() + ' 正在连接远程交易服务器...'
            self.statusBar().showMessage(rec_text)
            my_operating_record(rec_text)

    def my_sendRequest(self):
        self.nextBlockSize = 0
        self.socket.write(self.request)
        self.request = None

        rec_text = my_cur_time() + ' 正在发送您的交易指令...'
        self.statusBar().showMessage(rec_text)
        my_operating_record(rec_text)

    def my_readResponse(self):
        stream = QDataStream(self.socket)

        while True:
            if self.nextBlockSize == 0:
                if self.socket.bytesAvailable() < SIZEOF_UINT16:
                    break
                self.nextBlockSize = stream.readUInt16()
            if self.socket.bytesAvailable() < self.nextBlockSize:
                break

            ser_reply = stream.readQString()

            if ser_reply == 'None':
                QMessageBox.critical(self, '错误提示!',
                                     self.tr('您没有开通服务器交易功能!'))
                rec_text = my_cur_time() + ' 您没有开通服务器交易功能！'
                self.statusBar().showMessage(rec_text)
                my_operating_record(rec_text)
            else:
                rec_text = my_cur_time() + ' 服务器已接收指令：{0}'.format(ser_reply)
                self.statusBar().showMessage(rec_text)
                my_operating_record(rec_text)

            self.nextBlockSize = 0
            self.socket.close()
            self.my_updateUI()
            rec_text = my_cur_time() + ' 已断开服务器连接！'
            my_operating_record(rec_text)

    def my_serverHasStopped(self):
        self.socket.close()

    def my_serverHasError(self, error):
        self.socket.close()

        rec_text = my_cur_time() + ' 错误：{0}'.format(self.socket.errorString())
        self.statusBar().showMessage(rec_text)
        my_operating_record(rec_text)


class CDialog(QDialog):
    """
    配置文件对话框窗口
    """
    def __init__(self):
        super().__init__()
        self._initUI()
        self.my_center()

    def _initUI(self):
        self.setFixedSize(360, 320)
        self.setWindowTitle('设置交易环境变量')
        self.setWindowIcon(QIcon('myIcon.ico'))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        lbl1 = QLabel('您的MT4账号：', self)
        lbl1.move(30, 30)

        self.qle_number = QLineEdit(self)
        self.qle_number.resize(90, 25)
        self.qle_number.move(140, 25)
        regex = QRegExp(r'^[1-9]\d+$')
        self.qle_number.setValidator(QRegExpValidator(regex, self))

        self.rb11 = QRadioButton('在本地交易', self)
        self.rb11.move(30, 70)
        self.rb11.setChecked(True)
        self.rb11.toggled.connect(self.my_rb_toggled)

        self.rb12 = QRadioButton('在服务器上交易', self)
        self.rb12.move(160, 70)
        self.rb12.toggled.connect(self.my_rb_toggled)

        self.lbl2 = QLabel('在下面输入交易MT4的Files文件夹路径：', self)
        self.lbl2.move(30, 105)

        self.qle_directory = QLineEdit(self)
        self.qle_directory.resize(300, 25)
        self.qle_directory.move(30, 140)
        regex1 = QRegExp(r'^[C-Ec-e][\:][\\][A-Za-z0-9\\]+$')
        self.qle_directory.setValidator(QRegExpValidator(regex1, self))

        self.lbl3 = QLabel('在下面输入看盘MT4的Files文件夹路径：', self)
        self.lbl3.move(30, 185)

        self.qle_directory1 = QLineEdit(self)
        self.qle_directory1.resize(300, 25)
        self.qle_directory1.move(30, 220)
        self.qle_directory1.setValidator(QRegExpValidator(regex1, self))

        btn_save = QPushButton('保存', self)
        btn_save.move(70, 260)
        btn_save.clicked.connect(self.my_save_environment)

        btn_cancel = QPushButton('取消', self)
        btn_cancel.move(200, 260)
        btn_cancel.clicked.connect(self.close)

    def closeEvent(self, event):
        self.qle_number.setText('')
        self.qle_directory.setText('')
        self.rb11.setChecked(True)

    def my_rb_toggled(self):
        if self.rb11.isChecked():
            self.lbl2.setText('在下面输入交易MT4的Files文件夹路径：')
            regex1 = QRegExp(r'^[C-Ec-e][\:][\\][A-Za-z0-9\\]+$')
            self.qle_directory.setValidator(QRegExpValidator(regex1, self))
        elif self.rb12.isChecked():
            self.lbl2.setText('在下面输入服务器的IP地址和端口：')
            regex1 = QRegExp(r'^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}'
                             r'(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
                             r'((:2\d{3})|(:[1-6]\d{4}))$')
            self.qle_directory.setValidator(QRegExpValidator(regex1, self))

    def my_save_environment(self):
        """
        设置交易环境，可以是本地的MT4的Files文件夹路径，也可以是服务器IP地址加端口
        """
        save_yn = True
        qle_number = self.qle_number.text()
        qle_directory = self.qle_directory.text()
        qle_directory1 = self.qle_directory1.text()
        if len(qle_number.split()) > 0 and len(qle_directory.split()) > 0 \
                and len(qle_directory1.split()) > 0:

            config = configparser.ConfigParser()
            config['MT4'] = {'account_number': qle_number}

            if self.rb11.isChecked():
                cur_mode = 'Local'
            elif self.rb12.isChecked():
                cur_mode = 'Network'
            config['Pathway'] = {'mode': cur_mode}

            if cur_mode == 'Local':
                if os.path.exists(qle_directory) \
                        and qle_directory.find('\MQL4\Files') > 0:
                    config['Local'] = {'directory': qle_directory}
                else:
                    save_yn = False
                    QMessageBox.critical(self, '错误提示!',
                                         self.tr('请输入正确的交易MT4的Files文件夹路径!'))

            elif cur_mode == 'Network':
                if self.my_ip_yn(qle_directory):
                    host = qle_directory[: qle_directory.find(':')]
                    port = qle_directory[qle_directory.find(':') + 1:]
                    config['Network'] = {'host': host,
                                         'port': port}
                else:
                    save_yn = False
                    QMessageBox.critical(self, '错误提示!',
                                         self.tr('请输入正确的IP地址和端口号!'))

            if os.path.exists(qle_directory1) and qle_directory1.find('\MQL4\Files') > 0:
                config['ATR'] = {'directory': qle_directory1}
            else:
                save_yn = False
                QMessageBox.critical(self, '错误提示!', self.tr('请输入正确的看盘MT4的Files文件夹路径!'))

            if save_yn:
                with open('setting.cfg', 'w') as file_object:
                    config.write(file_object)

                rec_text = my_cur_time() + ' 设置了交易环境'
                my_operating_record(rec_text)
                QMessageBox.information(self, '操作提示!',
                                        self.tr('已成功设置了交易环境配置文件!'))

                self.close()


    def my_ip_yn(self, inp_text):
        """
        检查输入的IP地址和端口号是否符合规则
        格式为：127.0.0.1:2000
        """
        res = re.match(
            r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}'
            r'(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
            r'((:2\d{3})|(:[1-6]\d{4}))',
            inp_text)

        if res:
            return True
        else:
            return False

    def my_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + 128,
                  (screen.height() - size.height()) - 130)


def my_cur_time():
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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = CWind()
    d = CDialog()

    sub_menu = w.settingAct
    # 打开交易环境配置窗口
    sub_menu.triggered.connect(d.show)

    # 若第一次启动，没有配置文件，就打开交易环境配置窗口
    if os.path.isfile('setting.cfg') == False:
        d.show()

    sys.exit(app.exec_())

