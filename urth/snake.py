import pygame
import random
import noun # make this a pip package some day
import socket
import os, os.path
import subprocess
import json

def cue_noun(data):
    p = subprocess.Popen([vere_path, 'eval' ,'-cn', '--loom' ,'25'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate(input=data)
    mark = stdout_data.decode().split(' ')[0][1:]
    noun = stdout_data.decode().split(' ')[1:]
    noun = ' '.join(noun)
    return (mark,noun)
    


sock_name = '/slick/control'
pier_path = '/home/amadeo/learn_hoon/tasseg-sophec-mopfel-winrux/'
vere_path = '/home/amadeo/learn_hoon/urbit-test'
CELL_SIZE = 20

sock_path = pier_path+'.urb/dev/'+sock_name


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(sock_path)
data = sock.recv(1024*2)
mark, noun = cue_noun(data)
if(mark == '%init'):
    WIDTH = int(noun.split(' ')[0])*CELL_SIZE
    HEIGHT = int(noun.split(' ')[1][:-2])*CELL_SIZE
else:
    GRID_SIZE = 40
    WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

sock.settimeout(0.1)

pygame.init()

# Create a 15x15 grid, where each cell is 20x20 pixels

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_cell(pos, color):
    pygame.draw.rect(screen, color, (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def game_over():
    pygame.quit()

print("alsowtf")

snake = []
status=''
food = None
while True:

    try:
        data = sock.recv(1024*2)
        mark,noun = cue_noun(data)
        if(mark == '%init'):
            print(f"init: {noun[:-1]}")
        if(mark == '%state'):
            # [[16 27] [16 28] [16 29] [15 29] [14 29] 0] 117 [7 16] %living]
            pylist = noun.replace(' ',', ').replace('%',"'")
            pylist = '['+pylist[:-2]+"']"
            state = eval(pylist)
            snake = state[0][:-1]
            food = state[2]
            status = state[-1]
    except:
        pass

    direction =None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: 
                direction = b'\x00\x0b\x00\x00\x00\x01\xde\xb177:\xb976\xbc\x0e'
            if event.key == pygame.K_a: 
                direction = b'\x00\x0b\x00\x00\x00\x01\xde\xb177:\xb976\x9c\r'
            if event.key == pygame.K_s:
                direction = b'\x00\x0b\x00\x00\x00\x01\xde\xb177:\xb976\x9c\x0c'
            if event.key == pygame.K_d:
                direction = b'\x00\x0b\x00\x00\x00\x01\xde\xb177:\xb976\\\x0e'
            if event.key == pygame.K_SPACE:
                direction = b'\x00\x10\x00\x00\x00\x01\xde\xb177:\xb976\xe0\x99\x83\x0b\x1b+\x03'

    if(direction != None):
        #card = f"[%control {direction}]"
        #print(card)
        #p = subprocess.Popen([vere_path, 'eval' ,'-jn', '--loom' ,'25'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdout_data, stderr_data = p.communicate(input=card.encode())
        #print(stdout_data)
        sock.send(direction)


    # Draw everything
    screen.fill((0, 0, 0))
    for cell in snake: draw_cell(cell, WHITE)
    if(food != None):
        draw_cell(food, RED)

    pygame.display.update()
    if(status == '%ceased'): game_over()
