import sys
import qrcode
import cv2
import webbrowser


from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("qrcodegui.ui", self)
        self.show()

        self.current_file = ""
        self.actionScan.triggered.connect(self.scan_qr)
        self.actionLoad.triggered.connect(self.load_image)
        self.actionSave.triggered.connect(self.save_image)
        self.actionQuit.triggered.connect(self.quit)
        self.pushButton.clicked.connect(self.generate_code)
        self.pushButton_2.clicked.connect(self.read_code)

    def scan_qr(self):

        capture = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        while True:
            _, image = capture.read()
            data,one, _ = detector.detectAndDecode(image)
            if data:
                a = data
                break
            cv2.imshow('qrcodescanner', image)
            if cv2.waitKey(1)==ord('q'):
                break
        b = webbrowser.open(str(a))
        capture.release(a)
        cv2.destroyAllWindows

    def load_image(self):
        option = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files(*)", options=option)

        if filename != "":
            self.current_file = filename
            pixmap = QtGui.QPixmap(self.current_file)
            pixmap = pixmap.scaled(300, 300)
            self.label.setScaledContents(True)
            self.label.setPixmap(pixmap)

    def save_image(self):
        option = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG(*.png)", options=option)

        if filename != "":
            image = self.label.pixmap()
            image.save(filename, "PNG")

    def generate_code(self):
        code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=2)
        code.add_data(self.textEdit.toPlainText())
        code.make(fit=True)

        image = code.make_image(fill_color="black", back_color="white")
        image.save("currentqr.png")
        pixmap = QtGui.QPixmap("currentqr.png")
        pixmap = pixmap.scaled(300, 300)
        self.label.setScaledContents(True)
        self.label.setPixmap(pixmap)

    def read_code(self):
        image = cv2.imread(self.current_file)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(image)
        self.textEdit.setText(data)

    def quit(self):
        sys.exit(0)


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()
