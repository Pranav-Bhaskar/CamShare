import socket
import _thread
import cv2
import time
import pickle

PASSWORD = '123'
IP = socket.gethostname()
PORT = 8888
NUM = 69	#Maximum number of paralel connection's

'''
	1 -> Authenticate
	2 -> Authenticatication failed
	0 -> Authenticatication done / Send environment
	69 -> Over and out
	17 -> End Connection
'''

class connection_serverside():
	def __init__(self, c, md):
		self.link = c
		self.ip = md[0]
		self.port = md[1]
		self.sending_flag = False
	
	def auth(self):
		self.link.send('1'.encode('utf-8'))
		print('NEW USER ' + self.ip)
		data = self.link.recv(1024)
		print('User ' + self.ip + ' tried entering : ' + data.decode('utf-8'))
		if PASSWORD == str(data.decode('utf-8')):
			self.link.send('0'.encode('utf-8'))
			self.setter()
			return 1
		self.link.send('2'.encode('utf-8'))
		return 0
	
	def setter(self):
		data = self.link.recv(1024)
		self.link.send('2'.encode('utf-8'))
		self.sleep_time = int(data.decode('utf-8'))
	
	def send(self):
		data = self.link.recv(1024)
		if '17' == str(data.decode('utf-8')):
			return False
		return_value, image = camera.read()
		serialized_data = pickle.dumps(image, protocol=2)
		serialized_data_len = str(len(serialized_data))
		self.link.send(serialized_data_len.encode('utf-8'))
		data = self.link.recv(1024)
		if '17' == str(data.decode('utf-8')):
			return False
		self.link.send(serialized_data)
		return True
	
	def sender(self):
		while self.send():
			if not self.sending_flag:
				self.sending_flag = True
				print('Senting data to ' + self.ip)
		print('Connection closed with ' + self.ip)
		c.close()

if __name__ == "__main__":
	s = socket.socket()

	s.bind((IP, PORT))

	s.listen(NUM)

	camera = cv2.VideoCapture(0)

	while True:
		try:
			c, md = s.accept()
			cont = connection_serverside(c, md)
			if cont.auth():
				_thread.start_new_thread(cont.sender, ())
		except KeyboardInterrupt:
			print('\nStopping server.\nExitting')
			break
