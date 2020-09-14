#import pygame as pg
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

#pg.init()
#font_name = pg.font.match_font('arial')
class Player:
    def __init__(self):
        self.player1 = False
        self.player2 = False
    def player1_start(self):
        print("P1 is ready")
        self.player1 = True
    def player2_start(self):
        print("P2 is ready")
        self.player2 = True
    def both_player_ready(self):
        if self.player2 and self.player1:
            return True
        else:
            return False
    def reset_both_player(self):
        self.player1 = False
        self.player2 = False
    
def get_my_handler(pl):

    def my_handler(channel, data):
        inp = input_t.decode(data)
        out = output_t()
        

        # if inp.player == 1:
        #     out.player = inp.player
        #     if inp.motion == "start":
        #         pl.player1_start()
        #     elif inp.motion == "dead":
        #         print("send dead")
        #         out.motion == "1_dead"
        #         lc.publish("TO CLIENT", out.encode())
        #     else:
        #         out.motion = inp.motion
        #         lc.publish("TO CLIENT 2", out.encode())
        # elif inp.player == 2:
        #     if inp.motion == "start":
        #         pl.player2_start()
        #     elif inp.motion == "dead":
        #         print("send dead")
        #         out.motion == "2_dead"
        #         lc.publish("TO CLIENT 1", out.encode())
        #         lc.publish("TO CLIENT 2", out.encode())
        #     else:
        #         out.motion = inp.motion
        #         lc.publish("TO CLIENT 1", out.encode())
        # if pl.both_player_ready():
        #     start_game = output_t()
        #     start_game.motion = "start"
        #     print("publish message to start")
        #     pl.reset_both_player()
        #     lc.publish("TO CLIENT 2", start_game.encode())
        #     lc.publish("TO CLIENT 1", start_game.encode())


            
        if inp.motion == "start":
            print(inp.player)
            if inp.player == 1:
                pl.player1_start()
            elif inp.player == 2:
                pl.player2_start()
        else:
            out.player = inp.player
            out.motion = inp.motion
            lc.publish("TO CLIENT", out.encode())

        if pl.both_player_ready():
            start_game = output_t()
            start_game.motion = "start"
            print("publish message to start")
            pl.reset_both_player()
            lc.publish("TO CLIENT", start_game.encode())
        


            



    return my_handler


player = Player()
lc.subscribe("TO SERVER", get_my_handler(player))

while True:
    lc.handle_timeout(1)
    
