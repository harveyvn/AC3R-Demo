import os
import sys
from beamngpy import Vehicle

CART_PARTS_DICT = {'Tailgate': 'tailgate', 'Wagon Unibody': 'wagon_unibody', 'Rear Bumper': 'rear_bumper', 'Front Bumper Support': 'front_bumper_support', 'Front Bumper': 'front_bumper', 'Hood': 'hood', 'Right Headlight': 'right_headlight', 'Left Headlight': 'left_headlight', 'Front Right Fender': 'front_right_fender', 'Front Left Fender': 'front_left_fender', 'Single Exhaust': 'single_exhaust', 'Front Right Door': 'front_right_door', 'Front Left Door': 'front_left_door', 'Rear Right Door': 'rear_right_door', 'Rear Left Door': 'rear_left_door'}

class Car:
    def __init__(self, id, vehicle):
        self.name = "v" + id
        self.vehicle = vehicle
        self.damage = {}

    def set_damage(self, damage):
        self.damage = damage
