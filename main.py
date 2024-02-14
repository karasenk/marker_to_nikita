import sys
import os
import pygame
from characters import Nikita, Himik, Marker


def load_font(name, sz=32):
    fullname = os.path.join('fonts', name)
    if not os.path.isfile(fullname):
        print(f'Файл со шрифтом {fullname} не найден')
        sys.exit()
    return pygame.font.Font(fullname, sz)


pygame.init()
pygame.display.set_caption("попасть маркером в никиту")
size = width, height = 800, 800
screen = pygame.display.set_mode(size)

nikita = Nikita([400, 400])
himik = Himik([350, 750])

nikita.timer = pygame.time.get_ticks()

fnt = load_font('18534.TTF')
mainrun = True
markers = []

while mainrun:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainrun = False
            break
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                himik.move(1)
            elif event.key == pygame.K_LEFT:
                himik.move(-1)
            elif event.key == pygame.K_SPACE:
                x, y = himik.coords
                markers.append(Marker([x, y + 50]))
    if pygame.time.get_ticks() - nikita.timer >= 3000:
        nikita.change_dir()
        nikita.timer = pygame.time.get_ticks()
    nikita.move()
    to_del = []
    for i in range(len(markers)):
        markers[i].move()
        markers[i].check_collide(nikita, himik)
        screen.blit(markers[i].image, markers[i].coords)
        if markers[i].coords[1] <= -50 or markers[i].to_del:
            to_del.append(i)
    for num in to_del:
        del markers[num]
    score = fnt.render(str(himik.score), True, (255, 255, 255))
    screen.blit(score, (740, 0))
    screen.blit(himik.img, himik.coords)
    screen.blit(nikita.img, nikita.coords)
    pygame.display.flip()

pygame.quit()
