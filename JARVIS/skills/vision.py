def open_camera():
    try: import cv2
    except ImportError: return "OpenCV is not installed."
    cam=cv2.VideoCapture(0)
    if not cam.isOpened(): return "I could not access the camera."
    print("Camera active. Press Q to close.")
    while True:
        ok,frame=cam.read()
        if not ok: break
        cv2.imshow("JARVIS Vision",frame)
        if cv2.waitKey(1)&0xFF==ord("q"): break
    cam.release(); cv2.destroyAllWindows()
    return "Camera session closed."
