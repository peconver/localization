from asyncua import Client
import asyncio
import asyncua

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

url = 'opc.tcp://192.168.88.17:4840/freeopcua/server/'
client = asyncua.Client(url)

wheel1 = None
wheel2 = None
wheel3 = None
wheel4 = None

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'steps', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        global value1
        global value2
        global value3
        global value4
        global value5
        global value6
        global value7
        global value8        
        print(value1, value2, value3, value4, value5, value6, value7)        
        # msg.data = 'Hello World: %d' % self.i
        msg.data = ' '.join(map(str, [value1, value2, value3, value4, value5, value6, value7, value8]))
        self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1



async def test(args=None):
    rclpy.init(args=args)
    await client.connect() # RuntimeError
    
    minimal_publisher = MinimalPublisher()
    print("Reading wheels is running.. (odometry/read_wheels.py)")
    while(True):
        global value1
        global value2
        global value3
        global value4
        global value5
        global value6
        global value7
        global value8 
        
        await asyncio.sleep(0.020)
        wheel1 = client.get_node('ns=6;s=::AsGlobalPV:Enc_W_1') # krok motoru na krok kola: /24
        value1 = await wheel1.read_value()
        wheel2 = client.get_node('ns=6;s=::AsGlobalPV:Enc_W_2') # 
        value2 = await wheel2.read_value()

        wheel3 = client.get_node('ns=6;s=::AsGlobalPV:Enc_W_3') # 
        value3 = await wheel3.read_value()

        wheel4 = client.get_node('ns=6;s=::AsGlobalPV:Enc_W_4') # 
        value4 = await wheel4.read_value()     
        
        wheel1angle = client.get_node('ns=6;s=::AsGlobalPV:ANGLW1') # 
        value5 = await wheel1angle.read_value() 
        
        wheel2angle = client.get_node('ns=6;s=::AsGlobalPV:ANGLW2') # 
        value6 = await wheel2angle.read_value()    
        
        wheel3angle = client.get_node('ns=6;s=::AsGlobalPV:ANGLW3') # 
        value7 = await wheel3angle.read_value() 
        
        wheel4angle = client.get_node('ns=6;s=::AsGlobalPV:ANGLW4') # 
        value8 = await wheel4angle.read_value()                                                                 
                           

        rclpy.spin_once(minimal_publisher)
        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


asyncio.run(test())
