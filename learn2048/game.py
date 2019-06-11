from enum import Enum
import random


class Action(Enum):
  """Game Actions"""
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3


class Board:
  def __init__(self, *, size=(4, 4)):
    width, height = size
    total_size = width * height
    self.size = width, height, total_size
    # initialize board with two popup
    self._board = [0] * total_size
    for i in random.sample(range(total_size), k=2):
      self._board[i], = random.choices([1, 2], [.9, .1])

  def _move(self, action: Action):
    """
    perform an `action` to the current game board
    return a _new_ game board and the score correspond to the action
    """

    def flip_horizontal(board):
      """flip game board horizontally"""
      width, _, total_size = self.size
      return [
          x for i in range(0, total_size, width)
          for x in board[i:i + width][::-1]
      ]

    def transpose(board):
      """transpose game board"""
      width, height, total_size = self.size
      self.size = height, width, total_size
      return [
          board[i + c] for c in range(width)
          for i in range(0, total_size, width)
      ]

    def move_right(board):
      """slide game board to right"""
      width, _, total_size = self.size
      board_, score = [], 0
      for row in [board[i:i + width] for i in range(0, total_size, width)]:
        # `buf`: nonzero elements of `row`
        row_, buf = [], [x for x in row if x]
        while buf:
          x = buf.pop()
          # merge
          if buf and x == buf[-1]:
            buf.pop()
            x += 1
            score += 1 << x
          row_ += [x]
        board_ += [0] * (width - len(row_))
        board_ += row_[::-1]
      return board_, score

    board = self._board
    if action == Action.UP:
      board = transpose(board)
      board = flip_horizontal(board)
      board, score = move_right(board)
      board = flip_horizontal(board)
      board = transpose(board)
      return board, score
    elif action == Action.DOWN:
      board = transpose(board)
      board, score = move_right(board)
      board = transpose(board)
      return board, score
    elif action == Action.LEFT:
      board = flip_horizontal(board)
      board, score = move_right(board)
      board = flip_horizontal(board)
      return board, score
    elif action == Action.RIGHT:
      return move_right(board)
    else:
      raise Exception('Illegal Action')

  def _popup(self):
    """popup a grid of `2` or `4` in `self._board`"""
    board = self._board
    index = [i for i, x in enumerate(board) if x == 0]
    if index:
      idx = random.choice(index)
      board[idx], = random.choices([1, 2], [.9, .1])

  def _check_done(self, board):
    """check if `board` has done"""
    for action in Action:
      if self._move(action)[0] != board:
        return False
    return True

  def __str__(self):
    width, height, total_size = self.size
    bar = '+' + '-' * (6 * width) + '+'
    lines = [bar] + [
        '|' + ''.join('{0:6d}'.format((1 << x) & -2) for x in row) + '|' for
        row in [self._board[r:r + width] for r in range(0, total_size, width)]
    ] + [bar]
    return '\n'.join(lines)

  def step(self, action: Action):
    board, score = self._move(action)
    done = self._check_done(board)
    if board != self._board:
      self._board = board
      self._popup()
    return score, done


class Game2048Env:
  """2048 Game Environment"""
  metadata = {'render.modes': ['human', 'ansi']}

  def __init__(self, *, size=(4, 4)):
    self.size = size
    self._board = Board(size=size)
    self._score = 0
    self._viewer = None

  def step(self, action: Action):
    score, done = self._board.step(action)
    self._score += score
    return self._board, self._score, done, {}

  def reset(self):
    self._board = Board(size=self.size)
    self._score = 0
    return self._board

  def render(self, mode='human'):
    if mode == 'ansi':
      return self._board
    elif mode == 'human':
      if self._viewer is None:
        from learn2048.gui import GuiViewer
        self._viewer = GuiViewer()
      else:
        self._viewer.update_grids(self._board, self._score)
