# Problema de negócio

A Cury Company é uma empresa fictícia de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas.

Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Cury Company.

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores e etc. Apesar da empresa estar crescendo, em termos de entregas, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

Dentro desse contexto, o objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam algumas métricas da melhor forma possível para o CEO.

Entre os pedidos, tem-se:

## Visão empresa:

1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
5. Quantidade de pedidos por entregador por semana.
6. Localização central de cada cidade.

## Visão entregador:

1. Menor e maior idade dos entregadores.
2. Pior e melhor condição de veículo.
3. Avaliação média por entregador.
4. Avaliação média e desvio padrão por tipo de tráfego.
5. Avaliação média e desvio padrão por condições climáticas.
6. 10 entregadores mais rápidos.
7. 10 entregadores mais lentos.

## Visão restaurantes:

1. Quantidade de entregadores únicos.
2. Distância média dos restaurantes e locais de entrega.
3. Tempo médio e desvio padrão de entrega por cidade.
4. Tempo médio e desvio padrão de entrega por cidade e tipo de pedido.
5. Tempo médio e desvio padrão de entrega por cidade e tipo de tráfego.
6. Tempo médio de entrega durante os festivais.

# Premissas assumidas

- A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
- Marketplace foi o modelo de negócio assumido.
- Os 3 principais visões do negócio foram: Visão transação de pedidos, visão restaurante e visão entregadores.

# Estratégia da solução

O painel foi desenvolvido utilizando as métricas que refletem as visões do modelo de negócio da empresa, onde cada visão reflete as métricas pedidas.

# Top 3 Insights

1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais.
2. As cidades do tipo Semi-Urban não possuem condições baixas de trânsito.
3. As maiores variações no tempo de entrega ocorrem durante o clima ensolarado.

# Produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: [Dashboard Online](https://vanderson-curry-company.streamlit.app/)

![Painel gerencial](painel.gif)

# Conclusão

Com a conclusão do projeto foi possível obter um painel online para visualizar as métrica.

Da visão da Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e semana 13 do ano de 2022.

# Próximos passos

1. Reduzir o número de métricas.
2. Criar novos filtros.
3. Adicionar novas visões de negócio.

---

Link dos dados: [Clique aqui](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset)
