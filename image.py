import cv2 as cv
import math


class Image_calc():
    def __init__(self, caminho_img='', qnt_pontos=360):
        '''
        Inicializa a Classe
        :param caminho_img: caminho da imagem original
        :param qnt_pontos: especifica a quantidades de pontos no quadro
        :return: None
        '''
        if caminho_img != '':
            self.caminho_img = caminho_img
            self.img = cv.imread(self.caminho_img, 0)
            
            faixa_black = 170
            self.img[self.img>faixa_black] = 255
            self.img[self.img<=faixa_black] = 0
            
            self.img_copy = self.img.copy()
            self.img_copy[True] = 255
            self.altura, self.largura = self.img.shape

            self.linha_atual = 0

            self.pontos = self.get_pontos_circulo(qnt_pontos)
            self.pt_atual = self.pontos[0]

    def ar_config(self, caminho_img=str, qnt_pontos=360):
        '''
        Atualizar e resetar as configurações
        :param caminho_img: caminho da imagem original
        :param qnt_pontos: especifica a quantidades de pontos no quadro
        :return: None
        '''
        
        if caminho_img != '':
            self.caminho_img = caminho_img
            self.img = cv.imread(self.caminho_img, 0)
            
            faixa_black = 170
            self.img[self.img>faixa_black] = 255
            self.img[self.img<=faixa_black] = 0
            
            self.criar_img_copy()

            self.linha_atual = 0

            self.pontos = self.get_pontos_circulo(qnt_pontos)
            self.pt_atual = self.pontos[0]

    def criar_img_copy(self):
        '''
        Cria uma imagem com as mesmas dimensões e em branco da original
        :return: None
        '''

        self.img_copy = self.img.copy()
        self.img_copy[True] = 255
        self.altura, self.largura = self.img.shape

    def desenhar_linha_circular(self, img, largura, altura, x, y):
        '''
        Desenha uma linha do centro da imagem até algum ponto especifico.
        :param img: object Imagem a ser desenhada
        :param largura: int Largura da imagem
        :param altura: int Altura da imagem
        :param x: int eixo x da linha a ser desenhada
        :param y: int eixo y da linha a ser desenhada
        :return: None 
        '''
        cv.line(img, (int(largura/2), int(altura/2)), (x, y), (255))

    def desenhar_ponto(self, img, x, y):
        '''
        Desenha um circulo preto em determinado ponto
        :param img: object Imagem a ser desenhada
        :param x: int eixo x do ponto a ser desenhado
        :param y: int eixo y do ponto a ser desenhado
        :return: None 
        '''

        cv.circle(img,(x, y), 2, (0,0,0), -1 )

    def get_cordenada_por_argulo(self, largura=int, altura=int, angulo=int, ponto=int):
        '''
        Retorna um ponto que forma uma circunferencia, de arcordo com uma angulo qualquer
        :param largura: int Largura da imagem
        :param altura: int Altura da imagem
        :param angulo: int Angulo da direção que será colocado o ponto
        :param ponto: int Numero do ponto a ser indexado
        :return x, y, angulo, ponto
        '''

        x = int(((largura/2)*math.sin(math.radians(angulo))) + (largura/2))
        y = int(((altura/2)*math.cos(math.radians(angulo))) + (altura/2))
        return [x, y, angulo, ponto]

    def get_pontos_circulo(self, qnt_pontos=360):
        '''
        Retorna a localização de todos os pontos que formam uma circulo na imagem
        :param qnt_pontos: quantidade de pontos a ser incerida - default=360 
        :return pontos  
        '''

        max_pontos = 360
        if qnt_pontos > 360: max_pontos = qnt_pontos 

        passo = int(max_pontos/qnt_pontos)
        pontos = []

        for ponto in range(1, qnt_pontos+1):
            angulo = ponto*passo
            pontos.append(self.get_cordenada_por_argulo(self.largura, self.altura, angulo, ponto))
        return pontos

    def get_pontos_formadores_linha(self, p1=tuple, p2=tuple):
        '''
        Retorna todos os pontos que formam uma reta entre um ponto A e um B
        :param p1: tuple Ponto 1
        :param p2: tuple Ponto 2
        :return pontos
        '''
        PRECISAO = 0.1

        pontos = []

        if p1[0] > p2[0]:
            bigP = p2
            smaalP = p1
        else: 
            bigP = p1
            smaalP = p2

        if bigP[0]-smaalP[0] != 0:
            m = (bigP[1]-smaalP[1])/(bigP[0]-smaalP[0])
        else:
            m = 0
        
        n = smaalP[1] - (m*smaalP[0])

        pontos = []
        x = bigP[0]
        while x < smaalP[0]:
            x += PRECISAO
            y = (m*x)+n

            pontos.append((int(x-1), int(y-1)))

        return list(set(pontos))

    def get_maior_qnt_px_black(self, img, pnts, largura, altura):
        '''
        Retorna a quantidade de pixels pretos em uma lista de pontos
        :param img: object Imagem a ser analizada
        :param pnts: list Lista de pontos
        :param largura: int Largura da imagem
        :param altura: int Altura da imagem
        :return px_black
        '''
        px_black = 0
        for pnt in pnts:
            if 0 < pnt[0] < largura and 0 < pnt[1] < altura:
                if img[pnt[0], pnt[1]] == 0:
                    px_black += 1

        return px_black
    
    def save(self, fname='img_copy.jpg'):
        '''
        Salva a imagem
        :param fname: filename
        '''
        img_view = cv.flip(cv.rotate(self.img_copy, cv.ROTATE_90_CLOCKWISE), 1)
        cv.imwrite(fname, img_view)
    
    def img_return(self):
        '''
        Retorna a imagem original e a segunda imagem
        :return: img, img_view
        '''
                      
        img_view = cv.flip(cv.rotate(self.img_copy, cv.ROTATE_90_CLOCKWISE), 1)

        return self.img, img_view

    def etapa(self):
        '''
        Realiza uma etapa na construção da segunda figura
        :return img, img_view, msg 
        '''

        self.linha_atual += 1

        qnt_black = []
        for ponto in self.pontos:
            self.desenhar_ponto(self.img_copy, ponto[0], ponto[1])

            pts_linha = self.get_pontos_formadores_linha((self.pt_atual), (ponto[0], ponto[1]))

            qnt_black.append([self.get_maior_qnt_px_black(self.img, pts_linha, self.largura, self.altura), ponto[2], ponto[3]])

        maior = max(qnt_black)

        x, y, _, _ = self.get_cordenada_por_argulo(self.largura, self.altura, maior[1], maior[2])

        for pnt in self.get_pontos_formadores_linha((self.pt_atual), (x,y)):
            self.img.itemset((pnt), 255)

        cv.line(self.img_copy, (x,y), [self.pt_atual[0], self.pt_atual[1]], 0, 1)
    
        msg = f'{self.linha_atual} - de {self.pt_atual[3]} para {self.pontos[maior[2]-1][3]}'
        
        self.pt_atual = self.pontos[maior[2]-1]
              
        img_view = cv.flip(cv.rotate(self.img_copy, cv.ROTATE_90_CLOCKWISE), 1)

        return self.img, img_view, msg
