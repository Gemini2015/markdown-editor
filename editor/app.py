# coding=utf-8
__author__ = 'chengche'

import wx
from view.mainframe import MainFrame

from editor.model.config import *
from editor.model.post import *
from editor.model.image import *


class Editor(wx.App):
    def OnInit(self):

        # load config
        global_config.load()

        # load post list
        global_post_manager.load()

        # load image cache
        global_image_manager.load()

        main_frame = MainFrame(None, "Markdown Editor")
        main_frame.Show()
        return True

    def OnExit(self):
        # save config
        global_config.save()

        # save image cache
        global_image_manager.save()