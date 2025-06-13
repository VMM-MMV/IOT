import cv2

def read_stream(rtmp_url="rtmp://localhost/live/stream"):
    video_capture = cv2.VideoCapture(rtmp_url)
    while True:
        success, frame = video_capture.read()
        yield success, frame

if __name__ == "__main__":
    for success, frame in read_stream():
        if not success:
            break
        cv2.imshow('VIDEO', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
