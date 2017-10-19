# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 20:32:52 2017

@author: Administrator
"""
from PIL import ImageFont,Image,ImageDraw
import random
import numpy as np
import matplotlib.pyplot as plt

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
	return captcha_text    

class Captcha(object):
    def __init__(self,size=(100,40),fontSize=30):
        self.font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf',fontSize)
        self.size = size
        self.image = Image.new('RGBA',self.size,(255,)*4)
        self.texts = random_captcha_text(captcha_size=5)

    def rotate(self):
        rot = self.image.rotate(random.randint(-10,10),expand=0)
        fff = Image.new('RGBA',rot.size,(255,)*4)
        self.image = Image.composite(rot,fff,rot)

    def randColor(self):
        self.fontColor = (random.randint(0,250),random.randint(0,250),random.randint(0,250))

    def randNum(self,bits):
        return ''.join(str(random.randint(0,9)) for i in range(bits))

    def write(self,text,x):
        draw = ImageDraw.Draw(self.image)
        draw.text((x,4),text,fill=self.fontColor,font=self.font)
        
    def create_lines(self):
        """绘制干扰线"""
        n_line=(1, 2)
        size=(160, 60)
        line_num = random.randint(*n_line)  # 干扰线条数
        draw = ImageDraw.Draw(self.image)

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))
            
    def create_points(self):
        """绘制干扰点"""
        point_chance=2
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]
        width, height = (160, 60)
        draw = ImageDraw.Draw(self.image)

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def writeNum(self):
        x = 10
        xplus = 15
        for text in self.texts:
            self.randColor()
            self.write(text, x)
            self.rotate()
            self.create_lines()
            x += xplus
        return self.texts

    def save(self):
        self.image.save('captcha.jpg')
    
# 生成字符对应的验证码
def gen_captcha_text_and_image():
	
	img = Captcha()
	text = img.writeNum()

	captcha_image = np.array(img.image)
	return text, captcha_image

if __name__ == '__main__':
	# 测试
    while(1):
    	#text, image = generate_verify_image(length=4)
    	img = Captcha()
    	num = img.writeNum()
    	text = img.texts
    	image = img.image
    	print(image)
    	f = plt.figure()
    	ax = f.add_subplot(111)
    	ax.text(0.1, 0.9,text, ha='center', va='center', transform=ax.transAxes)
    	plt.imshow(image)
    	plt.show()
    	break

#img.save()