# coding=utf-8
__author__ = 'chengche'
import sys

sys.path.append("../")
from distutils.core import setup
import py2exe
import os
import glob

if len(sys.argv) == 1:
    sys.argv.append("py2exe")


def find_data_files(source, target, patterns):
    """
    Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
         Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    while len(patterns) > 0:
        pattern = patterns.pop(0)
        pattern = os.path.join(source, pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename, source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path, []).append(filename)
            if os.path.isdir(filename):
                new_pattern = os.path.join(os.path.relpath(filename, source), "*")
                patterns.append(new_pattern)
    return sorted(ret.items())


setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    name="Markdown Editor",
    version="0.0.1",
    description="Yet another markdown editor",
    author="Chris Cheng",

    # targets to build
    windows=["../launcher.py"],
    options={
        'py2exe': {
            'optimize': 2,
            'bundle_files': 1,
            'includes': ['editor',
                         'qiniu',
                         'gfm',
                         'mdx_gfm',
                         'mdx_partial_gfm',
                         'markdown',
                         'wx',
                         'requests',
                         'http'],
        },
    },
    data_files=find_data_files('../', '', [
        'README.md',
        'LICENSE',
        'templates/*',
        'res/*',
    ]),
)