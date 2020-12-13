import pygame
import sys
import random


def check_collisions(pipes):
    if bird_rect.top <= -100 or bird_rect.bottom >= H - 112:
        die_sound.play()
        return False
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            die_sound.play()
            return False
    return True


def spawn_pipe():
    pipe_y = random.randint(int(0.2 * H), int(0.6 * H))
    pipe_rect = pipe_surface.get_rect(midtop=(W + 30, pipe_y + pipe_spacing_y // 2))
    pipe_rect_inv = pipe_surface_inv.get_rect(
        midbottom=(W + 30, pipe_y - pipe_spacing_y // 2)
    )

    return pipe_rect, pipe_rect_inv


def draw_score(game_active):
    if game_active:
        score_surface = font.render(f"{int(score)}", False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(W // 2, 50))
        screen.blit(score_surface, score_rect)

    else:
        score_surface = font.render(f"Score: {int(score)}", False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(W // 2, 50))
        screen.blit(score_surface, score_rect)

        score_surface = font.render(f"High score: {int(high_score)}", False, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(W // 2, H - 50))
        screen.blit(score_surface, score_rect)


pygame.init()
pygame.display.set_caption("FlapPy Bird")
clock = pygame.time.Clock()
W, H = (int(0.5 * i) for i in (576, 1024))
screen = pygame.display.set_mode((W, H))
font = pygame.font.Font("assets/04B_19.ttf", 30)

# global variables
game_active = True
framerate = 144
g = 0.125
bird_start_x = 50
bird_start_y = H // 3
bird_max_dy = 6
jump_impulse = 4
pipe_spacing_y = 150
score = 0
high_score = 0
score_per_cycle = 1 / (framerate ** 2) * 100
bird_colour = random.choice(["blue", "red", "yellow"])
pipe_colour = random.choice(["green", "red"])


background = pygame.image.load(
    f"assets/background-{random.choice(['night', 'day'])}.png"
).convert()
game_over_surface = pygame.image.load("assets/gameover.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(W // 2, H // 2))

floor_surface = pygame.image.load("assets/base.png").convert()
floor_x = 0

bird_surface = pygame.image.load(f"assets/{bird_colour}bird-upflap.png").convert_alpha()
bird_rect = bird_surface.get_rect(center=(bird_start_x, bird_start_y))
bird_dy = 0

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
die_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
point_sound = pygame.mixer.Sound("sound/sfx_point.wav")
swoosh_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")

pipe_surface = pygame.image.load(f"assets/pipe-{pipe_colour}.png").convert()
pipe_surface_inv = pygame.transform.flip(pipe_surface, False, True)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, framerate * 10)
pipes = [spawn_pipe()]


# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                bird_dy = -jump_impulse
                if game_active:
                    flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                swoosh_sound.play()
                game_active = True
                pipes = []
                bird_rect.centery = bird_start_y
                bird_dy = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipes.append(spawn_pipe())

    # draw background
    screen.blit(background, (0, 0))

    # draw pipes
    for pipe in pipes:
        screen.blit(pipe_surface, pipe[0])
        screen.blit(pipe_surface_inv, pipe[1])

    # draw floor
    screen.blit(floor_surface, (floor_x, H - 112))
    screen.blit(floor_surface, (floor_x + W, H - 112))

    # draw bird
    rotated_bird = pygame.transform.rotozoom(bird_surface, -bird_dy * 3, 1)
    screen.blit(rotated_bird, bird_rect)

    # draw score
    draw_score(game_active)

    # check collisions
    if game_active:
        game_active = check_collisions(pipes)

    if game_active:
        # animate and despawn pipes
        for pipe in pipes:
            pipe[0].centerx -= 1
            pipe[1].centerx -= 1
        pipes = [pipe for pipe in pipes if pipe[0].right > -30]

        # animate bird
        bird_rect.centery += bird_dy
        bird_dy += g
        bird_dy = min(bird_max_dy, bird_dy)

        # animate floor
        floor_x -= 1
        if floor_x <= -W:
            floor_x = 0

        score += 0.01
        high_score = max(int(score), high_score)

    else:
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.update()
    clock.tick(framerate)
