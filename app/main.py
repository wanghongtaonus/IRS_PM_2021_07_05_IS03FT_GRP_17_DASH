# import fm
# if __name__ == '__main__':
#     all_symptoms=fm.search_by_id(1)
#     # new_dic=[v for v in symptoms.keys()]
#     # print(symptoms)
#     # print(new_dic[2:134])
#     pre_symptoms=[]
#     for v in list(all_symptoms.keys())[2:134]:
#         if(all_symptoms[v]==1):
#             pre_symptoms.append(v)
#     print(pre_symptoms)
#     illness=all_symptoms['illness']
#     print(illness)
#     print(pre_symptoms[v] for v in range(0,2))

#!/bin/bash
import sys, hashlib
import qdarkstyle
sys.path.append("../fm")
import fm

from PyQt5.QtGui import  QPixmap,QScreen
from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton, 
                            QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,
                            QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QRadioButton,
                            QTreeWidgetItem, QDesktopWidget)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # set windows name
        self.setWindowTitle("Search illness for doctors")

        # set status bar
        self.status = self.statusBar()
        self.status.showMessage("i am at main page～")

        # set window size
        self.resize(600, 400)

        # initial window located at center
        self.center()

        # set the window opacity
        self.setWindowOpacity(0.9) 

        # set windows style
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # set global layout, left and right show
        pagelayout = QGridLayout()

        # left initial layout
        # create left inital widgets
        top_left_frame = QFrame(self)  
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        #　left button vertical
        button_layout = QVBoxLayout(top_left_frame)

        # search　button
        search_btn = QPushButton(top_left_frame)
        search_btn.setFixedSize(100, 30), search_btn.setText("search")
        button_layout.addWidget(search_btn)
        # view　button
        friend_btn = QPushButton(top_left_frame)
        friend_btn.setFixedSize(100, 30), friend_btn.setText("view")
        button_layout.addWidget(friend_btn) 
        # exit button
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(100, 30), quit_btn.setText("exit")
        button_layout.addWidget(quit_btn)
        
        # 左下角为空白 必须要有布局，才可以显示至内容中
        bottom_left_frame = QFrame(self)
        blank_label = QLabel(bottom_left_frame)
        blank_layout = QVBoxLayout(bottom_left_frame)
        blank_label.setText("illness for doctor")
        blank_label.setFixedHeight(20)
        blank_layout.addWidget(blank_label)
        self.webEngineView = QWebEngineView(bottom_left_frame)
        self.webEngineView.close()
        blank_layout.addWidget(self.webEngineView)
        
        # 右侧开始布局 对应按钮布局
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # 右边显示为stack布局
        self.right_layout = QStackedLayout(right_frame)


        # search page based on id and name 
        self.search_id = QLineEdit(right_frame)
        self.search_id.setPlaceholderText("please input search id for patient：")
        self.search_id.setFixedWidth(400)
        search_name = QLineEdit(right_frame)
        search_name.setPlaceholderText("please input search name for patient ：")
        search_name.setFixedWidth(400)
        
        
        search_confirm_btn = QPushButton("submit")
        search_confirm_btn.setFixedSize(100, 30)
        search_layout = QVBoxLayout()
        search_widget = QWidget(right_frame)
        search_widget.setLayout(search_layout)
        search_layout.addWidget(self.search_id)
        search_layout.addWidget(search_name)
        
        
        search_layout.addWidget(search_confirm_btn)
        self.right_layout.addWidget(search_widget)

        # 建模园地 使用 TreeView　水平布局　应该读取数据库
        self.friend_tree = QTreeWidget(right_frame)
        self.friend_tree.setColumnCount(5)  # 一列 
        self.friend_tree.setHeaderLabels(['name', 'id', 'symptoms','illness','threapy']) # 设置标题
        root = QTreeWidgetItem(self.friend_tree) # 设置根节点
        self.friend_tree.setColumnWidth(2, 400) # 设置宽度s
        # 设置子节点
        root.setText(0, "name") # 0 表示位置
        root.setText(1, "id")
        root.setText(2, "symptoms")
        root.setText(3, "illness")
        root.setText(4, "网址")
        self.child_name = QTreeWidgetItem(root)
        
        # self.child_name.setText(0, "name")

        # child_name = QTreeWidgetItem(self.child_name)
        # child_name.setText(1, "1")
        # child_name.setText(4, "https://muyuuuu.github.io")
        

        # child_name = QTreeWidgetItem(child_name)
        # child_name.setText(1, "wanghongtao")
        # child_name.setText(2, "https://muyuuuu.github.io")
        # child_17 = QTreeWidgetItem(root)
        # child_17.setText(0, "17级")

        # child_lqr = QTreeWidgetItem(child_17)
        # child_lqr.setText(1, "李秋然")
        # child_lqr.setText(2, "https://dgimoyeran.github.io")

        friend_widget = QWidget(right_frame)
        friend_layout = QVBoxLayout()
        friend_widget.setLayout(friend_layout)
        friend_layout.addWidget(self.friend_tree)
        self.right_layout.addWidget(friend_widget)

        self.url = ''  #　后期会获取要访问的url
        

        # 三分界面，可拖动
        self.splitter1 = QSplitter(Qt.Vertical)
        top_left_frame.setFixedHeight(250)
        self.splitter1.addWidget(top_left_frame)
        self.splitter1.addWidget(bottom_left_frame)

        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        #　添加右侧的布局
        self.splitter2.addWidget(right_frame)

        # 窗口部件添加布局
        widget = QWidget()
        pagelayout.addWidget(self.splitter2)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        # 函数功能区
        search_btn.clicked.connect(self.show_search_page)
        search_confirm_btn.clicked.connect(self.show_friend_page)
        friend_btn.clicked.connect(self.show_friend_page)
        self.friend_tree.clicked.connect(self.show_firend_web)
        quit_btn.clicked.connect(self.quit_act)

    def init(self):
        # 刚开始要管理浏览器，否则很丑
        self.webEngineView.close()
        # 注意先后顺序，resize　在前面会使代码无效
        self.splitter1.setMinimumWidth(150)
        self.splitter2.setMinimumWidth(250)
        self.resize(600, 400)

    # TreeView 的点击事件
    def show_firend_web(self):
        item = self.friend_tree.currentItem()
        if item.text(4)[:4] == "http":
            self.url = item.text(4)
            self.resize(1800, 1200)
            self.webEngineView.show()
            self.splitter1.setFixedWidth(1400)
            self.webEngineView.load(QUrl(self.url))

    # display tree structure
    def show_friend_page(self):
        print(self.search_id.text())
        all_symptoms=fm.search_by_id(int(self.search_id.text()))
        print(all_symptoms)
        pre_symptoms=[]
        for v in list(all_symptoms.keys())[2:134]:
            if(all_symptoms[v]==1 ):
                pre_symptoms.append(v)
        name=all_symptoms['name']
        id=all_symptoms['id']
        print(pre_symptoms)
        illness=all_symptoms['illness']
        self.child_name.setText(0, str(name))
        self.child_name.setText(1, str(id))
        self.child_name.setText(2,str(pre_symptoms))
        self.child_name.setText(3,str(illness))
        self.child_name.setText(4,"https://www.cup.edu.cn/medical/disease/commondisease/16419.htm")
        primary_screen = QApplication.primaryScreen()
        sshot = primary_screen.grabWindow(0)
        sshot.save('sshot.pdf')
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(1)

    # display search page
    def show_search_page(self):
        self.init()
        self.center()
        self.right_layout.setCurrentIndex(0)


    # set windows location as center
    def center(self):
        '''
        获取桌面长宽
        获取窗口长宽
        移动
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # 退出按钮 有信息框的提示　询问是否确认退出
    def quit_act(self):
        # sender 是发送信号的对象
        sender = self.sender()
        print(sender.text() + '键被按下')
        qApp = QApplication.instance()
        qApp.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())