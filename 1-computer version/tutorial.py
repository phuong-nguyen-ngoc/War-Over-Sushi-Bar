
import pygame as pg
import random
import time
pg.init()
from chef import Chef
from block import Block
from bullet import Bullet
from common_setting import *
import game as gm
  



class Tutorial:
	
	def __init__(self):
		
		self.screen = pg.display.set_mode((WIDTH-200, HEIGHT))
		#self.background = pg.image.load(backgrounds[level-1])
		self.background = pg.image.load('background.png')
		self.screen.blit(pg.image.load('background.png'),(0,0))
	
		pg.display.set_caption("Chef War")
		#self.screen.blit(self.background, [250,250])
		self.clock = pg.time.Clock()
		self.running = True
		self.playing = True
		# groups
		self.all_sprites = pg.sprite.Group()		
		self.all_blocks = pg.sprite.Group()
		self.all_bullets = pg.sprite.Group()
		self.all_bonus = pg.sprite.Group()
		self.all_superbullets = pg.sprite.Group()

		self.chef1 = Chef(5,5, chef1_moves, False, self.all_bullets, self.all_sprites,self.all_superbullets)
		self.chef1.cabbage = 100
		self.all_sprites.add(self.chef1)
		
		#font variable
		self.font1 = pg.font.Font('caligraphy.ttf', 50) 
		self.font2 = pg.font.Font('Organo.ttf', 20) 
		self.font3 = pg.font.Font('Arial.ttf', 15) 
		self.font4 = pg.font.Font('Arial.ttf', 15) 	
		self.font5 = pg.font.Font('Organo.ttf', 10) 
		self.map = maps[1]
		
		self.block2 = Block(8, 7, 4, False, 4)
		self.block3 = Block(8, 6, 3, False, 1)
		self.block4 = Block(8, 5 , 0, True, 0)
		
		self.g = g = gm.Game(8)

		self.story_progress = True
		self.story_progress2 = True
		self.story_progress3 = True
		self.story_progress4 = True
		self.story_progress5 = True
		
		
	def button(self, msg,x,y,w,h,ic,ac):
		self.mouse = pg.mouse.get_pos()
		self.click = pg.mouse.get_pressed()
		self.screen.blit(pg.image.load('conf.png'),(300,950))

		if x+w > self.mouse[0] > x and y+h > self.mouse[1] > y:
			self.screen.blit(pg.image.load('conf-select.png'),(300,950))
			if self.click[0] == 1:
				self.story_progress = False
				self.story2()
				
			
	def button2(self, msg,x,y,w,h,ic,ac):
		self.mouse2 = pg.mouse.get_pos()
		self.click2 = pg.mouse.get_pressed()
		if x+w > self.mouse2[0] > x and y+h > self.mouse2[1] > y:
			self.screen.blit(pg.image.load('story2-select-con.png'),(100,200))
			if self.click2[0] == 1:
				self.story_progress2 = False
				self.players()
				
	def button3(self, msg,x,y,w,h,ic,ac):
		self.mouse3 = pg.mouse.get_pos()
		self.click3 = pg.mouse.get_pressed()
		
		self.screen.blit(pg.image.load('conf.png'),(x,y))
	
		
		if x+w > self.mouse3[0] > x and y+h > self.mouse3[1] > y:
			self.screen.blit(pg.image.load('conf-select.png'),(x,y))
			if self.click3[0] == 1:
				self.story_progress4 = False
				self.blockex()
				
				
	def button4(self, msg,x,y,w,h,ic,ac):
		self.mouse4 = pg.mouse.get_pos()
		self.click4 = pg.mouse.get_pressed()
		
		self.screen.blit(pg.image.load('bigcon.png'),(x,y))
	
		
		if x+w > self.mouse4[0] > x and y+h > self.mouse4[1] > y:
			self.screen.blit(pg.image.load('bigcon-select.png'),(x,y))
			if self.click4[0] == 1:
				self.story_progress3 = False
				self.controls()				
				

	def learnButton(self, msg,x,y,w,h,ic,ac):
		if self.lhold == False:
			self.mousel = pg.mouse.get_pos()
			self.clickl = pg.mouse.get_pressed()
		#pg.draw.rect(self.screen, ac,(x,y,w,h))
		text = self.font2.render( msg, True, (0,0,0))
		textRect = text.get_rect()
		textRect.center = ( (x+(w/2)), (y+(h/2)) )
		self.screen.blit(text,textRect)
		if x+w > self.mousel[0] > x and y+h > self.mousel[1] > y:
			if self.clickl[0] == 1:	
				#self.lhold = True
				self.story()
		
		
	def gameButton(self, msg,x,y,w,h,ic,ac):
		self.mouseg = pg.mouse.get_pos()
		self.clickg = pg.mouse.get_pressed()
		self.screen.blit(pg.image.load('pred.png'),(x,y))
		#pg.draw.rect(self.screen, ac,(x,y,w,h))
		if x+w > self.mouseg[0] > x and y+h > self.mouseg[1] > y:
			self.screen.blit(pg.image.load('pgreen.png'),(x,y))
			if self.clickg[0] == 1:
				self.playing = False
				self.g.run()
					
					
	def run(self):
		pg.mixer.music.load('song.wav')
		pg.mixer.music.play(-1)
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			#play the walking sound but will be none if movmt was invalid
			if self.chef1.get_sound() != None:	
				#self.chef1.get_sound().play()
				pass
		
			self.story()
	

	def update(self):

		hit_block = pg.sprite.groupcollide(self.all_blocks, self.all_bullets, False, True)
		hit_block2 = pg.sprite.groupcollide(self.all_blocks, self.all_superbullets, False, False) #if the block turn into the bonus -> True, False
		shoot_chef1 = pg.sprite.spritecollide(self.chef1, self.all_bullets, True)
		shoot_chef_1 = pg.sprite.spritecollide(self.chef1, self.all_superbullets, True)
		
		if shoot_chef1 or shoot_chef_1:
			self.chef1.is_hit()
			if self.chef1.get_life == 0:
				self.running= False


		for bl in hit_block.keys():
			bl.decrementHealth()
			if bl.getHealth() == 0:
				if bl.getBonus()==0:
					bl.kill()
				else:
					self.all_bonus.add(bl)
					self.all_blocks.remove(bl)

		for bl in hit_block2.keys(): 
			bl.setHealth(0)
			if bl.getHealth() == 0:
				if bl.getBonus()==0:
					bl.kill()
				else:
					self.all_bonus.add(bl)
					self.all_blocks.remove(bl)

		chef1_hit_bonus = pg.sprite.spritecollide(self.chef1, self.all_bonus, True)
		for bonus in chef1_hit_bonus:
			if bonus.getBonus() == 1:
				self.chef1.claim_life()
			elif bonus.getBonus() == 2:
				self.chef1.claim_cabbage()
			elif bonus.getBonus() == 4:
				self.chef1.gainSpeed()
			elif bonus.getBonus() == 5:
				self.chef1.claim_superbullet()
			elif bonus.getBonus() ==6:
				self.chef1.gainLight()
			else:
				self.chef1.claim_point()


		chef1_old_x = self.chef1.get_x()
		chef1_old_y = self.chef1.get_y()

		self.all_sprites.update()
		

		chef1_collide_block = pg.sprite.spritecollide(self.chef1, self.all_blocks, False)
		if chef1_collide_block:
			self.chef1.set_x(chef1_old_x)
			self.chef1.set_y(chef1_old_y)
	# 			self.chef1.set_sound(None)

		chef1_old_x = self.chef1.get_x()
		chef1_old_y = self.chef1.get_y()
		


		self.all_sprites.update()

		chef1_collide_block = pg.sprite.spritecollide(self.chef1, self.all_blocks, False)
		if chef1_collide_block:
			self.chef1.set_x(chef1_old_x)
			self.chef1.set_y(chef1_old_y)
			self.chef1.set_sound(None)

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				print("Quit")
				if self.playing:
					self.playing = False
				self.running = False

		

	def draw(self):

		
		# create a text suface object for drawing text 
		text = self.font1.render('Chef War', True, (0,0,255))
		#self.screen.blit(pg.image.load('sushibar.png'),(400,130))
		textRect = text.get_rect()  
		 
		# set the center of the rectangular object. 
		textRect.center = (400,100) 
	
		
		self.screen.blit(pg.image.load('left_margin.png'),(0,0))
		self.screen.blit(pg.image.load('right_margin.png'),(800,0))

		self.screen.blit(text, textRect)
		
		self.screen.blit(pg.image.load('2-R3.png'),(250,75))
		self.screen.blit(pg.image.load('1-L2.png'),(620,75))

		self.screen.blit(pg.image.load('sushi1.png'),(325,125))
		self.screen.blit(pg.image.load('sushi2.png'),(475,125))

		pg.display.update()
		

		self.learnButton("Learn to Play",250,500,300,50,(0,0,0),(255,0,0))
		pg.display.update()
		
	def story(self): 
		if self.story_progress == True:
			self.screen.blit(pg.image.load('story title.png'),(0,0))
			self.screen.blit(pg.image.load('left_margin.png'),(0,200))
			self.screen.blit(pg.image.load('right_margin.png'),(800,200))
			self.screen.blit(pg.image.load('story1.png'),(150,200))
			self.button("next",350,950,200,50,(0,0,0),(194,81,77))
			pg.display.update()
		else:
			self.story2()
		
		#self.screen.fill(pg.Color("black"))
	def story2(self): 
		if self.story_progress2 == True:
			self.screen.blit(pg.image.load('story title.png'),(0,0))
			self.screen.blit(pg.image.load('left_margin.png'),(0,200))
			self.screen.blit(pg.image.load('right_margin.png'),(800,200))
			self.screen.blit(pg.image.load('story2.png'),(100,200))
			self.button2("next",500,900,300,60,(0,0,0),(194,81,77))
			pg.display.update()
		else:
			self.players()
		#self.screen.fill(pg.Color("black"))
		
	def controls(self):
		if self.story_progress4 == True:
			#clear the screen 
			self.screen.blit(pg.image.load('background.png'),(200,200))
			self.screen.blit(pg.image.load('left_margin.png'),(0,200))
			self.screen.blit(pg.image.load('right_margin.png'),(800,200))
			self.screen.blit(pg.image.load('p1.png'),(0,0))
			self.screen.blit(pg.image.load('p2.png'),(0,600))
			self.button3("next",793,850,200,50,(0,0,0),(194,81,77))
			pg.display.update()
		else:
			self.blockex()
	
	def players(self):
		if self.story_progress3 == True:
			#clear the screen 
			self.screen.blit(pg.image.load('players.png'),(5,5))
			self.screen.blit(pg.image.load('background.png'),(200,200))
			self.screen.blit(pg.image.load('left_margin.png'),(0,200))
			self.screen.blit(pg.image.load('right_margin.png'),(800,200))
			#self.screen.blit(pg.image.load('fill.png'),(0,200))
			self.button4("next",250,450,500,100,(0,0,0),(194,81,77))
			pg.display.update()	
		else:
			self.controls()
		
	def blockex(self):
		if self.story_progress5 == True:
			self.screen.blit(pg.image.load('bonus.png'),(0,0))
			self.screen.blit(pg.image.load('background.png'),(200,200))
			self.screen.blit(pg.image.load('left_margin.png'),(0,200))
			self.screen.blit(pg.image.load('right_margin.png'),(800,200))
			self.all_sprites.draw(self.screen)
			#self.screen.blit(pg.image.load('sushibar.png'),(-10,800))
		


			self.all_blocks.add(self.block2)
			self.all_blocks.add(self.block3)
			self.all_blocks.add(self.block4)

			self.all_sprites.add(self.block2)
			self.all_sprites.add(self.block3)
			self.all_sprites.add(self.block4)
			self.all_sprites.update()


			self.gameButton("play game!",860,325,100,190,(0,0,0),(255,0,0))
			pg.display.update()




