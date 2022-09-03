from cmath import rect
import pygame
import sys
from collections.abc import MutableMapping
import obd
import time
from obd_data import car

default = {
    "speed": "88",
    "rpm": 2000,
    "coolant": "200",
    "load": 50
}

#variable to store if car is connected
connected = False
camera_connected = False

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

running = True

work_dir = sys.argv[0].replace("game.py", "")

try:
    sentra = car(sys.argv[1])
    print("Connected to car")
    connected = True
except IndexError:
    print("Not connecting to Car")


#init pygame
pygame.init()

#create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#set the title
pygame.display.set_caption("OBD 2 app")

#get the clock for controlling the frame rate
clock = pygame.time.Clock()

def center_x_text(text_element, rect):
    return (rect.width/2 - text_element.get_width()/2) + rect.x
def center_y_text(text_element, rect):
    return (rect.height/2 - text_element.get_height()/2) + rect.y

def handle_events():
    global running
    for event in pygame.event.get():
        #handle 'x' for exiting application (restart app)
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            running = False
        #press 'c' to clear DTCs
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            sentra.clearDTC()

def draw():
    global window
    global clock
    window.fill((0,0,0))

    color = (255, 255, 255)
    font_size = 30
    font = pygame.font.SysFont('/usr/share/fonts/TTF/Arial.ttf', font_size, False, False)
    font2 = pygame.font.SysFont('/usr/share/fonts/TTF/Arial.ttf', 50, False, False)


    if(not connected):
        data = default
    else:
        data = dict(sentra.getData())
    
    rect_size = WINDOW_WIDTH/3 -40

    speedRect = pygame.Rect((20, 20), (rect_size, rect_size))
    pygame.draw.rect(window, (255, 255, 255), speedRect, 2)
    speedText = font.render("Speed (MPH)", True, color)
    window.blit(speedText, (center_x_text(speedText, speedRect), speedRect.y + 10))

    speedSTAT = font2.render(str(data["speed"]), True, color)
    window.blit(speedSTAT, ((center_x_text(speedSTAT, speedRect), center_y_text(speedSTAT, speedRect))))


    rpmRect = pygame.Rect((speedRect.x + speedRect.width + 20, 20), (rect_size, rect_size))
    pygame.draw.rect(window, (255, 255, 255), rpmRect, 2)
    rpmText = font.render("RPM", True, color)
    window.blit(rpmText, (center_x_text(rpmText, rpmRect), rpmRect.y + 10))

    rpmSTAT = font2.render(str(data["rpm"]), True, color)
    window.blit(rpmSTAT, ((center_x_text(rpmSTAT, rpmRect), center_y_text(rpmSTAT, rpmRect))))


    tempRect = pygame.Rect((20, speedRect.y + speedRect.height + 20), (rect_size, rect_size))
    pygame.draw.rect(window, (255, 255, 255), tempRect, 2)
    tempText = font.render("Coolant (F)", True, color)
    window.blit(tempText, (center_x_text(tempText, tempRect), tempRect.y + 10))

    tempSTAT = font2.render(str(data["coolant"]), True, color)
    window.blit(tempSTAT, ((center_x_text(tempSTAT, tempRect), center_y_text(tempSTAT, tempRect))))


    loadRect = pygame.Rect((speedRect.x + speedRect.height + 20, speedRect.y + speedRect.height + 20), (rect_size, rect_size))
    pygame.draw.rect(window, (255, 255, 255), loadRect, 2)
    loadText = font.render("Engine Load", True, color)
    window.blit(loadText, (center_x_text(loadText, loadRect), loadRect.y + 10))

    loadSTAT = font2.render(str(data["load"]) + "%", True, color)
    window.blit(loadSTAT, ((center_x_text(loadSTAT, loadRect), center_y_text(loadSTAT, loadRect))))


    fpsText = font.render(str(int(clock.get_fps())), True, color)
    window.blit(fpsText, (0, WINDOW_HEIGHT-font_size))


while running:
    clock.tick(60)
    handle_events()
    draw()

    pygame.display.update()

pygame.quit()
sys.exit()

