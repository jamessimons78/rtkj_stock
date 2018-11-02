import os
import sys
import time
from PyQt5.QtNetwork import (QTcpSocket, QTcpServer, QHostAddress)
from PyQt5.QtCore import (QByteArray, QDataStream, QIODevice, Qt)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox)

host = '127.0.0.1'
port = 2000

SIZEOF_UINT16 = 2
# 将所有交易账号和文件夹路径读取到account_dir字典变量中
with open('account_dir.txt', 'r') as file_object:
    account_dir = eval(file_object.read())


class CSerWind(QMainWindow):
    """
    主窗口
    """
    def __init__(self):
        super().__init__()

        self.tcpServer = TcpServer(self)

        if not self.tcpServer.listen(QHostAddress(host), port):
            QMessageBox.critical(self, '交易服务器', '服务器启动失败：{0}'
                                 .format(self.tcpServer.errorString()))
            rec_text = _cur_time() + ' 服务器启动失败！'
            _operating_record(rec_text)
            self.close()
            return
        else:
            self._initUI()
            # 状态栏显示启动信息，并存入日志文件
            rec_text = _cur_time() + ' 开启交易服务器！'
            self.statusBar().showMessage(rec_text)
            _operating_record(rec_text)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '操作提示！',
                                     '您确定要关闭“交易服务器”？',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            rec_text = _cur_time() + ' 关闭交易服务器！'
            _operating_record(rec_text)
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.showMinimized()

    def _initUI(self):
        self.setFixedSize(600, 400)
        self.move(0, 60)
        self.setWindowTitle('交易服务器')
        self.setWindowIcon(QIcon('myIcon.ico'))

        self.show()


class Socket(QTcpSocket):

    def __init__(self, parent=None):
        super(Socket, self).__init__(parent)
        self.readyRead.connect(self._readRequest)
        self.disconnected.connect(self.deleteLater)
        self.nextBlockSize = 0

    def _readRequest(self):
        stream = QDataStream(self)
        if self.nextBlockSize == 0:
            if self.bytesAvailable() < SIZEOF_UINT16:
                return
            self.nextBlockSize = stream.readUInt16()
        if self.bytesAvailable() < self.nextBlockSize:
            return

        # MT4交易账号
        account_number = stream.readQString()
        # 交易指令
        trade_instruction = stream.readQString()

        rec_text = _cur_time() + ' 已经读取到来自 {0} 的交易指令：{1}'.format(account_number, trade_instruction)
        _operating_record(rec_text)

        directory = account_dir.get(account_number, 'None')
        if directory == 'None':
            reply = 'None'
            rec_text = _cur_time() + ' 交易账号 {0} 没有获得交易服务器的授权！'.format(account_number)
            _operating_record(rec_text)
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

            rec_text = _cur_time() + ' 已经将交易指令存到相应的MT4的Files文件夹里！'
            _operating_record(rec_text)

            reply = trade_instruction

        self._sendReply(reply)

    def _sendReply(self, inp_text):
        reply = QByteArray()
        stream = QDataStream(reply, QIODevice.WriteOnly)
        stream.writeUInt16(0)
        stream.writeQString(inp_text)
        stream.device().seek(0)
        stream.writeUInt16(reply.size() - SIZEOF_UINT16)
        self.write(reply)

        rec_text = _cur_time() + ' 已经将交易指令的接收情况反馈给客户端！'
        _operating_record(rec_text)


class TcpServer(QTcpServer):

    def __init__(self, parent=None):
        super(TcpServer, self).__init__(parent)

    def incomingConnection(self, socketId):
        socket = Socket(self)
        socket.setSocketDescriptor(socketId)


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
    file_name = 'ser_' + time.strftime('%Y-%m-%d', now) + '.txt'
    rec_text = time.strftime('%Y-%m-%d', now) + ' ' + inp_text + '\n'

    with open(file_name, 'a+', encoding='UTF-8') as file_object:
        file_object.write(rec_text)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = CSerWind()

    sys.exit(app.exec_())
