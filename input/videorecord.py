import cv2
import asyncio

async def record_video(filename, stop_event: asyncio.Event):
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    print("Video recording started...")

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

        cv2.imshow("Recording Preview", frame)
        cv2.waitKey(1)
        await asyncio.sleep(0.01)  # allows fast stop response

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Video recording stopped")
