import cv2
import numpy as np
import serial
import os
import time
import configparser
from mss import mss
import threading
import win32api
import sys

class PhantomWare:
    def __init__(self):
        os.system("title PhantomWare ~ AstraPy ~ github.com/astrapy")
        os.system('cls' if os.name == 'nt' else 'clear')

        banner = '''
┏┓┓           ┓ ┏      
┃┃┣┓┏┓┏┓╋┏┓┏┳┓┃┃┃┏┓┏┓┏┓
┣┛┛┗┗┻┛┗┗┗┛┛┗┗┗┻┛┗┻┛ ┗ 
                       
        '''

        columns = os.get_terminal_size().columns
        banner_l = banner.splitlines()
        center_b = '\n'.join(line.center(columns) for line in banner_l)
        print(center_b)

        self.config = configparser.ConfigParser()
        self.config_file = "settings.ini"
        self.load_config()

        self.sct = mss()
        self.screenshot = {
            'left': int((self.sct.monitors[1]['width'] / 2) - (self.fov / 2)),
            'top': int((self.sct.monitors[1]['height'] / 2) - (self.fov / 2)),
            'width': self.fov,
            'height': self.fov
        }

        self.lower = np.array([130, 80, 80])
        self.upper = np.array([165, 255, 255])

        self.arduino = None
        self.connect()

        d_thread = threading.Thread(target=self.detection, daemon=True)
        d_thread.start()

        conf_thread = threading.Thread(target=self.update_conf, daemon=True)
        conf_thread.start()

        self.main_loop()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.config["Aimbot"] = {
                "fov": "100",
                "x_speed": "1.0",
                "y_speed": "1.0"
            }
            self.config["Connection"] = {
                "com_port": "COM3"
            }
            self.config["Keybinds"] = {
                "keybind": "0x02"
            }
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)

        self.config.read(self.config_file)

        self.fov = int(self.config.get("Aimbot", "fov"))
        self.x_speed = float(self.config.get("Aimbot", "x_speed"))
        self.y_speed = float(self.config.get("Aimbot", "y_speed"))
        self.com_port = self.config.get("Connection", "com_port")
        self.keybind = int(self.config.get("Keybinds", "keybind"), 16)


    def update_conf(self):
        new_conf = os.path.getmtime(self.config_file)
        old_config = dict(self.config["Aimbot"])
        
        while True:
            old_conf = os.path.getmtime(self.config_file)
            if old_conf != new_conf:

                self.load_config()

                changed_set = []
                for setting in self.config["Aimbot"]:
                    if self.config["Aimbot"][setting] != old_config.get(setting, None):
                        changed_set.append(f"{setting}: {old_config.get(setting, 'N/A')} -> {self.config['Aimbot'][setting]}")

                if changed_set:
                    for change in changed_set:
                        print(f"Succesfully updated {change}")

                old_config = dict(self.config["Aimbot"])
                new_conf = old_conf

            time.sleep(1)

    def connect(self):
        while True:
            try:
                self.arduino = serial.Serial(self.com_port, 115200)
                print(f"Successfully connected to Arduino on {self.com_port}")
                break
            except serial.SerialException:
                print(f"Failed to connect to {self.com_port}")
                self.com_port = input("Enter new COM port: ").strip()

    def m_movement(self, x, y, z):
        if self.arduino:
            command = f"m{int(x)},{int(y)},{int(z)}\n"
            self.arduino.write(command.encode())

    def detection(self):
        center = self.fov / 2
        while True:
            self.sct = mss()
            if win32api.GetAsyncKeyState(self.keybind) < 0:
                try:
                    img = np.array(self.sct.grab(self.screenshot))
                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, self.lower, self.upper)

                    kernel = np.ones((5, 5), np.uint8)
                    dilated = cv2.dilate(mask, kernel, iterations=2)
                    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    closest_t = None
                    closest_dist = float('inf')
                    min_area = 200

                    for contour in contours:
                        if cv2.contourArea(contour) > min_area:
                            highest_p = min((tuple(c[0]) for c in contour), key=lambda p: p[1])
                            center_x, center_y = highest_p
                            distance = np.sqrt((center_x - center) ** 2 + (center_y - center) ** 2)

                            if distance < closest_dist:
                                closest_dist = distance
                                closest_t = highest_p
    
                    if closest_t:
                        center_x, center_y = closest_t
                        diff_x = center_x - center
                        diff_y = center_y - center

                        target_x = (diff_x * self.x_speed) + 5
                        target_y = (diff_y * self.y_speed) + 6
                        target_z = 1

                        self.m_movement(target_x, target_y, target_z)
                        cv2.circle(img, closest_t, 5, (0, 255, 0), -1)

                except Exception as e:
                    print(f"Error capturing screenshot: {e}")

            time.sleep(0.01)

    def main_loop(self):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    PhantomWare()
