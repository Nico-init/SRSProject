import os

print("hello a tutti quanti!!")

for key in os.environ:
    print(key, '=>', os.environ[key])


