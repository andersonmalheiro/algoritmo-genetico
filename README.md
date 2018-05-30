# Algoritmo genético
Modelagem e implementação de um algoritmo genético para formatação de treinos físicos.

# Problema
Todos que fazem exercícios precisam fazer uma sequência em um certo período de tempo. O algoritmo precisa capturar o tempo de treino e “Encaixar” os tipos de exercícios e suas séries de modo a ocupar melhor o tempo. Considere no mínimo 5 tipos de exercícios, com tempos e número de séries diferentes.

## Modelagem do indivíduo
Para a modelagem da solução para esse problema, estuda-se utilizar um indivíduo em que seu gene seja formado por uma lista em que cada alelo é composto por um exercício físico, utilizando a seguinte estrutura:

                  E1, E2, E3, ... En
      
Cada exercício consiste num objeto, possuindo como atributos: nome, número de séries e tempo de execução. A criação de um indivíduo é feita a partir de um sorteio baseado numa lista preestabelecida de exercícios e de acordo com o número de atividades que a pessoa deseja executar em um determinado intervalo de tempo.

## Função fitness
Para efetuar o cálculo fitness de cada indivíduo, leva-se em consideração o tempo total que a pessoa pretende treinar e a quantidade de exercícios diferentes que se deseja executar naquele intervalo de tempo. Para isso, na função fitness é verificada a quantidade de alelos diferentes em relação ao tipo do exercício, pois pode ocorrer de um indivíduo possuir o mesmo tipo de exercício mais de uma vez, porém com número de séries e tempo de execução diferentes, o que não é bom. Após feita essa contagem, a função faz uma soma do tempo de execução de cada exercício para definir em quanto tempo aquela lista de atividades será executada. Após obter esse tempo, é feito um cálculo para descobrir a porcentagem de sobra em relação ao tempo definido pela
pessoa, que será usado para bonificar o indivíduo, seguindo a seguinte função:

                        sobra = (T – Σte / T) * 100

Onde T é o tempo determinado pela pessoa e Σte é o somatório dos tempos de execução de cada exercício. Agora com essa porcentagem em mãos, é feita uma avaliação para atribuir pontos de bonificação, seguindo os seguintes critérios:

- Se não há sobra, o indivíduo recebe 1000 pontos;
- Se há uma sobra de até 5% o indivíduo recebe 400 pontos;
- Se há sobra de até 10% o indivíduo recebe 150 pontos;
- Se há sobra de até 30% o indivíduo recebe 50 pontos;
- Caso haja uma sobra de mais de 30% o indivíduo recebe 10 pontos.

Agora esses valores são aplicados a uma fórmula matemática que fará a diferenciação entre os indivíduos, que é a seguinte:

                  fitness = pontos + (10 * d3) – (10 * r3)

Onde ‘d’ é a quantidade de exercícios diferentes presentes na lista, e ‘r’ são os repetidos. Com isso, há uma maior pressão de seleção, fazendo com que indivíduos que possuam diferentes números de treinos distintos e sobra de tempo sejam muito diferentes dos outros.

## Seleção
A seleção de indivíduos para criar uma nova geração é feita a partir do método de Torneio. Nesse método, são selecionados dois indivíduos aleatoriamente da população, e o indivíduo com maior fitness vence o torneio. No algoritmo, são selecionados dois indivíduos por torneio, e de acordo com a taxa de Crossover determinada, eles podem sofrer um cruzamento, que gerará dois filhos a partir dos seus genes, ou poderão ser adicionados na nova geração automaticamente.

## Crossover
O método de crossover ou cruzamento faz com que sejam gerados dois novos indivíduos a partir dos genes dos pais, de acordo com a técnica de crossover de ponto único. No algoritmo, é definido um ponto de corte aleatoriamente, onde o genes dos pais são divididos, e as partes correspondentes serão passadas para os filhos de forma cruzada.

## Mutação
A mutação consiste em alterar algum indivíduo daquela população de forma que ele seja levado a novas possibilidades de resposta. No algoritmo, a função de mutação consiste em alterar N alelos aleatoriamente do gene de um indivíduo sorteado. N é um valor entre 1 e o número de alelos de um gene, que é sorteado aleatoriamente também.

## Desenvolvimento
Durante o desenvolvimento do algoritmo, surgiram algumas dificuldades em relação a obtenção da resposta esperada. Em um dado momento, percebeu-se que o algoritmo encontrava a resposta sempre muito rapidamente, geralmente na segunda geração da população, sendo que isso não é bom. Com isso foi necessário fazer algumas alterações no código, principalmente em relação aos valores de tempo de cada treino. Percebeu-se que quando se utilizava os valores inteiros fixos presentes na lista de treinos esse problema
ocorria, então para corrigir foi necessário que os tempos fossem gerados aleatoriamente e em formato decimal, dando uma maior  gama de possibilidades de resposta e dificultando um pouco mais o resultado. Também houveram mudanças em relação a mutação, pois inicialmente a função somente alterava um único alelo no gene do indivíduo selecionado, e geralmente isso não surtia um efeito tão forte. Sendo assim, a função de mutação passou a alterar até 3 alelos do indivíduo, fazendo com que as alterações causassem efeitos com mais intensidade de forma que levassem os indivíduos à possibilidades de respostas diferentes.

