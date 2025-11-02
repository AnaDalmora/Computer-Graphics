from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Rectangle:
    
    def __init__(self, x1, y1, x2, y2, R, G, B):

        self.x_min = min(x1, x2); self.x_max = max(x1, x2)
        self.y_min = min(y1, y2); self.y_max = max(y1, y2)
        self.x1, self.y1 = x1, y1; self.x2, self.y2 = x2, y2
        self.R = R; self.G = G; self.B = B
        
        self.is_selected = False
        self.rotation_angle = 0.0
        self.scale_factor = 1.0
        self.is_moving = False 
        
        self.center_x = (self.x_min + self.x_max) / 2.0
        self.center_y = (self.y_min + self.y_max) / 2.0

    def translate(self, dx, dy):
        self.x1 += dx; self.y1 += dy
        self.x2 += dx; self.y2 += dy
        self.x_min += dx; self.x_max += dx
        self.y_min += dy; self.y_max += dy
        self.center_x += dx
        self.center_y += dy
        
    def contains_point(self, px, py): #verifica se o objeto foi selecionado
        cx, cy = self.center_x, self.center_y
        px_t = px - cx; py_t = py - cy
        angle_rad = -math.radians(self.rotation_angle)
        cos_a = math.cos(angle_rad); sin_a = math.sin(angle_rad)
        px_r = px_t * cos_a - py_t * sin_a; py_r = px_t * sin_a + py_t * cos_a
        scale = self.scale_factor if self.scale_factor != 0 else 1.0
        px_s = px_r / scale; py_s = py_r / scale
        px_final = px_s + cx; py_final = py_s + cy
        
        return (self.x_min <= px_final <= self.x_max) and \
               (self.y_min <= py_final <= self.y_max)

    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.center_x, self.center_y, 0.0) 
        glRotatef(self.rotation_angle, 0.0, 0.0, 1.0)
        glScalef(self.scale_factor, self.scale_factor, 1.0)
        glTranslatef(-self.center_x, -self.center_y, 0.0) 

        glColor3f(self.R, self.G, self.B)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x_min, self.y_min)
        glVertex2f(self.x_max, self.y_min)
        glVertex2f(self.x_max, self.y_max)
        glVertex2f(self.x_min, self.y_max)
        glEnd()
        #se for selecionado desenha o quadrado amarelo no centro
        if self.is_selected:
            glPopMatrix()
            glPointSize(8.0)
            glColor3f(1.0, 1.0, 0.0)
            glBegin(GL_POINTS)
            glVertex2f(self.center_x, self.center_y)
            glEnd()
            glPushMatrix()

        glPopMatrix()