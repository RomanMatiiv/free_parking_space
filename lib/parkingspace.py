import logging
from lib import utils



class ParkingSpace:
    def __init__(self, x, y, w, h, free=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.free = free
        self.cur_iou = 0
        self.previous_iou = 0
        self.lockout_period = 0
        self.pt1 = (x, y)
        self.pt2 = (x + h, y + w)

    def get_color(self):
        green = (0, 255, 0)
        red = (0, 0, 255)

        if self.free:
            return green
        else:
            return red

    def ious_update(self, cur_iou):
        self.previous_iou = self.cur_iou
        self.cur_iou = cur_iou

    def blocked_still(self):
        if self.lockout_period == 0:
            return False
        else:
            self.lockout_period -= 1
            return True

    def block_off(self, lockout_period):
        self.lockout_period = lockout_period
