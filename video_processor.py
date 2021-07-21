import sys
import time

import cv2
import pytesseract
from pafy import pafy


def get_playback_url(video_url):
    pb_url = ''
    if "youtube.com" in video_url:
        yt = pafy.new(video_url)
        pb_url = yt.getbestvideo()
    else:
        pb_url = video_url
    return pb_url


class VideoProcessor:
    cap = None
    start_time = None

    def __init__(self, video_url):
        playback_url = get_playback_url(video_url)
        if not playback_url:
            raise Exception('Could not get playback URL')

        self.cap = cv2.VideoCapture(playback_url)
        self.start_time = time.time()
        if not self.cap.isOpened():
            raise Exception('Stop. Could not start video capture.')
        else:
            self.capture_fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.frame = None
            self.frame_text = None
            print('Video capture started successfully.')

    def __del__(self):
        self.cap.release()

    # Parameters:
    #   ocr_lang: See: https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
    #   time_code_seconds: Is the time in the stream at which the frame has to be captured
    #   qc_file_name_prefix: Save the frame and detected text at the specified file_name for manual quality checks
    # Returns
    #   result: False if there was an error.
    #   ocr_text: Is the detected OCR text.
    def detect_text(self, ocr_lang='eng', time_code_seconds=None):
        if not time_code_seconds:
            # now
            time_code_seconds = time.time()

        # Frames are zero indexed
        frame_index = ((time_code_seconds - self.start_time) * self.capture_fps) - 1
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, self.frame = self.cap.read()
        if not ret:
            print('Frame capture failed for frame: ' + frame_index)
            return False, ""
        # Convert to gray scale.
        frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        self.frame_text = pytesseract.image_to_string(frame, ocr_lang)

        return True, self.frame_text

    # Save the current frame and text to files.
    def snapshot(self, file_name_prefix):
        if self.frame and self.frame_text:
            cv2.imwrite(file_name_prefix + '.jpeg', self.frame, None)
            with open(file_name_prefix + '.txt', 'w') as file:
                file.write(self.frame_text)
