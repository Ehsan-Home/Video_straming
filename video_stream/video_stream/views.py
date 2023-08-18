import cv2
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views import View


class VideoStream(View):
    def __init__(self):
        self.camera = cv2.VideoCapture(0)  # Open USB camera

    def __del__(self):
        self.camera.release()

    def get_frame(self):
        ret, frame = self.camera.read()
        if ret:
            _, jpeg = cv2.imencode(".jpg", frame)
            return jpeg.tobytes()
        else:
            return None

    def generate(self):
        while True:
            frame = self.get_frame()
            if frame is not None:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
                )

    def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(
            self.generate(), content_type="multipart/x-mixed-replace; boundary=frame"
        )


class StreamView(View):
    template_name = "stream.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
