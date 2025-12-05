import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random


class BatteryPublisher(Node):
    def __init__(self):
        super().__init__('battery_publisher')
        self.publisher_ = self.create_publisher(Float32, '/battery_voltage', 10)
        self.timer = self.create_timer(60.0, self.timer_callback)
        self.get_logger().info('BatteryPublisher gestart')

    def timer_callback(self):
        voltage_value = random.uniform(11.0, 12.6)
        msg = Float32()
        msg.data = voltage_value
        self.publisher_.publish(msg)
        self.get_logger().info(f'batterijspanning: {voltage_value:.2f} V')


def main(args=None):
    rclpy.init(args=args)
    node = BatteryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
