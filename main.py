import algoritmo

# Variaveis
TEMPO = 60 #int(input("Informe quanto tempo voce quer treinar(em minutos): "))
TAM_POPULACAO = 200
NUM_EXERCICIOS = 10 #int(input("Informe quantos exercicios voce quer fazer: "))
TAXA_MUTACAO = 1 # em %
TAXA_CROSSOVER = 40 # em %
NUM_GERACOES = 200

populacaoInicial = algoritmo.Populacao(TAM_POPULACAO, 0, NUM_EXERCICIOS, TEMPO)

historico = algoritmo.multipleGeneration(populacaoInicial, NUM_GERACOES, NUM_EXERCICIOS, TAM_POPULACAO, TAXA_MUTACAO, TAXA_CROSSOVER, TEMPO)

melhores = algoritmo.melhoresIndividuosDoHistorico(historico)

medias = algoritmo.mediasHistorico(historico)

algoritmo.printResultado(historico)

algoritmo.grafico(melhores, medias)