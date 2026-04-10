import pygame  # type: ignore
import serial # type: ignore
import math
import time


PORT = '/dev/ttyACM0'
BAUD = 38400

WIDTH, HEIGHT = 900, 700
FPS = 60

OBJ_W, OBJ_H, OBJ_D = 1.20, 0.70, 0.50


COLOR = (0, 180, 255)
EDGE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)

AXIS_LEN = 2.0


ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

roll = pitch = yaw = 0.0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VIZU")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

running = True

while running:
    clock.tick(FPS)
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    pygame.display.flip()

pygame.quit()
ser.close()