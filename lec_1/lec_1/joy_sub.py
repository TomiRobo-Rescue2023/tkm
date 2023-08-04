#!/usr/bin/env python3

# This example shows a simple way to control the Motoron Motor Controller.
#
# The motors will stop but automatically recover if:
# - Motor power (VIN) is interrupted
# - A temporary motor fault occurs
# - A command timeout occurs
#
# This program will terminate if it does not receive an acknowledgment bit from
# the Motoron for a byte it has written or if any other exception is thrown by
# the underlying Python I2C library.
#
# The motors will stop until you restart this program if the Motoron
# experiences a reset.
#
# If a latched motor fault occurs, the motors experiencing the fault will stop
# until you power cycle motor power (VIN) or cause the motors to coast.

import time
import motoron
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

mc = motoron.MotoronI2C()

tr3 = 0
group = 0

# Reset the controller to its default settings, then disable CRC.  The bytes for
# each of these commands are shown here in case you want to implement them on
# your own without using the library.
mc.reinitialize()  # Bytes: 0x96 0x74
mc.disable_crc()   # Bytes: 0x8B 0x04 0x7B 0x43

# Clear the reset flag, which is set after the controller reinitializes and
# counts as an error.
mc.clear_reset_flag()  # Bytes: 0xA9 0x00 0x04

# By default, the Motoron is configured to stop the motors if it does not get
# a motor control command for 1500 ms.  You can uncomment a line below to
# adjust this time or disable the timeout feature.
# mc.set_command_timeout_milliseconds(1000)
# mc.disable_command_timeout()

# Configure motor 1
mc.set_max_acceleration(1, 140)
mc.set_max_deceleration(1, 300)

# Configure motor 2
mc.set_max_acceleration(2, 200)
mc.set_max_deceleration(2, 300)
class JoySubscriber(Node):
    def __init__(self):
        super().__init__("joy_subscriber")
        self.subscription_joy = self.create_subscription(Joy, "/joy", self.joy_callback, 10)
        self.subscription_joy

    def joy_callback(self, joy_msg):
   
        global tr3,group
       
        if(joy_msg.buttons[1]==1):
           tr3=1
           group=0
       
        if(joy_msg.buttons[0]==1):
           tr3=0
           group=0
           
        if(joy_msg.buttons[2]==1):
           group=1
       
        if(tr3==1 or group==1):
           right=-joy_msg.axes[4]
           left=joy_msg.axes[1]
       
           right_duty=int(right*1000)
           left_duty=int(left*1000)
       
           mc.set_speed(1, right_duty)

           mc.set_speed(2, left_duty)
           time.sleep(0.005)


def main(args=None):
    rclpy.init(args=args)
    sub = JoySubscriber()
    rclpy.spin(sub)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
#try:
#  while True:
#    if int(time.monotonic() * 1000) & 2048:
 #     mc.set_speed(1, 800)
  #  else:
   #   mc.set_speed(1, -800)
#
 #   mc.set_speed(2, 100)
    

  #  time.sleep(0.005)

#except KeyboardInterrupt:
 # pass
