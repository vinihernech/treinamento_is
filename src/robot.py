
from __future__ import print_function
from is_wire.core import Channel, Subscription, Message, StatusCode, Status, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor
import time
from random import randint
from RequisicaoRobo_pb2 import RequisicaoRobo
from is_msgs import common_pb2
from is_msgs.robot_pb2 import RobotTaskRequest
from google.protobuf.empty_pb2 import Empty
from is_msgs.common_pb2 import Position
import json

class Robot():

	def __init__(self, id, x,y,z):
		self.id = id
		self.pos_x = x
		self.pos_y = y
		self.pos_z = z
		
	def get_id(self):
		return self.id

	def set_position(self,x,y,z):
		self.pos_x = x
		self.pos_y = y
		self.pos_z = z

	def get_position(self):
		return self.pos_x, self.pos_y, self.pos_z


def get_position(Robot_info,ctx):
#Robot_info é uma msg do tipo RobotTaskRequest() com apenas o campo de ID preenchido para identificar o robô
	Robot_aux = RobotTaskRequest()
	for robot in robots:
		if robot.id == Robot_info.id:
			Robot_aux.basic_move_task.positions.extend([Position(x = 0, y = 0, z = 0)])
			Robot_aux.id = Robot_info.id
			Robot_aux.basic_move_task.positions[0].x, Robot_aux.basic_move_task.positions[0].y,Robot_aux.basic_move_task.positions[0].z= robot.get_position()
			log.info("Position was reported")
	
	return Robot_aux


def set_position(Robot_info,ctx):
#Robot_info é uma msg do tipo RobotTaskRequest(), só que além do campo de ID inclui a nova posição para o robô.
	time.sleep(0.2)
	if Robot_info.basic_move_task.positions[0].x < 0 or Robot_info.basic_move_task.positions[0].y < 0 or Robot_info.basic_move_task.positions[0].z < 0:
		log.error("The number must be positive")
		return Status(StatusCode.OUT_OF_RANGE, "The number must be positive")
		
	for robot in robots:
        	if robot.id == Robot_info.id:
            		set_x = Robot_info.basic_move_task.positions[0].x
            		set_y = Robot_info.basic_move_task.positions[0].y
            		set_z = Robot_info.basic_move_task.positions[0].z
            		robot.set_position(set_x, set_y, set_z)
            		log.info("Position was changed")
            		return Status(StatusCode.OK, why = "Position was changed")



config_file = '../etc/conf/config.json'
config = json.load(open(config_file, 'r'))
channel = Channel(config['broker_uri'])

Robot_1 = Robot(0, 0, 0,0)
Robot_2 = Robot(1, 3, 5,0)
Robot_3 = Robot(2, 8, 3,0)
robots = [Robot_1, Robot_2, Robot_3]



log = Logger(name='Robot')	
provider = ServiceProvider(channel)
logging = LogInterceptor()
provider.add_interceptor(logging)

provider.delegate( #get position
	topic = "Requisicao.Get_position",
	function = get_position,
	request_type = RobotTaskRequest, # 3
	reply_type = RobotTaskRequest)
	
provider.delegate(#set position
	topic = "Requisicao.Set_position",
	function = set_position,
	request_type = RobotTaskRequest,
	reply_type = Empty)
	
provider.run()


