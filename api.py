
from flask import Flask, json, request, Response, make_response
from .camera import SDCamera

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
  payload = json.loads(request.get_data().decode('utf-8'))
  prediction = SDCamera(youtube_url=payload['payload'])
  return make_response(prediction.get_frame())
#  return Response(gen(prediction),
#                  mimetype='multipart/x-mixed-replace; boundary=frame')
def gen(camera):
    #while True:
        #get camera frame
    frame = camera.get_frame()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def load_model():
  conn = S3Connection()
  bucket = conn.create_bucket(BUCKET_NAME)
  key_obj = Key(bucket)
  key_obj.key = MODEL_FILE_NAME

  contents = key_obj.get_contents_to_filename(MODEL_LOCAL_PATH)
  return joblib.load(MODEL_LOCAL_PATH)

def predict(data):
  # Process your data, create a dataframe/vector and make your predictions
  return SDCamera(youtube_url='https://www.youtube.com/watch?v=mRe-514tGMg')
