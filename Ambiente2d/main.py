from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Line import *
from Circle import *
from Triangle import *
from Rectangle import *
import numpy as np
import math

left = -10.0
right = 110.0
bottom = -10.0
top = 100.0

posicao_mouse_atual = (0.0, 0.0)

# VARIÁVEIS DE DESENHO
modo_desenho_ativo = False
vertices_poligono = []
poligonos = []
poligono = False

desenho_circulo_ativo = False
circulos_salvos = []
centro_circulo_temp = None 
raio_circulo_temp = 0.0
estado_clique_circulo = 0

desenho_triangulo_ativo = False
triangulos_salvos = []
p1_triangulo_temp = None
p2_triangulo_temp = None
estado_clique_triangulo = 0

desenho_retangulo_ativo = False
retangulos_salvos = []
p1_retangulo_temp = None
estado_clique_retangulo = 0

# VARIÁVEIS DE INTERAÇÃO
objetos_selecionados = [] 
modo_selecao_ativo = False 

MOVE_STEP = 1.0 

def unselect_all_and_clear_modes(keep_selection_mode=False): #Função de limpeza dos modos para bom funcionamento
   
    global objetos_selecionados
    global modo_desenho_ativo, desenho_circulo_ativo, desenho_triangulo_ativo, desenho_retangulo_ativo, modo_selecao_ativo
    global vertices_poligono, centro_circulo_temp, estado_clique_circulo, p1_triangulo_temp, p2_triangulo_temp, estado_clique_triangulo, p1_retangulo_temp, estado_clique_retangulo

    # Desseleciona os objetos na lista
    for obj in objetos_selecionados:
        obj.is_selected = False
    objetos_selecionados = []
        
    # Limpa estados de modo
    modo_desenho_ativo = False
    desenho_circulo_ativo = False
    desenho_triangulo_ativo = False
    desenho_retangulo_ativo = False
    
    vertices_poligono = []
    centro_circulo_temp = None
    estado_clique_circulo = 0
    p1_triangulo_temp = None
    p2_triangulo_temp = None
    estado_clique_triangulo = 0
    p1_retangulo_temp = None
    estado_clique_retangulo = 0
    
    if not keep_selection_mode:
        modo_selecao_ativo = False


def calculate_equilateral_point(p1, p2, mouse_pos): #calcula a terceira vertice do triangulo equilatero
    x1, y1 = p1; x2, y2 = p2; mx, my = mouse_pos
    mx_base = (x1 + x2) / 2.0; my_base = (y1 + y2) / 2.0
    side_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    if side_length == 0: return x1, y1
    height = side_length * (math.sqrt(3.0) / 2.0)
    dx = x2 - x1; dy = y2 - y1
    if side_length == 0: return mx_base, my_base

    ux = -dy / side_length; uy = dx / side_length

    x3_a = mx_base + height * ux; y3_a = my_base + height * uy
    x3_b = mx_base - height * ux; y3_b = my_base - height * uy

    dist_a_sq = (mx - x3_a)**2 + (my - y3_a)**2
    dist_b_sq = (mx - x3_b)**2 + (my - y3_b)**2

    if dist_a_sq < dist_b_sq:
        return x3_a, y3_a
    else:
        return x3_b, y3_b


def draw_polygon_from_vertices(vertex_list, R, G, B): #forma o desenho do poligono na tela a partir das linhas
    num_vertices = len(vertex_list)
    if num_vertices >= 2:
        for i in range(num_vertices - 1):
            x0, y0 = vertex_list[i]; x1, y1 = vertex_list[i+1]
            if hasattr(Line(0,0,0,0,0,0,0), 'draw_segment'):
                Line(x0, y0, x1, y1, R, G, B).draw_segment()
            else: Line(x0, y0, x1, y1, R, G, B).draw()
        if num_vertices >= 3:
            x_last, y_last = vertex_list[-1]; x_first, y_first = vertex_list[0]
            if hasattr(Line(0,0,0,0,0,0,0), 'draw_segment'):
                Line(x_last, y_last, x_first, y_first, R, G, B).draw_segment()
            else: Line(x_last, y_last, x_first, y_first, R, G, B).draw()


def showScreen():
    configure_visualization()
    glutSwapBuffers()

