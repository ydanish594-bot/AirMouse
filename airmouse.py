
import cv2
import pyautogui

# AirMouse settings
CAMERA_INDEX = 0
CONFIDENCE_LIMIT = 0.55

# Load reference photo
template = cv2.imread("airmouse_reference.jpg")

if template is None:
    raise RuntimeError("Reference photo not found!")

template_gray = cv2.cvtColor(
    template, cv2.COLOR_BGR2GRAY
)

camera = cv2.VideoCapture(
    CAMERA_INDEX, cv2.CAP_AVFOUNDATION
)

if not camera.isOpened():
    raise RuntimeError("Cannot open camera")

print("AirMouse photo matching started!")

screen_w, screen_h = pyautogui.size()

while True:
    success, frame = camera.read()

    if not success:
        break

    # Reduce camera image for faster matching
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    best_score = 0
    best_box = None

    # Search for the case at different sizes
    for scale in [
        0.20, 0.25, 0.30, 0.35,
        0.40, 0.45, 0.50, 0.55, 0.60
    ]:

        width = int(template_gray.shape[1] * scale)
        height = int(template_gray.shape[0] * scale)

        if width >= 640 or height >= 480:
            continue

        resized = cv2.resize(
            template_gray, (width, height)
        )

        result = cv2.matchTemplate(
            gray,
            resized,
            cv2.TM_CCOEFF_NORMED
        )

        _, score, _, location = cv2.minMaxLoc(result)

        if score > best_score:
            best_score = score
            best_box = (
                location[0],
                location[1],
                width,
                height
            )

    display = frame.copy()

    if best_box is not None and best_score >= CONFIDENCE_LIMIT:

        x, y, w, h = best_box

        cv2.rectangle(
            display,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

        cv2.putText(
            display,
            f"AIRPODS FOUND: {best_score:.2f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        print(
            f"Detected: X={x + w//2}, "
            f"Y={y + h//2}, Score={best_score:.2f}",
            end="\r"
        )

    else:
        cv2.putText(
            display,
            f"SEARCHING... Score: {best_score:.2f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    cv2.imshow("AirMouse - Photo Detection", display)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
print("\nAirMouse stopped!")
