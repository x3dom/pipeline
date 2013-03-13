# -*- coding: utf-8 -*-

def bytes(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "{0:.1f} {1}".format(num, x)
        num /= 1024.0
    return "{0:.1f} {1}".format(num, 'TB')
