import os
import cv2
import sys
import time
import pytesseract
import config

from pathlib import Path
from pytube import YouTube


def get_playback_url():
    video_url = config.options['video_url']
    pb_url = ''
    if "youtube.com" in video_url:
        yt = YouTube(video_url)

        # Pick the highest resolution available.
        streams = yt.streams \
            .filter(file_extension='mp4', type="video") \
            .order_by('resolution') \
            .desc()
        # Loop through Streams so that we use the AVC stream which most systems seem to support.
        # TODO: Expose video codec as a config
        for stream in streams:
            if "avc1" in stream.video_codec:
                pb_url = stream.url
                break
    else:
        pb_url = video_url
    return pb_url


if __name__ == '__main__':
    playback_url = get_playback_url()
    if not playback_url:
        print("Could not get playback URL")
        sys.exit(1)

    cap = cv2.VideoCapture(playback_url)
    if not cap.isOpened():
        print('Stop. Could not start video capture.')
        sys.exit(1)
    else:
        print('Video capture started successfully.')

    end_time = time.time() + (config.options['analysis_length'] * 60)
    # Ensure output folders exist
    Path(config.options['output_folder'] + os.sep + 'qc').mkdir(parents=True, exist_ok=True)
    frame_index = 0

    while True:
        current_time = time.time()

        cap.set(cv2.CAP_PROP_POS_MSEC, frame_index * config.options['frame_capture_period'] * 1000)
        ret, frame = cap.read()
        frame_index = frame_index + 1

        # Convert color from BGR to RGB for Tesseract
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ocr_text = pytesseract.image_to_string(img_rgb, lang=config.options['ocr_language'])

        with open(config.options['output_folder'] + os.sep + str(current_time) + '.txt', 'w') as file:
            file.write(ocr_text)
        cv2.imwrite(config.options['output_folder'] + os.sep + str(current_time) + '.jpeg', frame, None)

        # Store image periodically for quality control.
        if config.options['qc_enabled'] and end_time % time.time() < config.options['frame_capture_period']:
            file_name = config.options['output_folder'] + os.sep + 'qc' + os.sep + str(current_time)
            cv2.imwrite(file_name + '.jpeg', frame, None)
            with open(file_name + '.txt', 'w') as file:
                file.write(ocr_text)

        print(cap.get(cv2.CAP_PROP_POS_MSEC))
        print(current_time)
        time.sleep(config.options['frame_capture_period'])
        # cv2.waitKey(config.options['frame_capture_period'] * 1000)
        if current_time > end_time:
            break
    cap.release()
