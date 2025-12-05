import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class CmdSubscriber(Node):
    def __init__(self):
        super().__init__('cmd_subscriber')


        self.ser = serial.Serial('/dev/ttyACM0', 57600, timeout=0.1)


        self.left_speed = 0
        self.right_speed = 0

        self.create_subscription(String, 'key_cmd', self.callback, 10)

    def send_velocity(self):
        cmd = f"V {self.left_speed} {self.right_speed}\n"
        self.ser.write(cmd.encode())
        print("send:", cmd.strip())

    def callback(self, msg):
        key = msg.data

        if key == 'z':
            self.left_speed += 5
            self.right_speed += 5

        elif key == 's':

            self.left_speed -= 5
            self.right_speed -= 5

        elif key == 'a':

            self.left_speed += 5
            self.right_speed -= 5

        elif key == 'x':

            self.left_speed = 0
            self.right_speed = 0

        else:

            return

        self.send_velocity()

def main():
    rclpy.init()
    node = CmdSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
