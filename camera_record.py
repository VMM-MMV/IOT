import cv2
import subprocess

def start_stream(rtmp_url="rtmp://localhost/live/stream", camera_index=0):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    # Get width and height from the camera
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define ffmpeg command to push to RTMP
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f"{width}x{height}",
        '-r', '25',
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-f', 'flv',
        rtmp_url
    ]

    # Start ffmpeg subprocess
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    print(f"🚀 Streaming camera feed to {rtmp_url}")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Failed to grab frame")
                break

            # Write frame to ffmpeg stdin
            process.stdin.write(frame.tobytes())

    except KeyboardInterrupt:
        print("🛑 Stopping stream...")

    finally:
        cap.release()
        process.stdin.close()
        process.wait()

if __name__ == "__main__":
    start_stream()