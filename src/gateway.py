
from __future__ import print_function
from is_wire.core import Channel, Subscription, Message, StatusCode, Status, Logger
from is_wire.rpc import ServiceProvider, LogInterceptor
import time
from random import randint
from RequisicaoRobo_pb2 import RequisicaoRobo
from is_msgs import common_pb2
import socket
from is_msgs.robot_pb2 import RobotTaskRequest
from google.protobuf.empty_pb2 import Empty
from is_msgs.common_pb2 import Position
import json

def robotGateway(robotRequest, ctx):

	robotTaskRequest_aux = RobotTaskRequest()	
	if robotRequest.function == "get":
		robotTaskRequest_aux.id = robotRequest.id
		subscription = Subscription(channel)	
		request = Message(content = robotTaskRequest_aux, reply_to=subscription)
		channel.publish(request, topic="Requisicao.Get_position")
		try:
			reply = channel.consume(timeout=1.0)
			position = reply.unpack(RobotTaskRequest)
			robotRequest.positions.x = position.basic_move_task.positions[0].x
			robotRequest.positions.y = position.basic_move_task.positions[0].y
			robotRequest.positions.z = position.basic_move_task.positions[0].z
			return robotRequest
		except socket.timeout:
			log.info('No reply')
  			
	elif robotRequest.function == "set":
		robotTaskRequest_aux.id = robotRequest.id
		robotTaskRequest_aux.basic_move_task.positions.extend([Position(x = robotRequest.positions.x, y = robotRequest.positions.y, z = 															robotRequest.positions.z)])
		subscription = Subscription(channel)
		request = Message(content=robotTaskRequest_aux, reply_to=subscription)
		channel.publish(request, topic="Requisicao.Set_position")        
		try:
			reply = channel.consume(timeout=1.0)
			return Status(reply.status.code, why = reply.status.why)
		except socket.timeout:
			log.info('No reply')        		
	

				
config_file = '../etc/conf/config.json'
config = json.load(open(config_file, 'r'))
channel = Channel(config['broker_uri'])

log = Logger(name='Gateway')	

while True:
	subscription = Subscription(channel)
	subscription.subscribe(topic="Controle.Console")	
	received_message = channel.consume()
	received_struct = received_message.body.decode('utf-8')
	time.sleep(1)
		
	if received_struct == "Ligar sistema":
		rand = randint(0,1)
		if rand == 1:
			message_text = "Ligado"
			message = Message()
			message.body = message_text.encode('utf-8')
			channel.publish(message, topic= "Controle.Console")
			break
		else:
			message_text = "Não foi possível ligar o sistema"
			message = Message()
			message.body = message_text.encode('utf-8')
			channel.publish(message, topic= "Controle.Console")
			continue				
	time.sleep(1)




provider = ServiceProvider(channel)
logging = LogInterceptor()
provider.add_interceptor(logging)

provider.delegate(
	topic = "Requisicao.Robo",
	function = robotGateway,
	request_type = RequisicaoRobo,
	reply_type = RequisicaoRobo)

provider.run()

