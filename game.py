import pygame
import pygame.camera
import sys
import obd
import time
from obd_data import car

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480

running = True

sentra = car(sys.argv[1])

print(sentra.connection.is_connected())
#init pygame
pygame.init()

#create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#set the title
pygame.display.set_caption("OBD 2 app")
#pygame.display.set_icon(pygame.image.load('nissan.png'))
clock = pygame.time.Clock()

logo = pygame.image.load("/home/pi/logo.png")
logo.convert()
logo = pygame.transform.scale(logo, (177, 136))

meter = pygame.image.load("/home/pi/meter.png")
meter.convert()
meter = pygame.transform.scale(meter, (250, 250))

cam = pygame.camera.Camera("/dev/video0", (1280, 720))
cam.start()

def handle_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            running = False

def draw():
    global window
    global clock
    window.fill((0,0,0))

    window.blit(logo, (5*WINDOW_WIDTH/8, 5*WINDOW_HEIGHT/8))
    window.blit(meter, (0, WINDOW_HEIGHT/4))

    color = (255, 255, 255)
    font_size = 40
    font = pygame.font.SysFont('/usr/share/fonts/TTF/Arial.ttf', font_size, False, False)

    data = dict(sentra.getData())

    if "speed" in data:
        speedText = font.render("Speed: " + str(data["speed"]), True, color)
        window.blit(speedText, (0, 0))

    if "rpm" in data:
        rmpText = font.render(str(int(data["rpm"] // 1)), True, color)
        window.blit(rmpText, (250/2 - rmpText.get_rect().width/2
            , WINDOW_HEIGHT/4 + 250/2 - font_size/2))

    if "coolant" in data:
        tempText = font.render("Water Temp: " + str(data["coolant"]), True, color)
        window.blit(tempText, (0, (font_size+10)*2))

    fpsText = font.render(str(int(clock.get_fps())), True, color)
    window.blit(fpsText, (0, WINDOW_HEIGHT-font_size))

    load = data["load"] / 100
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(WINDOW_WIDTH/2, 0, 350, 40), 0)
    pygame.draw.rect(window, (255, 0, 255), pygame.Rect(WINDOW_WIDTH/2, 0, 350*load, 40), 0)

    window.blit(cam.get_image(), (0, 0))


while running:
    clock.tick(60)
    handle_events()
    draw()

    pygame.display.update()
pygame.quit()
sys.exit()
