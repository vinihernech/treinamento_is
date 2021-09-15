
from __future__ import print_function
from is_wire.core import Channel, Message, Subscription,StatusCode, Status, Logger
import time
from is_wire.rpc import ServiceProvider, LogInterceptor
from random import randint
from RequisicaoRobo_pb2 import RequisicaoRobo
import socket
from is_msgs import common_pb2
from is_msgs.robot_pb2 import RobotTaskRequest
from is_msgs.common_pb2 import Position
import json



config_file = '../etc/conf/config.json'
config = json.load(open(config_file, 'r'))
channel = Channel(config['broker_uri'])

log = Logger(name='Client')

while True:
	#Publisher
	message_text = "Ligar sistema"	
	message = Message()
	message.body = message_text.encode('utf-8')
	channel.publish(message, topic= "Controle.Console")
		
	#Sub
	subscription = Subscription(channel)
	subscription.subscribe(topic="Controle.Console")
	message = channel.consume()
	message.body.decode('utf-8')
	log.info(message.body.decode('utf-8'))	
	if message.body.decode('utf-8') == "Ligado":
		break	
	time.sleep(1)
	


while True:
	time.sleep(5)  
	RobotRequest = RequisicaoRobo()
	RobotRequest.id = 0 

	function = randint(0,1)
	
	if function == 0:
		RobotRequest.function = "set"
		RobotRequest.positions.x = randint(1,15)
		RobotRequest.positions.y = randint(1,15)
		RobotRequest.positions.z = randint(-3,15) #Para testar o tratamento de números negativos na posição
						
	else: 
		RobotRequest.function = "get"
		
	subscription = Subscription(channel)
	RobotMsg = Message(content = RobotRequest, reply_to = subscription)
	channel.publish(RobotMsg, topic = "Requisicao.Robo")
	
	try:
		reply = channel.consume(timeout=2.0)
		position = reply.unpack(RequisicaoRobo)
		if function == 1:
			log.info(f'Get Position | Robot ID: {RobotRequest.id} | Position: (X = {position.positions.x}, Y = {position.positions.y}, Z = {position.positions.z})')
		else:
			log.info(f'Set Position | Robot ID: {RobotRequest.id} | New Position: X = {RobotRequest.positions.x}, Y = {RobotRequest.positions.y}, Z = {RobotRequest.positions.z}')
			if reply.status.why == "The number must be positive":
				log.error(f'{reply.status.why}')
			else:
				log.info(f'{reply.status.why}')	
	except socket.timeout:
		log.warn('No reply')   
	    		
