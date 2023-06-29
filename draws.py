import random

import pygame as pygame

from textures import load_texture_house, load_texture_cat, load_texture_dog, load_texture_ball, load_texture_rain
from utils import draw_glDrawArray, getObj
from OpenGL.GL import *
from PIL import Image
import numpy


def people(gVertexArraySeparate, tex_coords, scale, rotate, translate):
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.9647059, 0.69411767, 0.36078432, 0.9])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.9647059, 0.69411767, 0.36078432, 0.9])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.9647059, 0.69411767, 0.36078432, 0.9])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.9647059, 0.69411767, 0.36078432, 0.9])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.9647059, 0.69411767, 0.36078432, 0.9])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.9647059, 0.69411767, 0.36078432, 0.9])
    glMaterialfv(GL_FRONT, GL_SHININESS, [128])
    glDisable(GL_LIGHT2)

    glPushMatrix()
    glScalef(*scale)
    glTranslate(*translate)
    glRotatef(rotate[0], 1, 0, 0)  # Rotação em torno do eixo X
    glRotatef(rotate[1], 0, 1, 0)  # Rotação em torno do eixo Z
    glRotatef(rotate[2], 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


def cat(gVertexArraySeparate, tex_coords, scale, rotate, translate):
    load_texture_cat()

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.88235295, 0.2784314, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.88235295, 0.2784314, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.88235295, 0.2784314, 0.0, 1.0])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.88235295, 0.2784314, 0.0, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.88235295, 0.2784314, 0.0, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.88235295, 0.2784314, 0.0, 1.0])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glPushMatrix()
    glScalef(*scale)
    glTranslate(*translate)
    glRotatef(rotate[0], 1, 0, 0)  # Rotação em torno do eixo X
    glRotatef(rotate[1], 0, 1, 0)  # Rotação em torno do eixo Z
    glRotatef(rotate[2], 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


def tree(gVertexArraySeparate, tex_coords):
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.645, 0.654, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.645, 0.654, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.45, 0.645, 0.0, 1.0])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.645, 0.654, 0.0, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.645, 0.654, 0.0, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.45, 0.645, 0.0, 1.0])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glPushMatrix()
    glScalef(0.80, 1.5, 0.80)
    glTranslate(3.35, 0, 3)
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


def dog(gVertexArraySeparate, tex_coords, scale, rotate, translate):
    load_texture_dog()

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.88235295, 0.2784314, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.88235295, 0.2784314, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.88235295, 0.2784314, 0.0, 1.0])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.88235295, 0.2784314, 0.0, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.88235295, 0.2784314, 0.0, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.88235295, 0.2784314, 0.0, 1.0])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glPushMatrix()
    glScalef(*scale)
    glTranslate(*translate)
    glRotatef(rotate[0], 1, 0, 0)  # Rotação em torno do eixo X
    glRotatef(rotate[1], 0, 1, 0)  # Rotação em torno do eixo Z
    glRotatef(rotate[2], 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


def house(gVertexArraySeparate, tex_coords, scale, rotate, translate):
    load_texture_house()

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.386928, 0.386928, 0.386928, 0.9])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.386928, 0.386928, 0.386928, 0.9])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.882353, 0.278431, 0.000000, 0.9])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0, 0, 0, 0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.386928, 0.386928, 0.386928, 0.9])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.882353, 0.278431, 0.000000, 0.9])

    glPushMatrix()
    glScalef(*scale)
    glTranslate(*translate)
    glRotatef(rotate[0], 1, 0, 0)  # Rotação em torno do eixo X
    glRotatef(rotate[1], 0, 1, 0)  # Rotação em torno do eixo Z
    glRotatef(rotate[2], 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


def ball(gVertexArraySeparate, tex_coords, scale, rotate, translate):
    load_texture_ball()

    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.500000, 0.500000, 0.500000, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.500000, 0.500000, 0.500000, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.0, 0.000000, 1.0])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.500000, 0.500000, 0.500000, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.500000, 0.500000, 0.500000, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.0, 0.0, 0.000000, 1.0])

    glPushMatrix()
    glScalef(*scale)
    glTranslate(*translate)
    glRotatef(rotate[0], 1, 0, 0)  # Rotação em torno do eixo X
    glRotatef(rotate[1], 0, 1, 0)  # Rotação em torno do eixo Z
    glRotatef(rotate[2], 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


def rain(gVertexArraySeparate, tex_coords, raindrops):
    load_texture_rain()

    # glEnable(GL_LIGHT2)
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2901961, 0.6666667, 0.80784315, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.2901961, 0.6666667, 0.80784315, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.015686275, 0.2784314, 0.36862746, 1.0])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.2901961, 0.6666667, 0.80784315, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.2901961, 0.6666667, 0.80784315, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.015686275, 0.2784314, 0.36862746, 1.0])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    for rain in raindrops:
        glPushMatrix()
        glScalef(0.80, 1.5, 0.80)
        glTranslate(*rain)
        glScalef(0.03, 0.05, 0.03)
        draw_glDrawArray(gVertexArraySeparate, tex_coords)
        glPopMatrix()


