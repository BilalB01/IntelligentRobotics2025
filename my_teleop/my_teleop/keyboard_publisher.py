import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class KeyboardPublisher(Node):
    def __init__(self):
        super().__init__('keyboard_publisher')
        self.pub = self.create_publisher(String, 'key_cmd', 10)
        print("z=forward, s=backward, a=left, e=right, q=quit")

    def run(self):
        while rclpy.ok():
            key = input("> ")
            if key == "q":
                break
            msg = String()
            msg.data = key
            self.pub.publish(msg)

def main():
    rclpy.init()
    node = KeyboardPublisher()
    node.run()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
