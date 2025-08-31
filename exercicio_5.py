from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np
from enum import Enum
import math
import numpy as np

left = -10.0
right = 10.0
bottom = -10.0
top = 10.0
w,h= 500,500
zoom_factor = 1

def configure_visualization():
    # estabelece a viewport
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
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
    # limpa cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glLoadIdentity()
    configure_visualization()
    # configurando cor de desenho - vermelho
    glColor3f(1.0, 0.0, 0.0)
    # desenha eixo x
    glBegin(GL_LINES)
    glVertex2f(-8.0, 0.0)
    glVertex2f(8.0, 0.0)
    glEnd()
    # desenha eixo y
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(0.0, -8.0)
    glVertex2f(0.0, 8.0)
    glEnd()

    glutSwapBuffers()
    

def draw_circle(r,cx,cy):
    glBegin(GL_LINE_LOOP)
    for angulo in range(0,360,10):
        x = cx + r*math.cos(math.radians(angulo))
        y = cy + r*math.sin(math.radians(angulo))
        glVertex2f(x,y)
    glEnd()

def draw_triangle(p1x,p2x,p3x,p1y,p2y,p3y):
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINE_LOOP)
    glVertex(p1x,p1y)
    glVertex(p2x,p2y)
    glVertex(p3x,p3y)
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

def mouse_callback(button, state, x, y):
    world_x, world_y = getWorldCoords(x, y)
    print(f"World coordinates: ({world_x:.2f}, {world_y:.2f})")
    
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
    wind = glutCreateWindow(b"Exercicio 03")
    # registro da funcao callback de redenho
    glutDisplayFunc(showScreen)
    # redesenho em estado idle
    #glutIdleFunc(showScreen)
    # registra eventos do teclado 
    glutKeyboardFunc(onKeyboard)
    #registra evento do mouse
    glutMouseFunc(mouse_callback)

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


