import sys
import threading
import time

import PyPDF2
import pyttsx3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import QThread, pyqtSignal

global pdfreader, pages, page_no, frm, to

class Main(QMainWindow):
    def __init__(self):
        page_no = 0
        super(Main, self).__init__()
        loadUi('main.ui', self)
        self.show()
        self.upload.clicked.connect(self.pdf_upload)
        self.play.clicked.connect(self.play_pressed)



    # def thread_start(self):
    #     x = threading.Thread(target = self.play_pressed())
    #     x.start()

    def pdf_upload(self):
        global pdfreader, pages
        fname = QFileDialog.getOpenFileName(self, 'Select the file')
        file_path = fname[0]
        print(file_path)
        self.location.setText(file_path)
        book = open(file_path, 'rb')
        pdfreader = PyPDF2.PdfFileReader(book)
        pages = pdfreader.numPages
        self.frm.setValue(1)
        self.to.setValue(pages)
        self.to.setMaximum(pages)

    def play_pressed(self):
        global frm, to, range_spk
        frm = self.frm.value() - 1
        to = self.to.value()
        range_spk = to - frm
        self.worker = Work()
        self.worker.start()
        self.worker.update_page.connect(self.page_update)
        self.worker.readed_page.connect(self.progressbar)

    def page_update(self, val):
        global range_spk
        self.label.setText(f'Reading Page no. {val}')

    def progressbar(self, val):
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(int((val / range_spk) * 100))

class Work(QThread):
    update_page = pyqtSignal(int)
    readed_page = pyqtSignal(int)
    def run(self):
        global pdfreader, pages, page_no, frm, to
        speaker = pyttsx3.init()
        i = 0
        for page_no in range(frm, to + 1):
            print(page_no)
            i += 1
            page = pdfreader.getPage(page_no)
            text = page.extractText()

            speaker.setProperty('rate', 12000)
            speaker.connect('started-word', self.onWord)
            speaker.say(text)
            self.update_page.emit(page_no + 1)
            speaker.runAndWait()
            self.readed_page.emit(i)

    def onWord(self, name, location, length):
        print(name, location, length)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())

# app = QtWidgets.QApplication(sys.argv)
# window = Login()
# widget=QtWidgets.QStackedWidget()
# widget.addWidget(window)
# widget.setFixedHeight(300)
# widget.setFixedWidth(300)
# widget.show()
# app.exec_()
