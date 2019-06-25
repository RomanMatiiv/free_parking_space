import cv2


BLUR_FILTER_SIZE = (3, 3)
THRESHOLD = 30


def to_gray_blur(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, BLUR_FILTER_SIZE, 0)

    return gray


def delete_static(static_back, fgmask):

    # Difference between background and curent frame
    diff_frame = cv2.absdiff(static_back, fgmask)

    # If change in between static background and
    # current frame is greater than TRESHOLD it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame,
                                 THRESHOLD,
                                 255,
                                 cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    return thresh_frame
