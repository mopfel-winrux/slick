from bitstream import BitStream
import noun

with open("/home/amadeo/learn_hoon/test.jam", mode='rb') as file:
    jam_file = file.read()


stream = BitStream(jam_file)
