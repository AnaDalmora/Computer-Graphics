from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

class Line():
    
    def __init__(self,x0,y0,x1,y1,R,G,B):
 
        self.x0 = x0; self.y0 = y0
        self.x1 = x1; self.y1 = y1
        
        self.R = R; self.G = G; self.B = B
        
        self.is_selected = False    
        self.rotation_angle = 0.0   
        self.scale_factor = 1.0     
        self.is_moving = False      
        
        #Referência para Rotação, Escala e Movimento
        self.center_x = (x0 + x1) / 2.0
        self.center_y = (y0 + y1) / 2.0

    def translate(self, dx, dy):
        self.x0 += dx
        self.y0 += dy
        self.x1 += dx
        self.y1 += dy
        
        self.center_x += dx
        self.center_y += dy

    def draw_segment(self):
        glColor3f(self.R, self.G, self.B)
        glBegin(GL_LINES)
        glVertex2f(self.x0, self.y0)
        glVertex2f(self.x1, self.y1)
        glEnd()

    def contains_point(self, px, py, tolerance=0.5): #Verifica se o ponto de seleção esta dentro de um objeto
        
        centro_x, centro_y = self.center_x, self.center_y
 
        px_t = px - centro_x; py_t = py - centro_y
        
        angle_rad = -math.radians(self.rotation_angle)
        cos_a = math.cos(angle_rad); sin_a = math.sin(angle_rad)
        px_r = px_t * cos_a - py_t * sin_a; py_r = px_t * sin_a + py_t * cos_a
        
        scale = self.scale_factor if self.scale_factor != 0 else 1.0
        px_s = px_r / scale; py_s = py_r / scale
        
        px_final = px_s + centro_x; py_final = py_s + centro_y

        x1, y1 = self.x0, self.y0
        x2, y2 = self.x1, self.y1
        
        L_sq = (x2 - x1)**2 + (y2 - y1)**2
        
        if L_sq == 0:
            distance = math.sqrt((px_final - x1)**2 + (py_final - y1)**2)
            return distance < tolerance
        
        t = ((px_final - x1) * (x2 - x1) + (py_final - y1) * (y2 - y1)) / L_sq
        
        t = max(0, min(1, t)) 
        
        closest_x = x1 + t * (x2 - x1)
        closest_y = y1 + t * (y2 - y1)
        
        distance = math.sqrt((px_final - closest_x)**2 + (py_final - closest_y)**2)
        
        return distance < tolerance

    def draw(self):
        
        glPushMatrix()

        glTranslatef(self.center_x, self.center_y, 0.0)
        
        glRotatef(self.rotation_angle, 0.0, 0.0, 1.0)
        glScalef(self.scale_factor, self.scale_factor, 1.0)
        
        glTranslatef(-self.center_x, -self.center_y, 0.0) 

        self.draw_segment()
        
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