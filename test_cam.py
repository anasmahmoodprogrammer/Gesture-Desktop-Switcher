import cv2

# Try the first 3 camera indices
for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✅ Camera found at index {i}")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Test Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        break
    else:
        print(f"❌ No camera at index {i}")