def mouse_Callback(button, state, x, y):
    global objetos_selecionados, modo_desenho_ativo, desenho_circulo_ativo, desenho_triangulo_ativo, \
       desenho_retangulo_ativo, modo_selecao_ativo, centro_circulo_temp, estado_clique_circulo, \
       circulos_salvos, raio_circulo_temp, p1_retangulo_temp, estado_clique_retangulo, retangulos_salvos, \
       p1_triangulo_temp, p2_triangulo_temp, estado_clique_triangulo, triangulos_salvos, vertices_poligono
    
    world_x, world_y = getWorldCoords(x, y)

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
        if modo_selecao_ativo:
            
            objeto_encontrado = None
            todos_objetos = retangulos_salvos + triangulos_salvos + circulos_salvos
            
            for obj in reversed(todos_objetos):
                if obj.contains_point(world_x, world_y):
                    objeto_encontrado = obj
                    break
            
            if objeto_encontrado:
                is_currently_selected = objeto_encontrado in objetos_selecionados
                
                if is_currently_selected:
                    objeto_encontrado.is_selected = False
                    objetos_selecionados.remove(objeto_encontrado)
        
                else:
                    objeto_encontrado.is_selected = True
                    objetos_selecionados.append(objeto_encontrado)
            
            elif not objetos_selecionados: # Clique no vazio
                unselect_all_and_clear_modes(keep_selection_mode=True)
            
            glutPostRedisplay()
            return 
            
        elif desenho_retangulo_ativo: 
            if estado_clique_retangulo == 0:
                p1_retangulo_temp = (world_x, world_y)
                estado_clique_retangulo = 1
            
            elif estado_clique_retangulo == 1:
                x1, y1 = p1_retangulo_temp
                x2, y2 = world_x, world_y
                
                if x1 != x2 and y1 != y2:
                    novo_retangulo = Rectangle(x1, y1, x2, y2, 1.0, 1.0, 0.0)
                    retangulos_salvos.append(novo_retangulo)
                
                p1_retangulo_temp = None
                estado_clique_retangulo = 0
                    
        elif desenho_triangulo_ativo:
            if estado_clique_triangulo == 0:
                p1_triangulo_temp = (world_x, world_y)
                estado_clique_triangulo = 1
            
            elif estado_clique_triangulo == 1:
                p2_triangulo_temp = (world_x, world_y)
                
                if p1_triangulo_temp != p2_triangulo_temp:
                    x3, y3 = calculate_equilateral_point(p1_triangulo_temp, p2_triangulo_temp, posicao_mouse_atual)
                    
                    novo_triangulo = Triangle(p1_triangulo_temp[0], p1_triangulo_temp[1], 
                                                p2_triangulo_temp[0], p2_triangulo_temp[1], 
                                                x3, y3, 1.0, 0.0, 1.0)
                    triangulos_salvos.append(novo_triangulo)
                
                p1_triangulo_temp = None
                p2_triangulo_temp = None
                estado_clique_triangulo = 0
                    
        elif desenho_circulo_ativo:
            if estado_clique_circulo == 0:
                centro_circulo_temp = (world_x, world_y)
                estado_clique_circulo = 1

            elif estado_clique_circulo == 1:
                if raio_circulo_temp > 0.5:
                    novo_circulo = Circle(centro_circulo_temp[0], centro_circulo_temp[1], raio_circulo_temp, 0.0, 0.0, 1.0)
                    circulos_salvos.append(novo_circulo)
                
                centro_circulo_temp = None
                raio_circulo_temp = 0.0
                estado_clique_circulo = 0
                    
        elif modo_desenho_ativo and poligono:
            vertices_poligono.append((world_x, world_y))

        glutPostRedisplay()
        
def motion_Callback(x, y):
    global posicao_mouse_atual, modo_desenho_ativo, desenho_retangulo_ativo, estado_clique_retangulo, p1_retangulo_temp, \
       desenho_triangulo_ativo, estado_clique_triangulo, p2_triangulo_temp, desenho_circulo_ativo, estado_clique_circulo, \
       raio_circulo_temp, centro_circulo_temp

    world_x, world_y = getWorldCoords(x, y)
    posicao_mouse_atual = (world_x, world_y) 

    # Previa do formato das formas
    if desenho_retangulo_ativo and estado_clique_retangulo == 1 and p1_retangulo_temp is not None:
        glutPostRedisplay()
        
    elif desenho_triangulo_ativo and estado_clique_triangulo == 1 and p1_triangulo_temp is not None:
        p2_triangulo_temp = posicao_mouse_atual
        glutPostRedisplay()

    elif desenho_circulo_ativo and estado_clique_circulo == 1 and centro_circulo_temp is not None:
        cx, cy = centro_circulo_temp; mx, my = posicao_mouse_atual
        distancia = math.sqrt((mx - cx)**2 + (my - cy)**2)
        raio_circulo_temp = distancia
        glutPostRedisplay()
    
    elif modo_desenho_ativo:
        glutPostRedisplay()


