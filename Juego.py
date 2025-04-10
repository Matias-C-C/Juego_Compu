#region Importaciones y declaraciones
import pygame, sys

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
ANCHO = 1000
ALTO = 650
e, m = 400, 10
x, y = 400, 500
vel = 10
fps = 30
clock = pygame.time.Clock()
pantalla = None
#endregion

def jugador_enemigo():
    jugador = pygame.image.load('player.png')
    jugador_rect = jugador.get_rect()
    jugador_rect.topleft = (x, y)
    enemigo = pygame.image.load('enemigo.png')
    enemigo_rect = jugador.get_rect()
    enemigo_rect.topleft = (e, m)
    fondo = pygame.image.load(ruta_imagen)
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

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
        if jugador_rect.x > ANCHO - jugador_rect.width:
            jugador_rect.x = ANCHO - jugador_rect.width

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(enemigo, enemigo_rect)
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

def dibujar_texto(texto, fuente, color, x, y):
        render = fuente.render(texto, True, color)
        rect = render.get_rect(center=(x, y))
        pantalla.blit(render, rect)
        return rect

def dibujar_boton():
        fondo_menu = pygame.image.load(ruta_menu)
        fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
        pantalla.blit(fondo_menu, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        boton_jugar = pygame.Rect(0, 0, 0, 0) 
        boton_exit = pygame.Rect(0, 0, 0, 0)

        dibujar_texto("Space Invaders", FUENTE_TITULO, BLANCO, ANCHO // 2, ALTO // 4)
        color_jugar = ROJO if boton_jugar.collidepoint(mouse_pos) else BLANCO
        boton_jugar_rect = dibujar_texto("JUGAR", FUENTE_BOTON, color_jugar, ANCHO // 2, ALTO // 2)
        
        color_exit = ROJO if boton_exit.collidepoint(mouse_pos) else BLANCO
        boton_exit_rect = dibujar_texto("EXIT", FUENTE_BOTON, color_exit, ANCHO // 2, ALTO // 2 + 80)

        if boton_jugar_rect.collidepoint(mouse_pos):
            if click[0]:  
                pantalla_inicio()

        if boton_exit_rect.collidepoint(mouse_pos):
            if click[0]:
                pygame.quit()
                sys.exit()

            boton_jugar = boton_jugar_rect
            boton_exit = boton_exit_rect

            pygame.display.flip()
            clock.tick(60)

def inicio():
    global pantalla, ruta_imagen, ruta_menu, FUENTE_TITULO, FUENTE_BOTON
    pygame.init()
    ruta_imagen = 'imagen_fondo.png'
    ruta_menu = 'fondo_d_menu.png'
    FUENTE_TITULO = pygame.font.SysFont('Arial', 80)
    FUENTE_BOTON = pygame.font.SysFont('Arial', 40)
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space Invaders")
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        dibujar_texto("Space Invaders", FUENTE_TITULO, BLANCO, ANCHO // 2, ALTO // 4)
        dibujar_boton()
        pantalla_inicio(ruta_imagen)
        jugador_enemigo()

    pygame.quit()

if __name__ == '__main__':
    inicio()