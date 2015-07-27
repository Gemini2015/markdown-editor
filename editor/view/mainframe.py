# coding=utf-8
__author__ = 'chengche'

import codecs

import wx
from wx.lib.splitter import MultiSplitterWindow
import wx.stc as stc
import wx.html2 as html2
import wx.aui as aui

from leftpanel import *


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(970, 270),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetMinSize((640, 480))

        splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter_wnd = splitter

        # Left Panel
        self.left_panel = LeftPanel(self.splitter_wnd)

        # NoteBook
        self.note_book = aui.AuiNotebook(self.splitter_wnd)

        # Preview Wnd
        self.web_view = html2.WebView.New(self.splitter_wnd, style=wx.SIMPLE_BORDER)

        splitter.AppendWindow(self.left_panel, 200)
        splitter.AppendWindow(self.note_book, 200)
        splitter.AppendWindow(self.web_view)

        minimum = 200
        self.splitter_wnd.SetMinimumPaneSize(minimum)

        # Bind Event
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.evt_aui_notebook_page_changed)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.evt_aui_notebook_page_close)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.evt_list_box_d_click)
        self.Bind(wx.EVT_CLOSE, self.on_main_frame_close)

        # Load Markdown prefix & suffix
        fp = codecs.open('templates/prefix.html', 'r', encoding='utf-8')
        self.markdown_prefix = fp.read()
        fp.close()
        fp = codecs.open('templates/suffix.html', 'r', encoding='utf-8')
        self.markdown_suffix = fp.read()
        fp.close()

    def on_main_frame_close(self, event):
        self.left_panel.save_config()
        event.Skip(True)

    def evt_list_box_d_click(self, event):
        post = event.GetClientData()
        if post is None:
            return
        post.open()

        text_ctl = PostEditCtl(self.note_book, post)

        self.update_markdown_preview(post)

        title = post.property.get('title', post.file_name)
        self.note_book.InsertPage(0, text_ctl, title, True)

    def evt_aui_notebook_page_changed(self, event):
        index = event.GetSelection()
        if index == wx.NOT_FOUND:
            return
        page = self.note_book.GetPage(index)
        self.update_markdown_preview(page.post)

    def evt_aui_notebook_page_close(self, event):
        index = event.GetSelection()
        if index == wx.NOT_FOUND:
            return
        page = self.note_book.GetPage(index)
        post = page.post
        if post.is_modified:
            event.Veto()
            return

    def update_markdown_preview(self, post):
        if post.markdown_preview == "":
            return
        text = self.markdown_prefix + post.markdown_preview + self.markdown_suffix
        self.web_view.SetPage(text, "")


class PostEditCtl(stc.StyledTextCtrl):
    def __init__(self, parent, post):
        stc.StyledTextCtrl.__init__(self, parent)
        self.post = post

        self.SetText(post.content)



