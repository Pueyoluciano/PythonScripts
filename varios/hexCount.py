import sys

if len(sys.argv) == 3:
    print(sys.argv)
    contador = int(sys.argv[1])
    cifras = int(sys.argv[2])
else:
    contador = 64
    cifras = 4

for i in range(0, contador):
    print('{:02X}'.format(i).zfill(cifras))