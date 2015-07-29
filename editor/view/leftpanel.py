# coding=utf-8
__author__ = 'chengche'

import os
import wx

from editor.model.post import *
from editor.model.config import *
from addpost import AddPostDialog
import wx.propgrid as wxpg


class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SIMPLE_BORDER | wx.TAB_TRAVERSAL)

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

        self.load_config()

    def on_add_post_btn_click(self, event):
        dlg = AddPostDialog(self)
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            dlg.property_edit.sync_property()
            post = dlg.property_edit.post
            post.file_path = os.path.join(global_config.root_path, "_posts", post.file_path)
            dlg.property_edit.post.save()
            self.update_post_list(global_config.root_path)
        dlg.Destroy()

    def on_setting_btn_click(self, event):
        dlg = SettingDialog(self, -1, "Setting", root_path=global_config.root_path)
        dlg.ShowModal()
        dlg.Destroy()

    def set_root_path(self, root_path):
        if os.path.exists(root_path):
            global_config.root_path = root_path
            self.update_post_list(root_path)

    def update_post_list(self, root_path):
        self.post_list_box.Clear()
        for post in global_post_manager.post_list:
            title = post.property.get('title', post.file_name)
            self.post_list_box.Append(title, post)

    def load_config(self):
        self.set_root_path(global_config.root_path)


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

        self.property_grid = wxpg.PropertyGrid(self)
        self.update_property_grid()
        sizer.Add(self.property_grid, 1, wx.EXPAND | wx.ALL)

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        btn_sizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btn_sizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.on_ok, btn)
        btn.SetDefault()
        btn_sizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn_sizer.AddButton(btn)
        btn_sizer.Realize()

        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def update_property_grid(self):
        self.property_grid.Append(wxpg.DirProperty("Root Path", value=global_config.root_path))
        self.property_grid.Append(wxpg.StringProperty("Access Key", value=global_config.access_key))
        self.property_grid.Append(wxpg.StringProperty("Secret Key", value=global_config.secret_key))
        self.property_grid.Append(wxpg.StringProperty("Domain", value=global_config.domain_name))
        self.property_grid.Append(wxpg.StringProperty("Bucket Name", value=global_config.bucket_name))

    def on_ok(self, event):
        property_list = self.property_grid.GetPropertyValues(as_strings=True)

        global_config.root_path = property_list.get('Root Path', '')
        global_config.access_key = property_list.get('Access Key', '')
        global_config.secret_key = property_list.get('Secret Key', '')
        global_config.domain_name = property_list.get('Domain', '')
        global_config.bucket_name = property_list.get('Bucket Name', '')

        event.Skip(True)