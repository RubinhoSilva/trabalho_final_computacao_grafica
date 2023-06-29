import random
from math import sin, cos
from random import randint

import numpy as np
import glfw
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutInitDisplayMode
from OpenGL.raw.GLUT import GLUT_SINGLE, GLUT_RGB, GLUT_DEPTH

from draws import people, cat, house, tree, dog, ball, rain, lightning, gram, rock, grams
from utils import framebuffer_size_callback, getObj

gCamAng = 0.
gCamHeight = 1.5
vertices = None
normals = None
faces = None
dropped = 0
modeFlag = 0
distanceFromOrigin = 130

window_width = 1200
window_height = 800

mouse_x = 0
mouse_y = 0

eyex = 0
eyey = 0.3
eyez = 4.5

rotation_speed = 0.2
translation_speed = 0.02

objeto = 0
transformacao = 0
angulo = 0

# HOUSE
house_rotateX = 1.3
house_rotateY = 72
house_rotateZ = 1.3
house_translateX = 0.1
house_translateY = 0.1
house_translateZ = 0.1
house_scaleX = 1.3
house_scaleY = 1.45
house_scaleZ = 1.3

# PEOPLE
people_rotateX = 250
people_rotateY = 0
people_rotateZ = 40
people_translateX = 10
people_translateY = 1.6
people_translateZ = 2
people_scaleX = 0.35
people_scaleY = 0.5
people_scaleZ = 0.35

# CAT
cat_rotateX = -90
cat_rotateY = 0
cat_rotateZ = 115
cat_translateX = -28.5
cat_translateY = -0.5
cat_translateZ = 0
cat_scaleX = 0.30
cat_scaleY = 0.5
cat_scaleZ = 0.30

# DOG
dog_rotateX = -100
dog_rotateY = 0
dog_rotateZ = -70
dog_translateX = -17
dog_translateY = 0
dog_translateZ = 0
dog_scaleX = 0.35
dog_scaleY = 0.55
dog_scaleZ = 0.35

# BALL
ball_rotateX = 0
ball_rotateY = 0
ball_rotateZ = 0
ball_translateX = -80
ball_translateY = 0
ball_translateZ = 0
ball_scaleX = 0.09
ball_scaleY = 0.09
ball_scaleZ = 0.09

dog_vertex, dog_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/dog/objeto.obj')
people_vertex, people_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/people/objeto.obj')
cat_vertex, cat_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/cat/objeto.obj')
tree_vertex, tree_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/tree/objeto.obj')
house_vertex, house_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/house/objeto.obj')
ball_vertex, ball_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/ball/objeto.obj')
rain_vertex, rain_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/rain/objeto.obj')
lightning_vertex, lightning_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/lightning/objeto.obj')
gram_vertex, gram_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/gram/objeto.obj')
rock_vertex, rock_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/rock/objeto.obj')
grams_vertex, grams_tex_coords = getObj('/Users/rubensfilho/Desktop/UTFPR/Computação Gráfica/teste/grams/objeto.obj')


# Parâmetros da chuva
num_raindrops = 100

# Lista de gotas de chuva
raindrops = []

# Parâmetros dos raios
lightning_probability = 0.1
lightning_duration = 40
lightning_timer = 0
is_lightning = False

def initialize():
    # Configuração da chuva
    for _ in range(num_raindrops):
        x = random.uniform(-15, 15)
        y = random.uniform(0, 10)
        z = random.uniform(2, 4)
        raindrops.append((x, y, z))

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Configuração do OpenGL
    glClearColor(0.2, 0.3, 0.4, 1.0)  # Cor de fundo azul escuro
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # glEnable(GL_DEPTH_TEST)
    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)

    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogfv(GL_FOG_COLOR, [0.7, 0.7, 0.7, 1.0])
    glFogf(GL_FOG_DENSITY, 1)
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogf(GL_FOG_START, -10000)
    glFogf(GL_FOG_END, 30000.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(distanceFromOrigin, 1, 1, 10)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0, 0.2, 4.56, 0, 0, 0, 0, 1, 0)

