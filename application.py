# main.py
# import the necessary packages
from flask import Flask, render_template, Response
from .camera import SDCamera
app = Flask(__name__)
@app.route('/')
def index():
    # rendering webpage
    return render_template('index.html')
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    return Response(gen(SDCamera(youtube_url='https://www.youtube.com/watch?v=mRe-514tGMg')),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='127.0.0.1',port='8000', debug=True)
