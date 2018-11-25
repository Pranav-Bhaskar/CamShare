import socket
import cv2
import _thread
import pickle
import time

IP = input('Enter IP : ')
PORT = 8888

class connection_clientside():
	def __init__(self, s):
		self.link = s
		self.reciving_flag = False
	
	def auth(self):
		data = input('Enter Password : ').strip()
		self.link.sendall(data.encode('utf-8'))
	
	def setter(self):
		self.link.sendall('1'.encode('utf-8'))
		self.link.recv(1024)
	
	def get(self):
		try:
			s.sendall('69'.encode('utf-8'))
			data_len = int(self.link.recv(1024).decode('utf-8'))
			#print(data_len)
			if data_len < 100:
				print('error')
				return
			s.sendall('69'.encode('utf-8'))
			data = b''
			while len(data) < data_len:
				block = self.link.recv(4096)
				data += block
			image = pickle.loads(data,encoding='bytes')
			cv2.imwrite('open.png', image)
			if not self.reciving_flag:
				self.reciving_flag = True
				print('Reciveving data from ' + IP) #+ self.ip)
		except KeyboardInterrupt:
			print('\nWill Begining Exitting')
			raise
		except:
			print('Connection Problem\nExitting')
			reciving_flag = False
			raise
		
	def dis(self):
		print('Closing Connection')
		if self.reciving_flag:
			self.reciving_flag = False
			self.link.sendall('17'.encode('utf-8'))
			self.link.close()

if __name__ == "__main__":
	s = socket.socket()

	s.connect((IP, PORT))

	con = connection_clientside(s)

	data = s.recv(1024)
	con.auth()
	data = s.recv(1024)
	print(data.decode())
	if data.decode('utf-8') is '2':
		exit()
	con.setter()
	while True:
		try:
			con.get()
		except:
			break
	con.dis()
