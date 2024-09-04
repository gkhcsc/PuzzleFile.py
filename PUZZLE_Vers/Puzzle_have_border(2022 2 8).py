'''
用的时候记得把它放到上一级文件夹里，因为还要依赖其他文件
'''

from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QLabel, QMenu, QAction, QHBoxLayout, QTextEdit,QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from data_buffer import data
object_self = None
shuffle_index = 0


class PuzzleLable(QLabel):
    def mousePressEvent(self, evt) -> None:
        global object_self
        object_self = self
        evt.ignore()


class Puzzle(QWidget):
    def __init__(self, pix_start):
        super().__init__()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.resize(590, 332)
        self.setMaximumSize(590, 332)




        self.grid_labout = QGridLayout()       
        self.pix_start = pix_start
        self.clicked_count = 0  # 判断点击行为
        self.Puzzle_lab_Name = "希儿"  #默认拼图

        self.x = None
        self.y = None
        self.a = None
        self.b = None
        self._data = data()

        self.Puzzle_lab(self.Puzzle_lab_Name)  
        self.layout_main()
        self.description()
    def closeEvent(self, a0) -> None:
        print(self.geometry())
    def contextMenu(self, point):
        menu = QMenu()
        pix_To_replace = QMenu("其他拼图", self)

        pix_other_Bronya = QAction("布洛妮娅", pix_To_replace)
        pix_other_SeeleVollerei = QAction("希儿", pix_To_replace)
        pix_To_replace.addAction(pix_other_Bronya)
        pix_To_replace.addAction(pix_other_SeeleVollerei)
        pix_other_Bronya.triggered.connect(self.pix_other_Bronya_replace)
        pix_other_SeeleVollerei.triggered.connect(
            self.pix_other_SeeleVollerei_replace)

        pix_To_shuffle = QAction("打乱拼图", self)
        pix_To_reset = QAction("还原拼图", self)
        pix_To_show_result = QAction("显示答案", self)
        show_description = QAction("显示说明", self)

        pix_To_shuffle.triggered.connect(self.to_shuffle)
        pix_To_shuffle.triggered.connect(
            lambda: self.pix_shuffle(self.pix_start))

        pix_To_reset.triggered.connect(
            lambda: self.pix_shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8]))

        pix_To_show_result.triggered.connect(self.show_result)
        show_description.triggered.connect(self.description)

        menu.addAction(pix_To_shuffle)
        menu.addAction(pix_To_reset)
        menu.addAction(pix_To_show_result)
        menu.addAction(show_description)
        menu.addMenu(pix_To_replace)

        menu.exec_(self.mapToGlobal(point))

    def pix_other_Bronya_replace(self):
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass
        self.Puzzle_lab_Name = "Bronya"
        self.Puzzle_lab(self.Puzzle_lab_Name)

    def pix_other_SeeleVollerei_replace(self):
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass
        self.Puzzle_lab_Name = "希儿"
        self.Puzzle_lab(self.Puzzle_lab_Name)

    def mousePressEvent(self, evt) -> None:
        global object_self
        if type(object_self) == PuzzleLable and evt.button() == Qt.MouseButton.LeftButton:
            index = self.grid_labout.indexOf(object_self)
            self.clicked_count += 1
            if self.clicked_count % 2 == 1:
                self.setWindowTitle("再点击一下移动")
                self.a = object_self
                self.x = self.grid_labout.getItemPosition(index)[:2]
                self.a.setFrameShape(QFrame.Shape.Box)
                self.a.setFrameShadow(QFrame.Shadow.Raised)
                self.a.setStyleSheet("border-width: 1px;border-color: rgb(255, 0, 0);border-style: solid")

            elif self.clicked_count % 2 == 0:
                self.setWindowTitle("已移动")
                self.b = object_self
                self.y = self.grid_labout.getItemPosition(index)[:2]
                self.movePix()
                self.a.setFrameShape(QFrame.Shape.NoFrame)
                self.a.setStyleSheet("border-width: 0px;border-color: rgb(255, 255, 255);border-style: solid")
            object_self = None
        else:
            self.setWindowTitle("请点击拼图")

    def Puzzle_lab(self, name: str):
        self.lab_11 = PuzzleLable(self)
        self.lab_12 = PuzzleLable(self)
        self.lab_13 = PuzzleLable(self)
        self.lab_21 = PuzzleLable(self)
        self.lab_22 = PuzzleLable(self)
        self.lab_23 = PuzzleLable(self)
        self.lab_31 = PuzzleLable(self)
        self.lab_32 = PuzzleLable(self)
        self.lab_33 = PuzzleLable(self)

        pix_11 = QPixmap(f"img\Puzzle\{name}_01.png")
        pix_12 = QPixmap(f"img\Puzzle\{name}_02.png")
        pix_13 = QPixmap(f"img\Puzzle\{name}_03.png")
        pix_21 = QPixmap(f"img\Puzzle\{name}_04.png")
        pix_22 = QPixmap(f"img\Puzzle\{name}_05.png")
        pix_23 = QPixmap(f"img\Puzzle\{name}_06.png")
        pix_31 = QPixmap(f"img\Puzzle\{name}_07.png")
        pix_32 = QPixmap(f"img\Puzzle\{name}_08.png")
        pix_33 = QPixmap(f"img\Puzzle\{name}_09.png")

        self.lab_11.setPixmap(pix_11)
        self.lab_12.setPixmap(pix_12)
        self.lab_13.setPixmap(pix_13)
        self.lab_21.setPixmap(pix_21)
        self.lab_22.setPixmap(pix_22)
        self.lab_23.setPixmap(pix_23)
        self.lab_31.setPixmap(pix_31)
        self.lab_32.setPixmap(pix_32)
        self.lab_33.setPixmap(pix_33)

        self.grid_labout.addWidget(self.lab_11, 0, 0)
        self.grid_labout.addWidget(self.lab_12, 0, 1)
        self.grid_labout.addWidget(self.lab_13, 0, 2)
        self.grid_labout.addWidget(self.lab_21, 1, 0)
        self.grid_labout.addWidget(self.lab_22, 1, 1)
        self.grid_labout.addWidget(self.lab_23, 1, 2)
        self.grid_labout.addWidget(self.lab_31, 2, 0)
        self.grid_labout.addWidget(self.lab_32, 2, 1)
        self.grid_labout.addWidget(self.lab_33, 2, 2)

    def layout_main(self):

        HLayout = QHBoxLayout()

        self.txt_line = QTextEdit(self)
        self.txt_line.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txt_line.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        HLayout.addLayout(self.grid_labout, 3)
        HLayout.addWidget(self.txt_line)

        self.grid_labout.setSpacing(3)
        self.setLayout(HLayout)

    def movePix(self):
        if self.y in self.movable_pix(self.x):
            self.grid_labout.addWidget(self.a, *(self.y))
            self.grid_labout.addWidget(self.b, *(self.x))
        else:
            self.setWindowTitle("只可以移动相邻格")

    def movable_pix(self, index: int):
        movable_arr = []

        movable_arr.append(tuple(list([index[0]+1, index[1]])))
        movable_arr.append(tuple(list([index[0]-1, index[1]])))
        movable_arr.append(tuple(list([index[0], index[1]-1])))
        movable_arr.append(tuple(list([index[0], index[1]+1])))

        a = []
        for i in range(4):
            for j in movable_arr[i]:
                if j < 0:
                    a.append(movable_arr[i])
        for i in a:
            movable_arr.remove(i)
        return movable_arr

    def pix_shuffle(self, startList: list):
        x_axis = None
        y_axis = None
        for i in range(len(startList)):  # i 表示第几个拼图
            x_axis = startList.index(i) % 3
            y_axis = startList.index(i)//3
            if i == 0:
                self.grid_labout.addWidget(self.lab_11, y_axis, x_axis)
            elif i == 1:
                self.grid_labout.addWidget(self.lab_12, y_axis, x_axis)
            elif i == 2:
                self.grid_labout.addWidget(self.lab_13, y_axis, x_axis)
            elif i == 3:
                self.grid_labout.addWidget(self.lab_21, y_axis, x_axis)
            elif i == 4:
                self.grid_labout.addWidget(self.lab_22, y_axis, x_axis)
            elif i == 5:
                self.grid_labout.addWidget(self.lab_23, y_axis, x_axis)
            elif i == 6:
                self.grid_labout.addWidget(self.lab_31, y_axis, x_axis)
            elif i == 7:
                self.grid_labout.addWidget(self.lab_32, y_axis, x_axis)
            elif i == 8:
                self.grid_labout.addWidget(self.lab_33, y_axis, x_axis)

    def to_shuffle(self):
        global shuffle_index
        self.index_array_verify = list(range(0, len(self._data.array_buffer)))[
            shuffle_index % len(self._data.array_buffer)]
        shuffle_index += 1
        self.pix_start = self._data.array_buffer[self.index_array_verify]
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass

    def show_result(self):
        try :
            self.txt_line.setText(str(self._data._result[self.index_array_verify]))
        except AttributeError :
            self.txt_line.setText("请先打乱拼图。")

    def description(self):
        self.txt_line.setText('''说明：
   只可以移动相邻的拼图。
   目的是将打乱后的图片还原成原始状态。
   右键有更多功能。
   答案以左上角带红点的拼图为准。

   注：每次打乱都是随机的，多打乱几次可能会刷到相同的打乱状态。 
        
        
        ''')


if __name__ == "__main__":

    app = QApplication([])
    puzzle = Puzzle([])
    puzzle.show()
    app.exec_()
