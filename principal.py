import pygame
import random
from pygame.sprite import spritecollide
from pygame.version import rev

ROJO = [255, 0, 0]
VERDE = [0, 255, 0]
VERDE_S = [0,255,0]
AZUL = [0, 0, 255]
AZUL_FONDO = [115, 215, 245]
BLANCO = [255, 255, 255]
GRIS = [245, 245, 245]
GRIS_CLARO = [225, 200, 200]
GRIS_CLARO_CLARO = [197, 197, 197]
NEGRO = [0, 0, 0]
AMARILLO = [255, 255, 0]
PURPURA = [128, 0, 128]
NARANJA = [255, 165, 0]
NARANJA_CLARO = [255, 170, 156]
NARANJA_CLARO_CLARO = [255, 230, 190]
ROSA = [255, 40, 210]
ROSA_CLARO = [255, 108, 160]
ROSA_CLARO_CLARO = [255, 205, 250]

ANCHO_VENTANA = 1000
ALTO_VENTANA = 640


class jugador(pygame.sprite.Sprite):
    # Creamos el constructor
    def __init__(self, matriz):
        pygame.sprite.Sprite.__init__(self)
        self.matriz = matriz
        self.col = 0
        self.fil = 2
        self.image = self.matriz[self.fil][self.col]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.velx = 0
        self.vely = 0
        self.bloques = pygame.sprite.Group()
        self.puntos = 0
        self.bajas = 0
        self.salud = 1000
        self.salto = False
        self.abajo = False
        self.piso = False
        self.derecha = True
        self.dibujar = False
        self.disparar = False
        self.muerte = False
        self.premuerte = False
        self.sonido = pygame.mixer.Sound(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\scream2.ogg')
        self.sonido2 = pygame.mixer.Sound(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\pistol-shot.ogg')
        self.sonido3 = pygame.mixer.Sound(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\lava.ogg')
    def update(self):
        if self.muerte:
            pass
        else:
            if self.disparar:
                self.velx = 0
                self.fil = 2
                if self.derecha:
                    if self.col < 1:
                        self.col += 1
                    else:
                        self.col = 0
                else:
                    if self.col < 4:
                        self.col += 1
                    else:
                        self.col = 3
                self.disparar = False
            else:
                cte = 0.9
                if self.velx != self.vely and self.dibujar:
                    self.dibujar = False
                    self.image = self.matriz[self.fil][self.col]
                    # Seleccion de sprites
                    if self.fil == 0 and not self.premuerte:
                        if self.derecha:  # Movimiento derecha
                            if self.salto:
                                if not self.piso:
                                    if self.col < 9:
                                        self.col += 1
                                    else:
                                        self.col = 6
                                else:
                                    self.col = 0
                                    self.fil = 2
                                    self.salto = False
                            else:
                                if self.col < 5:
                                    self.col += 1
                                else:
                                    self.col = 0
                        else:  # Movimiento Izquierda Con o sin salto
                            if self.salto:
                                if not self.piso:
                                    if self.col < 19:
                                        self.col += 1
                                    else:
                                        self.col = 16
                                else:
                                    self.col = 3
                                    self.fil = 2
                                    self.salto = False
                            else:
                                if self.col < 15:
                                    self.col += 1
                                else:
                                    self.col = 10
                    elif self.premuerte:  # Cuando se muere
                        self.fil = 1
                        if self.derecha:
                            #self.col = 2
                            if self.col < 2:
                                self.col += 1
                            else:
                                #self.col = 0
                                self.muerte = True
                        else:
                            #self.col = 5
                            if self.col < 5:
                                self.col += 1
                            else:
                                #self.col = 3
                                self.muerte = True
                    elif self.fil == 2 and not self.premuerte:  # Cuando se agacha
                        if self.abajo and self.piso:
                            if self.derecha:
                                self.col = 2
                            else:
                                self.col = 5
                    elif self.fil == 3 and self.premuerte:  # Cuando cae a la lava
                        print('no entra')
                        if self.col < 2:
                            self.col += 1
                        else:
                            self.muerte = True
                elif (self.velx == self.vely or (self.vely == cte and self.velx == 0)) and self.dibujar and not self.premuerte:
                    self.salto = False
                    self.dibujar = False
                    if self.fil == 2 and self.piso:  # Cuando se agacha
                        if self.abajo:
                            if self.derecha:
                                self.col = 2
                            else:
                                self.col = 5
                        else:
                            if self.derecha:
                                if self.col < 1:
                                    self.col += 1
                                else:
                                    self.col = 0
                            else:
                                if self.col < 4:
                                    self.col += 1
                                else:
                                    self.col = 3

                if not self.piso:
                    cte = 0.9
                    self.vely += cte
                else:
                    cte = 0
                    self.vely = 0
                if not self.premuerte:
                    self.rect.x += self.velx
                    # Colision con los bloques
                    ls_col = pygame.sprite.spritecollide(self, self.bloques, False)
                    for b in ls_col:
                        if b.especial:
                            j1.sonido3.play()
                            print('hello')
                            self.fil = 3
                            self.col = 0
                            self.vely = 0
                            self.velx = 0
                            self.premuerte = True
                            self.piso = True
                            self.salud = 0
                            break
                        if self.velx > 0:
                            if self.rect.right > b.rect.left:
                                self.rect.right = b.rect.left
                                self.velx = 0
                        else:
                            if self.rect.left < b.rect.right:
                                self.rect.left = b.rect.right
                                self.velx = 0
                    self.rect.y += self.vely
                    ls_col = pygame.sprite.spritecollide(self, self.bloques, False)
                    for b in ls_col:
                        if b.especial:
                            #print('hello')
                            self.fil = 3
                            self.col = 0
                            self.vely = 0
                            self.velx = 0
                            self.premuerte = True
                            self.piso = True
                            self.salud = 0
                            break
                        if self.vely > 0:
                            if self.rect.bottom > b.rect.top:
                                self.rect.bottom = b.rect.top
                                self.vely = 0
                        else:
                            if self.rect.top < b.rect.bottom:
                                self.rect.top = b.rect.bottom
                                self.vely = 0
                        

                    if self.rect.right > ANCHO_VENTANA:
                        self.rect.right = ANCHO_VENTANA
                        self.velx = 0
                    if self.rect.left < 0:
                        self.rect.left = 0
                        self.velx = 0

                    if self.rect.bottom > ALTO_VENTANA-48:
                        self.rect.bottom = ALTO_VENTANA-48
                        self.vely = 0
                        self.piso = True
                    else:
                        self.piso = False

                    if self.rect.top < 0:
                        self.rect.top = 0
                        self.vely = 0
                        self.piso = False


class raam(pygame.sprite.Sprite):
    # Creamos el constructor
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.jugadores = pygame.sprite.Group()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.salud = 100
        self.disparar = False
        self.muerte = False
        self.start = False
        self.temp = random.randrange(60,150)
    def update(self):
        if self.start:
            if self.temp == 0:
                self.disparar = True
            else:
                self.disparar = False
                self.temp -= 1
            self.image = self.lista[self.col]
            if self.col < 2:
                self.col += 1
            else:
                self.col = 0


class enemigo_dinamico(pygame.sprite.Sprite):
    # Creamos el constructor
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0
        self.bloques = pygame.sprite.Group()
        self.salud = 100
        self.dibujar = False
        self.limiteiz = True
        self.cont = 0
        self.temp = 0
    def update(self):
        if self.dibujar:
            self.cont += 1
            self.dibujar = False
        if self.cont == 2:
            self.cont = 0
            self.image = self.lista[self.col]
            # Seleccion de sprites
            if self.limiteiz:
                # Va hacia la izquierda
                if self.col == 1:
                    self.col = 0
                else:
                    self.col = 1
            else:
                # Va hacia la derecha
                if self.col == 3:
                    self.col = 2
                else:
                    self.col = 3

        self.rect.x += self.velx
        # Colision con los bloques
        ls_col = pygame.sprite.spritecollide(self, self.bloques, False)
        for b in ls_col:
            if self.velx > 0:
                if self.rect.right > b.rect.left:
                    self.rect.right = b.rect.left
                    self.velx = 0
            else:
                if self.rect.left < b.rect.right:
                    self.rect.left = b.rect.right
                    self.velx = 0


class enemigo_estatico(pygame.sprite.Sprite):
    # Creamos el constructor
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.jugadores = pygame.sprite.Group()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.salud = 100
        self.disparar = False
        self.temp = 45
    def update(self):
        if self.temp <= 0:
            self.temp = 45
            self.disparar = True
        else:
            self.temp -= 1
            self.disparar = False
        self.image = self.lista[self.col]
        for j in self.jugadores:
            if j.rect.right < (self.rect.left - 64):
                # Dispara a la izquierda
                if not self.disparar:
                    self.col = 2
                else:
                    self.col = 3
            elif j.rect.left > (self.rect.right + 64):
                # Dispara hacia la derecha
                if not self.disparar:
                    self.col = 0
                else:
                    self.col = 1


class bloque(pygame.sprite.Sprite):
    # Creamos el constructor
    def __init__(self, posicion, dimensiones, col=ROJO):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dimensiones)
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]
        self.especial = False


class plataforma(pygame.sprite.Sprite):
    # Creamos el constructor
    def __init__(self, pos, dim, col=BLANCO):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(dim)
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velx = 0

    def update(self):
        self.rect.x += self.velx


class lluvia(pygame.sprite.Sprite):
    # Creamos el constructor
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.jugadores = pygame.sprite.Group()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.tormenta = False
        self.dibujar = False
        self.sonido = pygame.mixer.Sound(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\storm.ogg')
    def update(self):
        if self.dibujar:
            if self.tormenta:
                self.image = self.lista[self.col]
                if self.col < 3:
                    self.col += 1
                else:
                    self.col = 0
            self.dibujar = False


class bala(pygame.sprite.Sprite):
    def __init__(self, pi, pf, img):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = pi[0]
        self.rect.y = pi[1]
        self.velx = 15
        self.constantes(pi,pf)
        self.jugador = False
    def constantes(self, pi, pf):
        pi = list(pi)
        pf = list(pf)
        #Para calcular el valor de a y b
        if pf[0]-pi[0] == 0:
            pf[0]+=1
        self.a = (pf[1]-pi[1])/(pf[0]-pi[0])#Diferencia de y sobre diferencia de x
        x=pi[0]
        y=pi[1]
        self.b = y - (self.a * x)
    def update(self):
        self.rect.x += self.velx
        self.rect.y = (self.a*self.rect.x) + self.b


class balaboss(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self, pos, imbala, vel, list_expl):
        pygame.sprite.Sprite.__init__(self)
        self.imbala = imbala
        self.col = 0
        self.lista = list_expl
        self.vel = vel
        self.image = self.imbala
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.explode = False
        self.sonido = pygame.mixer.Sound(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\misil.ogg')
        self.sonido2 = pygame.mixer.Sound(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\Small-explosion.ogg')
    def update(self):
        if self.explode:
            self.vel = 0
            self.image = self.lista[self.col]
            if self.col < 5:
                self.col += 1
            else:
                self.col = 0
        else:
            self.rect.x += self.vel


class explosion(pygame.sprite.Sprite):
    #Creamos el constructor
    def __init__(self, pos, lista):
        pygame.sprite.Sprite.__init__(self)
        self.lista = lista
        self.col = 0
        self.image = self.lista[self.col]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.sonido = pygame.mixer.Sound(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\Small-explosion.ogg')
    def update(self):
        self.image = self.lista[self.col]
        if self.col<5:
            self.col += 1
        else:
            self.col = 0


if __name__ == '__main__':
    # Inicialización del juego
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA])

#------------------------------------------------------------------------------------------------------------------FONDO - FUENTES
    fondo = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Map.png')
    info_fondo = fondo.get_rect()

    ancho_fondo = info_fondo[2]
    alto_fondo = info_fondo[3]

    # Organizo el fondo antes de empezar
    f_posx = 0
    f_posy = 0
    f_vel = -10  # Se desplaza hacia la izquierda

# ------------------------------------------------------------------------------------------------------------------RECORTE DE SPRITES
    linea = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Juego1\Juego\linea.png')

# --------------------------------------------------------------------------------------------------------RECORTE JUGADOR
    matriz_jugador = []
    imagen = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\arbol.png')

    # Para la primera fila de la matriz
    aux = []
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_1.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_2.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_3.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_4.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_5.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_6.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_7.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_8.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_9.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_10.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_1a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_2a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_3a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_4a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_5a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_6a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_7a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_8a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_9a.png')
    aux.append(im_jugador_1)
    im_jugador_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\1_10a.png')
    aux.append(im_jugador_1)
    matriz_jugador.append(aux)

    # Para la segunda fila
    aux = []
    im_jugador_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\2_1.png')
    aux.append(im_jugador_2)
    im_jugador_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\2_2.png')
    aux.append(im_jugador_2)
    im_jugador_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\2_3.png')
    aux.append(im_jugador_2)
    im_jugador_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\2_1a.png')
    aux.append(im_jugador_2)
    im_jugador_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\2_2a.png')
    aux.append(im_jugador_2)
    im_jugador_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\2_3a.png')
    aux.append(im_jugador_2)
    matriz_jugador.append(aux)

    # Para la tercera fila
    aux = []
    im_jugador_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\3_1.png')
    aux.append(im_jugador_3)
    im_jugador_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\3_2.png')
    aux.append(im_jugador_3)
    im_jugador_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\3_3.png')
    aux.append(im_jugador_3)
    im_jugador_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\3_1a.png')
    aux.append(im_jugador_3)
    im_jugador_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\3_2a.png')
    aux.append(im_jugador_3)
    im_jugador_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\3_3a.png')
    aux.append(im_jugador_3)
    matriz_jugador.append(aux)

    # Para la cuerta fila
    im_jugador_4 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Personaje\4.png')
    info_img = im_jugador_4.get_rect()
    ancho_img = info_img[2]
    sp_ancho = 3
    desplazamiento_x = (155/3)
    aux = []
    for i in range(sp_ancho):
        cuadro = im_jugador_4.subsurface(
            desplazamiento_x*i, 0, desplazamiento_x, 70)
        aux.append(cuadro)
    matriz_jugador.append(aux)

# --------------------------------------------------------------------------------------------------------RECORTE ENEMIGOS
    im_enemigo_1 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\Enemigo_1.png')
    info_img = im_enemigo_1.get_rect()

    matriz_enemigos = []
    ancho_img = info_img[2]
    sp_ancho = 4
    desplazamiento_x = (277/4)
    aux = []
    for i in range(sp_ancho):
        cuadro = im_enemigo_1.subsurface(
            desplazamiento_x*i, 0, desplazamiento_x, 95)
        aux.append(cuadro)
    matriz_enemigos.append(aux)

    aux = []
    im_enemigo_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\Enemigo_2_1.png')
    aux.append(im_enemigo_2)
    im_enemigo_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\Enemigo_2_2.png')
    aux.append(im_enemigo_2)
    im_enemigo_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\Enemigo_2_1a.png')
    aux.append(im_enemigo_2)
    im_enemigo_2 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\Enemigo_2_2a.png')
    aux.append(im_enemigo_2)
    matriz_enemigos.append(aux)

    aux = []
    im_enemigo_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\RAAM1.png')
    aux.append(im_enemigo_3)
    im_enemigo_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\RAAM2.png')
    aux.append(im_enemigo_3)
    im_enemigo_3 = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\RAAM3.png')
    aux.append(im_enemigo_3)
    matriz_enemigos.append(aux)

# --------------------------------------------------------------------------------------------------------RECORTE SALUD
    im_salud = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\vida.png')
    info_img = im_salud.get_rect()

    lista_salud = []
    ancho_img = info_img[2]
    sp_alto = 5
    desplazamiento_y = (118/5)
    for i in range(sp_alto):
        cuadro = im_salud.subsurface(0, desplazamiento_y*i, 150, desplazamiento_y)
        lista_salud.append(cuadro)

# --------------------------------------------------------------------------------------------------------RECORTE LLUVIA
    lista_lluvia = []
    im_lluvia = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Rain\lluvia1.png')
    lista_lluvia.append(im_lluvia)
    im_lluvia = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Rain\lluvia2.png')
    lista_lluvia.append(im_lluvia)
    im_lluvia = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Rain\lluvia3.png')
    lista_lluvia.append(im_lluvia)
    im_lluvia = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Rain\lluvia4.png')
    lista_lluvia.append(im_lluvia)

# --------------------------------------------------------------------------------------------------------BALAS
    img_bala = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\bala.png')

    img_balaboss = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Enemigos\misil.png')

# --------------------------------------------------------------------------------------------------------RECORTE EXPLOSION
    im_ex = pygame.image.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\explo.png')
    info_img = im_ex.get_rect()

    ancho_img = info_img[2]
    alto_img = info_img[3]

    lista_ex = []
    #Cuantos recortes hay a lo ancho y a lo alto
    sp_ancho = 6
    desplazamiento_x = 300
    for i in range(sp_ancho):
        cuadro = im_ex.subsurface(desplazamiento_x*i,0,desplazamiento_x,421)
        lista_ex.append(cuadro)

# ------------------------------------------------------------------------------------------------------------------INTERFAZ BIENVENIDA
    # Fuente del mensaje que arroja
    Fuente = pygame.font.Font(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\upheavtt.ttf', 30)
    # Fuente del mensaje que arroja
    Fuente2 = pygame.font.Font(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\upheavtt.ttf', 15)

    fondo_menu = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\menu.png')

    salgo = False
    pygame.mixer.init()
    pygame.mixer.music.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\inicio.ogg' )
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
                salgo = True
            
            
            pantalla.fill(NEGRO)
            pantalla.blit(fondo_menu, [0, 0])
            ubicacion_titulo = [230, 20]
            texto_titulo = "|-|-|-|-|-|-| SPECIAL OPS |-|-|-|-|-|-|"

            ubicacion_mensaje = [200, 120]
            texto = "1. PARA INICIAR EL JUEGO OPRIME 'SPACE'"

            ubicacion_mensaje2 = [120, 200]
            texto2 = "La Humanidad está en peligro... El General RAAM tiene en su poder un arma de destrucción masiva"

            ubicacion_mensaje3 = [90, 225]
            texto3 = "Tu serás Marcus Bandit, el soldado encargado de proteger la tierra del poder mercenario del enemigo..."

            ubicacion_mensaje4 = [100, 250]
            texto4 = "Estaras solo en el campo de batalla, sin refuerzos, sin equipo medico, sin ayuda, todo depende de ti..."

            ubicacion_mensaje5 = [120, 275]
            texto5 = "Lucha con todas tus fuerzas y derrota el ejercito del General RAAM para salvar la humanidad"

            ubicacion_imagen = [600, 530]

            ubicacion_autores1 = [100, 500]
            texto_autores1 = "|*|*|*|*|*|*| SANTIAGO QUINTERO ANGARITA |*|*|*|*|*|*|"

            ubicacion_autores2 = [150, 550]
            texto_autores2 = "|*|*|*|*|*|*| SANTIAGO SOTO GRAJALES |*|*|*|*|*|*|"

            img_texto_titulo = Fuente.render(texto_titulo, True, AMARILLO)
            pantalla.blit(img_texto_titulo, ubicacion_titulo)

            img_texto = Fuente.render(texto, True, BLANCO)
            pantalla.blit(img_texto, ubicacion_mensaje)

            img_texto2 = Fuente2.render(texto2, True, BLANCO)
            pantalla.blit(img_texto2, ubicacion_mensaje2)

            img_texto3 = Fuente2.render(texto3, True, BLANCO)
            pantalla.blit(img_texto3, ubicacion_mensaje3)

            img_texto4 = Fuente2.render(texto4, True, BLANCO)
            pantalla.blit(img_texto4, ubicacion_mensaje4)

            img_texto5 = Fuente2.render(texto5, True, BLANCO)
            pantalla.blit(img_texto5, ubicacion_mensaje5)

            img_texto_autores1 = Fuente.render(texto_autores1, True, AMARILLO)
            pantalla.blit(img_texto_autores1, ubicacion_autores1)

            img_texto_autores2 = Fuente.render(texto_autores2, True, AMARILLO)
            pantalla.blit(img_texto_autores2, ubicacion_autores2)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fade = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
                    fade.fill((0,0,0))
                    for alpha in range(0, 100):
                        fade.set_alpha(alpha)
                        pantalla.blit(fade, (0,0))
                        pygame.display.update()
                        pygame.time.delay(30)
                    fin = True
                    break

        pygame.display.flip()

# ------------------------------------------------------------------------------------------------------------------INICIALIZACIÓN DEL JUEGO
    lim_der = 600
    lim_iz = 400

    jugadores = pygame.sprite.Group()
    j1 = jugador(matriz_jugador)
    jugadores.add(j1)

    plataformas = pygame.sprite.Group()  # [POSICION],[DIMENSION]
    p1 = plataforma([15.5*32, 12.5*32], [5*32, 1*32])
    plataformas.add(p1)
    p2 = plataforma([22.5*32, 9.5*32], [4*32, 1*32])
    plataformas.add(p2)
    p3 = plataforma([28.5*32, 5.5*32], [6*32, 1*32])
    plataformas.add(p3)
    p4 = plataforma([62.5*32, 14.5*32], [4*32, 1*32])
    plataformas.add(p4)
    p5 = plataforma([67.5*32, 12.5*32], [4*32, 1*32])
    plataformas.add(p5)
    p6 = plataforma([73.5*32, 10.5*32], [3*32, 1*32])
    plataformas.add(p6)
    p7 = plataforma([79.5*32, 8.5*32], [3*32, 1*32])
    plataformas.add(p7)
    p8 = plataforma([86.5*32, 11.5*32], [3*32, 1*32])
    plataformas.add(p8)

    bloques = pygame.sprite.Group()  # [POSICION],[DIMENSION]
    b1 = bloque([57*32, 18*32], [1*32, 1*32])
    bloques.add(b1)
    b2 = bloque([58*32, 17*32], [1*32, 1*32])
    bloques.add(b2)
    b3 = bloque([59*32, 16*32], [2*32, 1*32])
    bloques.add(b3)
    b4 = bloque([94*32, 16*32], [2*32, 1*32])
    bloques.add(b4)
    b5 = bloque([96*32, 17*32], [1*32, 1*32])
    bloques.add(b5)
    b6 = bloque([97*32, 18*32], [1*32, 1*32])
    bloques.add(b6)
    besp = bloque([61*32, 18*32], [33*32, 2*32])
    besp.especial = True
    bloques.add(besp)



    enemigos_est = pygame.sprite.Group()  # [POSICION],[DIMENSION]
    es1 = enemigo_estatico([59*32, 2.5*32], matriz_enemigos[1])
    enemigos_est.add(es1)
    es2 = enemigo_estatico([45*32, 0.5*32], matriz_enemigos[1])
    enemigos_est.add(es2)
    es3 = enemigo_estatico([95*32, 2.5*32], matriz_enemigos[1])
    enemigos_est.add(es3)
    es4 = enemigo_estatico([116*32, 8*32], matriz_enemigos[1])
    enemigos_est.add(es4)
    es5 = enemigo_estatico([130*32, 8*32], matriz_enemigos[1])
    enemigos_est.add(es5)
    es6 = enemigo_estatico([143*32, 8*32], matriz_enemigos[1])
    enemigos_est.add(es6)
    es7 = enemigo_estatico([156*32, 8*32], matriz_enemigos[1])
    enemigos_est.add(es7)

    bosses = pygame.sprite.Group()
    boss = raam([ancho_fondo-(14*32), 13*32], matriz_enemigos[2])
    bosses.add(boss)

    aguaceros = pygame.sprite.Group()
    l = lluvia([0,0],lista_lluvia)
    aguaceros.add(l)

    balas=pygame.sprite.Group()

    explosiones = pygame.sprite.Group()

    balasboss = pygame.sprite.Group()

    j1.bloques = bloques
    for e in enemigos_est:
        e.jugadores = jugadores

    # Apariciones del enemigo dinamico
    pos_ed1 = [55*32, 15.5*32]
    pos_ed2 = [99*32, 15.5*32]

    lim_apariciones1_fondo = -400
    lim_apariciones2_fondo = -3400

    activateboss = True

    enemigos_din = pygame.sprite.Group()

    j1.abajo = False
    j1.velx = 0
    j1.vely = 0
    j1.fil = 2
    j1.col = 0
    start = False
    arreglarlimite = False

    bandera = False
    bandera2 = False
    colision = False
    revision = False
    cont = 0
    cont_enem = 0
    end = False
    jug = False
    final = False
    llu = True

# ------------------------------------------------------------------------------------------------------------------CICLO DEL JUEGO
    fondo_pausa = pygame.image.load(
        r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\pausa.png')
    pygame.mixer.music.stop()
    pygame.mixer.init()
    pygame.mixer.music.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\track.ogg' )
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    reloj = pygame.time.Clock()
    fin = False
    while not fin:
        if salgo:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
                salgo = True
            if not j1.muerte and not j1.premuerte: #Si muere paila
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        j1.disparar = True
                        pi = j1.rect.center #Donde esta el jugador
                        pf = event.pos #Donde se encuentra el raton al momento de hacer click
                        b=bala(pi,pf,img_bala)
                        j1.sonido2.play()
                        b.jugador = True
                        if pi[0]<pf[0]:
                            b.velx = 15
                        else:
                            b.velx = -15
                        aux = list(j1.rect.center)
                        if (pf[0] > aux[0]-10) and (pf[0] < aux[0]+10):
                            if b.velx <= 0:
                                b.velx = -1
                            else:
                                b.velx = 1
                        elif (pf[0] > aux[0]-50) and (pf[0] < aux[0]+50):
                            if b.velx <= 0:
                                b.velx = -5
                            else:
                                b.velx = 5
                        else:
                            if b.velx <= 0:
                                b.velx = -10
                            else:
                                b.velx = 10
                        balas.add(b)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        fin_pausa = False
                        while not fin_pausa:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    fin_pausa = True
                                    salgo = True
                                    break
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        fin_pausa = True
                            pantalla.fill(NEGRO)
                            pantalla.blit(fondo_pausa, [0, 0])
                            ubicacion_mensaje = [250,130]
                            texto = "SALUD: " + str(j1.salud)
                            ubicacion_mensaje2 = [250,230]
                            texto2 = "KILLS: " + str(j1.bajas)
                            ubicacion_mensaje3 = [250,360]
                            texto3 = "SCORE: " + str(j1.puntos)
                            img_texto = Fuente.render(texto,True, NARANJA)
                            img_texto2 = Fuente.render(texto2,True, BLANCO)
                            img_texto3 = Fuente.render(texto3,True, VERDE_S)
                            pantalla.blit(img_texto, ubicacion_mensaje)
                            pantalla.blit(img_texto2, ubicacion_mensaje2)
                            pantalla.blit(img_texto3, ubicacion_mensaje3)
                            pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        j1.velx = 10
                        j1.fil = 0
                        j1.col = 0
                        j1.derecha = True
                    if event.key == pygame.K_a:
                        j1.velx = -10
                        j1.fil = 0
                        j1.col = 10
                        j1.derecha = False
                    if event.key == pygame.K_w:
                        j1.vely = -20
                        if j1.derecha:
                            j1.col = 6
                        else:
                            j1.col = 16
                        j1.fil = 0
                        j1.piso = False
                        j1.salto = True
                    if event.key == pygame.K_s:
                        j1.vely = 0
                        j1.velx = 0
                        j1.fil = 2
                        j1.abajo = True
                if event.type == pygame.KEYUP:
                    j1.abajo = False
                    j1.velx = 0
                    j1.vely = 0
                    j1.fil = 2
                    if j1.derecha:
                        j1.col = 0
                    else:
                        j1.col = 3

# ------------------------------------------------------------------------------------------------------------------CONTROL DE PLATAFORMAS
        if not revision:
            for pl in plataformas:
                bandera = False
                #bandera2 = False
                if ((j1.rect.right > pl.rect.left) and (j1.rect.left < pl.rect.left)) or ((j1.rect.left < pl.rect.right) and (j1.rect.right > pl.rect.right)) or ((j1.rect.right > pl.rect.left) and (j1.rect.left > pl.rect.left) and (j1.rect.right < pl.rect.right) and (j1.rect.left < pl.rect.right)):
                    aux_pl = pl
                    revision = True
        else:
            if ((j1.rect.right > aux_pl.rect.left) and (j1.rect.left < aux_pl.rect.left)) or ((j1.rect.left < aux_pl.rect.right) and (j1.rect.right > aux_pl.rect.right)) or ((j1.rect.right > aux_pl.rect.left) and (j1.rect.left >= aux_pl.rect.left) and (j1.rect.right <= aux_pl.rect.right) and (j1.rect.left < aux_pl.rect.right)):
                if aux_pl.rect.top > j1.rect.bottom:
                    bandera = True
                if bandera:
                    ls_col = pygame.sprite.spritecollide(
                        j1, plataformas, False)
                    for p in ls_col:
                        j1.rect.bottom = p.rect.top
                        j1.vely = 0
                        j1.piso = True
                        if j1.premuerte:
                            revision = False
                            break
                        #bandera2 = True
                else:
                    j1.piso = False
                    #bandera2 = False
            else:
                j1.piso = False
                bandera = False
                revision = False
        # print(revision)

# ------------------------------------------------------------------------------------------------------------------CONTROL BALAS

        #Control
        for b in balas:
            if b.rect.y < -40 or b.rect.y > ALTO_VENTANA+40 or b.rect.x < -40 or b.rect.x > ANCHO_VENTANA+40:
                b.kill()

        for b in balasboss:
            if b.rect.y < -40 or b.rect.y > ALTO_VENTANA+40 or b.rect.x < -40 or b.rect.x > ANCHO_VENTANA+40:
                b.kill()

        ls_col = pygame.sprite.spritecollide(j1,balasboss,False)
        for b in ls_col:
            j1.salud = 0
            j1.fil = 1
            j1.premuerte = True
            if j1.derecha:
                j1.col = 0
            else:
                j1.col = 3
            b.sonido.play()
            b.explode = True
            b.rect.x -= 100
            b.rect.y -= 100
            break

        for bo in bosses:
            ls_col = pygame.sprite.spritecollide(bo,balas,False)
            if not bo.muerte:
                for b in ls_col:
                    if b.jugador:
                        if bo.salud <= 5:
                            bo.disparar = False
                            bo.start = False
                            bo.muerte = True
                            b.kill()
                            j1.puntos += 100
                            j1.bajas += 1
                            ex = explosion(bo.rect.topleft, lista_ex)
                            ex.sonido.play()
                            explosiones.add(ex)
                        else:
                            bo.salud -= 5
                            b.kill()

        if boss.muerte:
            for e in enemigos_est:
                e.kill()
            for e in enemigos_din:
                e.kill()
            

        for e in enemigos_din:
            ls_col = pygame.sprite.spritecollide(e,balas,False)
            for b in ls_col:
                if b.jugador: #que la bala sea del jugador
                    if e.salud <= 50:
                        e.kill()
                        b.kill()
                        j1.bajas += 1
                        j1.puntos += 10
                    else:
                        e.salud -= 50
                        b.kill()

        for e in enemigos_est:
            ls_col = pygame.sprite.spritecollide(e,balas,False)
            for b in ls_col:
                if b.jugador: #que la bala sea del jugador
                    if e.salud <= 25:
                        e.kill()
                        b.kill()
                        j1.bajas += 1
                        j1.puntos += 20
                    else:
                        e.salud -= 25
                        b.kill()

# ------------------------------------------------------------------------------------------------------------------CREACION ENEMIGOS DINAMICOS
        #print('posf: ',f_posx,' lim: ',lim_apariciones1_fondo)
        if not boss.muerte:
            if f_posx > lim_apariciones1_fondo and f_posx <= 0:
                if cont_enem == 25:
                    #print('creado')
                    cont_enem = 0
                    e_d = enemigo_dinamico(pos_ed1, matriz_enemigos[0])
                    enemigos_din.add(e_d)
                    e_d.velx = -8
                    e_d.limiteiz = True
                else:
                    cont_enem += 1
            elif f_posx <= lim_apariciones2_fondo:
                for b in bosses:
                    if activateboss:
                        pygame.mixer.music.stop()
                        pygame.mixer.init()
                        pygame.mixer.music.load(r'D:\UNIVERSIDAD\6to Semestre\Computación Gráfica\Final\Juego\Sonidos\boss.ogg' )
                        pygame.mixer.music.set_volume(0.4)
                        pygame.mixer.music.play()
                        b.start = True
                        activateboss = False
                if cont_enem == 60:
                    #print('creado')
                    cont_enem = 0
                    e_d = enemigo_dinamico(pos_ed2, matriz_enemigos[0])
                    enemigos_din.add(e_d)
                    e_d.velx = 8
                    e_d.limiteiz = False
                else:
                    cont_enem += 1

            
        for e in enemigos_din:
            if e.rect.right < -10 and e.limiteiz:
                e.kill()
            elif e.rect.left > (ANCHO_VENTANA+10) and not e.limiteiz:
                e.kill()

# ------------------------------------------------------------------------------------------------------------------MANEJO ENEMIGOS
        #Manejo boss
        for i in bosses:
            if i.disparar:
                i.temp = random.randrange(60,150)
                vel = random.randrange(3,6)
                vel *= -1
                bb = balaboss(i.rect.topleft,img_balaboss,vel,lista_ex)
                bb.sonido.play()
                balasboss.add(bb)
        
        #Disparo del enemigo estatico
        for e in enemigos_est:
            if e.disparar:
                pi = e.rect.center #Donde esta el jugador
                pf = j1.rect.center #Donde se encuentra el raton al momento de hacer click
                b=bala(pi,pf,img_bala)
                b.jugador = False
                if pi[0]<pf[0]:
                    b.velx = 15
                else:
                    b.velx = -15
                aux = list(e.rect.center)
                if (pf[0] > aux[0]-10) and (pf[0] < aux[0]+10):
                    if b.velx <= 0:
                        b.velx = -1
                    else:
                        b.velx = 1
                elif (pf[0] > aux[0]-50) and (pf[0] < aux[0]+50):
                    if b.velx <= 0:
                        b.velx = -5
                    else:
                        b.velx = 5
                else:
                    if b.velx <= 0:
                        b.velx = -10
                    else:
                        b.velx = 10
                balas.add(b)
        
        if not j1.muerte and not end:
            #print('entro')
            ls_col = pygame.sprite.spritecollide(j1,enemigos_din,False)
            for e in ls_col:
                if e.temp <= 0:
                    if j1.salud <= 20:
                        j1.fil = 1
                        j1.premuerte = True
                        if j1.derecha:
                            j1.col = 0
                        else:
                            j1.col = 3
                        end = True
                        j1.sonido.play()
                        break
                    else:
                        j1.salud -= 20
                        j1.sonido.play()
                        e.temp = 60
                        break
                else:
                    e.temp -= 1
            #balas que impactan al jugador
            ls_col = pygame.sprite.spritecollide(j1,balas,False)
            for b in ls_col:
                if not b.jugador: #que la bala no sea del jugador
                    if j1.salud <= 20:
                        j1.fil = 1
                        j1.premuerte = True
                        if j1.derecha:
                            j1.col = 0
                        else:
                            j1.col = 3
                        end = True
                        j1.sonido.play()
                        break
                    else:
                        j1.salud -= 20
                        j1.sonido.play()
                        b.kill()
                        break

        
        #print(j1.fil,' ',j1.col,' ',j1.muerte)
        
# ------------------------------------------------------------------------------------------------------------------LLUVIA
        if f_posx < -1500 and llu:
            for l in aguaceros:
                l.sonido.play()
                l.tormenta = True
                llu = False

# ------------------------------------------------------------------------------------------------------------------CONTROL LIMITES
        if j1.rect.right > lim_der:
            j1.rect.right = lim_der
            start = True
            if f_posx > -4120:
                arreglarlimite = True
                f_posx += f_vel
                for p in plataformas:
                    p.velx = -10
                for b in bloques:  # Bug
                    b.rect.x += f_vel
                for e in enemigos_est:
                    e.rect.x += f_vel
                for boss in bosses:
                    boss.rect.x += f_vel
                pos_ed1[0] += f_vel
                pos_ed2[0] += f_vel
                for e in enemigos_din:
                    e.rect.x += f_vel
                for b in balas:
                    b.rect.x += f_vel
                for b in balasboss:
                    b.rect.x += f_vel
        else:
            arreglarlimite = False
            for p in plataformas:
                p.velx = 0

        jugadores.update()
        enemigos_est.update()
        bosses.update()
        aguaceros.update()
        enemigos_din.update()
        balas.update()
        balasboss.update()
        plataformas.update()
        explosiones.update()
        pantalla.fill(NEGRO)
        pantalla.blit(fondo, [f_posx, f_posy])
        # plataformas.draw(pantalla)
        jugadores.draw(pantalla)
        enemigos_est.draw(pantalla)
        bosses.draw(pantalla)
        enemigos_din.draw(pantalla)
        balas.draw(pantalla)
        if l.tormenta:
            aguaceros.draw(pantalla)
        bloques.draw(pantalla)
        balasboss.draw(pantalla)
        explosiones.draw(pantalla)
        reloj.tick(30)
        #print(j1.muerte,j1.salud,j1.premuerte, j1.fil, j1.col)

        if cont == 1:
            j1.dibujar = True
            l.dibujar = True
            for e in enemigos_din:
                e.dibujar = True
            cont = 0
        else:
            cont += 1

# ------------------------------------------------------------------------------------------------------------------MENSAJES
        #Salud
        
        pantalla.blit(linea, [-475,0])
        if j1.salud == 100:
            pantalla.blit(lista_salud[0], [0,10]) 
        elif j1.salud == 80:
            pantalla.blit(lista_salud[1], [0,10])
        elif j1.salud == 60:
            pantalla.blit(lista_salud[2], [0,10])
        elif j1.salud == 40:
            pantalla.blit(lista_salud[3], [0,10])
        elif j1.salud == 20:
            pantalla.blit(lista_salud[4], [0,10])
        info = "SCORE: " + str(j1.puntos)
        color_score = BLANCO
        txt_info = Fuente.render(info, True, color_score)
        pantalla.blit(txt_info, [30,35])

        if boss.start:
            info2 = "RAAM: " + str(boss.salud)
            color_score2 = GRIS_CLARO
            txt_info2 = Fuente.render(info2, True, color_score2)
            pantalla.blit(txt_info2, [30,60])


        if j1.muerte or boss.muerte:
            if j1.muerte:
                jug = True
            if boss.muerte:
                final = True
            fade = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
            fade.fill((0,0,0))
            for alpha in range(0, 100):
                fade.set_alpha(alpha)
                pantalla.blit(fade, (0,0))
                pygame.display.update()
                pygame.time.delay(30)
            fin = True
            break

        pygame.display.flip()

    fin = False
    while not fin:
        if salgo:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    fin = True
                    break
        if jug:
            pantalla.fill(NEGRO)
            ubicacion_mensaje = [250,300]
            texto = "FIN DEL JUEGO: ERES EL PERDEDOR..."
            ubicacion_mensaje2 = [290,350]
            texto2 = "¡PRESIONA ESC PARA SALIR!"
            img_texto = Fuente.render(texto,True, BLANCO)
            img_texto2 = Fuente.render(texto2,True, BLANCO)
            pantalla.blit(img_texto, ubicacion_mensaje)
            pantalla.blit(img_texto2, ubicacion_mensaje2)
            
        if final:
            pantalla.fill(NEGRO)
            ubicacion_mensaje = [250,300]
            texto = "FIN DEL JUEGO: ERES EL GANADOR..."
            ubicacion_mensaje2 = [290,350]
            texto2 = "¡PRESIONA ESC PARA SALIR!"
            ubicacion_mensaje3 = [400,400]
            texto3 = "SCORE: " + str(j1.puntos)
            ubicacion_mensaje4 = [400,435]
            texto4 = "KILLS: " + str(j1.bajas)
            img_texto = Fuente.render(texto,True, BLANCO)
            img_texto2 = Fuente.render(texto2,True, BLANCO)
            img_texto3 = Fuente.render(texto3,True, AZUL)
            img_texto4 = Fuente.render(texto4,True, NARANJA)
            pantalla.blit(img_texto, ubicacion_mensaje)
            pantalla.blit(img_texto2, ubicacion_mensaje2)
            pantalla.blit(img_texto3, ubicacion_mensaje3)
            pantalla.blit(img_texto4, ubicacion_mensaje4)
       
        pygame.display.flip()
            
    pygame.quit()
    print('Fin del programa')
