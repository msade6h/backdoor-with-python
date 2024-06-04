import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import socket

class ClientThread(QThread):
    output_signal = pyqtSignal(str)

    def __init__(self, host, port, command_input, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self.command_input = command_input

    def run(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        self.output_signal.emit("vasl shod !\n")
        
        while True:
            command = self.command_input.text()
            self.conn.send(command.encode())
            output_data = self.conn.recv(1024).decode()
            self.output_signal.emit(output_data)

class RemoteCommandExecutor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Remote Command Executor by sade6h@gmail.com")

        layout = QVBoxLayout()

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)

        self.command_input = QLineEdit()
        layout.addWidget(self.command_input)

        self.send_button = QPushButton("Send Command")
        self.send_button.clicked.connect(self.send_command)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.host = '192.168.0.4'
        self.port = 999
        self.client_thread = ClientThread(self.host, self.port, self.command_input)
        self.client_thread.output_signal.connect(self.update_output)
        self.client_thread.start()

    def send_command(self):
        command = self.command_input.text()
        self.client_thread.conn.send(command.encode())
        self.command_input.clear()

    def update_output(self, output):
        self.output_display.append(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RemoteCommandExecutor()
    window.show()
    sys.exit(app.exec_())