def update_rain(dt):
    # Atualiza a posição da chuva
    for i, drop in enumerate(raindrops):
        x, y, z = drop
        y -= 0.5 * dt   # Velocidade da queda de chuva
        raindrops[i] = (x, y, z)

        # Reseta a posição da gota quando atinge o chão
        if y < 0:
            del raindrops[i]

def update_lightning(thunder_sounds):
    global is_lightning, lightning_timer

    if random.random() < lightning_probability:
        is_lightning = True
        # Reproduza o som de trovão
        thunder_sound = random.choice(thunder_sounds)
        thunder_sound.play()

        # Aguarde até o som terminar de ser reproduzido
        # pygame.time.wait(int(thunder_sound.get_length() * 1000))
        lightning_timer = lightning_duration
    else:
        is_lightning = False

    if lightning_timer > 0:
        lightning_timer -= 1

def background():
    global ball_rotateX, ball_rotateY, ball_rotateZ
    ball_rotateX += 10  # Incrementa o ângulo de rotação
    ball_rotateY += 10  # Incrementa o ângulo de rotação
    ball_rotateZ += 10  # Incrementa o ângulo de rotação

def render():

    glEnable(GL_LIGHTING)  # Habilita iluminação
    glShadeModel(GL_SMOOTH)

    # Configura as propriedades do modelo de iluminação global
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.9, 0.9, 0.9, 1.0])  # Cor ambiente global (RGB)

    rain(rain_vertex, rain_tex_coords, raindrops)

    if is_lightning:
        lightning(lightning_vertex, lightning_tex_coords)

    people(
        people_vertex, people_tex_coords,
        [people_scaleX, people_scaleY, people_scaleZ],
        [people_rotateX, people_rotateY, people_rotateZ],
        [people_translateX, people_translateY, people_translateZ]
    )
    house(
        house_vertex, house_tex_coords,
        [house_scaleX, house_scaleY, house_scaleZ],
        [house_rotateX, house_rotateY, house_rotateZ],
        [house_translateX, house_translateY, house_translateZ]
    )
    cat(
        cat_vertex, cat_tex_coords,
        [cat_scaleX, cat_scaleY, cat_scaleZ],
        [cat_rotateX, cat_rotateY, cat_rotateZ],
        [cat_translateX, cat_translateY, cat_translateZ]
    )
    dog(
        dog_vertex, dog_tex_coords,
        [dog_scaleX, dog_scaleY, dog_scaleZ],
        [dog_rotateX, dog_rotateY, dog_rotateZ],
        [dog_translateX, dog_translateY, dog_translateZ]
    )
    tree(tree_vertex, tree_tex_coords)
    ball(
        ball_vertex, ball_tex_coords,
        [ball_scaleX, ball_scaleY, ball_scaleZ],
        [ball_rotateX, ball_rotateY, ball_rotateZ],
        [ball_translateX, ball_translateY, ball_translateZ]
    )
    gram(gram_vertex, gram_tex_coords)
    rock(rock_vertex, rock_tex_coords)
    grams(grams_vertex, grams_tex_coords)

    glDisable(GL_LIGHTING)


