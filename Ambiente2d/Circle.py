import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class Circle:
    
    def __init__(self, cx, cy, r, R, G, B):
        self.cx = cx; self.cy = cy; self.r = r
        self.R = R; self.G = G; self.B = B
        
        self.is_selected = False
        self.rotation_angle = 0.0
        self.scale_factor = 1.0
        self.is_moving = False

    def translate(self, dx, dy):
        self.cx += dx
        self.cy += dy

    def contains_point(self, px, py): #verifica se a area do objeto foi selecionada
        cx, cy = self.cx, self.cy
        px_t = px - cx; py_t = py - cy
        angle_rad = -math.radians(self.rotation_angle)
        cos_a = math.cos(angle_rad); sin_a = math.sin(angle_rad)
        px_r = px_t * cos_a - py_t * sin_a; py_r = px_t * sin_a + py_t * cos_a
        scale = self.scale_factor if self.scale_factor != 0 else 1.0
        px_s = px_r / scale; py_s = py_r / scale
        distance_sq = px_s**2 + py_s**2
        return distance_sq <= (self.r + 0.5)**2

    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.cx, self.cy, 0.0)
        glRotatef(self.rotation_angle, 0.0, 0.0, 1.0)
        glScalef(self.scale_factor, self.scale_factor, 1.0)
        glTranslatef(-self.cx, -self.cy, 0.0) 

        glColor3f(self.R, self.G, self.B)
        glBegin(GL_LINE_LOOP)

        for angulo in range(0, 360, 10):
            x = self.cx + self.r * math.cos(math.radians(angulo))
            y = self.cy + self.r * math.sin(math.radians(angulo))
            glVertex2f(x, y)

        glEnd()
        
        #se for selecionado desenha o quadrado amarelo no centro
        if self.is_selected:
            glPopMatrix()
            glPointSize(8.0)
            glColor3f(1.0, 1.0, 0.0) 
            glBegin(GL_POINTS)
            glVertex2f(self.cx, self.cy)
            glEnd()
            glPushMatrix()

        glPopMatrix()