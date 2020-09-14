import pygame as pg
import random
import time

from chef import Chef
from block import Block
from bullet import Bullet
from common_setting import *
from speedbooster import SpeedBooster

import lcm
from client import input_t
from server import output_t

lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")

pg.init()
font_name = pg.font.match_font('arial')

def get_my_handler(game):
	def my_handler(channel, data):
		chef1_old_state = game.chef1.is_dead()
		chef1_old_state = game.chef2.is_dead()

		out = output_t.decode(data)
		if out.motion == "start":
				game.waiting = False
		if out.player == 1:
			# if out.motion == "dead":
			# 	if chef1_old_state == False:
			# 		print("chef1 set to dead")
			# 		game.chef1.set_dead()
			# 		game.chef2.claim_point()
			# 		game.chef2.claim_point() 
			c1 = out.motion
			if c1 == 'left':
				game.inf1 = 'left'
				#print("get message")
			elif c1 == 'right':
				game.inf1 = 'right'
				#print("get message")
			elif c1 == 'up':
				game.inf1 = 'up'
				#print("get message")
			elif c1 == 'down':
				game.inf1 = 'down'
				#print("get message")
			elif c1 == 'shoot':
				#print("get message")
				game.inf1 = 'shoot'

		elif out.player == 2:
			c2 = out.motion
			# if out.motion == "dead":
			# 	if chef2_old_state == False:
			# 		print("chef2 set to dead")
			# 		game.chef2.set_dead()
			# 		game.chef1.claim_point()
			# 		game.chef1.claim_point() 
			if c2 == 'left':
				game.inf2 = 'left'
				#print("get message")
			elif c2 == 'right':
				game.inf2 = 'right'
				#print("get message")
			elif c2 == 'up':
				game.inf2 = 'up'
				#print("get message")
			elif c2 == 'down':
				game.inf2 = 'down'
				#print("get message")
			elif c2 == 'shoot':
				game.inf2 = 'shoot'


	return my_handler
					
def draw_text(surf,text,size,x,y):
	font=pg.font.Font(font_name,size)
	text_surface = font.render(text, True, WHITE)
	text_rect= text_surface.get_rect()
	text_rect.midleft =(x,y)
	surf.blit(text_surface, text_rect)

