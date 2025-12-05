import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryMonitor(Node):
    def __init__(self):
        super().__init__('battery_monitor')
        self.sub = self.create_subscription(Float32, '/battery_voltage', self.callback, 10)

    def callback(self, msg):
        if msg.data < 11.5:
            print(f"Battery low: {msg.data:.2f} V")
        else:
            print(f"Battery: {msg.data:.2f} V")

def main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
