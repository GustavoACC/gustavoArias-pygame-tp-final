import pygame
from pygame.locals import *
from constantes import *

class Widget:
    def __init__(self,master_form,x,y,w,h,color_border,image_background,text,font,font_size,font_color):
        self.master_form = master_form
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_border = color_border
        if image_background != None:
            self.image_background = pygame.image.load(image_background)
            self.image_background = pygame.transform.scale(self.image_background,(w, h)).convert_alpha()
        else:
            self.image_background = None
        self._text = text
        if(self._text != None):
            pygame.font.init()
            self._custom_font = pygame.font.Font(font,font_size)
            self._font_color = font_color

    def render(self):
        
        self.slave_surface = pygame.Surface((self.w,self.h), pygame.SRCALPHA)
        self.slave_rect = self.slave_surface.get_rect()
        self.slave_rect.x = self.x
        self.slave_rect.y = self.y
        self.slave_rect_collide = pygame.Rect(self.slave_rect)
        self.slave_rect_collide.x += self.master_form.x
        self.slave_rect_collide.y += self.master_form.y
        
        if self.image_background:
            self.slave_surface.blit(self.image_background,(0,0))
        
        if(self._text != None):
            image_text = self._custom_font.render(self._text,True,self._font_color)
            self.slave_surface.blit(image_text,[
                self.slave_rect.width/2 - image_text.get_rect().width/2,
                self.slave_rect.height/2 - image_text.get_rect().height/2
            ])
            
        if self.color_border:
            pygame.draw.rect(self.slave_surface, self.color_border, self.slave_surface.get_rect(), 2)

    def update(self):
        pass

    def draw(self):
        self.master_form.surface.blit(self.slave_surface,self.slave_rect)