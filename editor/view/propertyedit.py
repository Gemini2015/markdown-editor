# coding=utf-8
__author__ = 'chengche'

import time
import wx
import wx.propgrid as wxpg
from editor.model.post import Post


class PropertyEdit(wx.Panel):
    def __init__(self, parent, post, is_add_post):
        wx.Panel.__init__(self, parent)

        self.post = post
        self.is_add_post = is_add_post

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.property_grid = pg = wxpg.PropertyGrid(self)
        sizer.Add(pg, 1, wx.EXPAND | wx.ALL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        btn = wx.Button(self, label="Add")
        self.Bind(wx.EVT_BUTTON, self.on_add_property, btn)
        hbox.Add(btn, 1, wx.CENTRE | wx.EXPAND)

        btn = wx.Button(self, label="Delete")
        self.Bind(wx.EVT_BUTTON, self.on_delete_property, btn)
        hbox.Add(btn, 1, wx.CENTRE | wx.EXPAND)

        if not self.is_add_post:
            btn = wx.Button(self, label="Save")
            self.Bind(wx.EVT_BUTTON, self.on_save, btn)
            hbox.Add(btn, 1, wx.CENTRE | wx.EXPAND)

            # btn = wx.Button(self, label="Cancel")
            # self.Bind(wx.EVT_BUTTON, self.on_cancel, btn)
            # hbox.Add(btn, 1, wx.CENTRE)

        sizer.Add(hbox, 0, wx.EXPAND)

        self.SetSizer(sizer)

        self.update_property_grid()

    def on_add_property(self, event):
        pass

    def on_delete_property(self, event):
        pass

    def on_save(self, event):
        if not self.is_add_post:
            self.sync_property()

    def on_cancel(self, event):
        pass

    def update_property_grid(self):
        pg = self.property_grid
        if not self.is_add_post and self.post is not None:
            for key in self.post.property:
                value = self.post.property[key]
                pg.Append(wxpg.StringProperty(key, value=value))
            return
        if self.is_add_post:
            pg.Append(wxpg.StringProperty("file name"))
            pg.Append(wxpg.StringProperty("layout", value="post"))
            pg.Append(wxpg.StringProperty("title"))
            pg.Append(wxpg.StringProperty("categories"))
            pg.Append(wxpg.StringProperty("description"))
            pg.Append(wxpg.StringProperty("codelang"))

    def sync_property(self):
        pg = self.property_grid
        if not self.is_add_post and self.post is not None:
            dic = pg.GetPropertyValues(as_strings=True)
            self.post.property = dic
            return
        if self.is_add_post:
            dic = pg.GetPropertyValues(as_strings=True)
            tstr = time.strftime('%Y-%m-%d')
            tstrfull = time.strftime('%Y-%m-%d %H:%M:%S')
            file_name = dic.get("file name", "")
            del dic["file name"]
            dic['date'] = tstrfull
            if file_name == "":
                return
            file_name = file_name.replace(' ', '-')
            file_path = tstr + '-' + file_name + ".markdown"
            self.post = Post(file_path)
            self.post.property = dic