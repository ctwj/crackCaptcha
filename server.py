from flask import Flask,request,render_template,Response,send_file
from create_image.cteate_image import gen_captcha_text_and_image

app = Flask(__name__)

@app.route('/')
def index():
	return 'bye'

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/captcha')
def captche():
	t,image = gen_captcha_text_and_image()
	print t
	image1 = file( t + '.jpg')
	resp = Resopnse(image1, mimetyp="image/jpeg") 
	return resp
	#return send_file(image, mimetype='image/jpg')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
