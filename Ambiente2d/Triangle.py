from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Triangle:
    
    def __init__(self, x1, y1, x2, y2, x3, y3, R, G, B):
        self.p1 = (x1, y1); self.p2 = (x2, y2); self.p3 = (x3, y3)
        self.R = R; self.G = G; self.B = B
        
        self.is_selected = False
        self.rotation_angle = 0.0
        self.scale_factor = 1.0
        self.is_moving = False 
        
        self.center_x = (x1 + x2 + x3) / 3.0
        self.center_y = (y1 + y2 + y3) / 3.0

    def translate(self, dx, dy):

        x1, y1 = self.p1; x2, y2 = self.p2; x3, y3 = self.p3
        self.p1 = (x1 + dx, y1 + dy)
        self.p2 = (x2 + dx, y2 + dy)
        self.p3 = (x3 + dx, y3 + dy)
        self.center_x += dx
        self.center_y += dy

    def sign(self, p1, p2, p3):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

    def contains_point(self, px, py): #verifica se o objeto foi selecionado

        cx, cy = self.center_x, self.center_y
        px_t = px - cx; py_t = py - cy
        angle_rad = -math.radians(self.rotation_angle)
        cos_a = math.cos(angle_rad); sin_a = math.sin(angle_rad)
        px_r = px_t * cos_a - py_t * sin_a; py_r = px_t * sin_a + py_t * cos_a
        scale = self.scale_factor if self.scale_factor != 0 else 1.0
        px_s = px_r / scale; py_s = py_r / scale
        px_final = px_s + cx; py_final = py_s + cy
        
        p = (px_final, py_final)
        s1 = self.sign(self.p1, self.p2, p); s2 = self.sign(self.p2, self.p3, p); s3 = self.sign(self.p3, self.p1, p)
        
        has_neg = (s1 < 0) or (s2 < 0) or (s3 < 0)
        has_pos = (s1 > 0) or (s2 > 0) or (s3 > 0)
        
        return not (has_neg and has_pos)

    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.center_x, self.center_y, 0.0) 
        glRotatef(self.rotation_angle, 0.0, 0.0, 1.0)
        glScalef(self.scale_factor, self.scale_factor, 1.0)
        glTranslatef(-self.center_x, -self.center_y, 0.0) 

        glColor3f(self.R, self.G, self.B)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.p1[0], self.p1[1])
        glVertex2f(self.p2[0], self.p2[1])
        glVertex2f(self.p3[0], self.p3[1])
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