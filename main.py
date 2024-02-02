import sys
from io import BytesIO

import requests
from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from geocoder import get_span

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.coords = '40.295028,54.505887'
        self.spn = None
        self.z = None
        self.initUI()
        self.getImage()
        self.searchconfirm.clicked.connect(lambda: self.get_coords())

    def load_image(self):
        self.imageShower.setPixmap(QPixmap("map.png"))

    def getImage(self):
        try:
            if self.z is None:
                z = ""
            else:
                z = f"&z={str(self.z)}"
            map_request = f"http://static-maps.yandex.ru/1.x/?" \
                          f"ll={self.coords}" \
                          f"&l=map{z}"
            response = requests.get(map_request)

            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
            img = Image.open(BytesIO(response.content))
            img.save("map.png")
            self.load_image()
        except Exception as exy:
            print(exy.__repr__())

    def get_coords(self):
        try:
            coords_text = self.searchinput.text().split(', ')
            self.coords = ','.join((coords_text[1], coords_text[0]))
            self.spn = get_span(self.coords)
            print(self.spn)
            self.get_zoom()
            self.getImage()
        except Exception as exy:
            print(exy.__repr__())

    def get_zoom(self):
        if 0.0055 < float(self.spn[0]) < 0.003:
            self.z = 16
        elif 0.0109 < float(self.spn[0]) < 0.0054:
            self.z = 15
        elif 0.0218 < float(self.spn[0]) < 0.0108:
            self.z = 14
        elif float(self.spn[0]) < 0.0217:
            self.z = 13

    def get_str_span(self):
        span = f"{format(self.spn[0], '.6f')},{format(self.spn[1], '.6f')}"
        return span

    def initUI(self):
        uic.loadUi('untitled.ui', self)
        self.setWindowTitle('Отображение карты')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
