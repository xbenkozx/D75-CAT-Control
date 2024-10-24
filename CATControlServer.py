from PySide6.QtCore import  QObject, Signal
from PySide6.QtNetwork import QTcpServer, QHostAddress

# ---------- CATControlServer Class ---------- #
class CATControlServer(QObject):
    tcpServer: QTcpServer = None

    newConnection = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tcpServer = QTcpServer(self)

        if not self.tcpServer.listen(address=QHostAddress("127.0.0.1"), port=8001):
            print("Unable to start CAT Control Server:", self.tcpServer.errorString())
            return

        self.tcpServer.newConnection.connect(self.handleNewConnection)

    def handleNewConnection(self):
        self.newConnection.emit()

        while self.tcpServer.hasPendingConnections():
            socket = self.tcpServer.nextPendingConnection()

            socket.readyRead.connect(lambda: self.handleData(socket))
            socket.disconnected.connect(lambda: self.handleDisconnect(socket))

    def handleData(self, socket):
        data = socket.readAll()
        print("Received data:", data.data())
        socket.write(data)  # Echo back the data

    def handleDisconnect(self, socket):
        pass
        # print("Client disconnected:", socket.peerAddress().toString())
    
# ---------- CATServer Class ---------- #