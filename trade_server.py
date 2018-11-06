import os
import sys
import time
import configparser
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import (QTcpSocket, QTcpServer, QAbstractSocket, QHostAddress)
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, pyqtSignal, QObject,
                          Qt, QThread, QReadWriteLock)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTextBrowser)

SIZEOF_UINT16 = 2


class CSerWind(QMainWindow):
    """
    主窗口
    """
    def __init__(self, inp_host, inp_port):
        super().__init__()

        self.lock = QReadWriteLock()

        self.recordSignal = RecordSignal()
        self.recordSignal.sendSignal.connect(self.my_record)

        self.tcpServer = TcpServer(self.recordSignal, self.lock)
        if not self.tcpServer.listen(QHostAddress(inp_host), inp_port):
            QMessageBox.critical(self, '交易服务器', '服务器启动失败：{0}'
                                 .format(self.tcpServer.errorString()))
            rec_text = my_cur_time() + ' 服务器启动失败！'
            try:
                self.lock.lockForWrite()
                self.recordSignal.sendSignal.emit(rec_text)
            finally:
                self.lock.unlock()
            self.close()
            return
        else:
            self._initUI()
            rec_text = my_cur_time() + ' 开启交易服务器！'
            try:
                self.lock.lockForWrite()
                self.recordSignal.sendSignal.emit(rec_text)
            finally:
                self.lock.unlock()

    def _initUI(self):
        self.setFixedSize(600, 400)
        self.move(0, 60)
        self.setWindowTitle('交易服务器')
        self.setWindowIcon(QIcon('myIcon.ico'))

        # 逐条显示交易服务器操作的每个记录
        self.text_browser = QTextBrowser(self)
        self.text_browser.resize(500, 160)
        self.text_browser.move(10, 220)

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '操作提示！',
                                     '您确定要关闭“交易服务器”？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            rec_text = my_cur_time() + ' 关闭交易服务器！'
            try:
                self.lock.lockForWrite()
                self.recordSignal.sendSignal.emit(rec_text)
            finally:
                self.lock.unlock()
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.showMinimized()

    def my_record(self, inp_text):
        """
        记录服务器操作日志保存到日志文件，并在主窗口TextBrowser组件中显示出来
        """
        now = time.localtime()
        file_name = 'ser_' + time.strftime('%Y-%m-%d', now) + '.txt'
        rec_text = inp_text + '\n'

        with open(file_name, 'a+', encoding='UTF-8') as file_object:
            file_object.write(rec_text)

        self.text_browser.append(inp_text)


