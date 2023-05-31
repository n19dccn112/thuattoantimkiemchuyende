import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
doc_dict = {"AAAAAAAAAAAAA": "Tài liệu A", "BBBBBBBBBBB": "Tài liệu B", "CCCCCCCCCCCCCC": "Tài liệu C"}

class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.title_label = QLabel('BM25', self)
        self.title_label.setFont(QFont('Arial', 30, QFont.Bold))  # Đặt kiểu chữ in đậm
        self.title_label.move(800, 10)

        search_label = QLabel('Tìm kiếm:', self)
        search_label.move(100, 100)

        self.search_combo = QComboBox(self)
        for key, value in doc_dict.items():
            self.search_combo.addItem(value, userData=key)
        self.search_combo.move(80, 20)

        search_button = QPushButton('Tìm', self)
        search_button.move(1550, 100)
        search_button.clicked.connect(self.search)

        self.doc_list_widget = QListWidget(self)
        self.doc_list_widget.move(100, 200)
        self.doc_list_widget.setFixedSize(1600, 600) # setFixedSize
        # self.setGeometry(300, 300, 340, 300) # setGeometry

        self.setGeometry(100, 100, 1800, 900)
        self.setWindowTitle('Tìm kiếm tài liệu')
        self.show()

    def search(self):
        selected_doc = self.search_combo.currentData()
        self.doc_list_widget.clear()
        if selected_doc == "AAAAAAAAAAAAA":
            self.doc_list_widget.addItem(QListWidgetItem('Tên tài liệu A'))
            self.doc_list_widget.addItem(QListWidgetItem('Mô tả tài liệu A'))
            self.doc_list_widget.addItem(QListWidgetItem('Ngày tạo tài liệu A'))
        elif selected_doc == "BBBBBBBBBBB":
            self.doc_list_widget.addItem(QListWidgetItem('Tên tài liệu A'))
            self.doc_list_widget.addItem(QListWidgetItem('Mô tả tài liệu A'))
            self.doc_list_widget.addItem(QListWidgetItem('Ngày tạo tài liệu A'))
        elif selected_doc == "CCCCCCCCCCCCCC":
            self.doc_list_widget.addItem(QListWidgetItem('Tên tài liệu A'))
            self.doc_list_widget.addItem(QListWidgetItem('Mô tả tài liệu A'))
            self.doc_list_widget.addItem(QListWidgetItem('Ngày tạo tài liệu A'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    search_widget = SearchWidget()
    sys.exit(app.exec_())

