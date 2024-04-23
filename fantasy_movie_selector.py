import sys
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import random

class CRandom:
    @staticmethod
    def random_index(stack_size):
        return random.randint(0, stack_size - 1)

class CReadFile:
    def __init__(self):
        self.stack_odd = []
        self.stack_even = []

    def read_file(self, filename):
        with open(filename, 'r') as file:
            for i, line in enumerate(file):
                movie_title = line.strip()
                if i % 2 == 0:
                    self.stack_even.append(movie_title)
                else:
                    self.stack_odd.append(movie_title)

class CFantasyMovies(QObject):
    surpriseMovieChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.stack_odd = []
        self.stack_even = []
        self.stack_temp = []
        self.current_stack = None

    @pyqtSlot(int)
    def on_number_entered(self, number):
        if number % 2 == 0:
            self.current_stack = self.stack_even
        else:
            self.current_stack = self.stack_odd
        if not self.current_stack:
            self.surpriseMovieChanged.emit("no other available films")
            return
        random_index = CRandom.random_index(len(self.current_stack))
        selected_movie = self.current_stack.pop(random_index)
        self.move_to_temp_stack(random_index)
        self.surpriseMovieChanged.emit(selected_movie)

    def move_to_temp_stack(self, index):
        while self.current_stack:
            if len(self.stack_temp) <= index:
                self.stack_temp.append(self.current_stack.pop())
            else:
                break

    def move_back_to_original_stack(self):
        while self.stack_temp:
            self.current_stack.append(self.stack_temp.pop())

# Example usage:
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    fantasy_movies = CFantasyMovies()

    engine.rootContext().setContextProperty("fantasyMovies", fantasy_movies)
    engine.load(QUrl.fromLocalFile('main.qml'))

    sys.exit(app.exec_())
