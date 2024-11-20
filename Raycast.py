# -*- coding: utf-8 -*-
import pygame
import math

try:
    pygame.init()
except:
    print("O modulo não foi inicializado com sucesso")

    
largura = 1118
altura = 512
pygame.display.set_caption("Raycaster")
sair = True

branco = (255,255,255)
vermelho = (255,0,0)
cinza = (150,150,150)
preto = (0,0,0)

pygame.font.init()
fonte_teste = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",12)

dr = 0.0174533 # one degree in radians

# ------------ JOGADOR
class Jogador:
    def __init__(self):
        self.tamanho = 8
        self.velocidade = 0.5
        self.pos_x = 200
        self.pos_y = 200
        self.del_x = 1
        self.del_y = 1
        self.angulo = 1

#------------- MAPA 

class Mapa:
    def __init__(self, tam_x, tam_y, dimencao_pixel, matriz):
        self.tam_x = tam_x
        self.tam_y = tam_y
        self.dimencao_pixel = dimencao_pixel
        self.matriz = matriz


mapx = 8
mapy = 8
mapt = 64
mapv = [[1,1,1,1,1,1,1,1],
        [1,0,2,0,0,0,0,1],
        [1,0,2,0,0,0,0,1],
        [1,0,2,0,0,0,0,1],
        [1,0,0,0,0,0,0,1],
        [1,0,0,0,0,3,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1]]



class Reta:
    def __init__(self, j):
        self.pos_xi = j.pos_x
        self.pos_yi = j.pos_y 
        self.pos_xf = 1
        self.pos_yf = 1 
    

def pintarMapa(fundo,preto,x,y,tamanho,mapv):
    for i in range(mapx):
        for j in range(mapy):
            if mapv[j][i] >= 1:
                #pygame.draw.rect(fundo, preto, [(i * tamanho),(j * tamanho),tamanho-1,tamanho-1])
                pygame.draw.rect(fundo, preto, [(i * tamanho),(j * tamanho),tamanho,tamanho])
            else:
                #pygame.draw.rect(fundo, cinza, [(i * tamanho),(j * tamanho),tamanho-1,tamanho-1])
                pygame.draw.rect(fundo, cinza, [(i * tamanho),(j * tamanho),tamanho,tamanho])

def distance(xa,ya,xb,yb):
    return math.sqrt(((xb-xa)*(xb-xa)) + ((yb-ya)*(yb-ya)))

def drawLines(distancia,a,c,cc,fundo):
    distancia = distancia  * math.cos(a)
    lineH = (m.dimencao_pixel*320)/distancia
    largura_linha = 10
    if(lineH>320):
        lineH = 320
    line = 160- lineH/2
    if(255 - int(distancia/2)+c > 255):
        cor = 255
    else:
        if(255 - int(distancia/2)+c< 0):
            cor = 0
        else:
            cor = 255 - int(distancia/2) + c

    if(cc == 1):
        pygame.draw.rect(fundo, (cor,cor,cor), [largura-(i*largura_linha)-16,line+50,largura_linha,lineH+100])
    if(cc == 2):
        pygame.draw.rect(fundo, (0,0,cor), [largura-(i*largura_linha)-16,line+50,largura_linha,lineH + 100])
    if(cc == 3):
        pygame.draw.rect(fundo, (cor,cor,0), [largura-(i*largura_linha)-16,line+50,largura_linha,lineH+ 100])
def drawRays(j,m,i,f):
    ra = j.angulo  +(dr*30) - (dr * i)
    cor_cubo = 0
    if(ra < 0):
        ra = ra + 2 * math.pi
    if(ra > 2*math.pi):
        ra = ra - 2 * math.pi
    if(ra == 0.0):
        ra = 0.0000000001
    for r in range(1):
#-------------------------------Check Horizontal lines---------------------------------------------------------------
        dof = 0
        aTan = -1/math.tan(ra)
        if(ra>math.pi):
            ry = int(j.pos_y/m.dimencao_pixel)*m.dimencao_pixel -0.0000000001# arredondando para o valor mais proximo multiplo de 64
            rx = (j.pos_y - ry) * aTan+j.pos_x
            yo = -m.dimencao_pixel
            xo = -yo*aTan
        if(ra<math.pi):
            ry = (int(j.pos_y/m.dimencao_pixel)*m.dimencao_pixel) + m.dimencao_pixel
            rx = (j.pos_y - ry) * aTan+j.pos_x
            yo = m.dimencao_pixel
            xo = -yo*aTan
        if(ra == 0 or ra == math.pi):
            rx = j.pos_x
            ry = j.pos_y
            dof = 8
        while (dof < 8):
            mx = int(rx/m.dimencao_pixel)
            my = int(ry/m.dimencao_pixel)
            if(mx <= 0): mx = 0 #######
            if(mx >= m.tam_x): mx = m.tam_x-1 #######
            if(my <= 0): my = 0 #######
            if(my >= m.tam_x): my = m.tam_x-1 #######
            mp = my*mx
            if m.matriz[my][mx] > 0:
                cor_cubo = m.matriz[my][mx]
                dof = 8
            else:
                rx = rx + xo
                ry = ry + yo
                dof = dof + 1
            rxx = rx
            ryy = ry

