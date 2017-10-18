#!/usr/bin/env python
# coding: utf-8

__author__ = 'outofmemory.cn'

from wheezy.captcha.image import captcha

from wheezy.captcha.image import background
from wheezy.captcha.image import curve
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text

from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp

import random
import web

from os import path
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

if __name__ == '__main__':
    import os,sys
    webPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0,webPath)

from run import session

_controllersDir = path.abspath(path.dirname(__file__))
_webDir = path.dirname(_controllersDir)
_fontsDir = path.join(path.dirname(_webDir),'fonts')

_chars = 'ABCDEFJHJKLMNPQRSTUVWXY3456789'

SESSION_KEY_CAPTCHA = 'captcha'

def isValidCaptcha(captchaInputName='captcha'):
    userInputVal = web.input().get(captchaInputName)
    if not userInputVal: return False
    correctVal = session[SESSION_KEY_CAPTCHA]
    return userInputVal.upper() == correctVal

class Captcha:
    '''验证码'''

    def GET(self):
        captcha_image = captcha(drawings=[
            background(),
            text(fonts=[
                path.join(_fontsDir,'78640___.ttf'),
                path.join(_fontsDir,'andyb.ttf')],
                drawings=[
                    warp(),
                    rotate(),
                    offset()
                ]),
            curve(),
            noise(),
            smooth()
        ])
        chars = random.sample(_chars, 4)
        session[SESSION_KEY_CAPTCHA] = ''.join(chars)
        image = captcha_image(chars)
        out = StringIO()
        image.save(out,"jpeg",quality=75)
        web.header('Content-Type','image/jpeg')
        return out.getvalue()

if __name__ == '__main__':
    print _fontsDir
    captcha_image_t = captcha(drawings=[
        background(),
        text(fonts=[
            path.join(_fontsDir,'78640___.ttf'),
            path.join(_fontsDir,'andyb.ttf')],
            drawings=[
                warp(),
                rotate(),
                offset()
            ]),
        curve(),
        noise(),
        smooth()
    ])
    chars_t = random.sample(_chars, 4)

    image_t = captcha_image_t(chars_t)
    image_t.save('test.jpeg','jpeg',quality=75)