def key_callback(window, key, scancode, action, mods):
    global objeto, transformacao, angulo

    global people_scaleX, people_scaleY, people_scaleZ
    global people_rotateX, people_rotateY, people_rotateZ
    global people_translateX, people_translateY, people_translateZ

    global house_scaleX, house_scaleY, house_scaleZ
    global house_rotateX, house_rotateY, house_rotateZ
    global house_translateX, house_translateY, house_translateZ

    global cat_scaleX, cat_scaleY, cat_scaleZ
    global cat_rotateX, cat_rotateY, cat_rotateZ
    global cat_translateX, cat_translateY, cat_translateZ

    global dog_scaleX, dog_scaleY, dog_scaleZ
    global dog_rotateX, dog_rotateY, dog_rotateZ
    global dog_translateX, dog_translateY, dog_translateZ

    if action == glfw.PRESS:
        if key == glfw.KEY_0:
            objeto = 0  # CASA
        elif key == glfw.KEY_1:
            objeto = 1  # PESSOA
        elif key == glfw.KEY_2:
            objeto = 2  # GATO
        elif key == glfw.KEY_3:
            objeto = 3  # CACHORRO
        elif key == glfw.KEY_4:
            objeto = 4  # ARVORE

        elif key == glfw.KEY_R:
            transformacao = 0  # ROTACAO
        elif key == glfw.KEY_T:
            transformacao = 1  # TRANSLACAO
        elif key == glfw.KEY_S:
            transformacao = 2  # ESCALA

        elif key == glfw.KEY_X:
            angulo = 0  # X
        elif key == glfw.KEY_Y:
            angulo = 1  # Y
        elif key == glfw.KEY_Z:
            angulo = 2  # Z


        elif key == glfw.KEY_UP:
            if objeto == 0:
                if transformacao == 0:
                    if angulo == 0:
                        house_rotateX += 10
                    elif angulo == 1:
                        house_rotateY += 10
                    elif angulo == 2:
                        house_rotateX += 10

                elif transformacao == 1:
                    if angulo == 0:
                        house_translateX += 0.1
                    elif angulo == 1:
                        house_translateY += 0.1
                    elif angulo == 2:
                        house_translateX += 0.1

                elif transformacao == 2:
                    house_scaleX += 0.1
                    house_scaleY += 0.1
                    house_scaleZ += 0.1

            elif objeto == 1:
                if transformacao == 0:
                    if angulo == 0:
                        people_rotateX += 10
                    elif angulo == 1:
                        people_rotateY += 10
                    elif angulo == 2:
                        people_rotateX += 10

                elif transformacao == 1:
                    if angulo == 0:
                        people_translateX += 0.1
                    elif angulo == 1:
                        people_translateY += 0.1
                    elif angulo == 2:
                        people_translateX += 0.1

                elif transformacao == 2:
                    people_scaleX += 0.1
                    people_scaleY += 0.1
                    people_scaleZ += 0.1

            elif objeto == 2:
                if transformacao == 0:
                    if angulo == 0:
                        cat_rotateX += 10
                    elif angulo == 1:
                        cat_rotateY += 10
                    elif angulo == 2:
                        cat_rotateX += 10

                elif transformacao == 1:
                    if angulo == 0:
                        cat_translateX += 0.1
                    elif angulo == 1:
                        cat_translateY += 0.1
                    elif angulo == 2:
                        cat_translateX += 0.1

                elif transformacao == 2:
                    cat_scaleX += 0.1
                    cat_scaleY += 0.1
                    cat_scaleZ += 0.1

            elif objeto == 3:
                if transformacao == 0:
                    if angulo == 0:
                        dog_rotateX += 10
                    elif angulo == 1:
                        dog_rotateY += 10
                    elif angulo == 2:
                        dog_rotateX += 10

                elif transformacao == 1:
                    if angulo == 0:
                        dog_translateX += 0.1
                    elif angulo == 1:
                        dog_translateY += 0.1
                    elif angulo == 2:
                        dog_translateX += 0.1

                elif transformacao == 2:
                    dog_scaleX += 0.1
                    dog_scaleY += 0.1
                    dog_scaleZ += 0.1

        elif key == glfw.KEY_DOWN:
            if objeto == 0:
                if transformacao == 0:
                    if angulo == 0:
                        house_rotateX -= 10
                    elif angulo == 1:
                        house_rotateY -= 10
                    elif angulo == 2:
                        house_rotateX -= 10

                elif transformacao == 1:
                    if angulo == 0:
                        house_translateX -= 0.1
                    elif angulo == 1:
                        house_translateY -= 0.1
                    elif angulo == 2:
                        house_translateX -= 0.1

                elif transformacao == 2:
                    house_scaleX -= 0.1
                    house_scaleY -= 0.1
                    house_scaleZ -= 0.1

            elif objeto == 1:
                if transformacao == 0:
                    if angulo == 0:
                        people_rotateX -= 10
                    elif angulo == 1:
                        people_rotateY -= 10
                    elif angulo == 2:
                        people_rotateX -= 10

                elif transformacao == 1:
                    if angulo == 0:
                        people_translateX -= 0.1
                    elif angulo == 1:
                        people_translateY -= 0.1
                    elif angulo == 2:
                        people_translateX -= 0.1

                elif transformacao == 2:
                    people_scaleX -= 0.1
                    people_scaleY -= 0.1
                    people_scaleZ -= 0.1

            elif objeto == 2:
                if transformacao == 0:
                    if angulo == 0:
                        cat_rotateX -= 10
                    elif angulo == 1:
                        cat_rotateY -= 10
                    elif angulo == 2:
                        cat_rotateX -= 10

                elif transformacao == 1:
                    if angulo == 0:
                        cat_translateX -= 0.1
                    elif angulo == 1:
                        cat_translateY -= 0.1
                    elif angulo == 2:
                        cat_translateX -= 0.1

                elif transformacao == 2:
                    cat_scaleX -= 0.1
                    cat_scaleY -= 0.1
                    cat_scaleZ -= 0.1

            elif objeto == 3:
                if transformacao == 0:
                    if angulo == 0:
                        dog_rotateX -= 10
                    elif angulo == 1:
                        dog_rotateY -= 10
                    elif angulo == 2:
                        dog_rotateX -= 10

                elif transformacao == 1:
                    if angulo == 0:
                        dog_translateX -= 0.1
                    elif angulo == 1:
                        dog_translateY -= 0.1
                    elif angulo == 2:
                        dog_translateX -= 0.1

                elif transformacao == 2:
                    dog_scaleX -= 0.1
                    dog_scaleY -= 0.1
                    dog_scaleZ -= 0.1

