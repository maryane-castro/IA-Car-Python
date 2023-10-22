# IA-Car-PYthon

Este é um projeto de simulação de carros autônomos desenvolvido utilizando a biblioteca Python Pygame e o algoritmo NEAT (NeuroEvolution of Augmenting Topologies). O objetivo deste projeto é treinar carros autônomos para navegar por um ambiente e aprender a evitar colisões com obstáculos. Este README fornece uma visão geral do projeto, suas principais características, e como executá-lo.

## Conteúdo
1. **Introdução**
2. **Requisitos**
3. **Instruções de Uso**
4. **Estrutura do Projeto**
5. **Funcionalidades Principais**
6. **Configurações e Parâmetros**
7. **Contribuições**
8. **Licença**

## 1. Introdução
Este projeto implementa um ambiente de simulação onde carros autônomos aprendem a se movimentar em um mapa, evitando colisões com obstáculos. Os carros são controlados por redes neurais treinadas usando o algoritmo NEAT. A simulação é renderizada com a biblioteca Pygame e pode ser executada para treinar gerações sucessivas de carros até que alcancem um bom desempenho.

## 2. Requisitos
Antes de executar o projeto, certifique-se de que possui os seguintes requisitos instalados:

- Python (versão 3.x)
- Pygame (para a renderização da simulação)
- NEAT-Python (implementação do NEAT em Python)

Você pode instalar o Pygame e NEAT-Python usando o pip:
```
pip install pygame==2.5.2
pip install neat-python==0.92
```

## 3. Instruções de Uso
Para executar a simulação, siga estas etapas:

1. Clone ou faça o download do repositório.
2. Certifique-se de ter todos os requisitos instalados.
3. Execute o arquivo `main.py` a partir da linha de comando ou de um ambiente de desenvolvimento Python.

A simulação será renderizada na tela e você poderá acompanhar o progresso dos carros autônomos à medida que aprendem a navegar no ambiente.

## 4. Estrutura do Projeto
O projeto é composto por vários arquivos, mas os principais são:

- `main.py`: O arquivo de ponto de entrada para executar a simulação.
- `Agente.py`: Define a classe `Agente` que representa os carros autônomos.
- `config.txt`: O arquivo de configuração do NEAT que define os parâmetros de treinamento.

## 5. Funcionalidades Principais
O projeto inclui as seguintes funcionalidades principais:

- Carros autônomos controlados por redes neurais treinadas pelo algoritmo NEAT.
- Renderização da simulação usando a biblioteca Pygame.
- Treinamento de carros autônomos para evitar colisões com obstáculos.
- Acompanhamento das estatísticas de treinamento, como gerações e carros ainda vivos.

## 6. Configurações e Parâmetros
O arquivo `config.txt` contém as configurações do NEAT, como o número de neurônios na rede neural, as funções de ativação, as probabilidades de mutação, etc. Você pode ajustar esses parâmetros para personalizar o treinamento dos carros autônomos.





## 7. Geração de Novos Mapas
A pasta `config_base` contém imagens que podem ser usadas como modelos para a geração de novos mapas de simulação. Essas imagens servem como referências para criar ambientes de treinamento diferentes e variados, permitindo avaliar como bem os carros autônomos treinados podem lidar com variações de terreno, obstáculos, layouts de estradas e outros desafios que podem surgir em ambientes reais.

Para gerar novos mapas de simulação com base nas imagens da pasta `config_base`, você pode implementar funcionalidades adicionais no projeto que carregam essas imagens e as usam como base para criar cenários de treinamento personalizados.

Lembre-se de manter as imagens na pasta `config_base` organizadas e nomeadas de forma adequada para facilitar a referência e a geração de novos mapas.

Sinta-se à vontade para explorar essa funcionalidade e personalizar o projeto de acordo com suas necessidades.


## 8. Contribuições

Contribuição do canal NeuralNine



## 9. Licença
Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para obter mais informações sobre os termos e condições.
