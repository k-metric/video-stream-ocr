import os
import time
import config
from pathlib import Path

from text_processor import TextProcessor
from video_processor import VideoProcessor

if __name__ == '__main__':
    # Ensure output folders exist
    Path(config.options['output_folder'] + os.sep + 'qc').mkdir(parents=True, exist_ok=True)

    video_processor = VideoProcessor(config.options['video_url'])
    text_processor = TextProcessor(config.options['search_terms'])
    end_time = video_processor.start_time + (config.options['analysis_length'] * 60)

    while True:
        current_time = time.time()
        file_name_prefix = config.options['output_folder'] + os.sep + 'qc' + os.sep + str(current_time)

        # Detect Text
        ret, ocr_text = video_processor.detect_text(config.options['ocr_language'])

        # Store image periodically for quality control.
        if config.options['qc_enabled'] and end_time % time.time() < config.options['frame_capture_period']:
            video_processor.snapshot(file_name_prefix)

        # Process Text
        file_content = "0"
        if text_processor.search(ocr_text):
            file_content = "1"
            if config.options['require_evidence']:
                video_processor.snapshot(file_name_prefix)

        with open(file_name_prefix + '.txt', 'w') as file:
            file.write(file_content)

        time.sleep(config.options['frame_capture_period'])
        if current_time > end_time:
            break
