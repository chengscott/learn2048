"""2048"""
__author__ = 'chengscott'
__version__ = '0.1'
f'Python >= 3.6 Required'
from learn2048.gui import GuiViewer
import argparse


def run_main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('-v',
                      '--version',
                      action='version',
                      version=f'learn2048 {__version__}')
  parser.add_argument('--width', default=4, type=int)
  parser.add_argument('--height', default=4, type=int)
  args = parser.parse_args()
  # GUI
  GuiViewer(size=(args.height, args.width), play=True)


if __name__ == '__main__':
  run_main()