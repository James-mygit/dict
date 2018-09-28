'''
	电子字典服务端
	name : James
	date : 2018-9-28
	This is a dict project for AID
'''
from socket import *
import pymysql as py
import sys
import os


class Dict_server(object):
	def __init__(self):
		self.ADDR = '0.0.0.0'
		self.port = 8888
		self.server_address = (self.ADDR,self.port)
		self.init_socket()
		self.db = py.connect('localhost','root','123456','dict',charset = 'utf8')
		self.cursor = self.db.cursor()
	#创建服务端监听套接字
	def init_socket(self):
		self.sockfd = socket()
		self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.sockfd.bind(self.server_address)
		self.sockfd.listen(5)
		print('Listen to the port:',self.port)

	# 等待客户端连接
	def server_forever(self):
		while True:
			try:
				c,addr = self.sockfd.accept()
				print('IP为%s的用户登录到服务器'%addr[0])
			except KeyboardInterrupt:
				sys.exit('服务端退出')
			except Exception as e:
				print(e)
				continue
			#创建多线程处理客户端连接
			pid = os.fork()
			if pid < 0:
				print('进程创建失败')
			if pid == 0:
				pass
				pid2 = os.fork()
				if pid2 < 0:
					print('进程创建失败')
				if pid2 == 0:
					self.sockfd.close()
					print('IP%s端口%d客户端处理开始....'%addr)
					# 客户端处理函数
					self.handleRequest(c)

			if pid > 0:
				c.close()
				pass

	# 注册函数
	def register(self, c ,data):
		sql_select_name = 'select name from user where name = "%s"'%data[1]
		sql_insert = 'insert into user (name, password) values ("%s", "%s")'%(data[1],data[2])
		try:
			# 判断名字是否重复
			self.cursor.execute(sql_select_name)
			rows = self.cursor.fetchall()
			if not rows:
				# 插入数据
				self.cursor.execute(sql_insert)
				self.db.commit()
				c.send(b'OK')
			else:
				c.send('用户名被占用,无法注册'.encode())
			print('MySQL写入成功')
			return data[1]
		except Exception as e:
			print('SQL语句执行失败！',e)
			self.db.rollback()

	def sign_in(self, c ,data):
		sql_select_name = 'select name,password from user where name = "%s"'%data[1]
		self.cursor.execute(sql_select_name)
		rows = self.cursor.fetchall()
		if not rows:
			print('用户名不存在')
		elif rows[0][0] == data[1]:
			print('%s用户名存在'%data[1])
			if rows[0][1] == data[2]:
				print('%s登录成功'%data[1])
				c.send(b'OK')
				return data[1]
			else:
				c.send('密码错误'.encode())
		else:
			c.send('用户名不存在'.encode())


	# 单词查询函数
	def select_word(self, c, data, name):
		sql_select_word = 'select exp from dict_select where name = "%s"'%data[1]
		self.cursor.execute(sql_select_word)
		rows = self.cursor.fetchall()
		if not rows:
			c.send(('未找到%s对应的结果'%data[1]).encode())
		else:
			c.send((rows[0][0][1:-1]).encode())
			sql_insert_history = 'insert into history \
								(name, select_name) values ("%s","%s")'%(name ,data[1])
			try:
				self.cursor.execute(sql_insert_history)
				self.db.commit()
			except Exception as e:
				print(e)
				self.db.rollback()
			print('查询结束')

	# 查看历史记录
	def select_history(self, c, data, name):
		if data[1] == 'self':
			sql_insert_history = 'select id,name,select_name,\
								DATE_FORMAT(time,"%Y年%m月%d日 %h:%i:%s") \
								from history where name = "{}"'.format(name)
			self.cursor.execute(sql_insert_history)
			rows = self.cursor.fetchall()
			c.send(str(rows).encode())
		elif data[1] == 'all':
			sql_insert_history = 'select id,name,select_name,\
								DATE_FORMAT(time,"%Y %m %d %h:%i:%s") \
								from history'
			self.cursor.execute(sql_insert_history)
			rows = self.cursor.fetchall()
			c.send(str(rows).encode())


	# 处理客户端请求
	def handleRequest(self,c):
		# 等待客户端请求+
		while True:
			data = c.recv(1024).decode()
			data = data.split('$@$')
			if not data or data == ['']:
				sys.exit('客户端退出')
			if data[0] == 'Z$':
				#接收到注册请求
				name = self.register(c, data)
			elif data[0] == 'D$':
				#接收到登录请求
				name = self.sign_in(c, data)
			elif data[0] == 'SW$':
				#接收到查询请求
				self.select_word(c, data, name)
			elif data[0] == 'SH$':
				#接收到查看历史记录请求
				self.select_history(c, data, name)

				




			


if __name__ == '__main__':
	serverfd = Dict_server()
	serverfd.server_forever()
