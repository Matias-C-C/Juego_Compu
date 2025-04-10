import pygame, sys

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
ANCHO = 800
ALTO = 650
x, y = 400, 500
vel = 10
fps = 30
clock = pygame.time.Clock()
pantalla = None

def jugador():
    jugador = pygame.image.load('player.png')
    jugador_rect = jugador.get_rect()
    jugador_rect.topleft = (x, y)
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        teclas = pygame.key.get_pressed()
        pygame.display.flip()
        if teclas[pygame.K_LEFT]:
            jugador_rect.x -= vel
        if teclas[pygame.K_RIGHT]:
            jugador_rect.x += vel  

        if jugador_rect.x < 0:
            jugador_rect.x = 0
        if jugador_rect.x > ANCHO:
            jugador_rect.x = 750

        pantalla.blit(jugador, jugador_rect)
        pygame.display.flip()
        clock.tick(fps)
        
    pygame.quit()

def pantalla_inicio(ruta_imagen):
    global pantalla
    fondo = pygame.image.load(ruta_imagen)
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    pantalla.blit(fondo, (0, 0))
    pygame.display.flip()

def menu(ruta_menu):
    fondo_menu = pygame.image.load(ruta_menu)
    fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
    pantalla.blit(fondo_menu, (0, 0))
    pygame.display.flip()

    eleccion1 = FUENTE_MINI.render('JUGAR', True, ROJO)
    eleccion1_rect = eleccion1.get_rect(center=(ANCHO // 4, ALTO // 2))
    
    eleccion2 = FUENTE_MINI.render('EXIT', True, ROJO)
    eleccion2_rect = eleccion2.get_rect(center=(ANCHO // 2, ALTO // 2))
    
    pantalla.blit(eleccion1, eleccion1_rect)
    pantalla.blit(eleccion2, eleccion2_rect)

    pygame.display.flip()

def eleccion():
    eleccion = None
    while eleccion is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ALTO // 2 - TAM_CELDA // 2 <= evento.pos[1] <= ALTO // 2 + TAM_CELDA // 2:
                    if ANCHO // 4 - 50 <= evento.pos[0] <= ANCHO // 4 + 50:
                        eleccion = 'JUGAR'
                    elif ANCHO // 2 - 50 <= evento.pos[0] <= ANCHO // 2 + 50:
                        eleccion = 'EXIT'
   
    if eleccion == 'JUGAR':
        pantalla_inicio(ruta_imagen)
    elif eleccion == 'EXIT':
        next

def inicio():
    global pantalla, ruta_imagen, ruta_menu, FUENTE, FUENTE_MINI
    pygame.init()
    FUENTE = pygame.font.SysFont('Arial', 80)
    FUENTE_MINI = pygame.font.SysFont('Arial', 30)
    ruta_imagen = 'imagen_fondo.png'
    ruta_menu = 'fondo_d_menu.png'
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space Invaders")
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        #menu(ruta_menu)
        #eleccion()
        pantalla_inicio(ruta_imagen)
        jugador()

    pygame.quit()

if __name__ == '__main__':
    inicio()