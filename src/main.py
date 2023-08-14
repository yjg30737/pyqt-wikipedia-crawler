import os, sys

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from script import get_languages, wikidoc_to_txt, wikicate_to_txt, open_directory

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit, QVBoxLayout, QWidget, QGroupBox, \
    QFormLayout, QComboBox, QHBoxLayout, QRadioButton, QMessageBox, QFileDialog
from PyQt5.QtCore import QThread, QCoreApplication

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    def __init__(self, lang, text, is_single_doc_f, save_dir):
        super(Thread, self).__init__()
        self.__lang = lang
        self.__text = text
        self.__is_single_doc_f = is_single_doc_f
        self.__save_dir = save_dir

    def run(self):
        try:
            if self.__is_single_doc_f:
                wikidoc_to_txt(wiki_lang=self.__lang, doc_name=self.__text, save_dir=self.__save_dir)
            else:
                wikicate_to_txt(wiki_lang=self.__lang, category=self.__text, save_dir=self.__save_dir)
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__lang = get_languages()
        self.__save_dir = ''

    def __initUi(self):
        self.setWindowTitle('Wikipedia Crawler')

        self.__lineEdit = QLineEdit()

        self.__langCmbBox = QComboBox()
        self.__langCmbBox.addItems(self.__lang.keys())
        self.__langCmbBox.setCurrentText('English')

        self.__singleDocRadBtn = QRadioButton()
        self.__singleDocRadBtn.setText('Single Document')
        self.__singleDocRadBtn.toggled.connect(self.__toggled)
        self.__singleDocRadBtn.setChecked(True)

        self.__categoryRadBtn = QRadioButton()
        self.__categoryRadBtn.setText('Category')

        lay = QHBoxLayout()
        lay.addWidget(self.__singleDocRadBtn)
        lay.addWidget(self.__categoryRadBtn)
        lay.setContentsMargins(0, 0, 0, 0)
        typeWidget = QWidget()
        typeWidget.setLayout(lay)

        lay = QFormLayout()
        lay.addRow('Language', self.__langCmbBox)
        lay.addRow('Type', typeWidget)

        settingsGrpBox = QGroupBox()
        settingsGrpBox.setTitle('Settings')
        settingsGrpBox.setLayout(lay)

        settingsGrpBox.setLayout(lay)

        self.__lineEdit.textChanged.connect(self.__textChanged)

        self.__btn = QPushButton('Crawl')
        self.__btn.clicked.connect(self.__run)
        self.__btn.setEnabled(False)

        lay = QVBoxLayout()
        lay.addWidget(settingsGrpBox)
        lay.addWidget(self.__lineEdit)
        lay.addWidget(self.__btn)
        lay.setAlignment(Qt.AlignTop)
        lay.setSpacing(5)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        self.setFixedSize(self.sizeHint())

    def __toggled(self, f):
        if f:
            self.__lineEdit.setPlaceholderText('Input the document name...')
        else:
            self.__lineEdit.setPlaceholderText('Input the category name...')

    def __textChanged(self, text):
        f = text.strip() != ''
        self.__btn.setEnabled(f)

    def __run(self):
        try:
            filename = QFileDialog.getExistingDirectory(self, 'Choose Directory to Save', '', QFileDialog.ShowDirsOnly)
            if filename:
                self.__save_dir = filename
                lang = self.__lang[self.__langCmbBox.currentText()]
                text = self.__lineEdit.text()

                # options are either single document or category, so it can be decided by True or False with only this
                is_single_doc_f = self.__singleDocRadBtn.isChecked()
                self.__t = Thread(lang, text, is_single_doc_f, save_dir=self.__save_dir)
                self.__t.started.connect(self.__started)
                self.__t.finished.connect(self.__finished)
                self.__t.start()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def __started(self):
        print('started')
        self.__btn.setEnabled(False)

    def __finished(self):
        print('finished')
        self.__btn.setEnabled(True)
        open_directory(self.__save_dir)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())