class Game:
	def __init__(self):
		pg.mixer.init()
		self.level = 1
		self.background = pg.image.load(backgrounds[self.level-1])
		self.board = pg.image.load(backimages[0])
		self.door = pg.image.load(backimages[1])
		self.right_margin = pg.image.load(backimages[2])
		self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
		pg.display.set_caption("Client1")
		#self.screen.blit(self.background, [250,250])	
		self.clock = pg.time.Clock()
		self.running = True
		self.playing = True
		self.waiting = True
		self.inf1 = ''
		self.inf2 = ''
		self.release = True
		#sprite groups
		self.all_sprites = pg.sprite.Group()		
		self.all_blocks = pg.sprite.Group()
		self.all_bullets = pg.sprite.Group()
		self.all_bonus = pg.sprite.Group()
		self.all_superbullets = pg.sprite.Group()
		self.pressTime = time.time()
		for i in range(20):
			map = maps[0]
			for j in range(20): 
				if map[i][j] == 1:
					bl = Block(j, i, 1)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 2:
					bl = Block(j, i, 0, True, 0)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 3:
					bl = Block(j, i, 3, False, 1)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 4:
					bl = Block(j, i, 2, False, 2)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 5:
					bl = Block(j, i, 3, False, 3)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 6:
					bl = Block(j, i, 1, False, 4)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 7:
					bl = Block(j,i, 3, False, 5)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 8:
					bl = Block(j,i, 2, False, 6)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 'b':
					self.chef1 = Chef(j, i, chef1_moves, True, self.all_bullets, self.all_sprites,self.all_superbullets, self.all_blocks)
					self.all_sprites.add(self.chef1)
					# self.chef1.set_center(j, i)
					# self.chef1.set_cabbage(10)
					# self.chef1.set_life(1)
				elif map[i][j] == 'a':
					self.chef2 = Chef(j, i, chef2_moves, False, self.all_bullets, self.all_sprites, self.all_superbullets, self.all_blocks)
					self.all_sprites.add(self.chef2)
					# self.chef2.set_center(j, i)
					# self.chef2.set_cabbage(10)
					# self.chef2.set_life(1)

	# def light_up()
		#if self.level == 5:
		self.fog=pg.Surface((800,800))
		self.fog.fill(BLACK)
		self.light_mask1=pg.image.load(light1).convert_alpha()
		self.light_mask2=pg.image.load(light2).convert_alpha()
		self.light_mask1= pg.transform.scale(self.light_mask1,LIGHT_RS)
		self.light_mask2= pg.transform.scale(self.light_mask2,LIGHT_RS)
		self.light_rect1=self.light_mask1.get_rect()
		self.light_rect2=self.light_mask2.get_rect()

	def move(self):
		if self.inf1 == 'left':
			self.chef1.move_left()
			#print("get message")
		elif self.inf1 == 'right':
			self.chef1.move_right()
			#print("get message")
		elif self.inf1 == 'up':
			self.chef1.move_forward()
			#print("get message")
		elif self.inf1 == 'down':
			self.chef1.move_backward()
			#print("get message")
		elif self.inf1 == 'shoot':
			#print("get message")
			self.chef1.shoot()	
		
		
		if self.inf2 == 'left':
			self.chef2.move_left()
			#print("get message")
		elif self.inf2 == 'right':
			self.chef2.move_right()
			#print("get message")
		elif self.inf2 == 'up':
			self.chef2.move_forward()
			#print("get message")
		elif self.inf2 == 'down':
			self.chef2.move_backward()
			#print("get message")
		elif self.inf2 == 'shoot':
			self.chef2.shoot()		
		
		


	def create(self):
		#0 is nothing
		#1 is empty bl
		#2 is not shootable
		#3 is life - health = 3
		#4 is cabbage - 2
		#5 is point - 3
	
		#def __init__(self, x, y, health, indestructable = False, bonus = 0 ):
		map = maps[self.level - 1]
		for i in range(20):
			for j in range(20): 
				if map[i][j] == 1:
					bl = Block(j, i, 1)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 2:
					bl = Block(j, i, 0, True, 0)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 3:
					bl = Block(j, i, 3, False, 1)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 4:
					bl = Block(j, i, 2, False, 2)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 5:
					bl = Block(j, i, 3, False, 3)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 6:
					bl = Block(j, i, 1, False, 4)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 7:
					bl = Block(j,i, 3, False, 5)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 8:
					bl = Block(j,i, 2, False, 6)
					self.all_sprites.add(bl)
					self.all_blocks.add(bl)
				elif map[i][j] == 'b':
					# self.chef1 = Chef(j, i, chef1_moves, False, self.all_bullets, self.all_sprites,self.all_superbullets)
					# self.all_sprites.add(self.chef1)
					self.chef1.set_center(j, i)
					self.chef1.set_cabbage(40)
					self.chef1.set_life(1)
					self.chef1.set_block_group(self.all_blocks)
				elif map[i][j] == 'a':
					# self.chef2 = Chef(j, i, chef1_moves, True, self.all_bullets, self.all_sprites, self.all_superbullets)
					# self.all_sprites.add(self.chef2)
					self.chef2.set_center(j, i)
					self.chef2.set_cabbage(40)
					self.chef2.set_life(1)
					self.chef2.set_block_group(self.all_blocks)

					
	def setup_next_level(self):
		for bul in self.all_bullets:
			bul.kill()
		for sbul in self.all_superbullets:
			sbul.kill()
		for bl in self.all_blocks:
			bl.kill()
		for bn in self.all_bonus:
			bn.kill()
		if not self.waiting:
			self.level += 1
			self.create()
		self.playing = True
		
	def update(self):
		self.move()
		self.reset_inf()
		hit_block = pg.sprite.groupcollide(self.all_blocks, self.all_bullets, False, True)
		hit_block2 = pg.sprite.groupcollide(self.all_blocks, self.all_superbullets, False, False) #if the block turn into the bonus -> True, False
		shoot_chef1 = pg.sprite.spritecollide(self.chef1, self.all_bullets, True)
		shoot_chef2 = pg.sprite.spritecollide(self.chef2, self.all_bullets, True)
		shoot_chef_1 = pg.sprite.spritecollide(self.chef1, self.all_superbullets, True)
		shoot_chef_2 = pg.sprite.spritecollide(self.chef2, self.all_superbullets, True)

		if shoot_chef1 or shoot_chef_1:
			self.chef1.is_hit()
		# 	if self.chef1.get_life == 0:
		# 		self.playing= False
			self.chef2.claim_point()
			self.chef2.claim_point()
		if shoot_chef2 or shoot_chef_2:
			self.chef2.is_hit()
		# 	if self.chef2.get_life == 0:
		# 		print('client 2 should be dead')
		# 		self.playing= False
			self.chef1.claim_point()
			self.chef1.claim_point()



		for bl in hit_block.keys():
			bl.decrementHealth()
			if bl.getHealth() == 0:
				if bl.getBonus()==0:
					bl.kill()
					sound = pg.mixer.Sound('blockcrack.wav')
					sound.play()
				else:
					sound = pg.mixer.Sound('powerupblock.wav')
					sound.play()
					self.all_bonus.add(bl)
					self.all_blocks.remove(bl)
	
		for bl in hit_block2.keys(): 
			bl.setHealth(0)
			if bl.getHealth() == 0:
				if bl.getBonus()==0:
					bl.kill()
					sound = pg.mixer.Sound('blockcrack.wav')
					sound.play()
				else:
					sound = pg.mixer.Sound('powerupblock.wav')
					sound.play()
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

		chef2_hit_bonus = pg.sprite.spritecollide(self.chef2, self.all_bonus, True)
		for bonus in chef2_hit_bonus:
			if bonus.getBonus() == 1:
				self.chef2.claim_life()
			elif bonus.getBonus() == 2:
				self.chef2.claim_cabbage()
			elif bonus.getBonus() == 4:
				self.chef2.gainSpeed()
			elif bonus.getBonus() == 5:
				self.chef2.claim_superbullet()
			elif bonus.getBonus() ==6:
				self.chef2.gainLight()
			else:
				self.chef1.claim_point()
		# chef1_old_x = self.chef1.get_x()
		# chef1_old_y = self.chef1.get_y()

		# chef2_old_x = self.chef2.get_x()
		# chef2_old_y = self.chef2.get_y()

		self.all_sprites.update()
		

	# 	chef1_collide_block = pg.sprite.spritecollide(self.chef1, self.all_blocks, False)
	# 	if chef1_collide_block:
	# 		self.chef1.set_x(chef1_old_x)
	# 		self.chef1.set_y(chef1_old_y)
	# # 			self.chef1.set_sound(None)

	# 	chef2_collide_block = pg.sprite.spritecollide(self.chef2, self.all_blocks, False)
	# 	if chef2_collide_block:
	# 		self.chef2.set_x(chef2_old_x)
	# 		self.chef2.set_y(chef2_old_y)
	# # 			self.chef2.set_sound(None)
	
	def run_level(self):
		pg.mixer.music.load('song.wav')
		pg.mixer.music.play(-1)
		while self.playing:

			# for bl in self.all_bullets:
			# 	bl.kill()
			# for bl in self.all_superbullets:
			# 	bl.kill()
			self.clock.tick(FPS)
			self.events()
			lc.handle_timeout(1)
			self.update()
			self.draw()			
			# if self.chef1.is_dead() or self.chef2.is_dead():
			# 	if self.level == 5:
			# 		self.running = False
			# 	self.playing = False
			if self.chef1.is_dead():
				out = input_t()
				out.player = 1
				out.motion = "dead"  
				lc.publish("TO SERVER", out.encode())
				if self.level == 5:
					self.running = False
				self.playing = False
			elif self.chef2.is_dead():
				out = input_t()
				out.player = 2
				out.motion = "dead"  
				lc.publish("TO SERVER", out.encode())
				if self.level == 5:
					self.running = False
				self.playing = False

		# for spr in self.all_sprites:
		# 	spr.kill()
	
	def level_successful(self):
		if self.playing == False:
			return True
		else: 
			return False
	
	def done(self):
		if self.running == False:
			return True
		else:
			return False

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				# if self.playing:
				# 	self.playing = False
				# self.running = False
				pg.quit()
		key = pg.key.get_pressed()
		sending_out = input_t()
		sending_out.player = 1
		judgeTime = time.time()
		if key[pg.K_LEFT]:
			if judgeTime - self.pressTime > 0.10:
				sending_out.motion = "left"	  
				lc.publish("TO SERVER", sending_out.encode())
				self.pressTime = time.time()
		elif key[pg.K_RIGHT]:
			if judgeTime - self.pressTime > 0.10:
				sending_out.motion = "right"  
				lc.publish("TO SERVER", sending_out.encode()) 
				self.pressTime = time.time()
		elif key[pg.K_UP]:
			if judgeTime - self.pressTime > 0.10:
				sending_out.motion = "up"	
				lc.publish("TO SERVER", sending_out.encode())
				self.pressTime = time.time()
		
		elif key[pg.K_DOWN]:
			if judgeTime - self.pressTime > 0.10:
				self.release = False
				sending_out.motion = "down"	  
				lc.publish("TO SERVER", sending_out.encode())
				self.pressTime = time.time()
		
		elif key[pg.K_SPACE]:
			if judgeTime - self.pressTime > 0.5:
				self.release = False
				sending_out.motion = "shoot"
				
				lc.publish("TO SERVER", sending_out.encode())
				self.pressTime = time.time()

	
	def makefog(self):
		self.fog.fill(BLACK)
		# if self.chef2.get_Light():
		# 	self.light_mask1= pg.transform.scale(self.light_mask1,LIGHT_RB)
		# 	self.light_rect1=self.light_mask1.get_rect()
		# 	self.chef2.set_endLight()
		# 	elapsed = self.chef2.get_endLight()-self.chef2.get_stLight()
		# 	if elapsed >= 5.00:
		# 		self.chef2.close_Light()
		# 		self.light_mask1= pg.transform.scale(self.light_mask1,LIGHT_RS)
		# 		self.light_rect1=self.light_mask1.get_rect()

		if self.chef1.get_Light():
			self.light_mask2= pg.transform.scale(self.light_mask2,LIGHT_RB)
			self.light_rect2=self.light_mask2.get_rect()
			self.chef1.set_endLight()
			elapsed = self.chef1.get_endLight()-self.chef1.get_stLight()
			if elapsed >= 5.00:
				self.chef1.close_Light()
				self.light_mask2= pg.transform.scale(self.light_mask2,LIGHT_RS)
				self.light_rect2=self.light_mask2.get_rect()
		
		# self.light_rect1.center=(self.chef2.get_center()[0]-200,self.chef2.get_center()[1]-200)
		self.light_rect2.center=(self.chef1.get_center()[0]-100,self.chef1.get_center()[1]-200)
		# self.fog.blit(self.light_mask1,self.light_rect1)
		self.fog.blit(self.light_mask2,self.light_rect2)
		self.screen.blit(self.fog,(100,200),special_flags=pg.BLEND_MULT)


	def draw(self):
		self.screen.blit(self.background, [100,200])
		self.screen.blit(self.right_margin,[900,200])
		self.screen.blit(self.door, [-100,200])
		self.screen.blit(self.board, [0, 0])
		self.all_sprites.draw(self.screen)
		#text to print
		# if self.chef2.get_Light():
		# 	t2 = 5.00-self.chef2.get_endLight()+self.chef2.get_stLight()
		# 	text_Light2 = str("%.1f" % t2)
		# else:
		# 	text_Light2 = 'No'
		
		if self.chef1.get_Light():
			t1 = 5.00-self.chef1.get_endLight()+self.chef1.get_stLight()
			text_Light1 = str("%.1f" % t1)
		else:
			text_Light1 = 'No'
		
		
		if self.chef2.get_speed():
			t4 = 5.00-self.chef2.get_endSpeed()+self.chef2.get_stSpeed()
			text_Speed2 = str("%.1f" % t4)
		else:
			text_Speed2 = 'No'
		
		if self.chef1.get_speed():
			t3 = 5.00-self.chef1.get_endSpeed()+self.chef1.get_stSpeed()
			text_Speed1 = str("%.1f" % t3)
		else:
			text_Speed1 = 'No'
		
		
		draw_text(self.screen, str(self.level), 55, 550, 40)#level
		draw_text(self.screen, str(self.chef2.get_cabbage()), 25, 100, 85)#c2 cabbage
		draw_text(self.screen, str(self.chef1.get_cabbage()), 25, 810, 85)#c1 cabbage
		draw_text(self.screen, str(self.chef2.get_life()), 25, 100, 127)#c2 life
		draw_text(self.screen, str(self.chef1.get_life()), 25, 810, 127)#c1 life
		draw_text(self.screen, str(self.chef2.get_point()), 40, 380, 130)#c2 score
		draw_text(self.screen, str(self.chef1.get_point()), 40, 600, 130)#c1 score
		draw_text(self.screen, str(self.chef2.get_superbullet()), 25, 225, 127)#c2 superbullet
		draw_text(self.screen, str(self.chef1.get_superbullet()), 25, 930, 127)#c1 superbullet
		draw_text(self.screen, text_Speed2, 25, 100, 167)#c2 speed up
		draw_text(self.screen, text_Speed1, 25, 810, 167)#c1 speed up
		draw_text(self.screen, '???', 25, 225, 85)#c2 light up
		draw_text(self.screen, text_Light1, 25, 930, 85)#c1 light up



		if self.level > 2:
			self.makefog()
		pg.display.update()


	def get_block(self, x, y):
		for bl in self.all_blocks:
			if bl.get_x() == x and bl.get_y() == y:
				return bl


	def show_start_screen(self):
		pg.mixer.music.load('song2.wav')
		pg.mixer.music.play(-1)
		
		background = pg.image.load('startscreen.png')
		self.screen.blit(background, [0,0])
		pg.display.update()
	
		click = False
		# waiting = True
		#click = pg.mouse.get_pressed()
		while self.waiting:
			if click == False: 
				lc.handle_timeout(10)
				for event in pg.event.get():
					if event.type == pg.QUIT:
						pg.quit()
					mouse = pg.mouse.get_pos()
					if 700 <  mouse[0] < 800 and 600 < mouse[1] < 850:
						background = pg.image.load('startscreen-select-play.png')
						self.screen.blit(background, [0,0])
						if event.type == pg.MOUSEBUTTONDOWN:				
							click = True
							
							start = input_t()
							start.motion = "start"
							start.player = 1
							print("client2 click")
							lc.publish("TO SERVER", start.encode())

							#waiting = False					
					elif 212 < mouse[0] < 314 and 862 < mouse[1] < 964:	
						background = pg.image.load('startscreen-select-tut.png')
						self.screen.blit(background, [0,0])
						if event.type == pg.MOUSEBUTTONDOWN:
							self.tutorial()
							
							#waiting = False
					elif 25 < mouse[0] < 145 and 855 < mouse[1] < 975:
						background = pg.image.load('startscreen-select-creds.png')
						self.screen.blit(background, [0,0])
						if event.type == pg.MOUSEBUTTONDOWN:	
							self.show_credit_screen()	
					else:
						background = pg.image.load('startscreen.png')
						self.screen.blit(background, [0,0])
					pg.display.update()	
			else:
				lc.handle_timeout(10)
				print("clicked")
				print(self.background)
				background = pg.image.load("missing2.png")							
				self.screen.blit(background, [0,0])
				pg.display.update()	
				for event in pg.event.get():
					if event.type == pg.QUIT:
						pg.quit()
	
	def show_credit_screen(self):
		print("show credit screen")
		background = pg.image.load('credit.png')
		self.screen.blit(background, [0,0])
		pg.display.update()
		credit = True
		while credit:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
				mouse = pg.mouse.get_pos()
				if 735 < mouse[0] < 1000 and 915 < mouse[1] < 1000:
					background = pg.image.load("credit-select-back.png")
					self.screen.blit(background, [0,0])
					if event.type == pg.MOUSEBUTTONDOWN:
						credit = False
						self.show_start_screen()
				else: 
					background = pg.image.load('credit.png')
					self.screen.blit(background, [0,0])
				pg.display.update()

	def show_end_screen(self):
		if self.chef1.get_point() > self.chef2.get_point():
			background = pg.image.load("player2_end.png")
		elif self.chef1.get_point() < self.chef2.get_point():
			background = pg.image.load("lose2.png")
		else:
			background = pg.image.load("tie.png")
		self.screen.blit(background, [0,0])
		pg.display.update()
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
				mouse = pg.mouse.get_pos()
				if event.type == pg.MOUSEBUTTONDOWN:
					if 750 <  mouse[0] < 1000 and 920 < mouse[1] < 1000:	
						pg.quit()

	def tutorial(self):
		title = pg.image.load("story title.PNG")
		block1 = Block(7, 6, 1)
		block2 = Block(7, 7, 3, False, 1)
		block3 = Block(7, 8, 3, False, 3)

		blocks = pg.sprite.Group()
		bonus = pg.sprite.Group()
		all_sprites = pg.sprite.Group()
		blocks.add(block1)
		blocks.add(block2)
		blocks.add(block3)
		all_sprites.add(block1)
		all_sprites.add(block2)
		all_sprites.add(block3)

		chef_test = Chef(10, 10, chef2_moves, True, self.all_bullets, all_sprites, self.all_superbullets, blocks)
		all_sprites.add(chef_test)


		click = 0
		
		tutorial = True
		while tutorial:	
			print(click)		
			#self.screen.blit(skip, [100, 100])
			self.screen.blit(self.background, [100,200])
			self.screen.blit(title, [0,0])
			self.screen.blit(self.right_margin,[900,200])
			self.screen.blit(self.door, [-100,200])
			#self.screen.blit(self.board, [0, 0])
			
			picture_blit = pg.image.load(tutorial_graphics[click])
			if click == 0 :
				self.screen.blit(picture_blit, [100, 200])
			elif click == 1 :
				self.screen.blit(picture_blit, [100, 200])
				tutorial1 = pg.image.load('tutorial1.PNG')
				self.screen.blit(tutorial1, [0, 0])
			else:
				self.screen.blit(picture_blit, [0,0])
				all_sprites.draw(self.screen)
			skip = pg.image.load("continue.png")
			skip.set_colorkey(WHITE)
			self.screen.blit(skip, [700, 930])

			
			self.clock.tick(FPS)
			key = pg.key.get_pressed()
			judgeTime = time.time()
			if key[pg.K_LEFT]:
				if judgeTime - self.pressTime > 0.05:
					chef_test.move_left()
					self.pressTime = time.time()
			elif key[pg.K_RIGHT]:
				if judgeTime - self.pressTime > 0.05:
					chef_test.move_right()
					self.pressTime = time.time()
			elif key[pg.K_UP]:
				if judgeTime - self.pressTime > 0.05:
					chef_test.move_forward()
					self.pressTime = time.time()
			elif key[pg.K_DOWN]:
				if judgeTime - self.pressTime > 0.05:
					chef_test.move_backward()
					self.pressTime = time.time()
			elif key[pg.K_SPACE]:
				if judgeTime - self.pressTime > 0.5:
					chef_test.shoot()
					self.pressTime = time.time()
				
			
			for event in pg.event.get():
				mouse = pg.mouse.get_pos()
				if event.type == pg.QUIT:
					pg.quit()
				if event.type == pg.MOUSEBUTTONDOWN:
					if 700 < mouse[0] < 1000 and 930 < mouse[1] < 1000:
						click+=1	
						if click == 4:
					#if 100 < mouse[0] < 350 and 100 < mouse[1] < 185:
							tutorial = False
							self.show_start_screen()

			hit_block = pg.sprite.groupcollide(blocks, self.all_bullets, False, True)
			for bl in hit_block.keys():
				bl.decrementHealth()
				if bl.getHealth() == 0:
					if bl.getBonus()==0:
						bl.kill()
						sound = pg.mixer.Sound('blockcrack.wav')
						sound.play()
					else:
						sound = pg.mixer.Sound('powerupblock.wav')
						sound.play()
						bonus.add(bl)
						blocks.remove(bl)
			hit_bonus = pg.sprite.spritecollide(chef_test, bonus, True)

			all_sprites.update()
			
			pg.display.update()
			# key = pg.key.get_pressed()
			# if key[pg.K_LEFT]:
			# 	chef_test.move_left()
			# elif key[pg.K_RIGHT]:
			# 	chef_test.move_right()
			# elif key[pg.K_UP]:
			# 	chef_test.move_forward()
			# elif key[pg.K_DOWN]:
			# 	chef_test.move_backward() 
			# elif key[pg.K_SPACE]:
			# 	chef_test.shoot()
		
			# pg.display.update()
		
