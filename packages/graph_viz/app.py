from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QPlainTextEdit
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from sensor_msgs.msg import CompressedImage
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String

class ROSBridge(QThread):
    change_ros_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        rospy.init_node('collect', anonymous=False)
        self.intersetion_stat = rospy.Subscriber(f"/{sys.argv[1]}/intersection_id",
                                                 String, self.callback, queue_size=1)
    def callback(self, data):
        self.change_ros_signal.emit(str(data.data))

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.msgs = []
        self.initUI()
        self.init_ros()

    def initUI(self):
        self.setWindowTitle("Stat of intersection")
        self.resize(200, 200)
        windowLayout = QVBoxLayout()
        self.create_top_layout()
        windowLayout.addLayout(self.top_layout)

    def create_top_layout(self):
        self.top_layout = QHBoxLayout()
        self.create_text_area()
        self.top_layout.addWidget(self.area)

    def create_text_area(self):
        self.area = QPlainTextEdit(self)
        
    def init_ros(self):
        self.thread = ROSBridge()
        # connect its signal to the update_image slot
        self.thread.change_ros_signal.connect(self.update_msg)
        # start the thread
        self.thread.start()

    @pyqtSlot(str)
    def update_msg(self, msg):
        message = str(msg)
        print(str(msg))
        self.msgs.append(message) 
        self.area.insertPlainText(message)       


if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    exit_code = app.exec_()
    #a.thread.stop()
    #a.thread.terminate()
    sys.exit()