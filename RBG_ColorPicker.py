from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np
from enum import Enum
import math
import numpy as np

left = -10.0
right = 110.0
bottom = -10.0
top = 100.0
w,h= 500,500
zoom_factor = 1
selected_R = 0.0
selected_G = 0.0
selected_B = 0.0

slider_R = 0.0
slider_B = 0.0
slider_G = 0.0

def configure_visualization():
    # estabelece a viewport
    glViewport(0, 0, 500, 500)
    glClearColor(137/255, 137/255, 137/255,1.0)
    glMatrixMode(GL_PROJECTION)
    # limpa cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # configura window (configura camera)
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def onReshape(w, h):
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    return

def showScreen():
    configure_visualization()
    drawGradient(0,80,100,10,R=1.0)
    drawGradient(0,60,100,10,G=1.0)
    drawGradient(0,40,100,10,B=1.0)
    
    #Reset Rectangle
    drawRectangle(70,0,30,10,R=0,G=0,B=0)
    #Result Rectangle
    drawRectangle(0,0,50,10,R=selected_R,G=selected_G,B=selected_B)
    #Sliders
    drawSlider(slider_R,80)
    drawSlider(slider_G,60)
    drawSlider(slider_B,40)

    glutSwapBuffers()

def sliderSelected(x, slider_x, tolerance=5):
    return abs(x - slider_x) <= tolerance

def drawSlider(x0,y0):
    if(0<=x0 <=100):
        glBegin(GL_QUADS)
        glColor3f(1, 1, 1) 
        glVertex2f(x0, y0)               # Bottom-left
        glVertex2f(x0, y0 +10)      # Top-left
        glVertex2f(x0 + 1, y0 + 10) # Top-right
        glVertex2f(x0 + 1, y0)          # Bottom-right
        glEnd()

def drawRectangle(x0, y0, width, height,R=1.0,G=1.0,B=1.0):
    glBegin(GL_QUADS)
    glColor3f(R, G, B) 
    glVertex2f(x0, y0)               # Bottom-left
    glVertex2f(x0, y0 + height)      # Top-left
    glVertex2f(x0 + width, y0 + height) # Top-right
    glVertex2f(x0 + width, y0)          # Bottom-right
    glEnd()


def drawGradient(x0, y0, width, height,R=0.0,G=0.0,B=0.0):
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.0, 0.0) # left - black
    glVertex2f(x0, y0)               # Bottom-left
    glVertex2f(x0, y0 + height)      # Top-left

    glColor3f(R, G, B) 
    glVertex2f(x0 + width, y0 + height) # Top-right
    glVertex2f(x0 + width, y0)          # Bottom-right
    glEnd()


def onKeyboard(key, x , y) -> None:
    global left, right, bottom, top, zoom_factor

    if key == b'o':
        left += zoom_factor
        right -= zoom_factor
        bottom += zoom_factor
        top -= zoom_factor
        glutPostRedisplay()

    if key == b'p':
        left -= zoom_factor
        right += zoom_factor
        bottom -= zoom_factor
        top += zoom_factor
        glutPostRedisplay()

    """Fecha com ESC."""
    if key == b'\x1b':  # ESC
        try:
            glutLeaveMainLoop()  # Funciona no FreeGLUT
        except Exception:
            os._exit(0)  # Saída imediata se glutLeaveMainLoop não existir

def mouseMotion(x,y):
    global selected_R, selected_G, selected_B, slider_G,slider_R,slider_B
    world_x, world_y = getWorldCoords(x, y)

    if(100>= world_x >=0):
        if 90 >= world_y >= 80 and sliderSelected(world_x,slider_R):
            selected_R = (world_x/100)
            slider_R = world_x
        elif 70 >= world_y >= 60 and sliderSelected(world_x,slider_G):
            selected_G = (world_x/100)
            slider_G = world_x
        elif 50 >= world_y >= 40 and sliderSelected(world_x,slider_B):
            selected_B = (world_x/100)
            slider_B = world_x

    glutPostRedisplay()
    print(f"R: {selected_R} G: {selected_G} B: {selected_B}")

def mouse_callback(button, state, x, y):

    global selected_R, selected_G, selected_B, slider_G,slider_R,slider_B
    world_x, world_y = getWorldCoords(x, y)
    print(world_x,world_y)

    if 10 >= world_y >= 0 and 100 >= world_x >=70:
        selected_R = 0.0
        selected_G = 0.0
        selected_B = 0.0
        slider_R = 0.0
        slider_B = 0.0
        slider_G = 0.0
        glutPostRedisplay()

def main():
    global wind
    # inicializa GLUT
    glutInit()
    print(chr(27))
    # dimensoes iniciais do canvas em pixels (tela)
    glutInitWindowSize(500, 500)
    # posicao inicial da minha aplicacao na tela
    glutInitWindowPosition(0, 0)
    # titulo na aplicacao
    wind = glutCreateWindow(b"RGB COLOR PICKER")
    # registro da funcao callback de redenho
    glutDisplayFunc(showScreen)
    # redesenho em estado idle
    #glutIdleFunc(showScreen)
    # registra eventos do teclado 
    glutKeyboardFunc(onKeyboard)
    #registra evento do mouse
    glutMouseFunc(mouse_callback)
    glutMotionFunc(mouseMotion)
    glutReshapeFunc(onReshape)

    # dispara o loop de eventos
    glutMainLoop()
    
def getWorldCoords(x,y):
    global left, right, bottom, top, zoom_factor
    # coordenadas do volume de visualização
    xr = right
    xl = left
    yt = top
    yb = bottom
    zn = 1.0
    zf = -1.0

    # matriz de projeçao (window + NDC)
    P =[
    [2/(xr-xl), 0.0, 0.0, -(xr+xl)/(xr-xl)],
    [0.0, 2/(yt-yb), 0.0, -(yt+yb)/(yt-yb)],
    [0.0, 0.0, -2/(zf-zn), -(zf+zn)/(zf-zn)],
    [0.0, 0.0, 0.0, 1.0],
    ]

    PM = np.array(P)

    # inversa da matriz de prozeção
    invP = np.linalg.inv(PM)

    # conversão das coordenadas do mouse para NDC
    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2*(x-viewport[0]))/viewport[2] -1
    yndc = (2*(ywin-viewport[1]))/viewport[3] -1
    zndc = 0
    wndc = 1
    vndc = np.array([xndc, yndc, zndc,wndc])

    # transformação de projeção inversa
    world = np.matmul(invP, vndc)
    #print("xd:{} yd:{} x:{:.2f} y:{:.2f}".format(x, ywin, world[0], world[1]))
    return world[0], world[1]

if __name__ == "__main__":
    main()


