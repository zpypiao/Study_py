import pygame, sys
form pygame.locals import *

class TankMain(object):
	# the mainwindow of tank game
	
	# start the game
	def startGame(self):
		pygame.init()
		# the size of window,the type(0:cannot change;RESIZEBLE;FULLSCREEN)
		screem = pygame.display.set_mode((600, 500), 0, 32)
		screem.display.set_caption('Tank Game')
		while True:
			# set the background color of window
			screem.fill((255, 255, 255))
			screem.blit(self.writeText(), (0, 5))
			self.getEvent()
			screem.display.update()

	def stopGame(self):
		# exit the program
		sys.exit()
	
	def writeText(self):
		'''display the context ont the left of screen'''
		
		# creat a font
		theFont = pygame.font.SysFont('simsun', 10)
		# set the text
		textSf = theFont.render('The number of tanks(enimy)'), True, (255, 0, 0))
		return textSf
	
	def getEvent(self):
		for every in pygame.event.get():
			if every.type == QUIT:
				self.stopGame()
			elif every.type == KEYDOWN:
				if every.key == K_LEEF:
					pass
				elif every.key == K_RIGHT:
					pass
				elif every.key == K_UP:
					pass
				elif every.key == K_DOWN:
					pass
				elif every.key = K_ESCAPE:
					self.stopGame()
				
			elif every.type == MOUSEBUTTONDOWN:
				pass
		
class BaseItem(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__()
		
class Tank(BaseItem):
	#define the ad of class
	width = 50
	height = 50
	
	def __init__(self):
		super().__init__()
		self.width = 200
		# the default direction is down;UDLR
		self.direction = 'U'
		self.images = {}
		self.images['U'] = pygame.image.load('./image/tankleft.jpg')
		self.images['D'] = pygame.image.load('./image/tankleft.jpg')
		self.images['L'] = pygame.image.load('./image/tankleft.jpg')
		self.images['R'] = pygame.image.load('./image/tankleft.jpg')
		self.image = self.images[self.direction]
		# decide the status of tank
		self.live = True
		
		
		
if __name__ == '__main__':
	game = TankMain()
	game.startGame()
