import json
from lib import parkingspace


def parse_parking_space_config(config):
    """
    Парсит из конфига данные о парковке

    Args:
        config: файл в формате
        {
        "spaces": {
            "space1": {
              "x": 82,
              "y": 296,
              "w": 102,
              "h": 270,
              "free": false
            },
            "space2"{:
                ...}
            },
        "min_size_object": 5000
        }

    Returns:
        словарь с парковочными местами
        парковочные места предствлены классом ParkingSpace

    """
    with open(config) as config_file:
        config = json.load(config_file)

    min_size_object = config["min_size_object"]

    spaces = []

    for cur_space_name in config['spaces'].keys():
        cur_space = config['spaces'][cur_space_name]
        cur_space = parkingspace.ParkingSpace(cur_space['x'],
                                              cur_space['y'],
                                              cur_space['w'],
                                              cur_space['h'],
                                              cur_space['free'])
        spaces.append(cur_space)

    return [spaces, min_size_object]


def iou(a, b, epsilon=1e-5):
    """ Given two boxes `a` and `b` defined as a list of four numbers

        It returns the Intersect of Union score for these two boxes.

        source: http://ronny.rest/tutorials/module/localization_001/iou/

    Args:
        a:          (list of 4 numbers) [x1,y1,x2,y2]
        b:          (list of 4 numbers) [x1,y1,x2,y2]
        epsilon:    (float) Small value to prevent division by zero
    where:
         x1,y1 represent the upper left corner
         x2,y2 represent the lower right corner

    Returns:
        (float) The Intersect of Union score.
    """
    # COORDINATES OF THE INTERSECTION BOX
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    # AREA OF OVERLAP - Area where the boxes intersect
    width = (x2 - x1)
    height = (y2 - y1)
    # handle case where there is NO overlap
    if (width<0) or (height <0):
        return 0.0
    area_overlap = width * height

    # COMBINED AREA
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    area_combined = area_a + area_b - area_overlap

    # RATIO OF AREA OF OVERLAP OVER COMBINED AREA
    iou = area_overlap / (area_combined+epsilon)

    return iou


def iou_custom(a, b, epsilon=1e-5):
    """ Given two boxes `a` and `b` defined as a list of four numbers

        Отличается от стандартной метрики тем, что в знаменателе не
        область общего пересечения а наибольшее пересечение
        одного из 2 премоугольников с числителем (area of overlap)

    Args:
        a:          (list of 4 numbers) [x1,y1,x2,y2]
        b:          (list of 4 numbers) [x1,y1,x2,y2]
        epsilon:    (float) Small value to prevent division by zero
    where:
         x1,y1 represent the upper left corner
         x2,y2 represent the lower right corner

    Returns:
        (float) The Intersect of Union score.
    """
    # COORDINATES OF THE INTERSECTION BOX
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    # AREA OF OVERLAP - Area where the boxes intersect
    width = (x2 - x1)
    height = (y2 - y1)
    # handle case where there is NO overlap
    if (width<0) or (height <0):
        return 0.0
    area_overlap = width * height

    width_a = a[2] - a[0]
    width_b = b[2] - b[0]
    height_a = a[3] - a[1]
    height_b = b[3] - b[1]

    a_area = width_a * height_a
    b_area = width_b * height_b

    return max([area_overlap/a_area+epsilon,
                area_overlap/b_area+epsilon])


def get_rectangle_for_iou(x,y,w,h):
    x1 = x
    y1 = y
    x2 = x + h
    y2 = y + w

    rectangle = [x1, y1, x2, y2]

    return rectangle

