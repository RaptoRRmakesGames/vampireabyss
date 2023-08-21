import pygame 

class Animation:
    
    def __init__(self, images, time=150):
        self.index = 0
        self.images = images
        
        self.max_index = len(self.images)-1
        
        self.frame_time = time
        self.next_frame = pygame.time.get_ticks() + self.frame_time
        
        self.done = False
        
    def reset_frame_time(self):
        self.next_frame = pygame.time.get_ticks() + self.frame_time
        
    def get_image(self):
        
        return self.images[self.index]
        
    def update(self):
        self.done = False
        
        time_now = pygame.time.get_ticks()
        
        if time_now > self.next_frame:
            
            self.reset_frame_time()
            
            if self.index == self.max_index:
                
                self.index = 0
                self.done = True
                return 
                
            self.index += 1
            
            
            
        
        

class Animator:
    
    def __init__(self, animations, starting_anim):
        
        self.animations = animations # {'run' : animation_object, }
        
        self.anim_name = starting_anim
        
        self.anim = self.animations[self.anim_name]
        
        
    def get_image(self):
        
        return self.anim.get_image()
    
    def update_animations(self):
        
        self.anim.update()
        
    def set_anim(self, animname):
        
        self.anim_name = animname
        self.anim = self.animations[animname]
        self.anim.index = 0
        self.anim.reset_frame_time()
        
    def set_anim_no_refresh(self, animname):
        
        old_index = self.anim.index
        old_frametime = self.anim.next_frame
        
        self.anim_name = animname
        self.anim = self.animations[animname]
        
        self.anim.index = old_index
        self.anim.next_frame = old_frametime
        
        if self.anim.index > self.anim.max_index:
            self.anim.index = 0
        

        
        