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
		
if __name__ == '__main__':
	game = TankMain()
	game.startGame()
