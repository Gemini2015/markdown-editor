# coding=utf-8
__author__ = 'chengche'

from editor.app import Editor


def main():
    app = Editor(False)
    app.MainLoop()

if __name__ == '__main__':
    main()