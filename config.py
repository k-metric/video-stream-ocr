import configargparse


def config_parse():
    p = configargparse.ArgParser(default_config_files=['./config'], auto_env_var_prefix='')
    p.add('-c', '--config', is_config_file=True, help='config file path')
    p.add('--video_url', required=True, type=str, help='HLS or Youtube stream URL to analyze')
    p.add('--frame_capture_period', required=True, type=int, help='period between frame capture in seconds')
    p.add('--analysis_length', required=True, type=int, help='how long to capture and analyze (minutes)')
    p.add('--ocr_language', required=True, type=str, help='Language for Tesseract OCR')
    p.add('--qc_enabled', required=True, type=bool, help='Enable saving images for quality control')
    p.add('--qc_captures', required=True, type=int, help='The number of images to capture for quality control')
    p.add('--output_folder', required=True, type=str, help='Directory to write results to')
    p.add('-v', help='verbose', action='store_true')
    return vars(p.parse_args())


options = config_parse()
print(options)
