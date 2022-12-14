# Modelagem Matemática do Futebol Brasileiro: um olhar no nível individual

[![.github/workflows/Scraping.yaml](https://github.com/IgorMichels/Brazilian_Soccer/actions/workflows/Scraping.yaml/badge.svg)](https://github.com/IgorMichels/Brazilian_Soccer/actions/workflows/Scraping.yaml)

Repositório com meu Trabalho de Conclusão de Curso (TCC) sobre o Futebol Brasileiro.

## Resumo

O futebol é uma paixão nacional. O Brasil, apesar de não ser o berço desse esporte, é
conhecido como “país do Futebol”, sendo natural que muitas conversas surjam com essa
natureza. Em geral tais conversas abrangem tópicos como “qual o melhor time”, “quem
irá ganhar uma determinada partida ou competição” ou então comparando dois jogadores,
avaliando qual é o melhor ou o preferido para um contratação do seu clube de coração.
Nesse sentido, o estudo desse esporte, a nível de modelagem, pode trazer um embasamento
matemático à conversa, deixando o “achismo” de lado.

No presente trabalho analisou-se o desempenho dos jogadores das Séries A e B do campeonato
brasileiro de futebol, organizado pela CBF (Confederação Brasileira de Futebol), sob
o ponto de vista da Inferência Bayesiana. Para tanto, realizou-se a raspagem dos dados
das súmulas de tais competições.

No contexto da modelagem três modelos foram propostos, um utilizando apenas os dados
das equipes que foram a campo, bem como o resultado dessas partidas, enquanto os outros
dois também se valiam da informação do mando de campo, com o intuito de modelar
o diferente comportamento, dentro e fora de casa. Os principais resultados se dão pela
estimação de distribuições de parâmetros que quantificam o desempenho dos jogadores,
possibilitando, dessa forma, comparar e ranquear os mesmos, além de ranquear os clubes
com maior influência dentro de seus domínios.

Palavras-chave: Modelagem matemática. Futebol. Inferência Bayesiana.


## Sumário

<details>
  <summary> Sumário (clique para expandir) </summary>
  
1. INTRODUÇÃO
2. REVISÃO DE LITERATURA
3. AQUISIÇÃO DOS DADOS
   * 3.1 Processo de raspagem
   * 3.2 Problemas durante a raspagem
   * 3.3 Automação do processo
4 MODELAGEM PROPOSTA
   * 4.1 Premissas utilizadas
   * 4.2 Tratamento e Seleção dos dados
     * 4.2.1 Tratamento dos dados
     * 4.2.2 Seleção dos dados
   * 4.3 Abordagem Frequentista
   * 4.4 Abordagem Bayesiana
     * 4.4.1 ADM - Attack and Defense Model
     * 4.4.2 HAM - Home Away Model
       * 4.4.2.1 HAM1
       * 4.4.2.2 HAM2
     * 4.4.3 Rodando os modelos
       * 4.4.3.1 Resultados
5. CONCLUSÃO
6. TRABALHOS FUTUROS
7. APÊNDICE A – CÓDIGOS STAN
   * A.1 Attack and Defense Model
   * A.2 Home Away Model 1
   * A.3 Home Away Model 2
</details>

## Texto

O texto pode ser encontrado [aqui](https://github.com/IgorMichels/Brazilian_Soccer/blob/main/Text/Modelagem%20Matem%C3%A1tica%20do%20Futebol%20Brasileiro.pdf).
