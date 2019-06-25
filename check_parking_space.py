import logging
import cv2

import time
from lib import utils
from lib import preprocessing


IOU_THRESHOLD = 0.70
LOCKOUT_PERIOD = 80

logging.basicConfig(level=logging.DEBUG)

video = cv2.VideoCapture('/media/roman/data/free_parking_space/our_parking1.mp4')

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(backgroundRatio=0.8)

logging.info("start parse spaces config")
config = '/home/roman/projects/free_parking_space/configs/our_parking_cam1.json'
spaces, min_size_object = utils.parse_parking_space_config(config)

logging.info("start read background")
check, frame = video.read()
if check:
    gray = preprocessing.to_gray_blur(frame)
    fgmask = fgbg.apply(gray)
    static_back = fgmask
else:
    logging.error("background dont read")

logging.info("start processing video")
while video.isOpened():
    # ВРЕМЕННО замедление видеопотока
    # time.sleep(0.7)

    check, frame = video.read()
    if not check:
        break
    # preprocessing______________________________________________________________________
    gray = preprocessing.to_gray_blur(frame)
    fgmask = fgbg.apply(gray)
    thresh_frame = preprocessing.delete_static(static_back, fgmask)

    contours, _ = cv2.findContours(thresh_frame.copy(),
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)
    cars = []

    # Сохраняем только машины
    for contour in contours:
        if cv2.contourArea(contour) > min_size_object:
            x, y, w, h = cv2.boundingRect(contour)
            cars.append([x, y, w, h])
    # main______________________________________________________________________
    for cur_space in spaces:

        # print(cur_space.lockout_period)

        if cur_space.blocked_still() or len(cars) == 0:
            color = cur_space.get_color()
            cv2.rectangle(frame, cur_space.pt1, cur_space.pt2, color)
            continue

        cur_space_rect = utils.get_rectangle_for_iou(cur_space.x,
                                                     cur_space.y,
                                                     cur_space.w,
                                                     cur_space.h)
        ious_with_all_cars = []
        for car in cars:
            x = car[0]
            y = car[1]
            w = car[2]
            h = car[3]

            # ВРЕМЕННО отрисовка прямоугольника автомобиля
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))

            cur_car_rect = utils.get_rectangle_for_iou(x, y, w, h)
            cur_iou = utils.iou_custom(cur_space_rect,
                                       cur_car_rect)
            ious_with_all_cars.append(cur_iou)

        max_cur_iou = max(ious_with_all_cars)
        cur_space.ious_update(max_cur_iou)

        # Выезд
        if (cur_space.previous_iou > cur_space.cur_iou and
            cur_space.previous_iou > IOU_THRESHOLD):
            logging.debug("Выезд")
            cur_space.free = True
            # cur_space.block_off(LOCKOUT_PERIOD)

        # Заезд
        if (cur_space.previous_iou<cur_space.cur_iou and
            cur_space.cur_iou>IOU_THRESHOLD):
            logging.debug("Заезд")
            cur_space.free = False
            cur_space.block_off(LOCKOUT_PERIOD)

        color = cur_space.get_color()

        cv2.rectangle(frame, cur_space.pt1, cur_space.pt2, color)
        cv2.putText(frame,
                    str(max_cur_iou)[:4],
                    cur_space.pt1,
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(255, 255, 255))
    # ______________________________________________________________________

    # cv2.imshow("fff", fgmask)
    cv2.imshow("fff", frame)
    if cv2.waitKey(33) == 27:
        break

logging.info("end")
video.release()
cv2.destroyAllWindows()

