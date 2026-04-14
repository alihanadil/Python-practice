import pygame
import datetime
import os

pygame.init()
screen = pygame.display.set_mode((1200, 700))
WHITE = (255, 255, 255)

base = r'C:\Users\User\work\practice9\mickeys_clock\images'
image_surface = pygame.image.load(os.path.join(base, 'clock.png')).convert_alpha()
mickey      = pygame.image.load(os.path.join(base, 'mUmrP.png')).convert_alpha()
hand_l      = pygame.image.load(os.path.join(base, 'hand_left_centered.png')).convert_alpha()
hand_r      = pygame.image.load(os.path.join(base, 'hand_right_centered.png')).convert_alpha()

resized_image = pygame.transform.scale(image_surface, (800, 600))
res_mickey    = pygame.transform.scale(mickey, (350, 350))
hand_l_base   = pygame.transform.scale(hand_l, (80, 80))   
hand_r_base   = pygame.transform.scale(hand_r, (100, 100)) 

clockc = (300, 170)

CLOCK_CENTER = (600, 320)

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    now = datetime.datetime.now()
    h = now.hour % 12 
    m = now.minute
    s = now.second

    minutes_angle = -(m * 6 + s * 0.1)        # 6° per minute, smooth with seconds
    hours_angle   = -(h * 30 + m * 0.5)       # 30° per hour, smooth with minutes


    rotated_minutes = pygame.transform.rotate(hand_l_base, minutes_angle)
    rotated_hours   = pygame.transform.rotate(hand_r_base, hours_angle)


    minutes_rect = rotated_minutes.get_rect(center=(600, 340))
    hours_rect   = rotated_hours.get_rect(center=(600,340))

    # Draw everything
    screen.fill(WHITE)

    image_rect = resized_image.get_rect()
    image_rect.center = (600, 340)
    screen.blit(resized_image, image_rect)

    mic_rect = res_mickey.get_rect(center=CLOCK_CENTER)
    screen.blit(res_mickey, mic_rect)

    screen.blit(rotated_hours, hours_rect)     
    screen.blit(rotated_minutes, minutes_rect)  

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()