#-------------------------------Check Vertical lines---------------------------------------------------------------
        dof = 0
        aTan = -math.tan(ra)
        p2 = math.pi/2
        p3 = 3*math.pi/2
        if(ra>p2 and ra <p3):
            rx = int(j.pos_x/m.dimencao_pixel)*m.dimencao_pixel -0.0000000001
            ry = (j.pos_x - rx) * aTan+j.pos_y
            xo = -m.dimencao_pixel
            yo = -xo*aTan
        if(ra<p2 or ra>p3):
            rx = (int(j.pos_x/m.dimencao_pixel)*m.dimencao_pixel) + m.dimencao_pixel
            ry = (j.pos_x - rx) * aTan+j.pos_y
            xo = m.dimencao_pixel
            yo = -xo*aTan
        if(ra == 0 or ra == math.pi):
            rx = j.pos_x
            ry = j.pos_y
            dof = 8
        while (dof < 8):
            mx = int(rx/m.dimencao_pixel)
            my = int(ry/m.dimencao_pixel)
            if(mx <= 0): mx = 0 #######
            if(mx >= m.tam_x): mx = m.tam_x-1 #######
            if(my <= 0): my = 0 #######
            if(my >= m.tam_x): my = m.tam_x-1 #######
            mp = my*mx
            if m.matriz[my][mx] > 0:
                if(cor_cubo < m.matriz[my][mx]):
                    cor_cubo = m.matriz[my][mx]
                dof = 8
            else:
                rx = rx + xo
                ry = ry + yo
                dof = dof + 1
    ca = j.angulo - ra 
    if(ca < 0):
        ca = ca + 2 * math.pi
    if(ca > 2*math.pi):
        ca = ca - 2 * math.pi

    #print(distance(j.pos_x,j.pos_y,rxx,ryy))
    #print("||",distance(j.pos_x,j.pos_y,rx,ry))
    if (distance(j.pos_x,j.pos_y,rxx,ryy) > distance(j.pos_x,j.pos_y,rx,ry)):
        cor = 10
        drawLines(distance(j.pos_x,j.pos_y,rx,ry),ca,cor,cor_cubo,f)
        return (rx,ry)
    else:
        cor = 150
        drawLines(distance(j.pos_x,j.pos_y,rxx,ryy),ca,cor,cor_cubo,f)
        return (rxx,ryy)


fundo = pygame.display.set_mode((largura,altura))

j = Jogador()
m = Mapa(mapx, mapy, mapt, mapv)
r = Reta(j)

raio = 50
clock = pygame.time.Clock()
FPS = 200
while sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        j.angulo = j.angulo - 0.01
        if j.angulo < 0:
            j.angulo = 2 * math.pi
        j.del_x = math.cos(j.angulo) 
        j.del_y = math.sin(j.angulo)
    if keys[pygame.K_d]:
        j.angulo = j.angulo + 0.01
        if j.angulo > 2 * math.pi:
            j.angulo = 0.1
        j.del_x = math.cos(j.angulo) 
        j.del_y = math.sin(j.angulo) 
    if keys[pygame.K_w]:
        j.pos_x = j.pos_x + j.del_x
        j.pos_y = j.pos_y + j.del_y
    if keys[pygame.K_s]:
        j.pos_x = j.pos_x - j.del_x
        j.pos_y = j.pos_y - j.del_y
    fundo.fill(branco)
    r = Reta(j)
    pintarMapa(fundo,preto,mapx,mapy,mapt,mapv)


    pygame.draw.circle(fundo, preto, (int(j.pos_x),int(j.pos_y)),j.tamanho)
    

    # ------------- CEU --------------------
    for i in range(20):
        pygame.draw.rect(fundo, (50+(5*i),50+(5*i),255), [altura,(12*i)+50,600,37])
    # ------------- CHÃO -------------------
    for i in range(15):
        pygame.draw.rect(fundo, (80+(2*i),40+(2*i),0), [altura,265+(12*i),600,37])
    # ------------- RAIOS ------------------
    for i in range(60):
        pygame.draw.line(fundo, vermelho, (j.pos_x,j.pos_y),drawRays(j,m,i,fundo))



    fps = clock.get_fps()
    clock.tick(FPS)

    fps_texto = "FPS: ",int(fps)
    fps_texto = str(fps_texto)
    texto = fonte_teste.render(fps_texto, 1, vermelho)
    fundo.blit(texto, (1000, 10))

    pygame.display.update()

pygame.quit()