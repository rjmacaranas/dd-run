"""
TODO:
    - game startup
    - end game (collision)
"""

import pygame
import random

pygame.init()

WHITE = (255,255,255)



# Set screen size
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("DD Run")
icon = pygame.image.load('dd_icon.png')
pygame.display.set_icon(icon)

# Obstacle Images
obstacle_size = 64
obstacle_size2 = 128
obstacle_img = pygame.image.load("cucumber.png")
obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_size, obstacle_size))
obstacle_img2 = pygame.image.load("feet.png")
obstacle_img2 = pygame.transform.scale(obstacle_img2, (obstacle_size2, obstacle_size2))
powerup_img = pygame.image.load("moldy-clothes.png")
powerup_img = pygame.transform.scale(powerup_img, (obstacle_size, obstacle_size))

obstacle_img_list = [obstacle_img, obstacle_img2, powerup_img]

obstacle_x = 730
obstacle_y = 465

obstacle_x2 = -100
obstacle_y2 = -100

obstacle_status = 0
obstacle_status2 = 0

obstacle_speed = 10

score = 0
hi_score = 0

dd_menu_img = pygame.image.load("menu.png")
dd_song_img = pygame.image.load("song_select.png")

# DD Images
size = 128
dd_stand_img = pygame.image.load("dd-stand.png")
dd_stand_img = pygame.transform.scale(dd_stand_img, (size, size))
dd_walk_img = pygame.image.load("dd-walk.png")
dd_walk_img = pygame.transform.scale(dd_walk_img, (size, size))
dd_jump_img = pygame.image.load("dd-jump.png")
dd_jump_img = pygame.transform.scale(dd_jump_img, (size, size))
dd_crawl_img = pygame.image.load("dd-crawl.png")
dd_crawl_img = pygame.transform.scale(dd_crawl_img, (size, size))
dd_crawl_img2 = pygame.image.load("dd-crawl-2.png")
dd_crawl_img2 = pygame.transform.scale(dd_crawl_img2, (size, size))
dd_stand_moldy_img = pygame.image.load("dd-stand-moldy.png")
dd_stand_moldy_img = pygame.transform.scale(dd_stand_moldy_img, (size, size))
dd_walk_moldy_img = pygame.image.load("dd-walk-moldy.png")
dd_walk_moldy_img = pygame.transform.scale(dd_walk_moldy_img, (size, size))
dd_jump_moldy_img = pygame.image.load("dd-jump-moldy.png")
dd_jump_moldy_img = pygame.transform.scale(dd_jump_moldy_img, (size, size))
dd_crawl_moldy_img = pygame.image.load("dd-crawl-moldy.png")
dd_crawl_moldy_img = pygame.transform.scale(dd_crawl_moldy_img, (size, size))
dd_crawl_moldy_img2 = pygame.image.load("dd-crawl-2-moldy.png")
dd_crawl_moldy_img2 = pygame.transform.scale(dd_crawl_moldy_img2, (size, size))
dd_move_list = [dd_stand_img, dd_walk_img, dd_jump_img, dd_crawl_img, dd_crawl_img2]
dd_moldy_list = [dd_stand_moldy_img, dd_walk_moldy_img, dd_jump_moldy_img, dd_crawl_moldy_img, dd_crawl_moldy_img2]

dd_move_status = 0
dd_mold_status = 0

dd_vulnerable_status = 1
invulnerable_frame = 0



frame = 1

# DD Coordinates
ddX = 40
ddY = 400

v = 5
m = 5

is_jump = False
is_crawl = False
running = True
start = False
song_select = False

song = None

def isCollision(obstacle_x, obstacle_x2, obstacle_y, obstacle_y2, ddX, ddY, obstacle_status):
    global dd_mold_status
    global dd_vulnerable_status
    global frame
    distance1 = ((obstacle_x - ddX) ** 2 + (obstacle_y - ddY)** 2) ** 0.5
    distance2 = ((obstacle_x2 - ddX) ** 2 + (obstacle_y2 - ddY)** 2) ** 0.5

    if dd_vulnerable_status == 1:
        # Cucumber Collision
        if obstacle_status == 0:
            if distance1 < 80 or distance2 < 80:
                if dd_mold_status == 0:
                    return "end"
                else:
                    dd_mold_status = 0
                    dd_vulnerable_status = 0
                    frame = 1

        # Foot Collision
        elif obstacle_status == 1:
            if ddY < 410 and (distance1 < 110 or distance2 < 110):
                if dd_mold_status == 0:
                    return "end"
                else:
                    dd_mold_status = 0
                    dd_vulnerable_status = 0
                    frame = 1

        elif obstacle_status == 2:
            if distance1 < 80 or distance2 < 80:
                return "moldify"