def configure_visualization():
    glViewport(0, 0, 500, 500)
    glClearColor(137/255, 137/255, 137/255, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    for p_vertices in poligonos:
        draw_polygon_from_vertices(p_vertices, 0.0, 0.0, 0.0)
        
    for circulo in circulos_salvos:
        circulo.draw()

    for triangulo in triangulos_salvos:
        triangulo.draw()

    for retangulo in retangulos_salvos:
        retangulo.draw()
        
    # Desenha Polígono em Construção
    num_vertices = len(vertices_poligono)
    if num_vertices >= 2:
        for i in range(num_vertices - 1):
            x0, y0 = vertices_poligono[i]; x1, y1 = vertices_poligono[i+1]
            if hasattr(Line(0,0,0,0,0,0,0), 'draw_segment'):
                Line(x0, y0, x1, y1, 1.0, 1.0, 1.0).draw_segment()
            else: Line(x0, y0, x1, y1, 1.0, 1.0, 1.0).draw()
            
    if modo_desenho_ativo and poligono and num_vertices >= 1:
        x0_provisorio, y0_provisorio = vertices_poligono[-1]
        x1_provisorio, y1_provisorio = posicao_mouse_atual
        if hasattr(Line(0,0,0,0,0,0,0), 'draw_segment'):
            Line(x0_provisorio, y0_provisorio, x1_provisorio, y1_provisorio, 1.0, 0.0, 0.0).draw_segment()
        else: Line(x0_provisorio, y0_provisorio, x1_provisorio, y1_provisorio, 1.0, 0.0, 0.0).draw()


    # Desenha Círculo em Construção
    if desenho_circulo_ativo and estado_clique_circulo == 1 and centro_circulo_temp is not None:
        cx, cy = centro_circulo_temp; raio = raio_circulo_temp
        Circle(cx, cy, raio, 0.0, 1.0, 1.0).draw()
        glPointSize(5.0); glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS); glVertex2f(cx, cy); glEnd()

    # Desenha Triângulo em Construção
    if desenho_triangulo_ativo and estado_clique_triangulo == 1 and p1_triangulo_temp is not None:
        x1, y1 = p1_triangulo_temp; x2, y2 = posicao_mouse_atual
        x3, y3 = calculate_equilateral_point(p1_triangulo_temp, (x2, y2), posicao_mouse_atual)
        R, G, B = 0.0, 1.0, 0.0
        
        if hasattr(Line(0,0,0,0,0,0,0), 'draw_segment'):
            Line(x1, y1, x2, y2, R, G, B).draw_segment()
            Line(x2, y2, x3, y3, R, G, B).draw_segment()
            Line(x3, y3, x1, y1, R, G, B).draw_segment()
        else:
            Line(x1, y1, x2, y2, R, G, B).draw(); Line(x2, y2, x3, y3, R, G, B).draw(); Line(x3, y3, x1, y1, R, G, B).draw()
        
    # Desenha Retângulo em Construção
    if desenho_retangulo_ativo and estado_clique_retangulo == 1 and p1_retangulo_temp is not None:
        x1, y1 = p1_retangulo_temp; x2, y2 = posicao_mouse_atual
        Rectangle(x1, y1, x2, y2, 0.0, 1.0, 1.0).draw()
        
    glutMouseFunc(mouse_Callback); glutMotionFunc(motion_Callback); glutPassiveMotionFunc(motion_Callback)
    
    glutSpecialFunc(specialKeys) 
    glutKeyboardFunc(onKeyboard)


