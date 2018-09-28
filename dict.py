'''生成数据库的可导入文件'''
import re
f = open('dict')
f1 = open('dict_1','w')
while True:
	for line in f:
		data = re.findall('^\w*',line)
		line = line[len(data[0]):]
		if line.isspace():
			line = 'Null'
		line = line.strip()
		f1.write(data[0])
		f1.write('$@$') 
		f1.write(repr(line)+'\n')
	break
f.close()