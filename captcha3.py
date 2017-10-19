#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import numpy as np
default_font = "./font/DejaVuSans.ttf" 


# 验证码中的字符, 就不用汉字了
number = ['0','1','2','3','4','5','6','7','8','9']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
ALPHABET = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# 验证码一般都无视大小写；验证码长度4个字符
def random_captcha_text(char_set=number+alphabet+ALPHABET, captcha_size=4):
	captcha_text = []
	for i in range(captcha_size):
		c = random.choice(char_set)
		captcha_text.append(c)
	return captcha_text                              # 验证码字体


# 生成验证码接口
def generate_verify_image(size=(160, 60),
                          img_type="GIF",
                          mode="RGB",
                          bg_color=(255, 255, 255),
                          fg_color=(0, 0, 255),
                          font_size=20,
                          font_type=default_font,
                          length=4,
                          draw_lines=True,
                          n_line=(1, 2),
                          draw_points=True,
                          point_chance=2,
                          save_img=False):

    """
    生成验证码图片
    :param size: 图片的大小，格式（宽，高），默认为(120, 30)
    :param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    :param mode: 图片模式，默认为RGB
    :param bg_color: 背景颜色，默认为白色
    :param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    :param font_size: 验证码字体大小
    :param font_type: 验证码字体，默认为 DejaVuSans.ttf
    :param length: 验证码字符个数
    :param draw_lines: 是否划干扰线
    :param n_line: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    :param draw_points: 是否画干扰点
    :param point_chance: 干扰点出现的概率，大小范围[0, 100]
    :param save_img: 是否保存为图片
    :return: [0]: 验证码字节流, [1]: 验证码图片中的字符串
    """

    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def create_lines():
        """绘制干扰线"""

        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """绘制干扰点"""

        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs(length):
        """绘制验证码字符"""

        c_chars = random_captcha_text(captcha_size=length)
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs(length)

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    captcha_image = np.array(img)
    return strs, captcha_image

def gen_captcha_text_and_image():
    return generate_verify_image()


if __name__ == '__main__':
	# 测试
    while(1):
    	text, image = generate_verify_image(length=4)
    	print(image)
    	f = plt.figure()
    	ax = f.add_subplot(111)
    	ax.text(0.1, 0.9,text, ha='center', va='center', transform=ax.transAxes)
    	plt.imshow(image)
    	plt.show()
    	break