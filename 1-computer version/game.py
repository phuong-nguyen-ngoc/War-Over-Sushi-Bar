import pygame as pg
import tutorial as tut
import random
import time
from chef import Chef
from block import Block
from bullet import Bullet
from common_setting import *
from speedbooster import SpeedBooster

pg.init()
font_name = pg.font.match_font('arial')

def draw_text(surf,text,size,x,y):
	font=pg.font.Font(font_name,size)
	text_surface = font.render(text, True, WHITE)
	text_rect= text_surface.get_rect()
	text_rect.midleft =(x,y)
	surf.blit(text_surface, text_rect)

class Game:
	def __init__(self, level, chef1_points = 0, chef2_points =0):
		pg.mixer.init()
		self.running = True
		if level == 0:
			self.background = pg.image.load('startscreen.png')
		elif level > 0 and level < 6 or level == 8:
			self.background = pg.image.load("background.png")
			self.board = pg.image.load(backimages[0])
			self.door = pg.image.load(backimages[1])
			self.right_margin = pg.image.load(backimages[2])
			self.skip = pg.image.load('SKIP.png')
			self.bonus_image = pg.image.load('BONUS.png')
		elif level == 6:
			if chef1_points > chef2_points:
				self.background = pg.image.load('player1_end.png')
			elif chef2_points > chef1_points: 
				self.background = pg.image.load('player2_end.png')
			else:
				self.background = pg.image.load('tie.PNG')
		elif level ==7:
			self.background = pg.image.load('credit.png')
		else:
			g = Game(0)
			g.run()
			self.running = False
		self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
		pg.display.set_caption("Chef War")
		#self.screen.blit(self.background, [250,250])
		self.level = level
		self.clock = pg.time.Clock()
		#sprite groups
		self.all_sprites = pg.sprite.Group()		
		self.all_blocks = pg.sprite.Group()
		self.all_bullets = pg.sprite.Group()
		self.all_bonus = pg.sprite.Group()
		self.all_superbullets = pg.sprite.Group()
		self.chef1_points = chef1_points
		self.chef2_points = chef2_points
		self.transition_image = pg.image.load('transition.png')
		self.show_transition = False
		self.darkmode = False
		print ('points:', self.chef1_points, self.chef2_points)
		

		#light up
		if self.level == 5:
			self.fog=pg.Surface((800,800))
			self.fog.fill(BLACK)
			self.light_mask1=pg.image.load(light1).convert_alpha()
			self.light_mask2=pg.image.load(light2).convert_alpha()
			self.light_mask1= pg.transform.scale(self.light_mask1,LIGHT_RS)
			self.light_mask2= pg.transform.scale(self.light_mask2,LIGHT_RS)
			self.light_rect1=self.light_mask1.get_rect()
			self.light_rect2=self.light_mask2.get_rect()

		if self.level > 0 and self.level < 6 or level == 8:
			if self.level > 0 and self.level < 6:
				self.map = maps[self.level - 1]
			else:
				self.map = tutorial
	
			for i in range(20):
				for j in range(20): 
					if self.map[i][j] == 1:
						bl = Block(j, i, 1)
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j] == 2:
						bl = Block(j, i, 0, True, 0)
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j]	== 3:
						bl = Block(j, i, 3, False, 1)
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j]	== 4:
						bl = Block(j, i, 2, False, 2)
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j]	== 5:
						bl = Block(j, i, 3, False, 3)
						self.all_sprites						
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j] == 6:
						bl = Block(j, i, 1, False, 4)
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j]	== 7:
						bl = Block(j,i, 3, False, 5)
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j]	== 8:
						bl = Block(j,i, 2, False, 6)
						self.all_sprites.add(bl)
						self.all_blocks.add(bl)
					elif self.map[i][j] == 'a':
						self.chef1 = Chef(j, i, chef1_moves, True, self.all_bullets, self.all_sprites,self.all_superbullets)
					elif self.map[i][j] == 'b':
						self.chef2 = Chef(j, i, chef2_moves, False, self.all_bullets, self.all_sprites, self.all_superbullets)
				
			#apend sprite here
			self.all_sprites.add(self.chef1)
			self.all_sprites.add(self.chef2)
		
			
				

	def run(self):
		music = ['sountrack.wav', 'song.wav','song2.wav']
		music_playing = music[2]
		if self.level == 0 or self.level >3 or self.level == 8:
			music_playing = music[2]
		elif self.level > 0 or self.level < 3:
			music_playing = music[1]
		self.playing = True
		pg.mixer.music.load(music_playing)
		pg.mixer.music.play(-1)
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			if self.level > 0 and self.level < 6:
				if self.chef1.is_dead() or self.chef2.is_dead():
					self.show_transition = True
				else:
					self.update()
			elif self.level == 8:
				self.update()
			if self.show_transition == False:
				self.draw()
			else:
				self.transition()
	
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
				self.chef1_points +=2

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
				self.chef2_points +=2

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


	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				print("Quit")
				if self.playing:
					self.playing = False
				self.running = False

	def makefog(self):
		self.fog.fill(BLACK)
		if self.chef2.get_Light():
			self.light_mask1= pg.transform.scale(self.light_mask1,LIGHT_RB)
			self.light_rect1=self.light_mask1.get_rect()
			self.chef2.set_endLight()
			elapsed = self.chef2.get_endLight()-self.chef2.get_stLight()
			if elapsed >= 5.00:
				self.chef2.close_Light()
				self.light_mask1= pg.transform.scale(self.light_mask1,LIGHT_RS)
				self.light_rect1=self.light_mask1.get_rect()

		if self.chef1.get_Light():
			self.light_mask2= pg.transform.scale(self.light_mask2,LIGHT_RB)
			self.light_rect2=self.light_mask2.get_rect()
			self.chef1.set_endLight()
			elapsed = self.chef1.get_endLight()-self.chef1.get_stLight()
			if elapsed >= 5.00:
				self.chef1.close_Light()
				self.light_mask2= pg.transform.scale(self.light_mask2,LIGHT_RS)
				self.light_rect2=self.light_mask2.get_rect()
		
		self.light_rect1.center=(self.chef2.get_center()[0]-100,self.chef2.get_center()[1]-200)
		self.light_rect2.center=(self.chef1.get_center()[0]-100,self.chef1.get_center()[1]-200)
		self.fog.blit(self.light_mask1,self.light_rect1)
		self.fog.blit(self.light_mask2,self.light_rect2)
		self.screen.blit(self.fog,(100,200),special_flags=pg.BLEND_MULT)

	def draw(self):
		if self.level == 0:
			self.screen.blit(self.background, [0,0])
			
			if self.level == 0:
				mouse = pg.mouse.get_pos()
				click = pg.mouse.get_pressed()
				if 700 <  mouse[0] < 800 and 600 < mouse[1] < 850:
					self.background = pg.image.load('startscreen-select-play.png')
					if click[0] == 1:
						g = Game(1)
						g.run()	
						self.playing = False	
				elif 212 < mouse[0] < 314 and 862 < mouse[1] < 964:
					self.background = pg.image.load('startscreen-select-tut.png')
					if click[0] == 1:
						t = tut.Tutorial()
						t.run()
						self.playing = False
				elif 42 < mouse[0] < 144 and 862 < mouse[1] < 964:
					self.background = pg.image.load('startscreen-select-creds.png')
					if click[0] == 1:
						g = Game(7)
						g.run()	
						self.playing = False
				else:
					self.background = pg.image.load('startscreen.png')						
			self.all_sprites.draw(self.screen)
			
		elif self.level > 0 and self.level < 6 or self.level == 8:
			self.screen.blit(self.right_margin,[900,200])
			self.screen.blit(self.door, [-100,200])
			self.screen.blit(self.background, [100,200])
			if self.level == 8:
				self.screen.blit(self.bonus_image, [0, 0])
			else:
				self.screen.blit(self.board, [0, 0])
			mouse = pg.mouse.get_pos()
			click = pg.mouse.get_pressed()
			if self.level ==8:
				self.screen.blit(self.skip, [740,910,210,50])
				if 740 < mouse[0] < 950 and 910 < mouse[1] < 960:
					self.skip = pg.image.load('SKIP-select.png')
					if click[0] == 1:
						g = Game(1)
						g.run()
						self.playing = False
				else:
					self.skip = pg.image.load('SKIP.png')
			self.all_sprites.draw(self.screen)
			#text to print
			if self.chef2.get_Light():
				t2 = 5.00-self.chef2.get_endLight()+self.chef2.get_stLight()
				text_Light2 = str("%.1f" % t2)
			else:
				text_Light2 = 'No'
		
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
				
			if self.level != 8:
				draw_text(self.screen, str(self.level), 55, 550, 40)#level
				draw_text(self.screen, str(self.chef1.get_cabbage()), 25, 100, 85)#c2 cabbage
				draw_text(self.screen, str(self.chef2.get_cabbage()), 25, 810, 85)#c1 cabbage
				draw_text(self.screen, str(self.chef1.get_life()), 25, 100, 127)#c2 life
				draw_text(self.screen, str(self.chef2.get_life()), 25, 810, 127)#c1 life
				draw_text(self.screen, str(self.chef1_points), 40, 380, 130)#c2 score
				draw_text(self.screen, str(self.chef2_points), 40, 600, 130)#c1 score
				draw_text(self.screen, str(self.chef1.get_superbullet()), 25, 225, 127)#c2 superbullet
				draw_text(self.screen, str(self.chef2.get_superbullet()), 25, 930, 127)#c1 superbullet
				draw_text(self.screen, text_Speed1, 25, 100, 167)#c2 speed up
				draw_text(self.screen, text_Speed2, 25, 810, 167)#c1 speed up
				draw_text(self.screen, text_Light1, 25, 225, 85)#c2 light up
				draw_text(self.screen, text_Light2, 25, 930, 85)#c1 light up




		
			if self.level == 5:
				self.makefog()
			#self.chef1.get_all_bullets.draw(self.screen)
		elif self.level == 6:
			self.screen.blit(self.background, [0,0])
			# pg.draw.rect(self.screen, BLACK, [740,910,210,50])
			mouse = pg.mouse.get_pos()
			click = pg.mouse.get_pressed()
			if 740 <  mouse[0] < 950 and 910 < mouse[1] < 960:
				if self.chef1_points > self.chef2_points:
					self.background = pg.image.load('player1_end-select-back.png')
				else:
					self.background = pg.image.load('player2_end-select-back.png')
				if click[0] == 1:
					g = Game(7)
					g.run()	
					self.playing = False
			else:
				if self.chef1_points > self.chef2_points:
					self.background = pg.image.load('player1_end.png')
				else:
					self.background = pg.image.load('player2_end.png')
		else:
			self.screen.blit(self.background, [0,0])
			mouse = pg.mouse.get_pos()
			click = pg.mouse.get_pressed()
			if 740 <  mouse[0] < 950 and 910 < mouse[1] < 960:
				self.background = pg.image.load('credit-select-back.png')
				if click[0] == 1:
					g = Game(0)
					g.run()
					self.playing = False
			else:
				self.background = pg.image.load('credit.png')
		pg.display.update()


		def show_start_screen(self):
			pass

		def show_go_screen(self):
			pass
			
	def transition(self):
		mouse = pg.mouse.get_pos()
		click = pg.mouse.get_pressed()
		if self.darkmode:
			self.transition_image = pg.image.load('darktransition.png')
			self.screen.blit(self.transition_image,[0,0])
			self.screen.blit(self.skip, [740,910,210,50])
			if 740 < mouse[0] < 950 and 910 < mouse[1] < 960:
				self.skip = pg.image.load('SKIP-select.png')
				if click[0] ==1:
					self.darkmode = False
					g = Game(5, self.chef1_points, self.chef2_points )
					g.run()
					self.running = False
					self.playing = False
					self.show_transition = False
				
			else:
				self.skip = pg.image.load('SKIP.png')
		else:
			self.screen.blit(self.transition_image,[0,0])
			if 750 <  mouse[0] < 965 and 925 < mouse[1] < 975:
				self.transition_image = pg.image.load('transition-next-select.png')
				if click[0] == 1:
					if self.level == 4:
						self.darkmode = True
					else:
						g = Game(self.level +1, self.chef1_points, self.chef2_points)
						g.run()
						self.running = False
						self.playing = False
						self.show_transition = False
			else:
				self.transition_image = pg.image.load('transition.png')
			draw_text(self.screen, str(self.level), 55, 550, 380)
			draw_text(self.screen, str(self.chef1_points), 60, 350, 460)#c2 score
			draw_text(self.screen, str(self.chef2_points), 60, 600, 460)#c1 score
		pg.display.update()
			
			

def main():
	g = Game(0)
	g.run()
	pg.quit()

if __name__ == '__main__':
	main()