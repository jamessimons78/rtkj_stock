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
        self._init_timer()

        self.socket = QTcpSocket()
        self.nextBlockSize = 0
        self.request = None

        self.socket.connected.connect(self._sendRequest)
        self.socket.readyRead.connect(self._readResponse)
        self.socket.disconnected.connect(self._serverHasStopped)
        self.socket.error.connect(self._serverHasError)

        # 若已经有交易环境配置文件，则打开并读到self.config变量中
        self.config = ()
        if os.path.isfile('setting.cfg') == True:
            self.config = self._read_config()

        # 状态栏显示启动信息，并存入日志文件
        rec_text = _cur_time() + ' 开启交易助手！'
        self.statusBar().showMessage(rec_text)
        _operating_record(rec_text)

    def _initUI(self):
        self.setFixedSize(300, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self._center()
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
        btn_open1.clicked.connect(self._btn_open1_Clicked)

        btn_close1 = QPushButton('撤单/平仓', self)
        btn_close1.setToolTip('撤销挂单或平掉已有仓位')
        btn_close1.resize(85, 25)
        btn_close1.move(200, 105)
        btn_close1.clicked.connect(self._btn_close1_Clicked)

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
        btn_open2.clicked.connect(self._btn_open2_Clicked)

        btn_close2 = QPushButton('撤单/平仓', self)
        btn_close2.setToolTip('撤销挂单或平掉已有仓位')
        btn_close2.resize(85, 25)
        btn_close2.move(200, 290)
        btn_close2.clicked.connect(self._btn_close2_Clicked)

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
            rec_text = _cur_time() + ' 关闭交易助手！'
            _operating_record(rec_text)
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.showMinimized()

    def _center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + 90,
                  (screen.height() - size.height() - 90))

    def _init_timer(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self._update_time)

    def _update_time(self):
        self.lcd.display(time.strftime("%X", time.localtime()))

    def _about(self):
        """
        关于菜单
        """
        QMessageBox.information(self, '联系我们——瑞讯银行智能化交易系统',
                                self.tr('微信：zyhj518，手机：13770675275。'))

    def _btn_open1_Clicked(self):
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

            self._send_signal(signal_text)
            # rec_text = _cur_time() + ' 执行' + signal_text + '操作'
            # self.statusBar().showMessage(rec_text)
            # _operating_record(rec_text)
        else:
            QMessageBox.information(self, '错误提示!',
                                    self.tr('请勾选交易方向后，再开仓!'))

    def _btn_close1_Clicked(self):
        """
        撤销挂单，或平掉已有仓位
        """
        signal_text = self.combo1.currentText() + 'CLOSE'

        self._send_signal(signal_text)
        # rec_text = _cur_time() + ' 执行' + signal_text + '操作'
        # self.statusBar().showMessage(rec_text)
        # _operating_record(rec_text)

    def _btn_open2_Clicked(self):
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

            self._send_signal(signal_text)
            # rec_text = _cur_time() + ' 执行' + signal_text + '操作'
            # self.statusBar().showMessage(rec_text)
            # _operating_record(rec_text)
        else:
            QMessageBox.critical(self, '错误提示!',
                                 self.tr('请勾选交易方向后，再开仓!'))

    def _btn_close2_Clicked(self):
        """
        撤销挂单，或平掉已有仓位
        """
        signal_text = self.combo2.currentText() + 'CLOSE'

        self._send_signal(signal_text)
        # rec_text = _cur_time() + ' 执行' + signal_text + '操作'
        # self.statusBar().showMessage(rec_text)
        # _operating_record(rec_text)

    def _read_config(self):
        """
        读取交易环境的配置文件,返回MT4账户和IP地址或文件夹
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

    def _send_signal(self, inp_text):
        """
        发送交易指令到MT4的Files文件夹，或发送到交易服务器
        """
        # 读取配置文件到字典变量
        if len(self.config) == 0:
            self.config = self._read_config()
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

            if self.socket.isOpen():
                self.socket.close()
            self.socket.connectToHost(host, port)

            rec_text = _cur_time() + ' 正在连接连接交易服务器{0}...'.format(host)
            self.statusBar().showMessage(rec_text)
            _operating_record(rec_text)

    def _sendRequest(self):
        self.nextBlockSize = 0
        self.socket.write(self.request)
        self.request = None

        rec_text = _cur_time() + ' 正在发送您的交易指令...'
        self.statusBar().showMessage(rec_text)
        _operating_record(rec_text)

    def _readResponse(self):
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
                rec_text = _cur_time() + ' 您没有开通服务器交易功能！'
                self.statusBar().showMessage(rec_text)
                _operating_record(rec_text)
            else:
                rec_text = _cur_time() + ' 服务器已经接收指令：{0}'.format(ser_reply)
                self.statusBar().showMessage(rec_text)
                _operating_record(rec_text)

            self.nextBlockSize = 0

    def _serverHasStopped(self):
        self.socket.close()
        # rec_text = _cur_time() + ' 错误：连接的服务器已经关闭！'
        # self.statusBar().showMessage(rec_text)
        # _operating_record(rec_text)

    def _serverHasError(self, error):
        self.socket.close()

        rec_text = _cur_time() + ' 错误：{0}'.format(self.socket.errorString())
        self.statusBar().showMessage(rec_text)
        _operating_record(rec_text)


class CDialog(QDialog):
    """
    配置文件对话框窗口
    """
    def __init__(self):
        super().__init__()
        self._initUI()
        self._center()

    def _initUI(self):
        self.setFixedSize(360, 220)
        self.setWindowTitle('设置交易环境相关变量')
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
        self.rb11.toggled.connect(self._rb_toggled)

        self.rb12 = QRadioButton('在服务器上交易', self)
        self.rb12.move(160, 70)
        self.rb12.toggled.connect(self._rb_toggled)

        self.lbl2 = QLabel('在下面输入MT4的Files文件夹路径：', self)
        self.lbl2.move(30, 105)

        self.qle_directory = QLineEdit(self)
        self.qle_directory.resize(300, 25)
        self.qle_directory.move(30, 140)
        regex1 = QRegExp(r'^[C-Ec-e][\:][\\][A-Za-z0-9\\]+$')
        self.qle_directory.setValidator(QRegExpValidator(regex1, self))

        btn_save = QPushButton('保存', self)
        btn_save.move(70, 180)
        btn_save.clicked.connect(self._save_environment)

        btn_cancel = QPushButton('取消', self)
        btn_cancel.move(200, 180)
        btn_cancel.clicked.connect(self.close)

    def _rb_toggled(self):
        if self.rb11.isChecked():
            self.lbl2.setText('在下面输入MT4的Files文件夹路径：')
            regex1 = QRegExp(r'^[C-Ec-e][\:][\\][A-Za-z0-9\\]+$')
            self.qle_directory.setValidator(QRegExpValidator(regex1, self))
        elif self.rb12.isChecked():
            self.lbl2.setText('在下面输入服务器的IP地址和端口：')
            regex1 = QRegExp(r'^((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}'
                             r'(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
                             r'((:2\d{3})|(:[1-6]\d{4}))$')
            self.qle_directory.setValidator(QRegExpValidator(regex1, self))

    def _save_environment(self):
        """
        设置交易环境，可以是本地的MT4的Files文件夹路径，也可以是服务器IP地址加端口
        """
        save_yn = True
        qle_number = self.qle_number.text()
        qle_directory = self.qle_directory.text()
        if len(qle_number.split()) > 0 and len(qle_directory.split()) > 0:

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
                                         self.tr('请输入正确的MT4的Files文件夹路径!'))

            elif cur_mode == 'Network':
                if self._ip_yn(qle_directory):
                    host = qle_directory[: qle_directory.find(':')]
                    port = qle_directory[qle_directory.find(':') + 1:]
                    config['Network'] = {'host': host,
                                         'port': port}
                else:
                    save_yn = False
                    QMessageBox.critical(self, '错误提示!',
                                         self.tr('请输入正确的IP地址和端口号!'))

            if save_yn:
                with open('setting.cfg', 'w') as file_object:
                    config.write(file_object)

                rec_text = _cur_time() + ' 设置了交易环境'
                _operating_record(rec_text)
                QMessageBox.information(self, '操作提示!',
                                        self.tr('已经成功设置了交易环境配置文件!'))
                self.close()


    def _ip_yn(self, inp_text):
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

    def _center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2 + 85,
                  (screen.height() - size.height()) - 180)


def _cur_time():
    """
    获取当前时间，返回字符串
    """
    now = time.localtime()
    cur_time = time.strftime('%H:%M:%S', now)
    return cur_time


def _operating_record(inp_text):
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

