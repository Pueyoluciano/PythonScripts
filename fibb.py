def fibb(n):
    a = 1
    b = 1
    c = 0
    print a
    print b
    for i in range(1,n-1):
        c = a + b
        a = b
        b = c
        # print str(i)+ ") " + str(c) + " " + str(c % 2)+ " " + str(c % 3)+ " " + str(c % 5)
        print str(c % 2) + " " + str(c % 3) + " " + str(c % 5) + " " + str(c % 7)

fibb(50)        