import numpy as np
import os
import time


board = np.zeros((20,5),dtype = 'float')
#board of size (20,5)
#velocity of agent in the range 0-100 
#velocity of other vechiles is 50 (assumption)

num_traffic_vechiles = 3
space_bet_vechiles = 3
board_velocity = 40
set_time_frame = 1

class agent():
	def __init__(self,board):
		#start from the middle..
		self.x = 10
		self.y = 2 
		self.velocity = 40 
		board[self.x , self.y ] = self.velocity

	def iterate(self,board):
		delta_x = int(((self.velocity - board_velocity)*set_time_frame)/10)
		board[self.x , self.y ] = 0		
		self.x -= delta_x
		board[self.x , self.y ] = self.velocity

	def update_speed(self,delta_velocity):
		self.velocity += delta_velocity	


class traffic_vechile():
	def __init__(self,board):
		self.x = 19
		self.y = np.random.randint(0,5)
		self.velocity = np.random.randint(50,70) 
		board[self.x , self.y ] = self.velocity

	def iterate(self,board):
		
		if ( (self.x == 10 ) and (self.y == 2) ):
			board[self.x , self.y ] = 50
		
		if( self.x > 0 ):
			if 	(board[self.x - 1, self.y ] == 0 ): #checking empty spot ahead
				board[self.x , self.y ] = 0 #leaving_spot
				delta_x = int(((self.velocity - board_velocity)*set_time_frame)/10)
				self.x -= delta_x
				board[self.x , self.y ] = self.velocity
			else:
				self.velocity = board[self.x - 1 , self.y]
				board[self.x , self.y ] = self.velocity
		else:
			self.x = 0
			board[self.x , self.y ] = 0
		



 
if __name__ == '__main__':
	os.system('clear')
	agent = agent(board)
	iteration = 0
	traffic_vechile_count = 0
	tf_vechile = []
	while (1):
		if (iteration % space_bet_vechiles == 0):
			tf_vechile.append(traffic_vechile(board))
		for i in range(len(tf_vechile)):	
			tf_vechile[i].iterate(board)
		agent.iterate(board)
		print board
		time.sleep(0.5)
		os.system('clear')
		iteration += 1
