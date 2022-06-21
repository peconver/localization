import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from nav_msgs.msg import Odometry



class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'steps',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        self.publisher_ = self.create_publisher(Odometry, 'odom_test', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.data = [-8,-8,-8,-8,-8]

    def listener_callback(self, msg):
        # self.get_logger().info('I heard: "%s"' % msg.data)
        self.data = msg.data.split()
        
        
    def timer_callback(self):


        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "world"
        msg.child_frame_id = "base_link"
        

        msg.pose.pose.position.x = -(float(self.data[0]) + 4831)/1000
        msg.pose.pose.position.y = 0.0
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = 0.0
        msg.pose.pose.orientation.w = 1.0
        

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%f"' % msg.pose.pose.position.x)



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
