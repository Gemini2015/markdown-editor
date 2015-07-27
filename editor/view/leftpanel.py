# coding=utf-8
__author__ = 'chengche'

import os
import wx

from editor.model.post import Post
from editor.model.config import Config


class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)

        self.root_path = ""
        self.post_list = []
        self.post_list_box = wx.ListBox(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(self, label="Add Post")
        self.Bind(wx.EVT_BUTTON, self.on_add_post_btn_click, btn)
        sizer.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL)

        sizer.Add(self.post_list_box, 1, wx.EXPAND)

        btn = wx.Button(self, label="Setting")
        self.Bind(wx.EVT_BUTTON, self.on_setting_btn_click, btn)
        sizer.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL)

        self.SetSizer(sizer)

        # load config
        self.config = Config()
        self.config.load()
        self.load_config()

    def on_add_post_btn_click(self, event):
        pass

    def on_setting_btn_click(self, event):
        dlg = SettingDialog(None, -1, "Setting", root_path=self.root_path)
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            self.set_root_path(dlg.dir_path)
        dlg.Destroy()

    def set_root_path(self, root_path):
        post_path = os.path.join(root_path, "_posts")
        if os.path.exists(root_path) and os.path.exists(post_path):
            self.root_path = root_path
            self.update_post_list(post_path)

    def update_post_list(self, posts_path):
        if not os.path.exists(posts_path) or not os.path.isdir(posts_path):
            return
        self.post_list = []
        file_list = os.listdir(posts_path)
        for post_file in file_list:
            post_file_path = os.path.join(posts_path, post_file)
            if not os.path.isfile(post_file_path):
                continue
            post = Post(post_file_path)
            post.parse()
            self.post_list.append(post)
        self.post_list_box.Clear()
        for post in self.post_list:
            title = post.property.get('title', post.file_name)
            self.post_list_box.Append(title, post)

    def load_config(self):
        self.set_root_path(self.config.root_path)

    def save_config(self):
        self.config.root_path = self.root_path
        self.config.save()


class SettingDialog(wx.Dialog):
    def __init__(self, parent, id_no, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE, root_path=""):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.Create(parent, id_no, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Root Path")
        h_box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.dir_path = root_path
        self.text = wx.TextCtrl(self, -1, self.dir_path, size=(250, -1))
        h_box.Add(self.text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        browser = wx.Button(self, -1, "Browser")
        h_box.Add(browser, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.evt_button_click, browser)

        sizer.Add(h_box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 5)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        btn_sizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btn_sizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btn_sizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn_sizer.AddButton(btn)
        btn_sizer.Realize()

        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def evt_button_click(self, event):
        dlg = wx.DirDialog(self, "Choose a root dir", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.CenterOnParent()
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            self.dir_path = dlg.GetPath()
            self.text.WriteText(self.dir_path)
        dlg.Destroy()