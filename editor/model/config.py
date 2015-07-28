# coding=utf-8
__author__ = 'chengche'

import os
import codecs
import json


class Config:
    def __init__(self):
        self.config_file_name = "config.json"
        self.root_path = ""
        self.access_key = ""
        self.secret_key = ""

    def load(self):
        if not os.path.exists(self.config_file_name):
            return
        fp = codecs.open(self.config_file_name, 'r', 'utf-8')
        json_str = fp.read()
        fp.close()

        obj = json.JSONDecoder().decode(json_str)

        self.root_path = obj.get(u'root_path', u'')
        self.access_key = obj.get(u'access_key', u'')
        self.secret_key = obj.get(u'secret_key', u'')

    def save(self):
        obj = {
            u'root_path': self.root_path,
            u'access_key': self.access_key,
            u'secret_key': self.secret_key
        }
        json_str = json.JSONEncoder().encode(obj)

        fp = codecs.open(self.config_file_name, 'w', 'utf-8')
        fp.write(json_str)
        fp.close()

