# This is pseudo-code, not runnable Python.
# It illustrates the structure of a simple ROS 2 publisher and subscriber.

# --- Publisher Node ---

# Import necessary ROS 2 libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyPublisher(Node):

    def __init__(self):
        # Initialize the node with the name 'my_publisher'
        super().__init__('my_publisher')

        # Create a publisher on the 'chatter' topic
        # The message type is String
        # The queue size is 10
        self.publisher_ = self.create_publisher(String, 'chatter', 10)

        # Create a timer that calls the 'publish_message' callback every 0.5 seconds
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.publish_message)
        self.i = 0

    def publish_message(self):
        # Create a new String message
        msg = String()
        # Set the data of the message
        msg.data = f'Hello World: {self.i}'
        # Publish the message
        self.publisher_.publish(msg)
        # Log the published message to the console
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    # Initialize the ROS 2 Python client library
    rclpy.init(args=args)
    # Create an instance of the publisher node
    my_publisher = MyPublisher()
    # 'spin' the node so its callbacks are called
    rclpy.spin(my_publisher)
    # Destroy the node explicitly
    my_publisher.destroy_node()
    # Shutdown the ROS 2 client library
    rclpy.shutdown()

# --- Subscriber Node ---

class MySubscriber(Node):

    def __init__(self):
        # Initialize the node with the name 'my_subscriber'
        super().__init__('my_subscriber')
        # Create a subscriber on the 'chatter' topic
        # The callback function 'listener_callback' is called when a message is received
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # Log the received message to the console
        self.get_logger().info(f'I heard: "{msg.data}"')

def main_subscriber(args=None):
    # Initialize rclpy
    rclpy.init(args=args)
    # Create the subscriber node
    my_subscriber = MySubscriber()
    # Spin the node
    rclpy.spin(my_subscriber)
    # Destroy the node and shutdown rclpy
    my_subscriber.destroy_node()
    rclpy.shutdown()

