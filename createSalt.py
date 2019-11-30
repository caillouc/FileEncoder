import os


salt = os.urandom(16)
with open(".encoderFileSalt", 'wb') as file:
    file.write(salt)
