# Image Translator for gameras and academics
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab
from PIL import Image
import numpy as np
import cv2
import os
import keyboard
## OCR
import pytesseract


class Capture(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        translatedText = tk.Label(root, text="Hello, world")
        translatedText.pack()
        root.title("Image Translator v 0.5")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle('Image Translator ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
      
    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('capture.png')

####TODO: Zwiększyć kontrast - przerobić na czarnobiały?
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

####TODO: Wprowadzić próbe rozczytania tekstu
        cv2.imshow('Captured Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def translate(whatLang):
    print("OCR obrazu .... w języku ", whatLang)
    pathToFile = os.path.dirname(os.path.abspath('capture.png'))+ '\capture.png'
    pytesseract.pytesseract.tesseract_cmd = r'F:\Silniki\TesseractOCR\tesseract'
    ocr_string = pytesseract.image_to_string(Image.open(pathToFile), lang=whatLang)
    print(ocr_string)
    return ocr_string
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # Press PAGE UP then PAGE DOWN to type "foobar".
##    keyboard.add_hotkey('page up', lambda: keyboard.write('foobar'))
##    keyboard.wait()
    window = Capture()
    
    if window: 
        ocr_string = translate('rus')
        print(ocr_string)
##    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
