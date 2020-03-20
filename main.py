from random import shuffle
import pygame
import pyaudio
import numpy

countNumbers = 150


toSort = list(range(0, countNumbers))
srted = list(range(0, countNumbers))

shuffle(toSort)
print(toSort)

pygame.init()
screen_width, screen_height = 1920, 1080
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
screen = pygame.display.set_mode((screen_width, screen_height), flags)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
clock = pygame.time.Clock()
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(width=2), channels=2, rate=44100, output=True)
font1 = pygame.font.SysFont('serif', 30)

run = True
y = screen_height
fps = 240
n = len(toSort)
x0 = 1
xn = screen_height
distance = screen_width/n
height_mplr = (screen_height / n)
width = distance - 1
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
# частота дискретизации
SAMPLE_RATE = 44100
# 16-ти битный звук (2 ** 16 -- максимальное значение для int16)
S_16BIT = 2 ** 16
ArrAcc = 0
Comps = 0

def generate_sample(freq, duration, volume):
    # амплитуда
    amplitude = numpy.round(S_16BIT * volume)
    # длительность генерируемого звука в сэмплах
    total_samples = numpy.round(SAMPLE_RATE * duration)
    # частоте дискретизации (пересчитанная)
    w = 2.0 * numpy.pi * freq / SAMPLE_RATE
    # массив сэмплов
    k = numpy.arange(0, total_samples)
    # массив значений функции (с округлением)
    return numpy.round(amplitude * numpy.sin(k * w))

def drawText():
    txt = font1.render(f"Selection Sort", 1, white)
    txt1 = font1.render(f"Count numbers: {countNumbers}", 1, white)
    txt2 = font1.render(f"Array accesses: {ArrAcc}", 1, white)
    txt3 = font1.render(f"Comparisons: {Comps}", 1, white)
    screen.blit(txt, (20, 20))
    screen.blit(txt1, (20, 55))
    screen.blit(txt2, (20, 90))
    screen.blit(txt3, (20, 125))

def drawGovno(curr, sel):
    screen.fill((0, 0, 0))
    drawText()
    for i in range(len(toSort)):
        if i == curr:
            pygame.draw.rect(screen, red, pygame.Rect(i * distance, y, width, -toSort[i]*height_mplr))
        elif i == sel:
            pygame.draw.rect(screen, blue, pygame.Rect(i * distance, y, width, -toSort[i]*height_mplr))
        else:
            pygame.draw.rect(screen, white, pygame.Rect(i * distance, y, width, -toSort[i]*height_mplr))
    pygame.display.flip()
    stream.write(numpy.array(generate_sample(toSort[curr]+20, 0.1, 1.0), dtype=numpy.int16))
    clock.tick(fps)



def listenKeys():
    run = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
    return run

run = True
current = 1
selected = 0
lstSrtd = len(toSort) - 1
while lstSrtd != 0:
    if run == False:
        break
    selected = 0
    current = 1
    while current != lstSrtd:
        if run == False:
            break
        drawGovno(current, selected)
        run = listenKeys()
        if toSort[current] > toSort[selected]:
            selected = current
        Comps+=1
        ArrAcc+=2
        current += 1
    if not (toSort[current] > toSort[selected]):
        toSort[selected], toSort[current] = toSort[current], toSort[selected]
        ArrAcc+=4
    ArrAcc+=2
    Comps+=1
    lstSrtd -= 1

if run == True:
    for i in range(n):
        if toSort[i] == srted[i]:
            pygame.draw.rect(screen, green, pygame.Rect(i * distance, y, width, -toSort[i] * height_mplr))
        else:
            pygame.draw.rect(screen, black, pygame.Rect(i * distance, y, width, -y))
            pygame.draw.rect(screen, red, pygame.Rect(i * distance, y, width, -toSort[i] * height_mplr))
        pygame.display.flip()
        stream.write(numpy.array(generate_sample(toSort[i]+20, 0.1, 1.0), dtype=numpy.int16))
        clock.tick(fps)

run = True
while run:
    run = listenKeys()


print(toSort)
print(toSort == srted)
