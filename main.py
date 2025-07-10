import pygame, time, sys

pygame.init()

screen = pygame.display.set_mode([600, 900])
screen.fill([0, 0, 0])

moon = pygame.image.load("sprites/moon.png")
moon2 = pygame.image.load("sprites/moon2.png")
rocket = pygame.image.load("sprites/rocket.png")

def default_variable():
	global height, velocity, fuel, thrust, ship_mass, gravity, delta_v, y_pos, ground, start, power, clock, hold, running, read_inst
	# переменные
	height = 2000
	velocity = -100.0 # скорость
	fuel = 1000.0
	thrust = 0 # тяга
	ship_mass = 5000.0
	gravity = 1.62
	delta_v = 0
	y_pos = 90
	ground = 550
	start = 90
	power = ship_mass * gravity
	clock = pygame.time.Clock()
	hold = False
	running = True
	read_inst = False

default_variable()

class Control(pygame.sprite.Sprite):
	def __init__(self, location = [0, 0]):
		pygame.sprite.Sprite.__init__(self)
		surf = pygame.surface.Surface([30, 10])
		surf.fill([255, 215, 0])
		self.image = surf.convert()
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.centery = location 

def calc_velocity():
    global delta_v, thrust, fuel, velocity, height, y_pos
    # Отсчитываем один виток pygame-цикла
    delta_t = 1/fps
    # Преобразуем позицию y ручки регулятора в реактивную тягу
    thrust = (500 - myControl.rect.centery) * 5.0
    # Вычитаем горючее в зависимости от тяги
    fuel -= thrust /(10 * fps)
    if fuel < 0:  fuel = 0.0
    if fuel < 0.1:  thrust = 0.0
    # Физическая формула
    delta_v = delta_t * (-gravity + 200 * thrust / (ship_mass + fuel))
    velocity = velocity + delta_v
    delta_h = velocity * delta_t
    height = height + delta_h
    # Преобразуем высоту в pygame-координату y
    y_pos = ground - (height * (ground - start) / 2000) - 90

def flames():
	flame_size = thrust / 15
	for i in range(2):
		startx = 296 - 10 + i * 20
		starty = y_pos + 275
		pygame.draw.polygon(screen, [255, 215, 0], 
			[(startx, starty), 
			(startx + 4, starty + flame_size), 
			(startx + 8, starty)], 0) 

myControl = Control([15, 500])

def read_instr(read_inst):
	while read_inst != True:
		instr = pygame.image.load("sprites/instr.png")
		press = pygame.image.load("sprites/press.png")
		screen.blit(instr, (0, 0, 600, 900))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					read_inst = True
		pygame.display.flip()
		time.sleep(0.5)
		screen.blit(press, (200, 750, 100, 200))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					read_inst = True
		time.sleep(0.5)

def display_stats():
	global acceleration
	font = pygame.font.SysFont("Tahoma", 36, bold = True)
	#fuel
	fuel_surf = font.render(str(f"Топливо {int(fuel)}"), 1, ("white"))
	screen.blit(fuel_surf, [20, 25])
	#height
	height_surf = font.render(str(f"Высота {int(height)}"), 1, ("white"))
	screen.blit(height_surf, [20, 65])
	#velocity
	velocity_surf = font.render(str(f"Скорость {int(abs(velocity))} м/с"), 1, ("white"))
	screen.blit(velocity_surf, [20, 110])
	#acceleration
	acceleration = delta_v * fps
	acceleration_surf = font.render(str(f"Ускорение {int(acceleration)}"), 1, ("white"))
	screen.blit(acceleration_surf, [20, 150])
	#thrust
	thrust_surf = font.render(str(f"Тяга {int(thrust)}"), 1, ("white"))
	screen.blit(thrust_surf, [20, 190])

def restart_game():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					default_variable()
					break
		break

def display_result():
	font = pygame.font.SysFont("Tahoma", 26, bold = True)
	if int(abs(velocity)) <= 10 and int(abs(velocity)) >= 1:
		result_surf = font.render("Вы идеально посадили корабль!", 1, ("white"))
		blit_message("Нажмите R чтобы начать заново", 75, 480)
		screen.blit(result_surf, [20, 450])
		pygame.display.flip()
		restart_game()
	
	elif int(abs(velocity)) <= 20 and int(abs(velocity)) >= 11:
		result_surf = font.render("Вы отлично посадили корабль!", 1, ("white"))
		screen.blit(result_surf, [20, 450])
		blit_message("Нажмите R чтобы начать заново", 75, 480)
		pygame.display.flip()
		restart_game()
	
	elif int(abs(velocity)) <= 25 and abs(velocity) >= 21:
		result_surf = font.render("Вы жестко посадили корабль!", 1, ("white"))
		screen.blit(result_surf, [20, 450])
		blit_message("Нажмите R чтобы начать заново", 75, 480)
		pygame.display.flip()
		restart_game()
	
	elif int(abs(velocity)) >= 26:
		result_surf = font.render("Вы посадили корабль слишком быстро!", 1, ("white"))
		screen.blit(result_surf, [20, 450])
		blit_message("Нажмите R чтобы начать заново", 75, 480)
		pygame.display.flip()
		restart_game()

def blit_message(text, x, y):
	font = pygame.font.SysFont("Tahoma", 26, bold = True)
	surf = font.render(text, 1, ("white"))
	screen.blit(surf, [x, y])

read_instr(read_inst)
while running == True:
	clock.tick(30)
	fps = clock.get_fps()
	if fps < 1: fps = 30
	if height > 0.01:
		calc_velocity()
		screen.blit(moon, [0, 0, 600, 900])
		screen.blit(moon2, [100, 650, 650, 100])
		flames()
		screen.blit(rocket, [200, y_pos, 50, 90])
		
		pygame.draw.rect(screen, [128, 128, 128], [25, 300, 10, 200], 0)
		screen.blit(myControl.image, myControl.rect)

		pygame.draw.rect(screen, [128, 128, 128], [80, 350, 24, 100], 2)
		fuelbar = 96 * fuel / 1000

		pygame.draw.rect(screen, [255, 215, 0], [84, 448 - fuelbar, 18, fuelbar], 0)
		display_stats()
		if y_pos <= -300:
			blit_message("Вы слетели с орбиты!", 150, 450)
			blit_message("Нажмите R чтобы начать заново", 75, 480)
			pygame.display.flip()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_r:
							default_variable()
							break
				break

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				hold = True
			
			elif event.type == pygame.MOUSEBUTTONUP:
				hold = False

			elif event.type == pygame.MOUSEMOTION:
				if hold == True:
					myControl.rect.centery = event.pos[1]
					if myControl.rect.centery < 300:
						myControl.rect.centery = 300
					if myControl.rect.centery > 500:
						myControl.rect.centery = 500
	if height <= 0:
		display_result()