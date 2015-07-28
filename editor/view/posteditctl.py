# coding=utf-8
__author__ = 'chengche'

import wx.stc as stc
import wx
import markdown

if wx.Platform == '__WXMSW__':
    faces = {'times': 'MS YaHei',
             'mono': 'Courier New',
             'helv': 'Arial',
             'other': 'Comic Sans MS',
             'size': 10,
             'size2': 8}
elif wx.Platform == '__WXMAC__':
    faces = {'times': 'Times New Roman',
             'mono': 'Monaco',
             'helv': 'Arial',
             'other': 'Comic Sans MS',
             'size': 12,
             'size2': 10}
else:
    faces = {'times': 'Times',
             'mono': 'Courier',
             'helv': 'Helvetica',
             'other': 'new century schoolbook',
             'size': 12,
             'size2': 10}


class PostEditCtl(stc.StyledTextCtrl):
    def __init__(self, parent, post):
        stc.StyledTextCtrl.__init__(self, parent)
        self.post = post

        self.SetText(post.content)
        self.SetModified(False)

        self.SetWrapMode(stc.STC_WRAP_WORD)

        # Set Style
        self.SetLexer(stc.STC_LEX_MARKDOWN)

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER1, "fore:#cb4b16, bold")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER2, "fore:#cb4b16, bold")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER3, "fore:#cb4b16")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER4, "fore:#cb4b16")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER5, "fore:#cb4b16")

        self.StyleSetSpec(stc.STC_MARKDOWN_LINE_BEGIN, "fore:#6c71c4")
        self.StyleSetSpec(stc.STC_MARKDOWN_LINK, "fore:#2aa198")

        self.StyleSetSpec(stc.STC_MARKDOWN_CODE, "fore:#3399FF")
        self.StyleSetSpec(stc.STC_MARKDOWN_CODE2, "fore:#3399FF")
        self.StyleSetSpec(stc.STC_MARKDOWN_CODEBK, "fore:#3399FF")

        self.StyleSetSpec(stc.STC_MARKDOWN_BLOCKQUOTE, "fore:#0066CC")

        self.StyleSetSpec(stc.STC_MARKDOWN_EM1, "fore:#C7254E")
        self.StyleSetSpec(stc.STC_MARKDOWN_EM2, "fore:#C7254E")

        self.StyleSetSpec(stc.STC_MARKDOWN_STRONG1, "fore:#C7254E")
        self.StyleSetSpec(stc.STC_MARKDOWN_STRONG2, "fore:#C7254E")

    def is_modified(self):
        return self.IsModified()

    def get_markdown_preview(self):
        text = self.GetText()
        if text == "":
            return ""
        markdown_preview = markdown.markdown(text, extensions=['gfm'])
        return markdown_preview