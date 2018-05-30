# Algoritmo genético
Modelagem e implementação de um algoritmo genético para formatação de treinos físicos.
# Problema
Todos que fazem exercícios precisam fazer uma sequência em um certo período de tempo. O algoritmo precisa capturar o tempo de treino e “Encaixar” os tipos de exercícios e suas séries de modo a ocupar melhor o tempo. Considere no mínimo 5 tipos de exercícios, com tempos e número de séries diferentes.

# Modelagem do indivíduo
Para a modelagem da solução para esse problema, estuda-se utilizar um indivíduo em que seu gene seja formado por uma lista em que cada alelo é composto por um exercício físico, utilizando a seguinte estrutura:
      E1 E2 E3 ... En
Cada exercício consiste num objeto, possuindo como atributos: nome, número de séries e tempo de execução. A criação de um indivíduo é feita a partir de um sorteio baseado numa lista preestabelecida de exercícios e de acordo com o número de atividades que a pessoa deseja executar em um determinado intervalo de tempo.
