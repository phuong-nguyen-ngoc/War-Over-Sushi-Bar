#Phuong Nguyen Ngoc, Elliot Zhou, Zixuan Wang, Eduardo Sosa, Katie Andre
#CS269
from common_setting import *
import pygame as pg

class Bullet(pg.sprite.Sprite):

	def __init__ (self, dir, posi, superbullet = False):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface((10,10))
		if superbullet:
			print('true')
			self.image = pg.image.load("superbullet-shoot.png").convert()
		else:
			self.image = pg.image.load("bullet-shoot.png").convert()
			print('false')
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.dir = dir
		if self.dir == 'up':
			self.rect.center=(posi[0],posi[1]-50)#self.rect.center=(posi[0]*40+120,posi[1]*40+220)
				
		elif self.dir == 'down':
			self.rect.center=(posi[0],posi[1]+50)

		elif self.dir == 'left':
			self.rect.center=(posi[0]-50,posi[1])
		
		elif self.dir == 'right':
			self.rect.center=(posi[0]+50,posi[1])
			
	
		self.target=None
		
		self.superbullet = superbullet

	
	def get_center(self):
		return self.rect.center	
	

	def update(self):
		if self.dir == 'up':
			self.rect.y-=20
			if self.rect.bottom<200:
				self.kill()
				
		elif self.dir == 'down':
			self.rect.y+=20
			if self.rect.top>1000:
				self.kill()
				
		elif self.dir == 'left':
			self.rect.x-=20
			if self.rect.left<100:
				self.kill()
		
		elif self.dir == 'right':
			self.rect.x+=20
			if self.rect.left>900:
				self.kill()
