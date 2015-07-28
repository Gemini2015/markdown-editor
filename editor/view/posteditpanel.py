# coding=utf-8
__author__ = 'chengche'

import wx
from posteditctl import PostEditCtl
from propertyedit import PropertyEdit


class PostEditPanel(wx.Panel):
    def __init__(self, parent, post, mainframe):
        wx.Panel.__init__(self, parent)

        self.post = post
        self.mainframe = mainframe

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.edit = PostEditCtl(self, post)
        sizer.Add(self.edit, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        btn = wx.Button(self, label="Save")
        self.Bind(wx.EVT_BUTTON, self.on_save_post, btn)
        hbox.Add(btn)

        btn = wx.Button(self, label="Preview")
        self.Bind(wx.EVT_BUTTON, self.on_update_preview, btn)
        hbox.Add(btn)

        btn = wx.Button(self, label="Meta")
        self.Bind(wx.EVT_BUTTON, self.on_set_meta, btn)
        hbox.Add(btn)

        btn = wx.Button(self, label="Image")
        self.Bind(wx.EVT_BUTTON, self.on_manage_image, btn)
        hbox.Add(btn)

        sizer.Add(hbox, 0, wx.ALIGN_CENTER | wx.ALL)

        self.SetSizer(sizer)

    def on_save_post(self, event):
        if not self.is_modified():
            return
        self.post.content = self.edit.GetText()
        self.post.save()
        self.edit.SetModified(False)

    def on_update_preview(self, event):
        self.mainframe.update_markdown_preview(self)

    def on_set_meta(self, event):
        win = PropertyPopupWindow(self, self.post, wx.SIMPLE_BORDER)

        btn = event.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

    def on_manage_image(self, event):
        pass

    def is_modified(self):
        return self.edit.is_modified()

    def get_markdown_preview(self):
        return self.edit.get_markdown_preview()


class PropertyPopupWindow(wx.PopupTransientWindow):
    def __init__(self, parent, post, style):
        wx.PopupTransientWindow.__init__(self, parent, style)

        self.post = post
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.property_edit = PropertyEdit(self, post, False)
        sizer.Add(self.property_edit, 1, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)
        self.Fit()