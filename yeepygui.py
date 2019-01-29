import yeepy
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

app = QtWidgets.QApplication([])
view = QQuickView()
url = QUrl("/home/drugo/yeepygui/yeepygui.qml")
view.setSource(url)
view.show()
#button = QtWidgets.QPushButton("Toggle")
#button.clicked.connect(yeepy.power_toggle)
#button.show()
app.exec_()
