#region Importaciones y declaraciones
import pygame, sys, random, os

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
ANCHO = 1000
ALTO = 650

x, y = 400, 500
vel = 10
velocidad_enemigo = 5
fps = 30
nombre_jugador = ""

clock = pygame.time.Clock()
pantalla = None
ruta_imagen = 'Imagenes\\imagen_fondo.png'
ruta_menu = 'Imagenes\\MENU.png.png'
fondo_avatar = 'Imagenes\\fondo avatar.png'
fondo_final = 'Imagenes\\fondo_d_menu.png'
fondo_score = 'Imagenes\\menu_puntajes.png.png'
ruta_avatar = ['Personajes\\avatar2.png', 'Personajes\\avatar.png', 'Personajes\\avatar1.png', 'Personajes\\avatar3.png']
avatar_seleccionado = ruta_avatar[0] 
#endregion

#region Funciones
def dibujar_texto(texto, fuente, color, x, y):
    render = fuente.render(texto, True, color)
    rect = render.get_rect(center=(x, y))
    pantalla.blit(render, rect)
    return rect

def guardar_puntaje(nombre, puntos):
    puntajes = leer_puntajes()
    puntajes[nombre] = max(puntos, puntajes.get(nombre, 0))
    with open('Juego\\puntajes.txt', 'w') as f:
        for jugador, score in sorted(puntajes.items(), key=lambda item: item[1], reverse=True):
            f.write(f"{jugador}:{score}\n")

def leer_puntajes():
    puntajes = {}
    if os.path.exists('Juego\\puntajes.txt'):
        with open('Juego\\puntajes.txt', 'r') as f:
            for linea in f:
                if ':' in linea:
                    nombre, score = linea.strip().split(':')
                    puntajes[nombre] = int(score)
    return puntajes

