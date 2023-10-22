import math
import random
import sys
import os

import neat
import pygame


mapa = 'project/maps_car/maps/map2.jpg'
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
        # Carregar agente do carro e girar
        self.agente = pygame.image.load(carro).convert()  # Converter para otimizar
        self.agente = pygame.transform.scale(self.agente, (carro_X, carro_Y))
        self.agente_girado = self.agente

        self.posicao = [830, 920]  # Posição inicial
        self.angulo = 0
        self.velocidade = 0

        self.velocidade_definida = False  # Sinalizador para velocidade padrão posteriormente

        self.centro = [self.posicao[0] + carro_X / 2, self.posicao[1] + carro_Y / 2]  # Calcular o centro

        self.radares = []  # Lista de sensores / radares
        self.radares_desenhados = []  # Radares a serem desenhados

        self.vivo = True  # Booleano para verificar se o carro colidiu

        self.distancia = 0  # Distância percorrida
        self.tempo = 0  # Tempo decorrido

    def desenhar(self, tela):
        tela.blit(self.agente_girado, self.posicao)  # Desenhar agente
        self.desenhar_radar(tela)  # OPCIONAL PARA SENSORES

    def desenhar_radar(self, tela):
        # Opcionalmente, desenhe todos os sensores / radares
        for radar in self.radares:
            posicao = radar[0]
            pygame.draw.line(tela, (0, 255, 0), self.centro, posicao, 1)
            pygame.draw.circle(tela, (0, 255, 0), posicao, 5)

    def verificar_colisao(self, mapa_jogo):
        self.vivo = True
        for ponto in self.quinas:
            # Se qualquer quina tocar a cor da borda -> colisão
            # Supõe retângulo
            if mapa_jogo.get_at((int(ponto[0]), int(ponto[1]))) == cor_borda:
                self.vivo = False
                break

    def verificar_radar(self, grau, mapa_jogo):
        comprimento = 0
        x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grau))) * comprimento)
        y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grau))) * comprimento)

        # Enquanto não atingirmos a cor_borda E comprimento < 300 (apenas um máximo) -> vá cada vez mais longe
        while not mapa_jogo.get_at((x, y)) == cor_borda and comprimento < 300:
            comprimento = comprimento + 1
            x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grau))) * comprimento)
            y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grau))) * comprimento)

        # Calcular a distância até a borda e adicionar à lista de radares
        dist = int(math.sqrt(math.pow(x - self.centro[0], 2) + math.pow(y - self.centro[1], 2)))
        self.radares.append([(x, y), dist])

    def atualizar(self, mapa_jogo):
        # Define a velocidade para 20 pela primeira vez
        # Apenas quando tiver 4 nós de saída com Acelerar e Desacelerar
        if not self.velocidade_definida:
            self.velocidade = 20
            self.velocidade_definida = True

        # Obter agente girado e mover na direção X correta
        # Não deixe o carro chegar mais perto do que 20px da borda
        self.agente_girado = self.rotacionar_centro(self.agente, self.angulo)
        self.posicao[0] += math.cos(math.radians(360 - self.angulo)) * self.velocidade
        self.posicao[0] = max(self.posicao[0], 20)
        self.posicao[0] = min(self.posicao[0], largura - 120)

        # Aumentar distância e tempo
        self.distancia += self.velocidade
        self.tempo += 1

        # Mesma coisa para a posição Y
        self.posicao[1] += math.sin(math.radians(360 - self.angulo)) * self.velocidade
        self.posicao[1] = max(self.posicao[1], 20)
        self.posicao[1] = min(self.posicao[1], largura - 120)

        # Calcular novo centro
        self.centro = [int(self.posicao[0]) + carro_X / 2, int(self.posicao[1]) + carro_Y / 2]

        # Calcular quatro quinas
        # O comprimento é metade do lado
        comprimento = 0.5 * carro_X
        esquerda_cima = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 30))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 30))) * comprimento]
        direita_cima = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 150))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 150))) * comprimento]
        esquerda_baixo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 210))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 210))) * comprimento]
        direita_baixo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 330))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 330))) * comprimento]
        self.quinas = [esquerda_cima, direita_cima, esquerda_baixo, direita_baixo]

        # Verificar colisões e limpar radares
        self.verificar_colisao(mapa_jogo)
        self.radares.clear()

        # De -90 a 120 com passo de 45, verificar radar
        for d in range(-90, 120, 45):
            self.verificar_radar(d, mapa_jogo)

    def obter_dados(self):
        # Obter distâncias até a borda
        radares = self.radares
        valores_retorno = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radares):
            valores_retorno[i] = int(radar[1] / 30)

        return valores_retorno

    def esta_vivo(self):
        # Função básica para verificar se o carro está vivo
        return self.vivo

    def obter_recompensa(self):
        # Calcular recompensa (talvez mudar?)
        # return self.distancia / 50.0
        return self.distancia / (carro_X / 2)

    def rotacionar_centro(self, imagem, angulo):
        # Girar o retângulo
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

    # Para todos os genomas passados, criar uma nova rede neural
    for i, g in genomas:
        rede = neat.nn.FeedForwardNetwork.create(g, config)
        redes.append(rede)
        g.fitness = 0

        carros.append(Agente())

    # Configurações do relógio
    # Configurações da fonte e carregamento do mapa
    relogio = pygame.time.Clock()
    fonte_geracao = pygame.font.SysFont("Arial", 30)
    fonte_vivos = pygame.font.SysFont("Arial", 20)
    mapa_jogo = pygame.image.load(mapa).convert()  # Converter para otimizar

    global geracao_atual
    geracao_atual += 1

    # Contador simples para limitar o tempo aproximadamente (não é uma boa prática)
    contador = 0

    while True:
        # Sair no evento de saída
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit(0)

        # Para cada carro, obtenha a ação que ele toma
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
        # Aumentar a aptidão se sim e quebrar o loop se não
        ainda_vivos = 0
        for i, carro in enumerate(carros):
            if carro.esta_vivo():
                ainda_vivos += 1
                carro.atualizar(mapa_jogo)
                genomas[i][1].fitness += carro.obter_recompensa()

        if ainda_vivos == 0:
            break

        contador += 1
        if contador == 30 * 40:  # Parar após cerca de 20 segundos
            break

        # Desenhar o mapa e todos os carros que estão vivos
        tela.blit(mapa_jogo, (0, 0))
        for carro in carros:
            if carro.esta_vivo():
                carro.desenhar(tela)

        # Exibir informações
        texto_geracao = fonte_geracao.render("Geração: " + str(geracao_atual), True, (255, 0, 0))
        retangulo_texto_geracao = texto_geracao.get_rect()
        retangulo_texto_geracao.center = (900, 450)
        tela.blit(texto_geracao, retangulo_texto_geracao)

        texto_vivos = fonte_vivos.render("Ainda Vivos: " + str(ainda_vivos), True, (255, 0, 0))
        retangulo_texto_vivos = texto_vivos.get_rect()
        retangulo_texto_vivos.center = (900, 490)
        tela.blit(texto_vivos, retangulo_texto_vivos)

        pygame.display.flip()
        relogio.tick(60)  # 60 FPS

if __name__ == "__main__":
    caminho_config = config_neat
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)

    # Criar população e adicionar relatórios
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    estatisticas = neat.StatisticsReporter()
    populacao.add_reporter(estatisticas)

    # Executar a simulação por um máximo de 1000 gerações
    populacao.run(executar_simulacao, 1000)
