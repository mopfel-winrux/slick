import pygame
import random
from noun import * # make this a pip package some day
import socket
import os, os.path
import subprocess
import json
import sys

def cue_noun(data):
    x = cue(int.from_bytes(data[5:], 'little'))

    hed_len = (x.head.bit_length()+7)//8
    mark = x.head.to_bytes(hed_len,'little').decode()
    noun = x.tail
    return (mark,noun)


sock_name = '/slick/control'
pier_path = '/home/amadeo/learn_hoon/nec/'
vere_path = '/home/amadeo/learn_hoon/urbit-test'
CELL_SIZE = 20

sock_path = pier_path+'.urb/dev/'+sock_name


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(sock_path)
data = sock.recv(1024*2)
mark, noun = cue_noun(data)
if(mark == 'init'):
    WIDTH = noun.head*CELL_SIZE
    HEIGHT = noun.tail*CELL_SIZE
else:
    GRID_SIZE = 40
    WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE


sock.settimeout(0.01)
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_cell(pos, color):
    pygame.draw.rect(screen, color, (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def game_over():
    pygame.quit()

snake = []
status=''
food = None
while True:

    try:
        data = sock.recv(1024*2)
        mark,noun = cue_noun(data)
        noun.pretty(False)
        if(mark == 'init'):
            print(f"init: {noun[:-1]}")
        if(mark == 'state'):
            snake = []
            snek = noun.head
            while(type(snek) == Cell):
                snake.append([snek.head.head, snek.head.tail])
                snek = snek.tail

            fod = noun.tail.tail.head
            
            food = [fod.head, fod.tail]

            tus = noun.tail.tail.tail

            tus_len = (tus.bit_length()+7)//8
            status = tus.to_bytes(tus_len,'little').decode()
    except TimeoutError:
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
        sock.send(direction)


    # Draw everything
    screen.fill((0, 0, 0))
    for cell in snake: draw_cell(cell, WHITE)
    if(food != None):
        draw_cell(food, RED)

    pygame.display.update()
    #if(status == 'ceased'): game_over()
