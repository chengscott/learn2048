from learn2048.game import Action, Board
import tkinter
from tkinter import Frame, Label, CENTER

BACKGROUND_COLOR = '#92877d'
BACKGROUND_COLOR_CELL_EMPTY = '#9e948a'

GRID_SIZE = 100
GRID_PADDING = 10

FONT = ('Verdana', 40, 'bold')

BACKGROUND_COLOR_LIST = [
    '',
    '#eee4da',
    '#ede0c8',
    '#f2b179',
    '#f59563',
    '#f67c5f',
    '#f65e3b',
    '#edcf72',
    '#edcc61',
    '#edc850',
    '#edc53f',
    '#edc22e',
    '#eee4da',
    '#edc22e',
    '#f2b179',
    '#f59563',
    '#f67c5f',
]

CELL_COLOR_LIST = [
    '',
    '#776e65',
    '#776e65',
    '#f9f6f2',
    '#f9f6f2',
    '#f9f6f2',
    '#f9f6f2',
    '#f9f6f2',
    '#f9f6f2',
    '#f9f6f2',
    '#f9f6f2',
    '#f9f6f2',
    '#776e65',
    '#f9f6f2',
    '#776e65',
    '#776e65',
    '#f9f6f2',
]


class GuiViewer(Frame):
  """2048 Game Grid"""

  def __init__(self, *, size=(4, 4), play=False):
    super().__init__()
    self.size = size
    self.play = play

    # frame
    self.grid()
    self.master.title('2048')
    self._grids = []
    self._init_grids()
    if play:
      self.master.bind('<Key>', self.key_down)
      self._board = Board(size=size)
      self.update_grids(self._board)
      self.mainloop()

  def key_down(self, event):
    key = event.keysym.lower()
    action = None
    if key == 'up' or key == 'w':
      action = Action.UP
    elif key == 'down' or key == 's':
      action = Action.DOWN
    elif key == 'left' or key == 'a':
      action = Action.LEFT
    elif key == 'right' or key == 'd':
      action = Action.RIGHT
    else:
      return
    if action:
      _, done = self._board.step(action)
      self.update_grids(self._board)

  def _init_grids(self):
    width, height = self.size
    # background
    background = Frame(self, bg=BACKGROUND_COLOR, width=width, height=height)
    background.grid()
    # grids
    for i in range(width):
      row = []
      for j in range(height):
        cell = Frame(background,
                     bg=BACKGROUND_COLOR_CELL_EMPTY,
                     width=GRID_SIZE,
                     height=GRID_SIZE)
        cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
        label = Label(master=cell,
                      text='',
                      bg=BACKGROUND_COLOR_CELL_EMPTY,
                      justify=CENTER,
                      font=FONT,
                      width=5,
                      height=3)
        label.grid()
        row += [label]
      self._grids += row

  def update_grids(self, board: Board):
    grids = self._grids
    for i, x in enumerate(board._board):
      if x == 0:
        grids[i].configure(text='', bg=BACKGROUND_COLOR_CELL_EMPTY)
      else:
        grids[i].configure(text=str(1 << x),
                           bg=BACKGROUND_COLOR_LIST[x],
                           fg=CELL_COLOR_LIST[x])
    self.update_idletasks()
    self.update()