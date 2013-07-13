#!/usr/bin/env python
import PIL.Image as IMG
from PIL.ExifTags import TAGS
import os
import sys
import time
import datetime

def get_exif_time(fn):
    ret = {}
    try:
        i = IMG.open(fn)
        info = i._getexif()
        for atag, value in info.items():
            decoded = TAGS.get(atag,atag)
            ret[decoded] = value
        t = datetime.datetime.fromtimestamp(time.mktime(time.strptime(ret['DateTimeOriginal'],'%Y:%m:%d %H:%M:%S')))
    except:
        return None
    return t

def get_file_time(fn):
    """
    Gets the current file time using the datetime module.

    Parameters
    ----------
    fn : string
        The file name to be analyzed.

    Returns
    -------
    result : string
        The time.
    """
    t = datetime.datetime.fromtimestamp(os.path.getmtime(fn))
    return t

def get_time(fn):
    t = get_exif_time(fn)
    if t:
        return t
    return get_file_time(fn)

def get_name(fn):
    str_format = '%Y-%m-%d-%H-%M-%S-%f'
    onemicrosec = datetime.timedelta(microseconds=1)
    t = get_time(fn)
    fext = fn[-4:]
    while True:
        new = os.path.join('/home','bellock','Pictures',str(t.year),'%s%s'%(t.strftime(str_format),fext))
        if os.path.basename(new) == fn:
            return None
        if not os.path.exists(new):
            return new
        t = t + onemicrosec
    return

def add_sec(t):
    return t + datetime.timedelta(seconds=1)

def rename_file(fn):
    old = os.path.abspath(fn)
    new = get_name(fn)
    if not new:
#        print 'Not Moving: %s'%old
        return
    print 'Moving: %s -> %s'%(old,new)
    os.renames(old,new)

def rename_path(pth):
    for root, dirs, files in os.walk(pth):
        for name in files:
            fn = os.path.join(root,name)
            if fn[-4:].lower() in ['.jpg','.gif','.bmp','.tif']:
                rename_file(fn)

rel_path = sys.argv[1]
if os.path.isdir(rel_path):
    rename_path(rel_path)
elif os.path.isfile(rel_path):
    rename_file(sys.argv[1])
