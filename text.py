import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class CRandom(QObject):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_random_index(size):
        return random.randint(0, size - 1)


class CFantasyMovies(QObject):
    movie_selected = pyqtSignal(str)

    def __init__(self, stack_odd, stack_even):
        super().__init__()
        self.stack_odd = stack_odd
        self.stack_even = stack_even
        self.stack_temp = []

    @pyqtSlot(int)
    def process_number(self, number):
        if number % 2 == 0:
            if self.stack_even:
                index = CRandom.get_random_index(len(self.stack_even))
                self.move_top_to_temp(self.stack_even)
                selected_movie = self.stack_even.pop(index)
                self.movie_selected.emit(selected_movie)
                self.move_temp_to_stack(self.stack_even)
            else:
                self.process_empty_stack(self.stack_odd)
        else:
            if self.stack_odd:
                index = CRandom.get_random_index(len(self.stack_odd))
                self.move_top_to_temp(self.stack_odd)
                selected_movie = self.stack_odd.pop(index)
                self.movie_selected.emit(selected_movie)
                self.move_temp_to_stack(self.stack_odd)
            else:
                self.process_empty_stack(self.stack_even)

    def move_top_to_temp(self, stack):
        if stack:
            self.stack_temp.append(stack[-1])

    def move_temp_to_stack(self, stack):
        if self.stack_temp:
            stack.append(self.stack_temp.pop())

    def process_empty_stack(self, stack):
        if not stack:
            self.movie_selected.emit("No other available films")


class CReadFile:
    def __init__(self):
        self.stack_odd = []
        self.stack_even = []

    def read_file(self, filename):
        with open(filename, 'r') as file:
            for index, line in enumerate(file):
                if index % 2 == 0:
                    self.stack_even.append(line.strip())
                else:
                    self.stack_odd.append(line.strip())


class GUI(QWidget):
    def __init__(self, stack_odd, stack_even):
        super().__init__()
        self.stack_odd = stack_odd
        self.stack_even = stack_even
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Fantasy Movies')
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel('Enter a number:')
        self.input_text = QLineEdit()
        self.ok_button = QPushButton('OK')
        self.quit_button = QPushButton('Quit')
        self.result_label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.quit_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.ok_button_clicked)
        self.quit_button.clicked.connect(self.close)

    def ok_button_clicked(self):
        number = int(self.input_text.text())
        fantasy_movies.process_number(number)

    @pyqtSlot(str)
    def update_result_label(self, movie_title):
        self.result_label.setText(movie_title)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    read_file = CReadFile()
    read_file.read_file('input.txt')

    fantasy_movies = CFantasyMovies(read_file.stack_odd, read_file.stack_even)

    gui = GUI(read_file.stack_odd, read_file.stack_even)
    fantasy_movies.movie_selected.connect(gui.update_result_label)

    gui.show()

    sys.exit(app.exec_())
