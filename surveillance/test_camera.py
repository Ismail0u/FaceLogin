# surveillance/test_camera.py
import cv2

def test_camera(source=0):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("❌ Impossible d'accéder à la caméra.")
        return

    print("🎥 Appuyez sur Q pour quitter.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Caméra en direct", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
