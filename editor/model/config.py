# coding=utf-8
__author__ = 'chengche'

import os
import codecs
import json


class Config:
    def __init__(self):
        self.config_file_name = "config.json"
        self.root_path = ""

    def load(self):
        if not os.path.exists(self.config_file_name):
            return
        fp = codecs.open(self.config_file_name, 'r', 'utf-8')
        json_str = fp.read()
        fp.close()

        obj = json.JSONDecoder().decode(json_str)

        self.root_path = obj.get(u'root_path', u'')

    def save(self):
        obj = {
            u'root_path': self.root_path,
        }
        json_str = json.JSONEncoder().encode(obj)

        fp = codecs.open(self.config_file_name, 'w', 'utf-8')
        fp.write(json_str)
        fp.close()

