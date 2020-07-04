from .src.object_detector.yolov3 import PeopleDetector
import cv2
import itertools
import numpy as np
import argparse
import os
import sys
import pafy


net = PeopleDetector()
net.load_network()

winName = 'predicted people'

class SDCamera(object):
    def __init__(self,image=None,video=None,camera=2,youtube_url=None):
        #outputFile = "yolo_out_py.avi"
        #YouTube Stream
        if youtube_url != None:
            url = youtube_url
            vPafy = pafy.new(url)
            play = vPafy.getbest(preftype="mp4")
            # Webcam input
            self.cap = cv2.VideoCapture(play.url)
        else:
            self.cap = cv2.VideoCapture(camera)
        # Get the video writer initialized to save the output video
        #self.vid_writer = cv2.VideoWriter(outputFile, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (round(
        #    self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), round(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    def get_frame(self):
        # get frame from the video
        hasFrame, frame = self.cap.read()

        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            cv2.waitKey(3000)
            # Release device
            self.cap.release()
        outs = net.predict(frame)
        net.process_preds(frame, outs)
        net.clear_preds()
        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = net._net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(frame, label, (0, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        #self.vid_writer.write(frame.astype(np.uint8))
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
