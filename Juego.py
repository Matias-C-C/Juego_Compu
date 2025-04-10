#region Importaciones y declaraciones
import pygame, sys, random

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
ANCHO = 1000
ALTO = 650

e, m = 400, 10
x, y = 400, 500
vel = 10
velocidad = 8
fps = 30

clock = pygame.time.Clock()
pantalla = None
ruta_imagen = 'imagen_fondo.png'
ruta_menu = 'fondo_d_menu.png'
fondo_avatar = 'fondo avatar.png'
ruta_avatar = ['player.png', 'avatar.png', 'avatar2.png']
#endregion

def dibujar_texto(texto, fuente, color, x, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y))
    pantalla.blit(render, rect)
    return rect

def menu_inicio():
    boton_jugar = pygame.Rect(0, 0, 0, 0)
    boton_exit = pygame.Rect(0, 0, 0, 0)
    boton_avatar = pygame.Rect(0, 0, 0, 0)
    boton_score = pygame.Rect(0, 0, 0, 0)

    ejecutando_menu = True
    while ejecutando_menu:
        fondo_menu = pygame.image.load(ruta_menu)
        fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
        pantalla.blit(fondo_menu, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        dibujar_texto("Space Invaders", FUENTE_TITULO, BLANCO, ANCHO // 2, ALTO // 4)

        color_jugar = ROJO if boton_jugar.collidepoint(mouse_pos) else BLANCO
        boton_jugar = dibujar_texto("JUGAR", FUENTE_BOTON, color_jugar, ANCHO // 3, ALTO // 1.75)

        color_avatar = ROJO if boton_avatar.collidepoint(mouse_pos) else BLANCO
        boton_avatar = dibujar_texto("AVATAR", FUENTE_BOTON, color_avatar, ANCHO // 3, ALTO // 1.30)

        color_score = ROJO if boton_score.collidepoint(mouse_pos) else BLANCO
        boton_score = dibujar_texto("SCORE", FUENTE_BOTON, color_score, ANCHO // 1.5, ALTO // 1.30)

        color_exit = ROJO if boton_exit.collidepoint(mouse_pos) else BLANCO
        boton_exit = dibujar_texto("EXIT", FUENTE_BOTON, color_exit, ANCHO // 1.5, ALTO // 2.25 + 80)

        if boton_jugar.collidepoint(mouse_pos) and click[0]:
            pygame.time.wait(200)
            jugador_enemigo()
            ejecutando_menu = False

        if boton_exit.collidepoint(mouse_pos) and click[0]:
            pygame.quit()
            sys.exit()
        
        if boton_avatar.collidepoint(mouse_pos) and click[0]:
            pygame.time.wait(200)
            avatar()
        
        if boton_score.collidepoint(mouse_pos) and click[0]:
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def avatar():
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        fondito = pygame.image.load(fondo_avatar)
        fondito = pygame.transform.scale(fondito, (ANCHO, ALTO))

def enemigo():
    enemigo = pygame.image.load('enemigo.png')
    enemigo_rect = enemigo.get_rect()
    enemigo_rect.topleft = (e, m)
    fondo = pygame.image.load(ruta_imagen)
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        if enemigo_rect.e < 0:
            enemigo_rect.e += velocidad
        if enemigo_rect.e > ANCHO - enemigo_rect.width:
            enemigo_rect.e -= velocidad

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(enemigo, enemigo_rect)
        pygame.display.flip()
        clock.tick(fps)
        corriendo = False

def jugador_enemigo():
    avatar = random.choice(ruta_avatar)
    jugador = pygame.image.load(avatar)
    jugador_rect = jugador.get_rect()
    jugador_rect.topleft = (x, y)

    fondo = pygame.image.load(ruta_imagen)
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            jugador_rect.x -= vel
        if teclas[pygame.K_RIGHT]:
            jugador_rect.x += vel  

        if jugador_rect.x < 0:
            jugador_rect.x = 0
        if jugador_rect.x > ANCHO - jugador_rect.width:
            jugador_rect.x = ANCHO - jugador_rect.width

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(jugador, jugador_rect)
        enemigo()
        
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

def inicio():
    global pantalla, FUENTE_TITULO, FUENTE_BOTON
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space Invaders")

    FUENTE_TITULO = pygame.font.SysFont('Arial', 80)
    FUENTE_BOTON = pygame.font.SysFont('Arial', 40)

    menu_inicio()

if __name__ == '__main__':
    inicio()