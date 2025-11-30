from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
import time

left = -15.0
right = 15.0
bottom = -15.0
top = 15.0
w, h = 800, 800


grid_size = 30  
grid_spacing = 1.0  
mass_x, mass_y = 0.0, 0.0  
mass_strength = 1.0  
time_offset = 0.0  
animation_speed = 0.02  
wave_amplitude = 0.3  
wave_frequency = 2.0  


def configure_visualization():
    glViewport(0, 0, w, h)
    glLoadIdentity()
    
def calculate_curvature(x, y, t):

    #distância euclidiana
    dx = x - mass_x
    dy = y - mass_y
    distance = math.sqrt(dx*dx + dy*dy)
    
    if distance < 0.1:
        distance = 0.1
    
    curvature = -mass_strength / math.pow(distance,2)
    wave = wave_amplitude * math.sin(wave_frequency * distance - t * 2.0) 
    curvature += wave * math.exp(-distance * 0.1) #Curvatura atenuando com a distância
    
    return curvature


def draw_spacetime_grid():

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1.5)
    
    # Desenha linhas horizontais 
    for i in range(-grid_size, grid_size):
        if i ==0:
            continue
        glBegin(GL_LINE_STRIP)
        for j in range(-grid_size, grid_size):
            x = j * grid_spacing
            z = i * grid_spacing
            y = calculate_curvature(x, z, time_offset)
            glVertex3f(x, y, z)
        glEnd()

    # Desenha linhas verticais
    for j in range(-grid_size, grid_size):
        if j ==0:
            continue
        glBegin(GL_LINE_STRIP)
        for i in range(-grid_size, grid_size):

            x = j * grid_spacing
            z = i * grid_spacing
            y = calculate_curvature(x, z, time_offset)

            glVertex3f(x, y, z)

        glEnd()


def draw_mass():

    glColor3f(1.0, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(mass_x, -0.5, mass_y)

    quadric = gluNewQuadric()
    gluSphere(quadric, 0.8, 25, 25)
    gluDeleteQuadric(quadric)
    
    glPopMatrix()


def showScreen():
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,1)   
    configure_visualization()
    glRotatef(30, 1, 0, 0)
    glRotatef(time_offset * 10, 0, 1, 0)
    
    draw_spacetime_grid()
    draw_mass()
    
    glutSwapBuffers()

def update_animation(value):

    global time_offset
    time_offset += animation_speed
    glutPostRedisplay()
    glutTimerFunc(16, update_animation, 0)


def onReshape(width, height):

    global w, h
    w, h = width, height
    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = w / h if h != 0 else 1
    glOrtho(left * aspect_ratio, right * aspect_ratio, bottom, top, -10.0, 10.0)
 
    glMatrixMode(GL_MODELVIEW)


def onKeyboard(key, x, y):

    global mass_strength, wave_amplitude, animation_speed

    if key == b'+':
        mass_strength = min(mass_strength * 1.2, 20.0)

    elif key == b'-':
        mass_strength = max(mass_strength * 0.8, 0.5)
    
    elif key == b'w':
        wave_amplitude = min(wave_amplitude + 0.1, 1.0)
    elif key == b'e':
        wave_amplitude = max(wave_amplitude - 0.1, 0.0)

    elif key == b'a':
        animation_speed = max(animation_speed - 0.01, 0.0)
    
    elif key == b's':
        animation_speed = min(animation_speed + 0.01, 0.1)
    
    elif key == b'r':
        global mass_x, mass_y
        mass_x, mass_y = 0.0, 0.0
        mass_strength = 5.0
        wave_amplitude = 0.3
        animation_speed = 0.02

    glutPostRedisplay()


def main():

    glutInit()

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Space-Time Curvature Grid")

    glutDisplayFunc(showScreen)
    glutReshapeFunc(onReshape)
    glutKeyboardFunc(onKeyboard)
    glutTimerFunc(0, update_animation, 0)
    
    print("Controle:")
    print("  +/- : Força da massa")
    print("  W/E : Amplitude da onda")
    print("  A/S : Velocidade da animação")
    print("  R   : Reset")

    glutMainLoop()

if __name__ == "__main__":
    main()