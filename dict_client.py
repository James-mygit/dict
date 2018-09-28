'''电子词典客户端'''
from socket import *
import sys
import getpass



class Dict_client(object):
	def __init__(self, addr, port):
		self.addr = addr
		self.port = int(port)
		self.server_address = (self.addr, self.port)
		print(self.server_address)
		self.init_socket()
	
	# 连接服务端
	def init_socket(self):
		self.sockfd = socket()
		self.sockfd.connect(self.server_address)
		
		# 消息收发函数
		self.handle_client()

	#登录函数
	def Sign_in(self):
		# 登录操作
		name = input('请输入用户名：').encode()
		password = input('请输入密码：').encode()
		print('验证中...')
		self.sockfd.send(b'D$'+b'$@$'+name+b'$@$'+password)
		data = self.sockfd.recv(1024)
		if data == b'OK':
			print('登录成功')
		else:
			print(data.decode())

	#注册函数
	def register(self):
		name = input('请输入用户名：').encode()
		while True:
			# 加密输入  ***************
			# 隐藏密码输入
			password = str(getpass.getpass('请输入密码：')).encode()
			password1 = str(getpass.getpass('请再次确认密码：')).encode()
			if password != password1:
				print("两次密码不一致,请重新输入")
				continue
			elif (b' ' in name) or (b' ' in password):
				print('用户名和密码不允许为空')
				continue
			else:
				print('验证中...')
				break
		self.sockfd.send(b'Z$'+b'$@$'+name+b'$@$'+password)
		data = self.sockfd.recv(1024)
		if data == b'OK':
			print('注册成功')
			# 自动登录
			self.sockfd.send(b'D$'+b'$@$'+name+b'$@$'+password)
			data = self.sockfd.recv(1024)
			if data == b'OK':
				print('登录成功')
			else:
				print(data.decode(),'请重试>>>')

	# 单词查询函数
	def select_word(self):
		print('开始查询...')
		word = input('请输入要查询的单词：').encode()
		self.sockfd.send(b'SW$'+b'$@$'+word)
		data = self.sockfd.recv(1024)
		print('查询结果如下：')
		print(word,':\n\t',data.decode(),'\n\n\n')

	# 查看历史查询记录函数
	def select_history(self):
		print('==========Welcome3===========')
		print('-- 1.查看记录  2.test查看所有   --')
		print('================= ===========')
		key = input('请选择:')
		if key == '1':
			L = []
			self.sockfd.send(b"SH$"+b'$@$'+b'self')
			data = self.sockfd.recv(4096).decode()[2:-2].split('), (')
			for x in data:
				L.append(x.split(', '))
			L_max = self.get_len(L)
			self.show(L, L_max)


		elif key == '2':
			L = []
			self.sockfd.send(b"SH$"+b"$@$"+b'all')
			data = self.sockfd.recv(4096).decode()[2:-2].split('), (')
			for x in data:
				L.append(x.split(', '))
			L_max = self.get_len(L)
			self.show(L, L_max)


	def get_len(self, rows):
	    L = []
	    L_max = []
	    for row in rows:
	        L1 = []
	        for x in row:
	            len_y = 0
	            for y in str(x):
	                if ord(y) > 127:
	                    len_y += 2
	                else:
	                    len_y += 1
	            L1.append(len_y)
	        L.append(L1)
	    for x in zip(*L):
	        L_max.append(max(x))
	    return L_max

	def show(self, rows, L_max):
	    # 开头
	    print('+',end='')
	    for x in L_max:       
	        print('-'*(x+2)+'+',end='')
	    print("")
	    # 内容
	    for row in rows:
	        print('|',end='')
	        count = 0
	        for x in row:
	            len_china = 0
	            for y in str(x):
	                if ord(y) > 127:
	                    len_china += 1
	            s = '%'+'-'+'%d'%(L_max[count]+1-len_china)+'s'
	            print(' '+s%str(x)+'|',end='')
	            count += 1
	        print("")
	    # 结尾
	    print('+',end='')
	    for x in L_max:       
	        print('-'*(x+2)+'+',end='')
	    print("")



	def handle_client(self):
		while True:
			while True:
				print('==========Welcome1===========')
				print('-- 1.注册  2.登录  3.退出 --')
				print('================= ===========')
				key = input('请选择：')
				if key == '1':
					# 注册操作
					self.register()
					break
				elif key == '2':
					# 登录
					self.Sign_in()
					break
				elif key == '3':
					# 退出
					sys.exit('客户端退出')
				else:
					print('输入错误请重新输入>>>')
					sys.stdin.flush() # 清除标准输入，防止恶意快速输入
			while True:
				print('=============Welcome2==============')
				print('-- 1.单词查询  2.查看历史记录  3.退出 --')
				print('===================================')
				key = input('请选择：')
				if key == '1':
					# 查询单词
					self.select_word()
				elif key == '2':
					# 查看历史记录
					self.select_history()
				elif key == '3':
					# 退出
					print('退出二级菜单')
					break
				else:
					print('输入错误请重新输入>>>')
					sys.stdin.flush() # 清除标准输入，防止恶意快速输入







if __name__ == '__main__':
	addr = sys.argv
	clientfd = Dict_client(addr[1],addr[2])

