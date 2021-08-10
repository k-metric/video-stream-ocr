# video-stream-ocr

Captures a video stream from Youtube and detects text in frames periodically.
Originally intended to detect question marks (?) in TV news streams to assess their factuality.

## Dependencies
- OpenCV
- Tesseract

## Build
A Dockerfile is included which bundles dependencies, just `docker build .`

## Running
- Edit the `config` file as per your requirement.
- You need a mount point where detected text and samples images are stored.
- Here is an example run command ``` docker run --mount type=bind,source=/tmp/data,target=/data -rm -d kmetric/video-stream-ocr:v0.11 ```