def lightning(gVertexArraySeparate, tex_coords):
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.7921569, 0.9372549, 0.44313726, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.7921569, 0.9372549, 0.44313726, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.7921569, 0.9372549, 0.44313726, 1.0])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.7921569, 0.9372549, 0.44313726, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.7921569, 0.9372549, 0.44313726, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.7921569, 0.9372549, 0.44313726, 1.0])
    glMaterialfv(GL_FRONT, GL_SHININESS, [128])

    glPushMatrix()
    glTranslate(random.uniform(-4, 4), 4, random.uniform(2, 3))
    glScalef(random.uniform(1, 2), random.uniform(1, 3), random.uniform(1, 2))
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


def gram(gVertexArraySeparate, tex_coords):
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.14117648, 0.25490198, 0.07058824, 0.6])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.14117648, 0.25490198, 0.07058824, 0.7])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.015686275, 0.35686275, 0.1254902, 0.8])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.14117648, 0.25490198, 0.07058824, 0.6])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.14117648, 0.25490198, 0.07058824, 0.7])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.015686275, 0.35686275, 0.1254902, 0.8])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glPushMatrix()
    glScalef(2, 0.4, 1.8)
    glTranslate(0, 0, 1.5)
    glRotatef(90, 1, 0, 0)  # Rotação em torno do eixo X
    glRotatef(0, 0, 1, 0)  # Rotação em torno do eixo Y
    glRotatef(100, 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()

def rock(gVertexArraySeparate, tex_coords):
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.21960784, 0.13333334, 0.023529412, 1])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.21960784, 0.13333334, 0.023529412, 1])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.4862745, 0.2627451, 0.050980393, 1])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.21960784, 0.13333334, 0.023529412, 1])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.21960784, 0.13333334, 0.023529412, 1])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.4862745, 0.2627451, 0.050980393, 1])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glPushMatrix()
    glScalef(17, 4, 8)
    glTranslate(-0.6, -2.45, 1)
    # glRotatef(-1, 1, 0, 0)  # Rotação em torno do eixo X
    # glRotatef(0, 0, 1, 0)  # Rotação em torno do eixo Y
    # glRotatef(2, 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()

def grams(gVertexArraySeparate, tex_coords):
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.05490196, 0.12156863, 0.011764706, 0.8])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.05490196, 0.12156863, 0.011764706, 0.8])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1882353, 0.1882353, 0.1882353, 0.8])

    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.05490196, 0.12156863, 0.011764706, 0.8])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.05490196, 0.12156863, 0.011764706, 0.8])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.1882353, 0.4392157, 0.011764706, 0.8])
    # glMaterialfv(GL_FRONT, GL_SHININESS, [1000.0 / 128.0])

    glPushMatrix()
    glScalef(1, 0.7, 1)
    glTranslate(3.1, 0, 1.6)
    # glRotatef(-1, 1, 0, 0)  # Rotação em torno do eixo X
    glRotatef(50, 0, 1, 0)  # Rotação em torno do eixo Y
    # glRotatef(2, 0, 0, 1)  # Rotação em torno do eixo Z
    draw_glDrawArray(gVertexArraySeparate, tex_coords)
    glPopMatrix()


