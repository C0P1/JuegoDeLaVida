import pygame
import numpy as np

# Definición de colores
BLACK = (0, 0, 0)   #Muerto o vacío
GREEN = (0, 255, 0) #Sano
RED = (255, 0, 0)   #Enfermo
LIGHT_BLUE = (16, 174, 222) #Recuperado o en recuperación

# Definición de estados-------------------------------------------------------------------------------------
DEAD = 0    #Estado muerto o vacío (Negro)
ALIVE = 1   #Estado vivo (Verde)
INFECTED = 2 #Infectado (Rojo)
RECOVERING = 3  #Recuperandose o recuperado (Azul)

# Definición de parámetros--------------------------------------------------------------------------------------
GRID_SIZE = 50  # Cambia esto para cambiar el tamaño de la cuadrícula
INITIAL_POPULATION = 1000 #Como no todo el grid puede estar lleno, aquí movemos y ajustamos la población inicial
INITIAL_INFECTED = 10 #Para evitar pasar por la probabilidad de influenza sin gente, aplicamos este como inicial para testeo
INFECTION_TIME = 14 #Unidades de tiempo que pasa el espécimen enfermo
CONTAGIOUS_TIME = 7 #Unidades de tiempo disponibles para poder contagiar a un vecino SOLAMENTE sano
RECOVERY_TIME = 120 #Unidades de tiempo de "inmunidad" a volverse a enfermar
INFLUENZA_PROBABILITY = 5 / 100000 #Una entre 100,000 habitantes para enfermar de la nada
CONTAGIOUS_PROBABILITY = [0.7, 0.3] #Durante el tiempo de infección después de 7 unidades de tiempo la probabilidad de contagio baja de 70% a 30%
RECOVERY_PROBABILITY = 0.6 #Durante cada unidad de tiempo tiene un 60% de recuperarse
DEATH_PROBABILITY = 0.000075  # Originalmente 0.00000075, pero esta es la probabilidad de que en una unidad de tiempo el espécimen muera

# Inicialización de la cuadrícula-------------------------------------------------------
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Población inicial--------------------------------------------------------------------
alive_cells = np.random.choice(GRID_SIZE*GRID_SIZE, INITIAL_POPULATION, replace=False)
grid[np.unravel_index(alive_cells, (GRID_SIZE, GRID_SIZE))] = ALIVE

# Infección inicial------------------------------------------------------------------
infected_cells = np.random.choice(alive_cells, INITIAL_INFECTED, replace=False)
grid[np.unravel_index(infected_cells, (GRID_SIZE, GRID_SIZE))] = INFECTED

# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE*10, GRID_SIZE*10)) #Inicializamos la ventana de visualización

# Bucle principal del juego, correrá de forma indefinida hasta que nosotros cerremos la ventana.
while True:

    #pygame.time.wait(100)
    #En caso de cerrar el juego para la ejecución.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN: #De testeo definimos que cuando demos clic en una celda se transforme directamente a enfermo
            x, y = pygame.mouse.get_pos()
            grid[x // 10, y // 10] = INFECTED

    # Actualización de la cuadrícula
    new_grid = grid.copy()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            state = grid[i, j] #Verifica el estado del espécimen en una parte específica del grid
            if state == DEAD:
                continue #Evita contar o realizar procesos en la cuadrícula si el espécimen está muerto
            elif state == ALIVE: #Caso contrario
                # Comprobar si se infecta
                infected_neighbors = 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue    #Aquí aplica la continuidad de que el grid también se afecte por los bordes
                        ni = (i + di) % GRID_SIZE
                        nj = (j + dj) % GRID_SIZE
                        if grid[ni, nj] == INFECTED:
                            infected_neighbors += 1 #Cuenta la cantidad de vecinos infectados y la incrementa usando moore de bordes
                if infected_neighbors > 0 and np.random.rand() < CONTAGIOUS_PROBABILITY[min(infected_neighbors-1, 1)]:
                    #Si la cantidad de vecinos infectados es mayor que 0 y se aplica la probabilidad de contagio este pasa a ser infectado
                    new_grid[i, j] = INFECTED
                    #Este aplica que si la influeza lo infecta aunque NO halla vecinos cerca pero la probabilidad es baja.
                elif np.random.rand() < INFLUENZA_PROBABILITY:
                    new_grid[i, j] = INFECTED
            elif state == INFECTED: #En caso de que este esté ya esté infectado se realiza lo siguiente.
                # Comprobar si se recupera o muere
                if np.random.rand() < DEATH_PROBABILITY: #Si consigue un número menor que la probabidad de muerte, este muere
                    new_grid[i, j] = DEAD
                elif np.random.rand() < RECOVERY_PROBABILITY: #Si consigue un número menor que la probabilidad de recuperación se recupera
                    new_grid[i, j] = RECOVERING
            elif state == RECOVERING: #En caso de que si se está recuperando
                # Comprobar si se recupera completamente
                if np.random.rand() < 1/RECOVERY_TIME: #Si la cantidad de tiempo ha pasado correctamente entonces pasa a ser vivo
                    new_grid[i, j] = ALIVE

    # Actualización de la pantalla por los colores correspondientes
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = BLACK
            if grid[i, j] == ALIVE:
                color = GREEN
            elif grid[i, j] == INFECTED:
                color = RED
            elif grid[i, j] == RECOVERING:
                color = LIGHT_BLUE
            pygame.draw.rect(screen, color, pygame.Rect(i*10, j*10, 10, 10))

    pygame.display.flip()
    grid = new_grid #Imprime la nueva pantalla de colores correspondientes
