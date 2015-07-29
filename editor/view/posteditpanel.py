# coding=utf-8
__author__ = 'chengche'

import wx
from posteditctl import PostEditCtl
from propertyedit import PropertyEdit
from editor.model.image import *
import wx.propgrid as wxpg
from addimage import AddImageDialog


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
        win = ImagePopupWindow(self, self.post, wx.SIMPLE_BORDER)

        btn = event.GetEventObject()
        pos = btn.ClientToScreen((0, 0))
        sz = btn.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()

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


class ImagePopupWindow(wx.PopupTransientWindow):
    def __init__(self, parent, post, style):
        wx.PopupTransientWindow.__init__(self, parent, style)

        self.post = post
        self.image_list = [] # global_image_manager.get_image_list(post)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.property_grid = wxpg.PropertyGrid(self)
        self.update_property_grid()
        sizer.Add(self.property_grid, 1, wx.EXPAND | wx.ALL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        btn = wx.Button(self, label="Add")
        self.Bind(wx.EVT_BUTTON, self.on_add_image, btn)
        hbox.Add(btn, 1, wx.CENTRE | wx.EXPAND)

        btn = wx.Button(self, label="Delete")
        self.Bind(wx.EVT_BUTTON, self.on_delete_image, btn)
        hbox.Add(btn, 1, wx.CENTRE | wx.EXPAND)

        sizer.Add(hbox, 0, wx.EXPAND)

        self.update_property_grid()

        self.SetSizer(sizer)
        self.Fit()

    def update_property_grid(self):
        self.image_list = global_image_manager.get_image_list(self.post)
        self.property_grid.Clear()
        for image in self.image_list:
            self.property_grid.Append(wxpg.StringProperty(image.file_name, value=image.url_path))

    def on_add_image(self, event):
        dlg = AddImageDialog(self, self.post)
        ret = dlg.ShowModal()
        dlg.Destroy()
        if ret == wx.ID_OK:
            self.update_property_grid()

    def on_delete_image(self, event):
        pass