def ingresar_nombre():
    global nombre_jugador
    nombre = ""
    ingresando = True
    while ingresando:
        fondo = pygame.image.load(fondo_score)
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        pantalla.blit(fondo, (0, 0))
        dibujar_texto("Ingresa tu nombre", FUENTE_TITULO, BLANCO, ANCHO // 2, ALTO // 3)
        dibujar_texto(nombre, FUENTE_BOTON, BLANCO, ANCHO // 2, ALTO // 2)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre:
                    nombre_jugador = nombre
                    ingresando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.unicode.isalnum() or evento.unicode == " ":
                    nombre += evento.unicode
        pygame.display.flip()
        clock.tick(30)

def mostrar_vidas(vidas):
    for i in range(vidas):
        pygame.draw.rect(pantalla, ROJO, (900 - i*30, 10, 20, 20))

def mostrar_puntajes():
    ejecutando = True
    while ejecutando:
        fondo_menu = pygame.image.load(fondo_score)
        fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
        pantalla.blit(fondo_menu, (0, 0))

        puntajes = leer_puntajes()
        dibujar_texto("PUNTAJES", FUENTE_TITULO, BLANCO, ANCHO // 2, 100)

        for i, (nombre, puntaje) in enumerate(list(puntajes.items())[:10]):
            dibujar_texto(f"{i+1}. {nombre}: {puntaje}", FUENTE_BOTON, BLANCO, ANCHO // 2, 180 + i*40)

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        volver_btn = dibujar_texto("VOLVER", FUENTE_BOTON, ROJO if pygame.Rect(430, 580, 140, 40).collidepoint(mouse_pos) else BLANCO, ANCHO // 2, 600)

        if volver_btn.collidepoint(mouse_pos) and click[0]:
            pygame.time.wait(200)
            ejecutando = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def jugador_enemigo():
    global avatar_seleccionado, nombre_jugador
    jugador = pygame.image.load(avatar_seleccionado)
    jugador = pygame.transform.scale(jugador, (100, 100))
    jugador_rect = jugador.get_rect()
    jugador_rect.topleft = (x, y)

    enemigo_img = pygame.image.load('Personajes\\enemigo.png')
    enemigo_img = pygame.transform.scale(enemigo_img, (50, 50))
    filas_enemigos = 1

    def generar_enemigos(filas):
        enemigos_nuevos = []
        for fila in range(filas):
            for i in range(8):
                rect = enemigo_img.get_rect()
                rect.topleft = (100 + i * 100, 100 + fila * 60)
                enemigos_nuevos.append(rect)
        return enemigos_nuevos

    enemigos = generar_enemigos(filas_enemigos)
    direccion = 1
    velocidad_enemigos = 3

    balas_jugador = []
    balas_enemigas = []
    puntos = 0
    vidas = 3
    ultimo_disparo_enemigo = pygame.time.get_ticks()
    ultimo_disparo_jugador = pygame.time.get_ticks()
    fondo = pygame.image.load(ruta_imagen)
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    oleada_en_espera = False
    tiempo_oleada = 0
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                ahora = pygame.time.get_ticks()
                
                if ahora - ultimo_disparo_jugador >= 1000: 
                    nueva_bala = pygame.Rect(jugador_rect.centerx, jugador_rect.top, 5, 10)
                    balas_jugador.append(nueva_bala)
                    ultimo_disparo_jugador = ahora

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jugador_rect.x -= vel
        if teclas[pygame.K_RIGHT]:
            jugador_rect.x += vel

        jugador_rect.x = max(0, min(ANCHO - jugador_rect.width, jugador_rect.x))

        for bala in balas_jugador[:]:
            bala.y -= 15
            if bala.y < 0:
                balas_jugador.remove(bala)

        for bala in balas_enemigas[:]:
            bala.y += 15
            if bala.y > ALTO:
                balas_enemigas.remove(bala)

        for bala in balas_enemigas[:]:
            if bala.colliderect(jugador_rect):
                balas_enemigas.remove(bala)
                vidas -= 1
                if vidas <= 0:
                    guardar_puntaje(nombre_jugador, puntos)
                    pantalla_fin("¡Perdiste!", puntos)
                    return

        mover_abajo = False
        for enemigo in enemigos:
            enemigo.x += direccion * velocidad_enemigos
            if enemigo.right >= ANCHO or enemigo.left <= 0:
                mover_abajo = True

        if mover_abajo:
            direccion *= -1
            for enemigo in enemigos:
                enemigo.y += 20

        for bala in balas_jugador[:]:
            for enemigo_rect in enemigos[:]:
                if bala.colliderect(enemigo_rect):
                    balas_jugador.remove(bala)
                    enemigos.remove(enemigo_rect)
                    puntos += 1
                    break

        ahora = pygame.time.get_ticks()
        if ahora - ultimo_disparo_enemigo > 1500 and enemigos:
            enemigo_random = random.choice(enemigos)
            bala = pygame.Rect(enemigo_random.centerx, enemigo_random.bottom, 5, 10)
            balas_enemigas.append(bala)
            ultimo_disparo_enemigo = ahora

        if not enemigos and not oleada_en_espera:
            oleada_en_espera = True
            tiempo_oleada = pygame.time.get_ticks()

        if oleada_en_espera and pygame.time.get_ticks() - tiempo_oleada >= 3000:
            filas_enemigos += 1
            if filas_enemigos > 5:
                guardar_puntaje(nombre_jugador, puntos)
                pantalla_fin("¡GANASTE EL JUEGO!", puntos)
                return
            enemigos = generar_enemigos(filas_enemigos)
            oleada_en_espera = False

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(jugador, jugador_rect)
        for enemigo_rect in enemigos:
            pantalla.blit(enemigo_img, enemigo_rect)
        for bala in balas_jugador:
            pygame.draw.rect(pantalla, ROJO, bala)
        for bala in balas_enemigas:
            pygame.draw.rect(pantalla, BLANCO, bala)

        dibujar_texto(f"Puntos: {puntos}", FUENTE_BOTON, BLANCO, 100, 30)
        mostrar_vidas(vidas)

        pygame.display.flip()
        clock.tick(fps)

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

        color_jugar = ROJO if boton_jugar.collidepoint(mouse_pos) else BLANCO
        boton_jugar = dibujar_texto("JUGAR", FUENTE_BOTON, color_jugar, ANCHO // 3, ALTO // 1.75)

        color_avatar = ROJO if boton_avatar.collidepoint(mouse_pos) else BLANCO
        boton_avatar = dibujar_texto("AVATAR", FUENTE_BOTON, color_avatar, ANCHO // 3, ALTO // 1.30)

        color_score = ROJO if boton_score.collidepoint(mouse_pos) else BLANCO
        boton_score = dibujar_texto("SCORE", FUENTE_BOTON, color_score, ANCHO // 1.6, ALTO // 1.30)

        color_exit = ROJO if boton_exit.collidepoint(mouse_pos) else BLANCO
        boton_exit = dibujar_texto("EXIT", FUENTE_BOTON, color_exit, ANCHO // 1.6, ALTO // 2.25 + 80)

        if boton_jugar.collidepoint(mouse_pos) and click[0]:
            pygame.time.wait(200)
            ingresar_nombre()
            jugador_enemigo()
            ejecutando_menu = False

        if boton_exit.collidepoint(mouse_pos) and click[0]:
            pygame.quit()
            sys.exit()

        if boton_avatar.collidepoint(mouse_pos) and click[0]:
            pygame.time.wait(200)
            avatar()

        if boton_score.collidepoint(mouse_pos) and click[0]:
            mostrar_puntajes()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def avatar():
    global avatar_seleccionado 
    corriendo = True

    imagenes_avatar = [pygame.image.load(ruta) for ruta in ruta_avatar]
    rects_avatar = []

    for i, img in enumerate(imagenes_avatar):
        img = pygame.transform.scale(img, (100, 100))
        imagenes_avatar[i] = img
        rect = img.get_rect()
        rect.topleft = (150 + i * 200, 300)
        rects_avatar.append(rect)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                print ("holaaa")
                for i, rect in enumerate(rects_avatar):
                    if rect.collidepoint(evento.pos):
                        avatar_seleccionado = ruta_avatar[i]
                        corriendo = False  

        fondito = pygame.image.load(fondo_avatar)
        fondito = pygame.transform.scale(fondito, (ANCHO, ALTO))
        pantalla.blit(fondito, (0, 0))

        dibujar_texto("SELECCIONA TU AVATAR", FUENTE_TITULO, BLANCO, ANCHO // 2, 100)

        for i in range(len(imagenes_avatar)):
            pantalla.blit(imagenes_avatar[i], rects_avatar[i])

        pygame.display.flip()
        clock.tick(fps)

def pantalla_fin(mensaje, puntos):
    ejecutando = True
    while ejecutando:
        fondo = pygame.image.load(fondo_final)
        fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
        pantalla.blit(fondo, (0, 0))

        dibujar_texto(mensaje, FUENTE_TITULO, BLANCO, ANCHO // 2, ALTO // 3.3)
        dibujar_texto(f"Puntaje: {puntos}", FUENTE_BOTON, BLANCO, ANCHO // 2, ALTO // 2.5)

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        boton_menu = dibujar_texto("VOLVER AL MENÚ", FUENTE_BOTON, ROJO if pygame.Rect(300, 400, 400, 50).collidepoint(mouse_pos) else BLANCO, ANCHO // 2, 420)
        boton_salir = dibujar_texto("SALIR", FUENTE_BOTON, ROJO if pygame.Rect(400, 480, 200, 50).collidepoint(mouse_pos) else BLANCO, ANCHO // 2, 500)

        if boton_menu.collidepoint(mouse_pos) and click[0]:
            pygame.time.wait(200)
            ejecutando = False
            menu_inicio()

        if boton_salir.collidepoint(mouse_pos) and click[0]:
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def inicio():
    global pantalla, FUENTE_TITULO, FUENTE_BOTON
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Space Invaders")

    FUENTE_TITULO = pygame.font.SysFont('Arial', 80)
    FUENTE_BOTON = pygame.font.SysFont('Arial', 40)

    menu_inicio()
# endregion

if __name__ == '__main__':
    inicio()