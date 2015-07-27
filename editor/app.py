# coding=utf-8
__author__ = 'chengche'

import wx
from view.mainframe import MainFrame


class Editor(wx.App):
    def OnInit(self):
        main_frame = MainFrame(None, "Markdown Editor")
        main_frame.Show()
        return True