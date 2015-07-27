# coding=utf-8
__author__ = 'chengche'

import os
import codecs
import markdown


class Post:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.property = {}
        self.content = ""
        self.markdown_preview = ""
        self.is_modified = False
        self.is_open = False

    def parse(self):
        if not os.path.exists(self.file_path) or not os.path.isfile(self.file_path):
            return
        fp = codecs.open(self.file_path, 'r', 'utf-8')
        start = False
        line = fp.readline()
        while line != "":
            line = line.strip(u' ')
            line = line.strip(u'\n')
            line = line.strip(u'\r')
            if line.startswith(u'---'):
                if start:
                    break
                start = True
                line = fp.readline()
                continue
            (key, sep, value) = line.partition(u':')
            key = key.strip(u' ')
            value = value.strip(u' \t"')
            value = value.strip(u'"')
            self.property[key] = value
            line = fp.readline()
        fp.close()

    def open(self):
        if not os.path.exists(self.file_path) or not os.path.isfile(self.file_path):
            return
        fp = codecs.open(self.file_path, 'r', 'utf-8')
        start = False
        line = fp.readline()
        while line != "":
            line = line.strip(u' ')
            line = line.strip(u'\n')
            line = line.strip(u'\r')
            if line.startswith(u'---'):
                if start:
                    break
                start = True
                line = fp.readline()
                continue
            line = fp.readline()
        self.content = fp.read()
        fp.close()
        self.update_markdown()
        self.is_open = True

    def save(self):
        if not self.is_modified:
            return
        if not os.path.exists(self.file_path) or not os.path.isfile(self.file_path):
            return

        fp = codecs.open(self.file_path, 'w', 'utf-8')
        fp.write(u'---\n')
        for (key, value) in self.property:
            line = u"%s: %s\n" % key, value
            fp.write(line)
        fp.write(u'---\n\n')
        fp.write(self.content)
        fp.close()

        self.is_modified = False

    def update_markdown(self):
        if self.content == "":
            return
        self.markdown_preview = markdown.markdown(self.content, extensions=['gfm'])
