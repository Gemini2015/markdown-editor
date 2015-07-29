# coding=utf-8
__author__ = 'chengche'

import codecs
import os
import json
from post import *
from qiniu import Auth
from qiniu import BucketManager
import qiniu
import urlparse


class Image:
    def __init__(self, post):
        self.post = post
        self.title = ""
        self.alt = ""
        self.file_name = ""
        self.file_path = ""
        self.prefix = ""
        self.key = ""
        self.url_path = ""
        self.mime_type = ""
        self.post_file_name = ""

    def parse(self, dic):
        self.title = dic.get('title', '')
        self.alt = dic.get('alt', '')
        self.file_name = dic.get('file_name', '')
        self.file_path = dic.get('file_path', '')
        self.prefix = dic.get('prefix', '')
        self.url_path = dic.get('url_path', '')
        self.key = dic.get('key', '')
        self.mime_type = dic.get('mime_type', '')
        self.post_file_name = dic.get('post_file_name', '')

        if self.post_file_name != "":
            self.post = global_post_manager.get_post(self.post_file_name)

    def dump(self):
        post_file_name = self.post_file_name
        if self.post:
            post_file_name = self.post.file_name
        dic = {
            'title': self.title,
            'alt': self.alt,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'prefix': self.prefix,
            'url_path': self.url_path,
            'key': self.key,
            'post_file_name': post_file_name,
            'mime_type': self.mime_type
        }
        return dic

    def update(self):
        if self.post is None:
            return
        if self.file_path == "":
            return
        ext = os.path.splitext(self.file_path)[1]
        ext_dic = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png"
        }
        self.mime_type = ext_dic.get(ext, 'text/plain')
        self.file_name = os.path.basename(self.file_path)
        # prefix
        # post/{post-name with out ext}
        post_name_without_ext = os.path.splitext(self.post.file_name)[0]
        self.prefix = "post" + "/" + post_name_without_ext
        self.key = self.prefix + "/" + self.file_name


class ImageManager:
    def __init__(self):
        self.cache_file_name = "image-cache.json"

        self.image_list = []

    def get_image_list(self, post):
        image_list = [img for img in self.image_list if img.post_file_name == post.file_name]
        return image_list

    def save(self):
        image_dic_list = []
        for image in self.image_list:
            image_dic = image.dump()
            image_dic_list.append(image_dic)
        json_str = json.JSONEncoder().encode(image_dic_list)

        fp = codecs.open(self.cache_file_name, 'w', 'utf-8')
        fp.write(json_str)
        fp.close()

    def load(self):
        if not os.path.exists(self.cache_file_name):
            return
        fp = codecs.open(self.cache_file_name, 'r', 'utf-8')
        json_str = fp.read()
        fp.close()

        self.image_list = []
        image_dic_list = json.JSONDecoder().decode(json_str)

        for img_dic in image_dic_list:
            image = Image(None)
            image.parse(img_dic)
            self.image_list.append(image)

    def sync_image(self):
        pass

    def upload_image(self, image):
        if global_config.access_key == ""\
                or global_config.secret_key == ""\
                or global_config.domain_name == ""\
                or global_config.bucket_name == "":
            return
        if image is None or image.file_path == "":
            return
        image.update()
        q = Auth(str(global_config.access_key), str(global_config.secret_key))

        file_path = image.file_path
        key = image.key
        mime_type = image.mime_type

        token = q.upload_token(str(global_config.bucket_name), str(key))
        ret, info = qiniu.put_file(token, key, file_path, mime_type=mime_type, check_crc=True)
        if info.status_code == 200:
            image.url_path = urlparse.urljoin("http://" + global_config.domain_name, image.key)
            self.image_list.append(image)


global_image_manager = ImageManager()