while running:

    screen.fill((156, 206, 255))
    obstacle_x2 = -1000
    obstacle_y2 = -1000
    while not start:
        screen.blit(dd_menu_img, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
        pygame.display.update()

    while not song_select:
        screen.blit(dd_song_img, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    song = "spongebob.mp3"
                elif event.key == pygame.K_2:
                    song = "lefestin.mp3"
                elif event.key == pygame.K_3:
                    song = "dogsout.mp3"
                elif event.key == pygame.K_4:
                    song = "rocketman.mp3"
                elif event.key == pygame.K_5:
                    song = "bugcat.mp3"
            if song is not None:
                song_select = True
                pygame.mixer_music.load(song)
                pygame.mixer_music.play(-1)
        pygame.display.update()

    screen.blit(obstacle_img_list[obstacle_status], (obstacle_x, obstacle_y))
    #screen.blit(obstacle_img_list[obstacle_status2], (obstacle_x2, obstacle_y2))

    #Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render("score: " + str(score), 1, WHITE)
    screen.blit(text, (100,10))

    if score > hi_score:
        hi_score = score
    font = pygame.font.Font(None, 74)
    text = font.render("high score: " + str(hi_score), 1, WHITE)
    screen.blit(text, (100, 50))

    # loop obstacle
    if obstacle_x > 0:
        obstacle_x -= obstacle_speed
        obstacle_x2 -= obstacle_speed
    else:
        obstacle_status = random.randint(0, 1)
        score += 100
        if score % 1000 == 0 and obstacle_speed < 100:
            obstacle_status = 2
            obstacle_speed += 2


        obstacle_x = 730
        if obstacle_status == 0:
            obstacle_y = 465

        elif obstacle_status == 1:
            obstacle_y = 295

    if obstacle_x == 400:
        obstacle_status2 = random.randint(0, 1)
        score += 100
        obstacle_x2 = 730
        if obstacle_status2 == 0:
            obstacle_y2 = 465

        elif obstacle_status2 == 1:
            obstacle_y2 = 295

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not is_jump:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    is_jump = True

                if event.key == pygame.K_DOWN:
                    dd_move_status = 3
                    ddY += 10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_crawl = False
                    dd_move_status = 0
                    ddY -= 10

    if is_jump:

        F = (1 / 2) * m * (v ** 2)  # Calculating the force
        dd_move_status = 2
        ddY -= F
        v = v - 0.5  # Decreasing velocity while going up and becoming negative while coming down
        if v < 0:  # Maximum height
            m = -5  # Counter negative velocity
        if v == -5.5:  # Object reaches original state
            is_jump = False
            dd_move_status = 0
            # Set to original v and m
            v = 5
            m = 5

    pygame.time.delay(20)

    collision = isCollision(obstacle_x, obstacle_x2, obstacle_y, obstacle_y2, ddX, ddY, obstacle_status)
    if collision == "end":
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over", 1, WHITE)
        screen.blit(text, (400, 300))
        font = pygame.font.Font(None, 50)
        text = font.render("Press space to restart!", 1, WHITE)
        screen.blit(text, (400, 450))
        screen.blit(dd_move_list[dd_move_status], (ddX, ddY))
        pygame.display.update()
        game_open = True
        while game_open:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quitting...")
                    game_open = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # reset the game
                        song_select = False
                        song = None
                        print("resetting...")
                        dd_move_status = 0
                        dd_mold_status = 0
                        frame = 1
                        ddX = 40
                        ddY = 400
                        v = 5
                        m = 5
                        is_jump = False
                        is_crawl = False
                        running = True
                        obstacle_x = 730
                        obstacle_y = 465
                        obstacle_x2 = -100
                        obstacle_y2 = -100
                        obstacle_status = 0
                        obstacle_status2 = 0
                        obstacle_speed = 10
                        score = 0
                        game_open = False



    if collision == "moldify":
        dd_mold_status = 1

    if dd_mold_status == 0:
        screen.blit(dd_move_list[dd_move_status], (ddX, ddY))
    if dd_mold_status == 1:
        screen.blit(dd_moldy_list[dd_move_status], (ddX, ddY))

    if frame == 5:
        if dd_move_status == 0 or dd_move_status == 1:
            dd_move_status = not dd_move_status
        elif dd_move_status == 3:
            dd_move_status = 4
        elif dd_move_status == 4:
            dd_move_status = 3
        frame = 1
    frame += 1

    if not dd_vulnerable_status:
        if invulnerable_frame < 20:
            invulnerable_frame += 1
        else:
            dd_vulnerable_status = 1
            invulnerable_frame = 0



    pygame.display.update()