from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication, QLabel, QMenu, QAction, QHBoxLayout, QTextEdit
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
    def __init__(self):
        super().__init__()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        self.MainWin()  # 设置主窗口属性
        self.layout_main()  # 进行布局
        self.Vars()  # 初始化变量

        self.pix_start = None  # 初始化拼图状态

        self.Puzzle_lab(self.Puzzle_lab_Name)  # 绘制拼图

    def Vars(self):
        self.clicked_count = 0  # 判断点击行为
        self.Puzzle_lab_Name = "希儿"  # 默认拼图
        self.index_array_verify = 0   #当前拼图状态列表的下标
        self.index_x = None   #存储第一个点击的拼图的位置
        self.index_y = None   #存储第二个点击的拼图的位置
        self.a = None   #存储第一个点击的拼图
        self.b = None   #存储第二个点击的拼图
        self._data = data(1)

    def MainWin(self):
        self.resize(500, 300)
        self.setMaximumSize(500, 300)
        self.setWindowTitle("拼图游戏")

    def contextMenu(self, point):
        menu = QMenu()
        pix_To_replace = QMenu("其他拼图", self)

        # targgered=self.pix_other_Bronya_replace 为连接槽的另一种方法,详见下面的代码
        pix_other_Bronya = QAction(
            "布洛妮娅", pix_To_replace, triggered=self.pix_other_Bronya_replace)
        pix_other_SeeleVollerei = QAction(
            "希儿", pix_To_replace, triggered=self.pix_other_SeeleVollerei_replace)
        pix_other_Theresa = QAction(
            "德丽莎", pix_To_replace, triggered=self.pix_other_Theresa_replace)

        pix_To_replace.addAction(pix_other_Theresa)
        pix_To_replace.addAction(pix_other_Bronya)
        pix_To_replace.addAction(pix_other_SeeleVollerei)
        pix_other_BronyaAndSeele = QAction(
            "布洛妮娅and希儿", pix_To_replace, triggered=self.pix_other_BronyaAndSeele_replace)

        pix_To_replace.addAction(pix_other_BronyaAndSeele)

        pix_other_FuhHua = QAction(
            "符华", pix_To_replace, triggered=self.pix_other_FuhHua_replace)

        pix_To_replace.addAction(pix_other_FuhHua)

        pix_To_shuffle = QAction("打乱拼图", self)
        pix_To_reset_puzzle = QAction("重置当前状态", self, triggered=self.to_reset)
        pix_To_reset = QAction("还原拼图", self)
        pix_To_show_result = QAction("显示答案", self)
        show_description = QAction("显示说明", self)

        pix_To_reset_puzzle.triggered.connect(self.to_reset)
        pix_To_reset_puzzle.triggered.connect(
            lambda: self.pix_shuffle(self.pix_start))

        pix_To_shuffle.triggered.connect(self.to_shuffle)
        pix_To_shuffle.triggered.connect(
            lambda: self.pix_shuffle(self.pix_start))

        pix_To_reset.triggered.connect(
            lambda: self.pix_shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8]))
        pix_To_reset.triggered.connect(self.description)
        pix_To_reset.triggered.connect(self.cls_result)

        pix_To_show_result.triggered.connect(self.show_result)
        show_description.triggered.connect(self.description)

        menu.addAction(pix_To_shuffle)
        menu.addAction(pix_To_reset_puzzle)
        menu.addAction(pix_To_reset)
        menu.addAction(pix_To_show_result)
        menu.addAction(show_description)
        menu.addMenu(pix_To_replace)

        menu.exec_(self.mapToGlobal(point))

    def to_reset(self):
        self.pix_start = self._data.array_buffer[self.index_array_verify]
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass

    def pix_other_FuhHua_replace(self):
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass
        self.Puzzle_lab_Name = "_1符华"
        self.Puzzle_lab(self.Puzzle_lab_Name)  # 更新拼图

    def pix_other_BronyaAndSeele_replace(self):
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass
        self.Puzzle_lab_Name = "布洛妮娅and希儿"
        self.Puzzle_lab(self.Puzzle_lab_Name)  # 更新拼图

    def pix_other_Theresa_replace(self):
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass
        self.Puzzle_lab_Name = "_1德丽莎"
        self.Puzzle_lab(self.Puzzle_lab_Name)  # 更新拼图

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
                if self.grid_labout.getItemPosition(index)[:2] == self.grid_labout.getItemPosition(self.grid_labout.indexOf(self.lab_11))[:2]:
                    self.setWindowTitle("再点击一下移动")
                    self.a = object_self
                    self.index_x = self.grid_labout.getItemPosition(index)[:2]
                else:
                    self.setWindowTitle("只可以移动带红点的拼图")
                    self.clicked_count -= 1
            elif self.clicked_count % 2 == 0:
                self.setWindowTitle("已移动")
                self.b = object_self
                self.index_y = self.grid_labout.getItemPosition(index)[:2]
                self.movePix()

            object_self = None
        else:
            self.setWindowTitle("请点击拼图")

    def cls_result(self):
        self.index_array_verify = 0

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
        self.grid_labout = QGridLayout()

        HLayout = QHBoxLayout()

        self.txt_line = QTextEdit(self)
        self.txt_line.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.txt_line.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        HLayout.addLayout(self.grid_labout, 3)
        HLayout.addWidget(self.txt_line)

        self.grid_labout.setSpacing(4)
        self.setLayout(HLayout)

        self.description()  # 初始化说明

    def movePix(self):

        if self.index_y in self.movable_pix(self.index_x):
            self.grid_labout.addWidget(self.a, *(self.index_y))
            self.grid_labout.addWidget(self.b, *(self.index_x))
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
        self.description()
        self.index_array_verify = list(range(1, len(self._data.array_buffer)))[
            shuffle_index % (len(self._data.array_buffer)-1)]
        shuffle_index += 1
        self.pix_start = self._data.array_buffer[self.index_array_verify]
        if self.clicked_count % 2 == 1:
            self.clicked_count -= 1
        elif self.clicked_count % 2 == 0:
            pass

    def show_result(self):
        try:
            self.txt_line.setText(
                str(self._data._result[self.index_array_verify]).strip("[]"))
        except AttributeError:
            self.txt_line.setText("请先打乱拼图。")

    def description(self):
        self.txt_line.setText('''说明：
   只可以移动相邻的拼图。
   目的是将打乱后的图片还原成原始状态。
   右键有更多功能。
   只可以移动带红点的拼图。

   注：每次打乱都是随机的，多打乱几次可能会刷到相同的打乱状态。 
        
        
        ''')


if __name__ == "__main__":

    app = QApplication([])
    puzzle = Puzzle()
    puzzle.show()
    app.exec_()
