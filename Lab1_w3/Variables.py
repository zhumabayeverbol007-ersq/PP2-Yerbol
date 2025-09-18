                                                #1 Python Variables
x = 5
y = "John"
print(x)
print(y)

x = 4       # x is of type int
x = "Sally" # x is now of type str
print(x)

x = str(3)    # x will be '3'
y = int(3)    # y will be 3
z = float(3)  # z will be 3.0

x = 5
y = "John"
print(type(x))
print(type(y))

x = "John"
# is the same as
x = 'John'

a = 4
A = "Sally"
#A will not overwrite a

                                                   #2 Variable Names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#2myvar = "John" 
#my-var = "John" error
#my var = "John"

                                                   #3 Assign Multiple Values
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)

x = y = z = "Orange"
print(x)
print(y)
print(z)

fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)
                                                    #4 Output Variables
x = "Python is awesome"
print(x)

x = "Python"
y = "is"
z = "awesome"
print(x, y, z)

x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

x = 5
y = 10
print(x + y)

#x = 5
#y = "John"
#print(x + y)

x = 5
y = "John"
print(x, y)
                                                    #5 Global Variables
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()



x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)



def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)



x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)