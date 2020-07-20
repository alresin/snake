from random import randint
import pygame
pygame.init()

def log(*args):
	print(*args)
	#pass

def config():
	global NUMBER_OF_CELLS, speed_of_snake, SIZE_OF_CELL

	cells = input('Введите ширину и высоту поля в клетках через запятую: ')
	speed = input('Введите скорость змейки (5-15): ')
	cell_size =	input('Введите размер клетки в пикселях: ')

	if cells.strip() != '': 	NUMBER_OF_CELLS = tuple([int(x) for x in cells.split(',')])
	if speed.strip() != '': 	speed_of_snake = int(speed)
	if cell_size.strip() != '': SIZE_OF_CELL = int(cell_size)

speed_of_snake = 11

NUMBER_OF_CELLS = 40, 40
SIZE_OF_CELL = 15

white = (255, 255, 255)
light_grey = (120, 120, 120)
dark_grey = (110, 110, 110)
brown = (148,73,23)
black = (0, 0, 0)

class Snake():
	def __init__(self, length = 5):
		self.head_x = size[1] // 2
		self.head_y = size[1] // 2
		self.way = 1
		self.last_point = (self.head_x - 5 * SIZE_OF_CELL, self.head_y)
		self.tail = []

		for i in range(length):
			self.tail.append([self.head_x - i * SIZE_OF_CELL, self.head_y])

	def draw(self):
		i = 1
		while (i < len(self.tail)):
			pos = self.tail[i]
			i += 1

			block = pygame.Surface((SIZE_OF_CELL, SIZE_OF_CELL))
			block.fill(brown)
			window.blit(block, pos)

		window.blit(heads[self.way], self.tail[0])

	def move(self):
		global not_over, apple_point

		if self.way == 0: different_of_now_and_next_pos = (0, -SIZE_OF_CELL)
		if self.way == 1: different_of_now_and_next_pos = (SIZE_OF_CELL, 0)
		if self.way == 2: different_of_now_and_next_pos = (0, SIZE_OF_CELL)
		if self.way == 3: different_of_now_and_next_pos = (-SIZE_OF_CELL, 0)

		self.last_point =  self.tail.pop(-1)

		self.tail.insert(0, [self.tail[0][0] + different_of_now_and_next_pos[0], self.tail[0][1] + different_of_now_and_next_pos[1]])

		if self.tail[0][0] < 0 or self.tail[0][0] > size[0] - SIZE_OF_CELL or \
			self.tail[0][1] < 0 or self.tail[0][1] > size[1] - SIZE_OF_CELL:		#проверка выхода за поле
			not_over = False

		for i in range(len(self.tail)):								#проверка наезда на хвост
			for o in range(i + 1, len(self.tail)):
				if self.tail[i] == self.tail[o]:
					self.eat_himself()
					break

		if apple_point == self.tail[0]:								#проверка на яблоки и их поедание
			self.tail.append(self.last_point)

			apple_point = []

			if len(self.tail) == size[0] * size[1]:
				draw_menu_interface(win_text)

		self.draw()

	def eat_himself(self):
		eating_block_point = self.tail.index(self.tail[0], 1)
		
		self.last_point = eating_block_point
		self.tail = self.tail[:eating_block_point]

