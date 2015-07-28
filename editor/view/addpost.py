# coding=utf-8
__author__ = 'chengche'

import wx
from propertyedit import PropertyEdit


class AddPostDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.property_edit = PropertyEdit(self, None, True)
        sizer.Add(self.property_edit, 1, wx.EXPAND)

        # hbox = wx.BoxSizer(wx.HORIZONTAL)
        #
        # btn = wx.Button(self, label="Save")
        # self.Bind(wx.EVT_BUTTON, self.on_add_property, btn)
        # hbox.Add(btn, 1, wx.CENTRE | wx.EXPAND)
        #
        # btn = wx.Button(self, label="Cancel")
        # self.Bind(wx.EVT_BUTTON, self.on_delete_property, btn)
        # hbox.Add(btn, 1, wx.CENTRE | wx.EXPAND)

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



