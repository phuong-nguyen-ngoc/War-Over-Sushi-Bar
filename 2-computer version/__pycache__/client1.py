import pygame as pg
import random

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
		out = output_t.decode(data)
		if out.stat[0] == 'left':
			game.chef2.move_left()
		elif out.stat[0] == 'right':
			game.chef2.move_right()
		elif out.stat[0] == 'up':
			game.chef2.move_forward()
		elif out.stat[0] == 'down':
			game.chef2.move_backward()
		elif out.stat[0] == 'shoot':
			game.chef2.shoot()
		# if out.object == "start_game":
		# 	game.waiting = False

		# # if out.object == "end_game":
		# # 	game.running = False
		# # 	game.playing = False

		# if out.object == "player":			
		# 	#update player state
		# 	if out.stat[0] == 2:
		# 		game.chef2.set_image(out.graphics)
		# 		game.chef2.image.set_colorkey(BLACK)
		# 		game.chef2.set_x(out.stat[1])
		# 		game.chef2.set_y(out.stat[2])
		# 		game.chef2.set_life(out.stat[3])
		# 		game.chef2.set_cabbage(out.stat[4])
		# 		game.chef2.set_point(out.stat[5])

		# 	elif out.stat[0] == 1:
		# 		game.chef1.set_image(out.graphics)
		# 		game.chef1.image.set_colorkey(BLACK)
		# 		game.chef1.set_x(out.stat[1])
		# 		game.chef1.set_y(out.stat[2])
		# 		game.chef1.set_life(out.stat[3])
		# 		game.chef1.set_cabbage(out.stat[4])
		# 		game.chef1.set_point(out.stat[5])

		# if out.object == "block":
		# 	bl = game.get_block(out.stat[0], out.stat[1]) 
		# 	if not bl == None:
		# 		if out.stat[2] == 0:
		# 			bl.kill()
		# 		else:
		# 			bl.change_to_bonus_graphics()
		
		# if out.object == "bonus":
		# 	bl = game.get_block(out.stat[0], out.stat[1])
		# 	if not bl == None: 
		# 		bn = bl.getBonus()
		# 		if out.stat[2] == 1:
		# 			if bn == 1:
		# 				game.chef1.claim_life()
		# 			elif bn == 2:
		# 				game.chef1.claim_cabbage()
		# 			elif bn == 3:
		# 				game.chef1.claim_point()
		# 			elif bn == 4:
		# 				game.chef1.gainSpeed()
		# 			elif bn == 5:
		# 				game.chef1.claim_superbullet()
		# 			elif bn == 6:
		# 				game.chef1.gainLight()
		# 		else:
		# 			if bn == 1:
		# 				game.chef2.claim_life()
		# 			elif bn == 2:
		# 				game.chef2.claim_cabbage()
		# 			elif bn == 3:
		# 				game.chef2.claim_point()
		# 			elif bn == 4:
		# 				game.chef2.gainSpeed()
		# 			elif bn == 5:
		# 				game.chef2.claim_superbullet()
		# 			elif bn == 6:
		# 				game.chef2.gainLight()
		# 		bl.kill()

		# if out.object == "bullet":
		# 	bul = Bullet("up", (out.stat[0], out.stat[1] + 50))
		# 	game.all_bullets.add(bul)
		# 	game.all_sprites.add(bul)

		# # if out.object == "superbullet":
		# # 	bul = Bullet("up", (out.stat[0], out.stat[1] + 50), False)
		# # 	game.all_bullets.add(bul)
		# # 	game.all_sprites.add(bul)  

		# if out.object == "1_clear_spbullet":
		# 	game.chef1.clear_superbullet()
        
		# if out.object == "2_clear_spbullet":
		# 	game.chef2.clear_superbullet()

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
		#sprite groups
		self.all_sprites = pg.sprite.Group()		
		self.all_blocks = pg.sprite.Group()
		self.all_bullets = pg.sprite.Group()
		self.all_bonus = pg.sprite.Group()
		self.all_superbullets = pg.sprite.Group()
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
					self.chef1 = Chef(j, i, chef1_moves, False, self.all_bullets, self.all_sprites,self.all_superbullets)
					self.all_sprites.add(self.chef1)
					# self.chef1.set_center(j, i)
					# self.chef1.set_cabbage(10)
					# self.chef1.set_life(1)
				elif map[i][j] == 'a':
					self.chef2 = Chef(j, i, chef2_moves, True, self.all_bullets, self.all_sprites, self.all_superbullets)
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
					self.chef1.set_cabbage(10)
					self.chef1.set_life(1)
				elif map[i][j] == 'a':
					# self.chef2 = Chef(j, i, chef1_moves, True, self.all_bullets, self.all_sprites, self.all_superbullets)
					# self.all_sprites.add(self.chef2)
					self.chef2.set_center(j, i)
					self.chef2.set_cabbage(10)
					self.chef2.set_life(1)

					
	def setup_next_level(self):
		for bl in self.all_blocks:
			bl.kill()
		self.level += 1
		self.create()
		self.playing = True

	def update(self):
		
		hit_block = pg.sprite.groupcollide(self.all_blocks, self.all_bullets, False, True)
		hit_block2 = pg.sprite.groupcollide(self.all_blocks, self.all_superbullets, False, False) #if the block turn into the bonus -> True, False
		shoot_chef1 = pg.sprite.spritecollide(self.chef1, self.all_bullets, True)
		shoot_chef2 = pg.sprite.spritecollide(self.chef2, self.all_bullets, True)
		shoot_chef_1 = pg.sprite.spritecollide(self.chef1, self.all_superbullets, True)
		shoot_chef_2 = pg.sprite.spritecollide(self.chef2, self.all_superbullets, True)

		if shoot_chef1 or shoot_chef_1:
			self.chef1.is_hit()
			if self.chef1.get_life == 0:
				self.running= False
			self.chef2_points +=1
		if shoot_chef2 or shoot_chef_2:
			self.chef2.is_hit()
			if self.chef2.get_life == 0:
				self.running= False
			self.chef1_points +=1



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
				self.chef1_points +=1

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
				self.chef2_points +=1

		chef1_old_x = self.chef1.get_x()
		chef1_old_y = self.chef1.get_y()

		chef2_old_x = self.chef2.get_x()
		chef2_old_y = self.chef2.get_y()

		self.all_sprites.update()
		

		chef1_collide_block = pg.sprite.spritecollide(self.chef1, self.all_blocks, False)
		if chef1_collide_block:
			self.chef1.set_x(chef1_old_x)
			self.chef1.set_y(chef1_old_y)
	# 			self.chef1.set_sound(None)

		chef2_collide_block = pg.sprite.spritecollide(self.chef2, self.all_blocks, False)
		if chef2_collide_block:
			self.chef2.set_x(chef2_old_x)
			self.chef2.set_y(chef2_old_y)
	# 			self.chef2.set_sound(None)
	
	def run_level(self):
		pg.mixer.music.load('song.wav')
		pg.mixer.music.play(-1)
		while self.playing:
			if self.chef1.get_speed() == True:
				self.chef1.set_endSpeed()
				elapsed = self.chef1.get_endSpeed() - self.chef1.get_stSpeed()
				if elapsed >= 5.00:
					self.chef1.close_speed()
			
			if self.chef2.get_speed() == True:
				self.chef2.set_endSpeed()
				elapsed = self.chef2.get_endSpeed() - self.chef2.get_stSpeed()
				if elapsed >= 5.00:
					self.chef2.close_speed()

			for bl in self.all_bullets:
				bl.kill()
			# for bl in self.all_superbullets:
			# 	bl.kill()
			#self.clock.tick(FPS)
			self.events()
			lc.handle_timeout(1)
			self.draw()			
			if self.chef1.is_dead() or self.chef2.is_dead():
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
				if self.playing:
					self.playing = False
				self.running = False
		key = pg.key.get_pressed()
		sending_out = input_t()
		sending_out.player = 1
		if key[pg.K_LEFT]:
			sending_out.move = "left"	  
		elif key[pg.K_RIGHT]:
			sending_out.move = "right"	   
		elif key[pg.K_UP]:
			sending_out.move = "up"		
		elif key[pg.K_DOWN]:
			sending_out.move = "down"	  
		elif key[pg.K_SPACE]:
			sending_out.move = "shoot"	   
		lc.publish("CLIENT_INPUT", sending_out.encode())
	
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
		self.light_rect2.center=(self.chef1.get_center()[0]-200,self.chef1.get_center()[1]-200)
		# self.fog.blit(self.light_mask1,self.light_rect1)
		self.fog.blit(self.light_mask2,self.light_rect2)
		self.screen.blit(self.fog,(200,200),special_flags=pg.BLEND_MULT)


	def draw(self):
		self.screen.blit(self.background, [200,200])
		self.screen.blit(self.door, [0,200])
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
		draw_text(self.screen, text_Light2, 25, 225, 85)#c2 light up
		draw_text(self.screen, text_Light1, 25, 930, 85)#c1 light up



		if self.level == 5:
			self.makefog()
		pg.display.update()


	def get_block(self, x, y):
		for bl in self.all_blocks:
			if bl.get_x() == x and bl.get_y() == y:
				return bl


	def show_start_screen(self):
		background = pg.image.load('startscreen.png')
		self.screen.blit(background, [0,0])
		pg.display.update()
	
		# waiting = True
		#click = pg.mouse.get_pressed()
		while self.waiting:
			lc.handle_timeout(10)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
				mouse = pg.mouse.get_pos()
				if event.type == pg.MOUSEBUTTONDOWN:
					if 700 <  mouse[0] < 800 and 600 < mouse[1] < 850:				
						background = pg.image.load("missing2.png")
						start = input_t()
						start.player = 1
						start.move = "start"
						lc.publish("CLIENT_INPUT", start.encode())
						#waiting = False					
					if 212 < mouse[0] < 314 and 862 < mouse[1] < 964:	
						background = pg.image.load("missing2.png")			
						start = input_t()
						start.player = 1
						start.move = "start"
						lc.publish("CLIENT_INPUT", start.encode())
						#waiting = False
					if 42 < mouse[0] < 144 and 862 < mouse[1] < 964:	
						background = pg.image.load("missing2.png")			
						start = input_t()
						start.player = 1
						start.move = "start"
						lc.publish("CLIENT_INPUT", start.encode())
						#waiting = False	
					self.screen.blit(background, [0,0])
					pg.display.update()

	def show_waiting_screen(self):
		pass

	def show_go_screen(self):
		pass
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

game = Game()
lc.subscribe("SERVER_OUTPUT", get_my_handler(game))

game.show_start_screen()

while not game.done():
	game.run_level()
	if game.level_successful():
		game.setup_next_level()
pg.quit()






