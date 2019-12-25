import os
import time
import pigpio

class Motor(object):
    def __init__(self, en=False):
        if en:
            self.pigpiod()
        self.pi = pigpio.pi()
        self.max_speed = 2500  # Max Throttle
        self.min_speed = 900  # Min Throttle

        self.m1 = 19  # Front	CW-L
        self.m2 = 13  # Front	CCW-R
        self.m3 = 12  # Back	CW-R
        self.m4 = 18  # Back	CCW-L

        self.m1_temp = self.min_speed  # Front	CW-R	TEMP-VALUE
        self.m2_temp = self.min_speed  # Front	CCW-R	TEMP-VALUE
        self.m3_temp = self.min_speed  # Back	CW-R	TEMP-VALUE
        self.m4_temp = self.min_speed  # Back	CCW-L	TEMP-VALUE

    def pigpiod(self):
        os.system("sudo pigpiod")

    def off(self):
        self.pi.set_servo_pulsewidth(self.m1, 0)
        self.pi.set_servo_pulsewidth(self.m2, 0)
        self.pi.set_servo_pulsewidth(self.m3, 0)
        self.pi.set_servo_pulsewidth(self.m4, 0)

    def setmax(self):
        self.pi.set_servo_pulsewidth(self.m1, self.max_speed)
        self.pi.set_servo_pulsewidth(self.m2, self.max_speed)
        self.pi.set_servo_pulsewidth(self.m3, self.max_speed)
        self.pi.set_servo_pulsewidth(self.m4, self.max_speed)

    def setmin(self):
        self.pi.set_servo_pulsewidth(self.m1, self.min_speed)
        self.pi.set_servo_pulsewidth(self.m2, self.min_speed)
        self.pi.set_servo_pulsewidth(self.m3, self.min_speed)
        self.pi.set_servo_pulsewidth(self.m4, self.min_speed)
    
    def start(self):
        self.off()
        time.sleep(1)

        self.setmax()
        time.sleep(1)

        self.setmin()
        time.sleep(1)

    def stop(self):
        self.setmin()

    def setspeed(self, v1, v2, v3, v4):
        if v1 != self.m1_temp:
            self.pi.set_servo_pulsewidth(self.m1, v1)
        if v2 != self.m2_temp:
            self.pi.set_servo_pulsewidth(self.m2, v2)
        if v3 != self.m3_temp:
            self.pi.set_servo_pulsewidth(self.m3, v3)
        if v4 != self.m4_temp:
            self.pi.set_servo_pulsewidth(self.m4, v4)
        self.m1_temp = v1
        self.m2_temp = v2
        self.m3_temp = v3
        self.m4_temp = v4

    def esc(self):  
        '''This is the auto calibration procedure of a normal ESC'''
        self.off()
        print("Disconnect the Battery and Propellers!!!")
        print("Then Press Enter!!!")
        inp = input()
        if inp == "":
            self.setmax()

            print("Connect the battery Now!!!")
            print("You will here two beeps then Press Enter (within 5sec)!!!")

            inp = input()
            if inp == "":
                self.setmin()

                print("Wait for Gradual falling tone then press Enter!!!")

                inp = input()
                if inp == "":
                    self.off()
                    time.sleep(1)
                    self.stop()

                    print("MAX/MIN THORTTLE SAVED")
                    print("Success!!!")
