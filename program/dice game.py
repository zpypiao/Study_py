import random

class Game:
	
	def __init__(self,player1,player2):
		self.player1 = player1
		self.player2 = player2
		print('Sucessfully restart the game')
	
	def start_game(self):
		self.player1.cast()
		self.player2.cast()
		'''player1_dice_count_list = [dice.count for dice in self.player1.dices]
		player2_dice_count_list = [dice.count for dice in self.player2.dices]
		print("Player1's count is %d"%player1_dice_count_list)
		print("Player2's count is %d"%player2_dice_count_list)'''
		print(self.player1,'\n',self.player2,sep='')
		
class Player:
	
	def __init__(self,name,sex,*dice):
		self.name = name
		self.sex = sex
		self.dices = dice #the dices player have
	
	def __str__(self):
		player_dice_count_list = [dice.count for dice in self.dices]
		return "%s 's dice count is %s"%(self.name,player_dice_count_list)
	
	#player cast the dice
	def cast(self):
		for dice in self.dices:
			dice.move()
	
	def guess_dice(self):
		return (4,2)

class Dice:
	
	def __init__(self):
		self.count = 0
	
	#change the count of dice
	def move(self):
		self.count = random.randint(1,6)
	
dice1 = Dice()
dice2 = Dice()
dice3 = Dice()
dice4 = Dice()
dice5 = Dice()
dice6 = Dice()

player1 = Player('zpy','man',dice1,dice2,dice3)
player2 = Player('xyj','woman',dice4,dice5,dice6)

for i in range(1,6):
    print('the %d of game'%i)
	game = Game(player1,player2)
	game.start_game()
