import random
import exercicios
import operator
import matplotlib.pyplot as plt

class Exercicio:
    def __init__(self, tipo, series, tempo):
        self.tipo = tipo
        self.series = series
        self.tempo = tempo

    def getTipo(self):
        return self.tipo
    
    def getSeries(self):
        return self.series

    def getTempo(self):
        return self.tempo

    def __str__(self):
        return '({} {}, {} min)'.format(self.tipo, self.series, self.tempo)
        
    def __repr__(self):
        return '({} {}, {} min)'.format(self.tipo, self.series, self.tempo)


class Individuo:	
    def __init__(self, gene, tempo):
        self.gene = gene
        self.fitness = 0

    def getGene(self):
        return self.gene

    def getFitness(self):
        return self.fitness

    def setFitness(self, fitness):
        self.fitness = fitness

    # Calcula o fitness do individuo
    # O cálculo leva em consideração a soma dos tempos de cada exercício, e a quantidade de exercícios repetidos
    def calcularFitness(self, tempoTreino):    
        score = 0
        tempo = 0
        repetidos = 0
        pontos = 0

        tipos = []
        for treino in self.gene:
            tipos.append(treino.getTipo())

        for t_atual, t_comparado in zip(self.gene, self.gene[1:]):
            if t_atual.getTipo() == t_comparado.getTipo():
                repetidos += 1
                    
        for alelo in self.gene:
            tempo += alelo.getTempo()

        acertos = len(self.gene) - repetidos

        distancia_tempo = (abs(tempoTreino - tempo)/tempoTreino) * 100
        
        if distancia_tempo == 0:
            pontos = 1000        
        elif distancia_tempo <= 5:
            pontos = 400
        elif distancia_tempo <= 10:
            pontos = 150
        elif distancia_tempo <= 30:
            pontos = 50
        else:
            pontos = 10
        
        score = pontos + (10 * pow(acertos, 3)) - (10 * pow(repetidos,3))
        
        self.fitness = score

    def __str__(self):
        return '{}, FITNEES= {}'.format(self.gene, self.fitness)
    
    def __repr__(self):
        return '{}, FITNESS= {}'.format(self.gene, self.fitness)


class Populacao:
    def __init__(self, tamPopulacao, geracao, numExercicios, tempo, individuos=None):
        if individuos == None:        
            self.individuos = gerarPopulacao(tamPopulacao, numExercicios, tempo)
            self.geracao = geracao
        else:
            self.individuos = individuos
            self.geracao = geracao

    def getIndividuos(self):
        return self.individuos

    def getGeracao(self):
        return self.geracao

    def avaliarPopulacao(self, tempo):
        for individuo in self.individuos:
            individuo.calcularFitness(tempo)

    def getMelhorIndividuo(self):
        melhor = self.individuos[0]
        for i in self.individuos:
            if i.getFitness() > melhor.getFitness():
                melhor = i
        return melhor

    def getPiorIndividuo(self):
        pior = self.individuos[0]
        for i in self.individuos:
            if i.getFitness() < pior.getFitness():
                pior = i
        return pior

    def getMediaFitness(self):
        soma = 0
        for i in self.individuos:
            soma += i.getFitness()
        
        media = soma / len(self.individuos)

        return media    


# Sorteia um exercicio da lista
def gerarExercicio():
    tmp = random.choice(exercicios.EXERCICIOS)    
    tmp[2] = round(random.uniform(1, 15), 2)
    # tmp[2] = random.randint(1,15)
    return Exercicio(tmp[0], tmp[1], tmp[2])


# Gera um individuo a partir do numéro de exercícios definidos
def gerarIndividuo(numExercicios, tempo):
    gene = []
    # teste = random.randint(5, 10)
    for i in range(numExercicios):
        gene.append(gerarExercicio())

    individuo = Individuo(gene, tempo)
    # individuo.setFitness(calcularFitness(individuo, tempo))

    return individuo


# Gera uma população a partir do tamanho e número de exercicios definidos
def gerarPopulacao(sizePopulation, numExercicios, tempo):
    populacao = []
    i = 0
    while i < sizePopulation:
        populacao.append(gerarIndividuo(numExercicios, tempo))
        i += 1
    return populacao


# Seleção por torneio
# Seleciona dois indivíduos aleatóriamente da população e retorna o melhor
def torneio(populacao):
    competidor1 = random.choice(populacao.getIndividuos())
    competidor2 = random.choice(populacao.getIndividuos())

    if competidor1.getFitness() > competidor2.getFitness():
        return competidor1
    else:
        return competidor2    
    

