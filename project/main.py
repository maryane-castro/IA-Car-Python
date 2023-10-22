import math
import random
import sys
import os

import neat
import pygame


mapa = 'project/maps_car/maps/map3.jpg'
carro = 'project/maps_car/cars/car1.png'
config_neat = 'project/config.txt'

largura = 1920
altura = 1080
carro_X = 60
carro_Y = 60
cor_borda = (255, 255, 255, 255)  # color colisao
geracao_atual = 0 

class Agente:

    def __init__(self):
        self.agente = pygame.image.load(carro).convert()  
        self.agente = pygame.transform.scale(self.agente, (carro_X, carro_Y))
        self.agente_girado = self.agente

        self.posicao = [830, 920]  # Posição inicial
        self.angulo = 0
        self.velocidade = 0

        self.velocidade_definida = False  

        self.centro = [self.posicao[0] + carro_X / 2, self.posicao[1] + carro_Y / 2]  

        self.radares = []  
        self.radares_desenhados = []  

        self.vivo = True  

        self.distancia = 0  
        self.tempo = 0  

    def desenhar(self, tela):
        tela.blit(self.agente_girado, self.posicao)  
        self.desenhar_radar(tela)  

    def desenhar_radar(self, tela):
        for radar in self.radares:
            posicao = radar[0]
            pygame.draw.line(tela, (0, 255, 0), self.centro, posicao, 1)
            pygame.draw.circle(tela, (0, 255, 0), posicao, 5)

    def verificar_colisao(self, mapa_jogo):
        self.vivo = True
        for ponto in self.quinas:
            # Se qualquer quina tocar a cor da borda -> colisão
            if mapa_jogo.get_at((int(ponto[0]), int(ponto[1]))) == cor_borda:
                self.vivo = False
                break

    def verificar_radar(self, grau, mapa_jogo):
        comprimento = 0
        x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grau))) * comprimento)
        y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grau))) * comprimento)

        while not mapa_jogo.get_at((x, y)) == cor_borda and comprimento < 300:
            comprimento = comprimento + 1
            x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grau))) * comprimento)
            y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grau))) * comprimento)

        dist = int(math.sqrt(math.pow(x - self.centro[0], 2) + math.pow(y - self.centro[1], 2)))
        self.radares.append([(x, y), dist])

    def atualizar(self, mapa_jogo):
        if not self.velocidade_definida:
            self.velocidade = 20
            self.velocidade_definida = True


        self.agente_girado = self.rotacionar_centro(self.agente, self.angulo)
        self.posicao[0] += math.cos(math.radians(360 - self.angulo)) * self.velocidade
        self.posicao[0] = max(self.posicao[0], 20)
        self.posicao[0] = min(self.posicao[0], largura - 120)

        self.distancia += self.velocidade
        self.tempo += 1

        self.posicao[1] += math.sin(math.radians(360 - self.angulo)) * self.velocidade
        self.posicao[1] = max(self.posicao[1], 20)
        self.posicao[1] = min(self.posicao[1], largura - 120)

        self.centro = [int(self.posicao[0]) + carro_X / 2, int(self.posicao[1]) + carro_Y / 2]


        comprimento = 0.5 * carro_X
        esquerda_cima = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 30))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 30))) * comprimento]
        direita_cima = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 150))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 150))) * comprimento]
        esquerda_baixo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 210))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 210))) * comprimento]
        direita_baixo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 330))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 330))) * comprimento]
        self.quinas = [esquerda_cima, direita_cima, esquerda_baixo, direita_baixo]

        self.verificar_colisao(mapa_jogo)
        self.radares.clear()

        for d in range(-90, 120, 45):
            self.verificar_radar(d, mapa_jogo)

    def obter_dados(self):
        radares = self.radares
        valores_retorno = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radares):
            valores_retorno[i] = int(radar[1] / 30)

        return valores_retorno

    def esta_vivo(self):
        return self.vivo

    def obter_recompensa(self):
        return self.distancia / (carro_X / 2)

    def rotacionar_centro(self, imagem, angulo):
        retangulo = imagem.get_rect()
        imagem_girada = pygame.transform.rotate(imagem, angulo)
        retangulo_girado = retangulo.copy()
        retangulo_girado.center = imagem_girada.get_rect().center
        imagem_girada = imagem_girada.subsurface(retangulo_girado).copy()
        return imagem_girada


def executar_simulacao(genomas, config):
    redes = []
    carros = []

    pygame.init()
    tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)

    for i, g in genomas:
        rede = neat.nn.FeedForwardNetwork.create(g, config)
        redes.append(rede)
        g.fitness = 0

        carros.append(Agente())


    relogio = pygame.time.Clock()
    fonte_geracao = pygame.font.SysFont("Arial", 30)
    fonte_vivos = pygame.font.SysFont("Arial", 20)
    mapa_jogo = pygame.image.load(mapa).convert()  

    global geracao_atual
    geracao_atual += 1

    contador = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit(0)

        for i, carro in enumerate(carros):
            saida = redes[i].activate(carro.obter_dados())
            escolha = saida.index(max(saida))
            if escolha == 0:
                carro.angulo += 10  # Esquerda
            elif escolha == 1:
                carro.angulo -= 10  # Direita
            elif escolha == 2:
                if (carro.velocidade - 2 >= 12):
                    carro.velocidade -= 2  # Diminuir a velocidade
            else:
                carro.velocidade += 2  # Acelerar

        # Verificar se o carro ainda está vivo
        ainda_vivos = 0
        for i, carro in enumerate(carros):
            if carro.esta_vivo():
                ainda_vivos += 1
                carro.atualizar(mapa_jogo)
                genomas[i][1].fitness += carro.obter_recompensa()

        if ainda_vivos == 0:
            break

        contador += 1
        if contador == 30 * 40:  
            break

        tela.blit(mapa_jogo, (0, 0))
        for carro in carros:
            if carro.esta_vivo():
                carro.desenhar(tela)

        texto_geracao = fonte_geracao.render("Geração: " + str(geracao_atual), True, (255, 0, 0))
        retangulo_texto_geracao = texto_geracao.get_rect()
        retangulo_texto_geracao.center = (900, 450)
        tela.blit(texto_geracao, retangulo_texto_geracao)

        texto_vivos = fonte_vivos.render("Ainda Vivos: " + str(ainda_vivos), True, (255, 0, 0))
        retangulo_texto_vivos = texto_vivos.get_rect()
        retangulo_texto_vivos.center = (900, 490)
        tela.blit(texto_vivos, retangulo_texto_vivos)

        pygame.display.flip()
        relogio.tick(60)  

if __name__ == "__main__":
    caminho_config = config_neat
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)

    # Gerar população e adicionar relatórios
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    estatisticas = neat.StatisticsReporter()
    populacao.add_reporter(estatisticas)

    # Executar a simulação por um máximo de 1000 gerações
    populacao.run(executar_simulacao, 1000)
