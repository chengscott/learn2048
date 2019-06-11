from learn2048.game import Action, Board
import tkinter
from tkinter import Frame, Label, CENTER

BACKGROUND_COLOR_CELL_EMPTY = '#9e948a'


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
      self._score = 0
      self.update_grids(self._board, self._score)
      self.mainloop()

  def key_down(self, event):
    """capture keydown events"""
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
      score, _ = self._board.step(action)
      self._score += score
      self.update_grids(self._board, self._score)

  def _init_grids(self):
    """initialize game grids"""
    TOP_BG_COLOR = '#faf8ef'
    SCORE_BG_COLOR = '#bbada0'
    GRID_SIZE = 100
    GRID_PADDING = 10
    FONT = ('Verdana', 20, 'bold')
    FONT_TITLE = ('Verdana', 50, 'bold')

    width, height = self.size
    ## self frame
    self.configure(bg=TOP_BG_COLOR)
    ## top frame
    top = Frame(self, bg=TOP_BG_COLOR)
    top.grid()
    # 2048 label
    Label(top,
          text='2048',
          height=2,
          fg='#776e65',
          bg=TOP_BG_COLOR,
          padx=100,
          font=FONT_TITLE).grid(row=0, column=0)
    ## score frame
    score_box = Frame(top, bg=SCORE_BG_COLOR, padx=10, width=100)
    score_box.grid(row=0, column=1, padx=20, pady=20)
    # SCORE label
    Label(score_box,
          text='SCORE',
          fg='#eee4da',
          bg=SCORE_BG_COLOR,
          padx=10,
          font=FONT).grid(row=0, column=1)
    # display score
    score_label = Label(score_box,
                        text='0',
                        fg='#ffffff',
                        bg=SCORE_BG_COLOR,
                        font=FONT)
    score_label.grid(row=1, column=1)
    self._score_label = score_label

    ## background frame
    background = Frame(self, bg='#92877d', width=width, height=height)
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

  def update_grids(self, board: Board, score: int):
    """update game grids"""
    bg_colors = (
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
    )
    cell_colors = (
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
    )

    self._score_label.configure(text=str(score))
    grids = self._grids
    for i, x in enumerate(board._board):
      if x == 0:
        grids[i].configure(text='', bg=BACKGROUND_COLOR_CELL_EMPTY)
      else:
        grids[i].configure(text=str(1 << x),
                           bg=bg_colors[x],
                           fg=cell_colors[x])
    self.update_idletasks()
    self.update()