# Crossover
# Define um ponto de corte de onde vai copiar a parte correspondente do gene do pai nos filhos
def crossover(pai1, pai2, tempo):
    gene_filho1 = []
    gene_filho2 = []
    
    corte = random.randint(0, len(pai1.getGene()) - 1)

    gene_filho1.extend(pai1.getGene()[:corte])
    gene_filho1.extend(pai2.getGene()[corte:])

    gene_filho2.extend(pai2.getGene()[:corte])
    gene_filho2.extend(pai1.getGene()[corte:])

    filho1 = Individuo(gene_filho1, tempo)
    filho2 = Individuo(gene_filho2, tempo)

    return filho1, filho2


# Aplica mutação em um individuo
# A mutação consiste em sortear um exercicio aleatoriamente da lista,
# e trocar um dos exercicios do individuo por ele
def mutacao(individuo, tempo):
    novoGene = []
    novoGene.extend(individuo.getGene())
    num_Mutacoes = random.randint(1, 3)
    for i in range(num_Mutacoes):
        indice = random.randint(0, len(individuo.getGene()) - 1)    
        novoGene[indice] = gerarExercicio()

    mutante = Individuo(novoGene, tempo)

    return mutante


# Aplica mutação na população, trocando individuos por mutantes aleatoriamente, de acordo com a taxa de mutação
def mutarPopulacao(populacao, taxa_Mutacao, tempo):
    for i in range(len(populacao.getIndividuos())):
        aux = int(random.random() * 100)               
        if aux <= taxa_Mutacao:            
            mutante = mutacao(populacao.getIndividuos()[i], tempo)
            populacao.getIndividuos()[i] = mutante            
    
    return populacao


# Cria uma nova geração a partir da anterior, através de indivíduos selecionados por torneio e reprodução via crossover
def novaGeracao(populacaoAnterior, numGeracao, taxaCrossover, tempo, numExercicios):
    novosIndividuos = []
    while len(novosIndividuos) < len(populacaoAnterior.getIndividuos()):
        pai1 = torneio(populacaoAnterior)
        pai2 = torneio(populacaoAnterior)

        aux = random.random() * 100
        if aux <= taxaCrossover:
            filho1, filho2 = crossover(pai1, pai2, tempo)
            novosIndividuos.append(filho1)
            novosIndividuos.append(filho2)
        else:
            novosIndividuos.append(pai1)
            novosIndividuos.append(pai2)    
    novaPopulacao = Populacao(len(novosIndividuos), numGeracao, numExercicios, tempo, novosIndividuos)
    return novaPopulacao


def multipleGeneration(populacaoInicial, numGeracao, numExercicios, tamPopulacao, taxaMutacao, taxaCrossover, tempo):
    historico = []
    populacaoInicial.avaliarPopulacao(tempo)
    historico.append(populacaoInicial)

    for i in range(numGeracao):
        novaPopulacao = novaGeracao(historico[i], i + 1, taxaCrossover, tempo, numExercicios)
        novaPopulacao = mutarPopulacao(novaPopulacao, taxaMutacao, tempo)
        novaPopulacao.avaliarPopulacao(tempo)        
        historico.append(novaPopulacao)
        # Verifica se o melhor individuo da geração tem o fitness igual ao melhor esperado e termina o algoritmo
        if novaPopulacao.getMelhorIndividuo().getFitness() == 1000 + (10 * pow(len(novaPopulacao.getMelhorIndividuo().getGene()), 3)):
            break        
    
    return historico


#print result:
def printResultado(historico):
    melhor = historico[-1].getMelhorIndividuo()

    print('\n----------------------Melhor resposta-----------------------------\n')
    print(melhor)
    print('Num. geracao = ', len(historico) - 1)
    tempo = 0
    for t in melhor.getGene():
        tempo += t.getTempo()
    print('Tempo= ', tempo)


#analysis tools
def melhoresIndividuosDoHistorico(historico):
    melhores = []
    for populacao in historico:
        melhores.append(populacao.getMelhorIndividuo().getFitness())
    
    return melhores

def pioresIndividuosDoHistorico(historico):
    piores = []
    for populacao in historico:
        piores.append(populacao.getPiorIndividuo().getFitness())
    
    return piores


def mediasHistorico(historico):
    medias = []
    for populacao in historico:
        medias.append(populacao.getMediaFitness())

    return medias


def grafico(melhoresFitness, mediaHistorica):
    # plt.style.use(['dark_background'])    
    plt.grid()
    plt.plot(melhoresFitness, color = 'blue', linestyle = '-', label = "Melhores fitness")
    plt.plot(mediaHistorica, color = 'orange', linestyle = '-', label="Média da população")    
    plt.ylabel('Fitness')
    plt.xlabel('Geração')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()