# for i in range (5):

# 	g1 = Game(i+1)
# 	lc.subscribe("SERVER_OUTPUT", get_my_handler(g1))
# 	g1.run()
# 	pg.quit()

# for i in range (5):
# 	g1 = Game(i+1)
# 	subscription = lc.subscribe("SERVER_OUTPUT", get_my_handler(g1))
# 	g1.show_start_screen()	
# 	while g1.running:
# 		g1.run()
# 		g1.show_go_screen()
# 	lc.unsubscribe(subscription)
# pg.quit()

	def show_transition_screen(self):
		self.waiting = True
		if self.level == 2:
			background = pg.image.load("darktransition.png")
			background = pg.transform.scale(background, (1000,1000))
			self.screen.blit(background, [0,0])
			skip = pg.image.load("continue.PNG")
			self.screen.blit(skip, [700, 930])
		else:
			background = pg.image.load('transition.png')
			self.screen.blit(background, [0,0])
		if not self.level == 2:
			draw_text(self.screen, str(self.level), 55, 550, 375)
			draw_text(self.screen, str(self.chef2.get_point()), 40, 380, 465)#c2 score
			draw_text(self.screen, str(self.chef1.get_point()), 40, 600, 465)#c1 score
		pg.display.update()
		while self.waiting:
			lc.handle_timeout(1)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
				mouse = pg.mouse.get_pos()
				if event.type == pg.MOUSEBUTTONDOWN:
					if 750 <  mouse[0] < 1000 and 920 < mouse[1] < 1000:	
						background = pg.image.load("missing1.png")	
						self.screen.blit(background, [0,0])
						pg.display.update()		
						next = input_t()
						next.player = 1
						next.motion = "start"
						lc.publish("TO SERVER", next.encode())
						#waiting = False
	def reset_inf(self):
		self.inf1 = ''
		self.inf2 = ''


										
					


game = Game()
lc.subscribe("TO CLIENT", get_my_handler(game))

game.show_start_screen()

while not game.done():
	game.run_level()
	if game.level_successful():
		if not game.level == 5:
			game.show_transition_screen()
			game.setup_next_level()
game.show_end_screen()
pg.quit()