def getWorldCoords(x,y):
    global left, right, bottom, top
    xr = right; xl = left; yt = top; yb = bottom; zn = 1.0; zf = -1.0
    P = [[2/(xr-xl), 0.0, 0.0, -(xr+xl)/(xr-xl)],
         [0.0, 2/(yt-yb), 0.0, -(yt+yb)/(yt-yb)],
         [0.0, 0.0, -2/(zf-zn), -(zf+zn)/(zf-zn)],
         [0.0, 0.0, 0.0, 1.0],]
    PM = np.array(P)
    invP = np.linalg.inv(PM)
    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2*(x-viewport[0]))/viewport[2] - 1
    yndc = (2*(ywin-viewport[1]))/viewport[3] - 1
    zndc = 0; wndc = 1
    vndc = np.array([xndc, yndc, zndc, wndc])
    world = np.matmul(invP, vndc)
    return world[0], world[1]


#Teclas de movimento
def specialKeys(key,x,y) -> None:
    global objetos_selecionados
    
    if not objetos_selecionados:
        return
        
    dx, dy = 0.0, 0.0
    
    if key == GLUT_KEY_LEFT:
        dx = -MOVE_STEP
    elif key == GLUT_KEY_RIGHT:
        dx = MOVE_STEP
    elif key == GLUT_KEY_UP:
        dy = MOVE_STEP
    elif key == GLUT_KEY_DOWN:
        dy = -MOVE_STEP

    if dx != 0.0 or dy != 0.0:
        for obj in objetos_selecionados:
            if hasattr(obj, 'translate'):
                obj.translate(dx, dy)

        glutPostRedisplay()


def onKeyboard(key,x,y) -> None:
    global objetos_selecionados, modo_desenho_ativo, vertices_poligono, poligono, poligonos, \
       desenho_circulo_ativo, estado_clique_circulo, centro_circulo_temp, \
       desenho_triangulo_ativo, estado_clique_triangulo, p1_triangulo_temp, \
       desenho_retangulo_ativo, estado_clique_retangulo, p1_retangulo_temp, modo_selecao_ativo

    if objetos_selecionados:
        
        # ROTAÇÃO
        if key == b'z' or key == b'Z':
            for obj in objetos_selecionados:
                if hasattr(obj, 'rotation_angle'): obj.rotation_angle += 5.0
            glutPostRedisplay(); return

        elif key == b'x' or key == b'X':
            for obj in objetos_selecionados:
                if hasattr(obj, 'rotation_angle'): obj.rotation_angle -= 5.0
            glutPostRedisplay(); return
            
        # ESCALA
        elif key == b'+':
            for obj in objetos_selecionados:
                if hasattr(obj, 'scale_factor'): obj.scale_factor *= 1.1 
            glutPostRedisplay(); return
        
        elif key == b'-':
            for obj in objetos_selecionados:
                if hasattr(obj, 'scale_factor') and obj.scale_factor > 0.1: obj.scale_factor *= 0.9 
            glutPostRedisplay(); return


    if key == b's' or key == b'S':
        # Limpa todos os modos de desenho/mover
        unselect_all_and_clear_modes(keep_selection_mode=True) 
        modo_selecao_ativo = not modo_selecao_ativo
        if modo_selecao_ativo:
            print("Modo Seleção (S): ATIVADO.")
        else:
            print("Modo Seleção (S): DESATIVADO.")
            
    # Ativação de desenho
    if key in (b'p', b'P', b'c', b'C', b't', b'T', b'r', b'R'):
        
        if (key == b'p' or key == b'P') and modo_desenho_ativo:
             if len(vertices_poligono) >= 2: poligonos.append(list(vertices_poligono))

        unselect_all_and_clear_modes(keep_selection_mode=False) 
        
        if key == b'p' or key == b'P': modo_desenho_ativo = True; poligono = True; print(b"Modo Desenho Poligono: ATIVADO.")
        elif key == b'c' or key == b'C': desenho_circulo_ativo = True; print(b"Modo Desenho Circulo: ATIVADO.")
        elif key == b't' or key == b'T': desenho_triangulo_ativo = True; print(b"Modo Desenho Triangulo: ATIVADO.")
        elif key == b'r' or key == b'R': desenho_retangulo_ativo = True; print(b"Modo Desenho Retangulo: ATIVADO.")
    
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"AMBIENTE 2D INTERATIVO") 

    glutMouseFunc(mouse_Callback)
    glutMotionFunc(motion_Callback)
    glutPassiveMotionFunc(motion_Callback)
    glutKeyboardFunc(onKeyboard)
    glutDisplayFunc(showScreen)
    glutMainLoop()

if __name__ == "__main__":
    main()