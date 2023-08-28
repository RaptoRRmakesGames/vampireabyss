import pygame 
import os

from scripts.settings import ROOM_SIZE
from scripts.utils import get_images_from_spritesheet

def draw_grid(tile_size):
    
    grid_surf = pygame.Surface((100*tile_size, 100*tile_size)).convert()
    
    for x in range(100):
        
        for y in range(100):
            
     
            pygame.draw.rect(grid_surf, (100,100,100), pygame.Rect(x*tile_size, y*tile_size, tile_size, tile_size), 1)
            
    grid_surf.set_colorkey((0,0,0))
    return grid_surf
    
tile_imgs = get_images_from_spritesheet(pygame.image.load('assets/images/world/room_tiles.png'), 16)
index = 0

surf = pygame.image.load('assets/images/world/room.png') if os.path.exists('assets/images/world/room.png') else pygame.Surface((ROOM_SIZE, ROOM_SIZE))

screen = pygame.display.set_mode((600,600))

display = pygame.Surface((300,300))

clock = pygame.time.Clock()

scroll = [0,0]

run = True

grid = draw_grid(16)

draw_grid_b = True

zoom = 1

def keys():
    global zoom
    
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        
        scroll[0] -= 2
        
    if keys[pygame.K_d]:
        
        scroll[0] += 2
    
    if keys[pygame.K_w]:
        
        scroll[1] -= 2
        
    if keys[pygame.K_s]:
        
        scroll[1] += 2
        
    if not zoom > 2:
        if keys[pygame.K_e]:
            
            zoom += zoom * 0.01
    if not  zoom < 0.5:
        if keys[pygame.K_q]:
            
            zoom -= zoom * 0.01
        
def render():

    display.blit(surf, (64-scroll[0], 64-scroll[1]))
    if draw_grid_b:
        display.blit(grid, (-800-scroll[0], -800-scroll[1]))
        pygame.draw.rect(display, (255,0,0), surf.get_rect(topleft=(64-scroll[0], 64-scroll[1]) ), 3)
    

while run:
    
    pygame.display.set_caption(str(round(clock.get_fps())))
    
    screen.fill((0,0,0))
    display.fill((0,0,0))
    
    clock.tick(60)
    
    mouse_pos = (
        pygame.mouse.get_pos()[0]/2,
        pygame.mouse.get_pos()[1]/2
        )
    
    current_x = round(int((mouse_pos[0]+ 16) / 16 ) + scroll[0] /16  ) 
    current_y = round(int((mouse_pos[1]+ 16) / 16 ) + scroll[1] /16  ) 
    
    selected_img = tile_imgs[index]
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            
            run = False 
            
            pygame.image.save(surf, 'assets/images/world/room.png')
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_g:
                
                draw_grid_b = not draw_grid_b
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if surf.get_rect(topleft=(64-scroll[0], 64-scroll[1]) ).collidepoint(mouse_pos):
                
                # surf.blit(selected_img, (current_x * 16 - 16*5 - scroll[0], current_y * 16 - 16 * 5- scroll[1]))
                surf.blit(selected_img, (((current_x -5) *16, (current_y -5) *16)))
                print('hah')
                
                
    keys()
    render()

    
    screen.blit(pygame.transform.scale(display, (600,600)), (0,0))
    
    pygame.display.update()