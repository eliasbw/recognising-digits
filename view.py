from tkinter import *
from tkinter import ttk
import numpy as np

global value


class Cell:
    FILLED_COLOR_BG = "green"
    EMPTY_COLOR_BG = "white"
    FILLED_COLOR_BORDER = "green"
    EMPTY_COLOR_BORDER = "black"

    def __init__(self, master, x, y, size):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = False

    def _switch(self):
        """ Switch if the cell is filled or not. """
        self.fill = not self.fill

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master is not None:
            _fill = Cell.FILLED_COLOR_BG
            outline = Cell.FILLED_COLOR_BORDER

            if not self.fill:
                _fill = Cell.EMPTY_COLOR_BG
                outline = Cell.EMPTY_COLOR_BORDER

            x_min = self.abs * self.size
            x_max = x_min + self.size
            y_min = self.ord * self.size
            y_max = y_min + self.size

            self.master.create_rectangle(x_min, y_min, x_max, y_max, fill=_fill, outline=outline)


class CellGrid(Canvas):
    def __init__(self, master, nr_rows, nr_cols, cell_size, *args, **kwargs):

        Canvas.__init__(self, master, width=cell_size * nr_cols, height=cell_size * nr_rows, *args, **kwargs)
        self.height = nr_cols
        self.cell_size = cell_size

        self.grid = []
        for row in range(nr_rows):

            line = []
            for column in range(nr_cols):
                line.append(Cell(self, column, row, cell_size))

            self.grid.append(line)

        # memorize the cells that have been modified to avoid many switching of state during mouse motion.
        self.switched = []

        # bind click action
        self.bind("<Button-1>", self.handleMouseClick)
        # bind moving while clicking
        self.bind("<B1-Motion>", self.handleMouseMotion)
        # bind release button action - clear the memory of midified cells.
        self.bind("<ButtonRelease-1>", lambda event: self.switched.clear())

        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

    def _eventCoords(self, event):
        row = int(event.y / self.cell_size)
        column = int(event.x / self.cell_size)
        return row, column

    def handleMouseClick(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]
        cell._switch()
        cell.draw()
        # add the cell to the list of cell switched during the click
        self.switched.append(cell)

    def handleMouseMotion(self, event):
        row, column = self._eventCoords(event)
        cell = self.grid[row][column]

        if cell not in self.switched:
            cell._switch()
            cell.draw()
            self.switched.append(cell)

    def return_grid_values(self):
        global value
        values = np.array([np.array([int(cell.fill) for cell in col], dtype=float) for col in self.grid], dtype=float)
        value = values


def combined_functions(functions):
    for function in functions:
        function()


def create_view_input():
    global value
    app = Tk()
    frame = Frame(app)
    frame.pack()

    bottomframe = Frame(app)
    bottomframe.pack(side=TOP)

    grid = CellGrid(app, 16, 10, 20)
    grid.pack()

    # app.bind('<ButtonRelease-1>', lambda e: grid.return_grid_values())
    app.bind('<Escape>', lambda e: app.destroy())
    evaluate = Button(frame, text="Evaluate", fg="black", command=lambda: grid.return_grid_values())
    evaluate.pack(side=LEFT)

    close = Button(frame, text="Close", fg="black", command=lambda: app.destroy())
    close.pack(side=BOTTOM)

    app.mainloop()
    return value


if __name__ == '__main__':
    array = create_view_input()

