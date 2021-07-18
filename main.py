import os

import cv2
import sys
import pytesseract

from pytube import YouTube

def get_playback_url():
    video_url = os.getenv("VIDEO_URL")
    return video_url

yt = YouTube('https://www.youtube.com/watch?v=bu7h_md33So')

# TODO: Loop through Streams so that we get AVCI codec which most computers support. There is no regex support
stream = yt.streams\
    .filter(file_extension='mp4', video_codec="avc1.42001E")\
    .order_by('resolution')\
    .desc().first()

cap = cv2.VideoCapture(stream.url)
if not cap.isOpened():
    print('Unable to open URL')
    sys.exit(-1)
else:
    print('OpenCV opened the URL successfully')

# retrieve FPS and calculate how long to wait between each frame to be display
fps = cap.get(cv2.CAP_PROP_FPS)
wait_ms = int(1000/fps)
print('FPS:', fps)

while(True):
    # read one frame
    ret, frame = cap.read()
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imwrite("/tmp/ytimage-large.jpeg", frame, None)
    print(pytesseract.image_to_string(img_rgb))
    break
    # TODO: perform frame processing here

    # display frame
    # cv2.imshow('frame',frame)
    # if cv2.waitKey(wait_ms) & 0xFF == ord('q'):
    #     break

cap.release()





