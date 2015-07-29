# coding=utf-8
__author__ = 'chengche'

import wx
import wx.propgrid as wxpg
from editor.model.image import *


class AddImageDialog(wx.Dialog):
    def __init__(self, parent, post):
        wx.Dialog.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.post = post
        self.image = Image(post)

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
        self.property_grid.Append(wxpg.FileProperty("File Path", value="C:\\Users\\chengche\\Pictures\\20155.jpg"))
        self.property_grid.Append(wxpg.StringProperty("Title", value="20155"))
        self.property_grid.Append(wxpg.StringProperty("Alt", value="20155"))

    def on_ok(self, event):
        dic = self.property_grid.GetPropertyValues(as_strings=True)

        self.image.file_path = dic.get('File Path', '')
        self.image.title = dic.get('Title', '')
        self.image.alt = dic.get('Alt', '')

        global_image_manager.upload_image(self.image)

        event.Skip(True)