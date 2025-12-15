import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class CmdSubscriberVel(Node):
    def __init__(self):
        super().__init__('cmd_subscriber_vel')
        self.ser = serial.Serial('/dev/ttyACM0', 57600, timeout=0.1)

        self.left = 0
        self.right = 0

        self.create_subscription(String, 'key_cmd', self.callback, 10)
    """ def clamp(self, value, min_value=-255, max_value=255):
        return max(min(value, max_value), min_value)

    def send(self):
        # Appliquer les limites AVANT l'envoi
        self.left = self.clamp(self.left)
        self.right = self.clamp(self.right)
       """
    def send(self):
        cmd = f"V {self.left} {self.right}\n"
        self.ser.write(cmd.encode())

    def callback(self, msg):
        key = msg.data

        if key == 'z':
            self.left -= 5
            self.right -= 5
        elif key == 's':
            self.left += 5
            self.right += 5
        elif key == 'a':
            self.left -= 5
            self.right += 5
        elif key == 'e':
            self.left +=5
            self.right -=5
        elif key == 'x':
            self.left = 0
            self.right = 0
        else:
            return

        self.send()

def main():
    rclpy.init()
    node = CmdSubscriberVel()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