class Button():
	def __init__(self, text, bg_color, font_size, height, function, indent = 15):
		self.text = text
		self.bg_color = bg_color
		self.font = pygame.font.SysFont('comicsansms', font_size)
		self.height = height
		self.indent = indent
		self.function = function

	def draw(self):
		text = self.font.render(self.text, True, white)
		self.point = ((size[0] - text.get_width()) // 2, self.height)

		bg = pygame.draw.rect(window, self.bg_color, (self.point[0], self.point[1], 
								text.get_width() + 2 * self.indent, text.get_height() + 2 * self.indent))

		window.blit(text, (self.point[0] + self.indent, self.point[1] + self.indent))

		self.sides = (self.height, self.point[0] + text.get_width(), 
						self.height + text.get_height(), self.point[0])

	def check_for_click_and_pos(self, mouse_pos):
		if mouse_pos[0] >= self.sides[3] and mouse_pos[0] <= self.sides[1] and \
			mouse_pos[1] >= self.sides[0] and mouse_pos[1] <= self.sides[2]:
			self.bg_color = dark_grey

			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.function()
		else:
			self.bg_color = light_grey

def quit():
	global run
	run = False

def set_apple():
	global apple_point
	x = randint(0, NUMBER_OF_CELLS[0] - 1) * SIZE_OF_CELL
	y = randint(0, NUMBER_OF_CELLS[1] - 1) * SIZE_OF_CELL

	if snake.tail.count([x, y]):
		set_apple()

	elif apple_point == []:
		apple_point = [x, y]
	
	window.blit(apple, apple_point)

def draw_gaming_interface():
	window.fill(black)

	snake.move()

	set_apple()

def load_images():
	global apple, heads

	apple = pygame.image.load('apple.png')
	head0 = pygame.image.load('head0.png')
	head1 = pygame.image.load('head1.png')
	head2 = pygame.image.load('head2.png')
	head3 = pygame.image.load('head3.png')

	heads = [head0, head1, head2, head3]

def start_app():
	global window, lose_text, start_text, button_new_game, button_quit, run, not_pause, started, not_over, pause, size

	size = NUMBER_OF_CELLS[0] * SIZE_OF_CELL, NUMBER_OF_CELLS[1] * SIZE_OF_CELL

	pygame.display.set_caption('Snake v0.1')
	window = pygame.display.set_mode(size)

	button_new_game = 	Button('New game', light_grey, min(size) // 15, size[1] // 2.7, start_game, min(size) // 40)
	button_quit = 		Button('Quit', light_grey, min(size) // 15, size[1] // 1.8, quit, min(size) // 40)

	font = pygame.font.SysFont('comicsansms', int(min(size) // 8.5))

	start_text = 	font.render('Snake v1.0', True, white)
	lose_text = 	font.render('Game Over', True, white)
	win_text = 		font.render('You Win!', True, white)

	pause = pygame.Surface((min(size) // 5, min(size) // 4))						#need fix, quikly!!!
	pygame.draw.rect(pause, white, (1, 1, pause.get_width() // 5, pause.get_height()))
	pygame.draw.rect(pause, white, (pause.get_width() // 1.25, 1, pause.get_width() // 5, pause.get_height()))

	run = 		True
	not_pause = True
	started = 	False
	not_over = 	True

def start_game():
	global snake, apple_point, not_over, started

	started = 	True
	not_over = 	True
	
	snake = Snake()
	apple_point = []

def draw_menu_interface(text):
	window.fill(black)

	window.blit(text, ((size[0] - text.get_width()) // 2,
				(size[1] - text.get_height()) // 2 - size[1] // 4))

	button_new_game.draw()
	button_quit.draw()

	mouse_pos = pygame.mouse.get_pos()

	button_new_game.check_for_click_and_pos(mouse_pos)
	button_quit.check_for_click_and_pos(mouse_pos)

def main():
	global events, run, not_pause, not_over, snake

	load_images()
	start_app()

	while run:
		pygame.time.delay(1000 // speed_of_snake)

		if not_over and started: final_way = snake.way

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.KEYDOWN and not_over and started:
				if event.key == pygame.K_p:
					not_pause = not not_pause
				if event.key == pygame.K_w and snake.way != 2:
					final_way = 0
				elif event.key == pygame.K_d and snake.way != 3:
					final_way = 1
				elif event.key == pygame.K_s and snake.way != 0:
					final_way = 2
				elif event.key == pygame.K_a and snake.way != 1:
					final_way = 3 
		
		if not_over and started: snake.way = final_way

		if not_pause and not_over and started:
			draw_gaming_interface()

		if not not_pause:
			window.blit(pause, ((size[0] - pause.get_width()) // 2, (size[0] - pause.get_height()) // 2))

		if not not_over:
			draw_menu_interface(lose_text)

		if not started:
			draw_menu_interface(start_text)

		pygame.display.flip()

	pygame.quit()

if __name__ == '__main__':
	config()
	main()