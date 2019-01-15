import random

a = (3,4,5,6,7,8,9,0,'e','r','t','y','u','i')
b = ('q','w','e','r','t','y','u','i','a','s','d','f','g','h','j','z','x','c','v','b')
c = ('a','s','d','f','g','h','j','z','x','c','v','b','n','m')

A = ([3,2,0],[4,3,0],[5,4,0],[6,5,0],[7,6,0],[8,7,0],[9,8,0],[0,9,0],['e',2,1],['r',3,1],['t',4,1],['y',5,1],['u',6,1],['i',7,1])
B = (['q',0,1],['w',1,1],['e',2,1],['r',3,1],['t',4,1],['y',5,1],['u',6,1],['i',7,1],['a',0,2],['s',1,2],['d',2,2],['f',3,2],['g',4,2],['h',5,2],['j',6,2],['z',0,3],['x',1,3],['c',2,3],['v',3,3],['b',4,3])
C = (['a',0,2],['s',1,2],['d',2,2],['f',3,2],['g',4,2],['h',5,2],['j',6,2],['z',0,3],['x',1,3],['c',2,3],['v',3,3],['b',4,3],['n',5,3],['m',6,3])

d = (A,B,C)

# 1 [0,0]
# 2 [1,0]
# 3 [2,0]
# 4 [3,0]
# 5 [4,0]
# 6 [5,0]
# 7 [6,0]
# 8 [7,0]
# 9 [8,0]
# 0 [9,0]
# q [0,1]
# w [1,1]
# e [2,1]
# r [3,1]
# t [4,1]
# y [5,1]
# u [6,1]
# i [7,1]
# o [8,1]
# p [9,1]
# a [0,2]
# s [1,2]
# d [2,2]
# f [3,2]
# g [4,2]
# h [5,2]
# j [6,2]
# k [7,2]
# l [8,2]
# z [0,3]
# x [1,3]
# c [2,3]
# v [3,3]
# b [4,3]
# n [5,3]
# m [6,3]

#     0   1   2   3   4   5   6   7   8   9
e = ( 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 0 ) # 0
f = ('q','w','e','r','t','y','u','i','o','p') # 1
g = ('a','s','d','f','g','h','j','k','l')	  # 2
h = ('z','x','c','v','b','n','m')			  # 3

i = (e,f,g,h) # i[y][x]

letra = ["",0,0] # [#,x,y]

l = [(0,0),(-1,1),(-1,1),(1,0)]
m = [(0,0),(1,-1),(0,1),(1,-1),(0,1)]
p = [(0,0),(1,-1),(1,-1),(1,0),(-1,1)]

salir = 0
	

while (salir != 1):
	passwd  = ""
	passwd2 = ""
	aaa = ""
	
	letra = random.choice(d[0])[:] # l
	passwd2 += str(letra[0])
	for ifor in l:
		letra[1] += ifor[0]
		letra[2] += ifor[1]
		passwd += str(i[letra[2]][letra[1]])

	letra = random.choice(d[1])[:] # m
	passwd2 += str(letra[0])
	
	for ifor in m:
		letra[1] += ifor[0]
		letra[2] += ifor[1]
		passwd += str(i[letra[2]][letra[1]])

	letra = random.choice(d[2])[:] # p
	passwd2 += str(letra[0])

	for ifor in p:
		letra[1] += ifor[0]
		letra[2] += ifor[1]
		passwd += str(i[letra[2]][letra[1]])

	for j in range(3):
		aaa += str(random.choice(range(1,10)))

	passwd += aaa
	passwd2 += aaa

	print passwd2	
	print passwd	
	op = str(raw_input("terminar?"))
	if (op == "1" or op == "s" or op == "S" or op == "y" or op == "Y" or op == "\n"):
		salir = 1
		
	
raw_input("Presione una tecla cualquiera para continuar...")