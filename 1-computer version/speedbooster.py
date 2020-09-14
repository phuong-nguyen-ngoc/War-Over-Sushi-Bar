#Phuong Nguyen Ngoc, Elliot Zhou, Zixuan Wang, Eduardo Sosa, Katie Andre
#CS269

import pygame as pg

class SpeedBooster(pg.sprite.Sprite):
	def __init__(self, x, y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((10,10))
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		self.rect.center = (x,y)
	
	def get_rect_center(self):
		return self.rect.center
	def set_rect_center(self, x,y):
		self.rect.center = (x,y)