class Thread(QThread):

    def __init__(self, socketId, recordSignal, lock, parent=None):
        super().__init__(parent)
        self.socketId = socketId
        self.recordSignal = recordSignal
        self.lock = lock

    def run(self):
        socket = QTcpSocket()
        if not socket.setSocketDescriptor(self.socketId):
            self.error.connect(socket.error)
            return
        while socket.state() == QAbstractSocket.ConnectedState:
            nextBlockSize = 0
            stream = QDataStream(socket)
            if socket.waitForReadyRead() and \
                    socket.bytesAvailable() >= SIZEOF_UINT16:
                nextBlockSize = stream.readUInt16()
            else:
                rec_text = ' 无法正常读取客户端的请求！'
                self.my_sendReply(socket, rec_text)
                rec_text = my_cur_time() + rec_text
                try:
                    self.lock.lockForWrite()
                    self.recordSignal.sendSignal.emit(rec_text)
                finally:
                    self.lock.unlock()
                return

            if socket.bytesAvailable() < nextBlockSize:
                if not socket.waitForReadyRead(5000) or \
                        socket.bytesAvailable() < nextBlockSize:
                    rec_text = ' 无法正常读取客户端的数据！'
                    self.my_sendReply(socket, rec_text)
                    rec_text = my_cur_time() + rec_text
                    try:
                        self.lock.lockForWrite()
                        self.recordSignal.sendSignal.emit(rec_text)
                    finally:
                        self.lock.unlock()
                    return

            # MT4交易账号
            account_number = stream.readQString()
            # 交易指令
            trade_instruction = stream.readQString()
            rec_text = my_cur_time() + ' 已读取到来自 {0} 的交易指令：{1}'.format(account_number, trade_instruction)
            try:
                self.lock.lockForWrite()
                self.recordSignal.sendSignal.emit(rec_text)
            finally:
                self.lock.unlock()

            try:
                self.lock.lockForRead()
                directory = account_dir.get(account_number, 'None')
            finally:
                self.lock.unlock()

            if directory == 'None':
                reply_text = 'None'
                rec_text = my_cur_time() + ' 交易账号 {0} 没有获得交易服务器的授权！'.format(account_number)
                try:
                    self.lock.lockForWrite()
                    self.recordSignal.sendSignal.emit(rec_text)
                finally:
                    self.lock.unlock()
            else:
                file_path = directory
                # 将交易指令存到相应账号MT4的Files文件夹里
                symbols = ['EURUSD', 'GBPUSD', 'XAUUSD', 'USDJPY']
                for symbol in symbols:
                    if trade_instruction.find(symbol) >= 0:
                        trade_symbol = symbol
                # 检查交易品种的子文件夹是否存在，不存在就新建相应的子文件夹
                if os.path.exists(file_path + '\\' + trade_symbol) == False:
                    os.mkdir(file_path + '\\' + trade_symbol)
                file_path = file_path + '\\' + trade_symbol + '\\'
                # 将指令存到对应的子文件夹里
                file_name = file_path + 'trade_signal.txt'
                with open(file_name, 'w') as file_object:
                    file_object.write(trade_instruction)

                reply_text = trade_instruction

            try:
                self.lock.lockForWrite()
                rec_text = my_cur_time() + ' 已将交易指令存到相应的MT4的Files文件夹里！'
                self.recordSignal.sendSignal.emit(rec_text)
            finally:
                self.lock.unlock()

            self.my_sendReply(socket, reply_text)
            socket.waitForDisconnected()

    def my_sendReply(self, socket, inp_text):
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.writeUInt16(0)
        stream.writeQString(inp_text)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        socket.write(reply)

        try:
            self.lock.lockForWrite()
            rec_text = my_cur_time() + ' 已将交易指令{0}的接收情况反馈给客户端！'.format(inp_text)
            self.recordSignal.sendSignal.emit(rec_text)
        finally:
            self.lock.unlock()


class TcpServer(QTcpServer):

    def __init__(self, recordSignal, lock):
        super().__init__()
        self.recordSignal = recordSignal
        self.lock = lock

    def incomingConnection(self, socketId):
        thread = Thread(socketId, self.recordSignal, self.lock, self)
        thread.finished.connect(thread.deleteLater)
        thread.start()


class RecordSignal(QObject):
    """
    创建一个信号触发器，用于记录服务器操作
    """
    # str为传入槽的一个参数类型
    sendSignal = pyqtSignal(str)


def my_cur_time():
    """
    获取当前时间，返回字符串
    """
    now = time.localtime()
    cur_time = time.strftime('%H:%M:%S', now)
    return cur_time


def my_read_config(inp_filename):
    """
    读取交易服务器的IP地址及端口号
    """
    config = configparser.ConfigParser()
    config.read(inp_filename)

    host = config.get('Network', 'host')
    port = config.get('Network', 'port')
    return host, port


if __name__ == '__main__':

    # 配置交易服务器需绑定的IP地址及端口号
    config_filename = 'ser_setting.cfg'
    if os.path.isfile(config_filename) == True:
        config = my_read_config(config_filename)
        host = config[0]
        port = int(config[1])
    else:
        host = '0.0.0.0'
        port = 2000

    # 将所有交易账号和文件夹路径读取到account_dir字典变量中
    with open('account_dir.txt', 'r') as file_object:
        account_dir = eval(file_object.read())

    app = QApplication(sys.argv)
    tServer = CSerWind(host, port)

    sys.exit(app.exec_())
