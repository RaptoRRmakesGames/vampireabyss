import pygame 
import os 
from random import choice 

from scripts.settings import ROOM_SIZE

def load_images_from_folder(folder_path, rotation = 0, flip=False, sizeup= 1):
    images = []  # List to store loaded images
    
    folder_path = os.path.abspath(folder_path)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                image_surface = pygame.transform.flip(pygame.transform.rotate(pygame.image.load(file_path), rotation),False if rotation ==90 or rotation == -90 else flip, False if rotation ==180 or rotation == 0 else flip).convert_alpha()
                
                img_width = image_surface.get_width()
                img_height = image_surface.get_height()
                
                image_surface = pygame.transform.scale(image_surface, (img_width *sizeup, img_height * sizeup))
                
                images.append(image_surface)
            except pygame.error as e:
                print(f"Error loading image {filename}: {e}")
    return images

def get_images_from_spritesheet(img: pygame.Surface, single_img_x):
    
    imgs = []
    
    iters = img.get_width() // single_img_x
    
    for i in range(iters):
        
        sub = img.subsurface(pygame.Rect(single_img_x * i, 0, single_img_x, img.get_height()))
        
        imgs.append(sub)
        
    return imgs

def create_room_img():
    
    tiles = get_images_from_spritesheet(pygame.image.load('assets/images/world/room_tiles.png').convert_alpha(), 16)
    
    img = pygame.Surface((ROOM_SIZE + 32, ROOM_SIZE + 32))
    
    for x in range((ROOM_SIZE+ 32)//16):
        
        for y in range((ROOM_SIZE+ 32)//16):
            
            crd = (x * 16, y * 16)
            
            if y == 0 and x == 0:
                img.blit(tiles[choice([5,5,5,5])], crd)
                
                continue
            
            if y == 29 and x == 0:
                img.blit(tiles[choice([6,6,6, 6])], crd)
                
                continue
            
            if y == 0 and x == 29:
                img.blit(tiles[choice([8,8,8,8])], crd)
                
                continue
            
            if y == 29 and x == 29:
                img.blit(tiles[choice([7,7,7,7])], crd)
                
                continue
            
            if y == 0:
                
                img.blit(tiles[choice([1,1,1,1])], crd)
                continue
                
            
            if y == 29:
                
                img.blit(tiles[choice([3,3,3,3])], crd)
                continue
                
            if x == 0:
                
                img.blit(tiles[choice([2,2,2,2])], crd)
                continue
            
            if x == 29:
                
                img.blit(tiles[choice([4,4,4,4])], crd)
                continue
            
            img.blit(tiles[choice([0,0,0,0])], crd)
            
            
    img.convert_alpha()
    return img