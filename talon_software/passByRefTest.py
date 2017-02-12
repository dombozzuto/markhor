# test pass by ref

def pbrTest(x):
    x += 5


x = 5
print x
pbrTest(x)
print x
