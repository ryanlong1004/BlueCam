from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import numpy as np

app = Flask(__name__)
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
picam2.start()


def generate_frames():
    """
    Generator function that captures frames from a camera, encodes them as JPEG,
    and yields them as byte streams formatted for HTTP multipart responses.

    Yields:
        bytes: A byte stream containing the JPEG-encoded frame with HTTP multipart
        headers.
    """
    while True:
        frame = picam2.capture_array()
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


@app.route("/video_feed")
def video_feed():
    """
    Generates a video feed response for streaming video frames.

    This function creates an HTTP response with a MIME type of 
    "multipart/x-mixed-replace", which is commonly used for streaming 
    video content. The response is generated using the `generate_frames()` 
    function, which provides the video frames to be streamed.

    Returns:
        Response: An HTTP response object that streams video frames 
        with the appropriate MIME type for video streaming.
    """
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
