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
        
    def get_image(self) -> pygame.Surface:
        
        return self.images[self.index]
    
    def all_images(self) -> [pygame.Surface, pygame.Surface]:
        
        return self.images
    
    def return_self_turned(self,degrees) -> pygame.Surface:

        return Animation([pygame.transform.rotate(img, degrees) for img in self.images], self.frame_time)
            
    def return_self_flipped(self, xbool, ybool) -> 'Animation' :
        
        return Animation([pygame.transform.flip(img, xbool, ybool) for img in self.images], self.frame_time)
    
    def return_self_copied(self) -> 'Animation':
        
        return Animation(self.images, self.frame_time)
        
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
        
    def set_base_anim(self):
        self.anim = self.animations[self.anim_name]
        
    def clone_in_4_dirs_and_flip(self, anim_name):
        
        animation = self.animations[anim_name]
        
        self.animations[anim_name + '_up_' +'left'] = Animation(animation.return_self_copied().images, animation.frame_time)
        self.animations[anim_name + '_down_' +'left'] = Animation(animation.return_self_turned(180).images, animation.frame_time)
        self.animations[anim_name + '_left_' +'left'] = Animation(animation.return_self_turned(90).images, animation.frame_time)
        self.animations[anim_name + '_right_' +'left'] = Animation(animation.return_self_turned(-90).images, animation.frame_time)
        
        self.animations[anim_name + '_up_' +'right'] = Animation(animation.return_self_copied().return_self_flipped(True, False).images, animation.frame_time)
        self.animations[anim_name + '_down_' +'right'] = Animation(animation.return_self_turned(180).return_self_flipped(True, False).images, animation.frame_time)
        self.animations[anim_name + '_left_' +'right'] = Animation(animation.return_self_turned(90).return_self_flipped(False, True).images, animation.frame_time)
        self.animations[anim_name + '_right_' +'right'] = Animation(animation.return_self_turned(-90).return_self_flipped(False, True).images, animation.frame_time)

        
    def get_anim_names(self) -> list:
        
        return [*self.animations.keys()]
    
    def clone_in_4_dirs(self, anim_name):
        
        animation = self.animations[anim_name]
        
        self.animations[anim_name + '_up'] = Animation(animation.return_self_turned(0).images, animation.frame_time)
        self.animations[anim_name + '_down'] = Animation(animation.return_self_turned(180).images, animation.frame_time)
        self.animations[anim_name + '_left'] = Animation(animation.return_self_turned(90).images, animation.frame_time)
        self.animations[anim_name + '_right'] = Animation(animation.return_self_turned(-90).images, animation.frame_time)
        
    def get_image(self) -> pygame.Surface:
        
        return self.anim.get_image()
    
    def update_animations(self):
        
        self.anim.update()
        
    def set_anim(self, animname : str):
        
        self.anim_name = animname
        self.anim = self.animations[animname]
        self.anim.index = 0
        self.anim.reset_frame_time()
        
    def set_anim_no_refresh(self, animname : str):
        
        old_index = self.anim.index
        old_frametime = self.anim.next_frame
        
        self.anim_name = animname
        self.anim = self.animations[animname]
        
        self.anim.index = old_index
        self.anim.next_frame = old_frametime
        
        if self.anim.index > self.anim.max_index:
            self.anim.index = 0
        

        
        