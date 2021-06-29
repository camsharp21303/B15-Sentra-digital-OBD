import pygame
import pygame.camera
import sys
import obd
import time
from obd_data import car

default = {
    "speed": "88",
    "rpm": 2000,
    "coolant": "200",
    "load": 50
}

connected = False

WINDOW_WIDTH = 720
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
#pygame.camera.init()

#create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#set the title
pygame.display.set_caption("OBD 2 app")
pygame.display.set_icon(pygame.image.load('nissan.png'))
clock = pygame.time.Clock()

logo = pygame.image.load(work_dir + "logo.png")
logo.convert()
logo = pygame.transform.scale(logo, (177, 136))

meter = pygame.image.load(work_dir + "meter.png")
meter.convert()
meter = pygame.transform.scale(meter, (250, 250))

#cam = pygame.camera.Camera("/dev/video0", (1280, 720))
#cam.start()

def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            running = False

def draw():
    global window
    global clock
    window.fill((0,0,0))
    #cam_image = cam.get_image()
    #cam_image = pygame.transform.scale(cam_image, (350, 196))
    #window.blit(cam_image, (WINDOW_WIDTH/2 - cam_image.get_width()/2, 10))

    #window.blit(logo, (5*WINDOW_WIDTH/8, 5*WINDOW_HEIGHT/8))
    #window.blit(meter, (0, WINDOW_HEIGHT/4))

    color = (255, 255, 255)
    font_size = 30
    font = pygame.font.SysFont('/usr/share/fonts/TTF/Arial.ttf', font_size, False, False)
    font2 = pygame.font.SysFont('/usr/share/fonts/TTF/Arial.ttf', 50, False, False)


    if(not connected):
        data = default
    else:
        data = dict(sentra.getData())

    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(0, WINDOW_HEIGHT/2, 170, 170), 2)
    speedText = font.render("Speed (MPH)", True, color)
    window.blit(speedText, (85 - speedText.get_width()/2, WINDOW_HEIGHT/2 + 10))

    speedSTAT = font2.render(str(data["speed"]), True, color)
    window.blit(speedSTAT, (85 - speedSTAT.get_width()/2, WINDOW_HEIGHT/2 + 85))


    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(180, WINDOW_HEIGHT/2, 170, 170), 2)
    rpmText = font.render("RPM", True, color)
    window.blit(rpmText, (265 - rpmText.get_width()/2, WINDOW_HEIGHT/2 + 10))

    rpmSTAT = font2.render(str(data["rpm"]), True, color)
    window.blit(rpmSTAT, (265 - rpmSTAT.get_width()/2, WINDOW_HEIGHT/2 + 85))


    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(360, WINDOW_HEIGHT/2, 170, 170), 2)
    tempText = font.render("Coolant (F)", True, color)
    window.blit(tempText, (445 - tempText.get_width()/2, WINDOW_HEIGHT/2 + 10))

    tempSTAT = font2.render(str(data["coolant"]), True, color)
    window.blit(tempSTAT, (445 - tempSTAT.get_width()/2, WINDOW_HEIGHT/2 + 85))


    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(540, WINDOW_HEIGHT/2, 170, 170), 2)
    loadText = font.render("Engine Load", True, color)
    window.blit(loadText, (625 - loadText.get_width()/2, WINDOW_HEIGHT/2 + 10))

    loadSTAT = font2.render(str(data["load"]) + "%", True, color)
    window.blit(loadSTAT, (625 - loadSTAT.get_width()/2, WINDOW_HEIGHT/2 + 85))


    fpsText = font.render(str(int(clock.get_fps())), True, color)
    window.blit(fpsText, (0, WINDOW_HEIGHT-font_size))


while running:
    clock.tick(60)
    handle_events()
    draw()

    pygame.display.update()
pygame.camera.quit()
pygame.quit()
sys.exit()