def timer_callback(dt, thunder_sounds):
    update_rain(dt)
    update_lightning(thunder_sounds)


def main():
    pygame.init()
    pygame.display.set_mode((window_width, window_height))  # change to the real resolution

    pygame.mixer.init()
    pygame.mixer.music.load('rain.mp3')  # Substitua pelo caminho do seu arquivo de som
    pygame.mixer.music.play(-1)  # Reproduz o som de fundo em loop infinito

    # Carregue o arquivo de som de trovão
    thunder_sounds = []
    thunder_sounds.append(pygame.mixer.Sound("lightning/sound-1.mp3"))
    thunder_sounds.append(pygame.mixer.Sound("lightning/sound-2.mp3"))
    thunder_sounds.append(pygame.mixer.Sound("lightning/sound-3.mp3"))

    # Inicializa a biblioteca GLFW
    if not glfw.init():
        return

    # Cria uma janela de exibição
    window = glfw.create_window(window_width, window_height, 'Trabalho Final', None, None)
    if not window:
        glfw.terminate()
        return

    # Define a janela de contexto atual
    glfw.make_context_current(window)

    # Define a função de retorno de chamada para eventos de teclado
    glfw.set_key_callback(window, key_callback)

    # Define a função de retorno de chamada para redimensionamento do framebuffer
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # Define o intervalo de troca de buffers verticalmente sincronizado (V-Sync)
    glfw.swap_interval(1)



    dt = 0.0
    prev_time = glfw.get_time()

    while not glfw.window_should_close(window):
        # Processa todos os eventos da janela
        glfw.poll_events()

        initialize()

        background()

        # Renderiza a cena
        render()

        current_time = glfw.get_time()
        dt = current_time - prev_time
        prev_time = current_time

        timer_callback(dt, thunder_sounds)

        # Troca os buffers da janela
        glfw.swap_buffers(window)

    # Encerra a biblioteca GLFW
    glfw.terminate()
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
