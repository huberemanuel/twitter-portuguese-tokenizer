# Twitter Portuguese Tokenizer
Tokenizador de Tweets para o português, voltado ao mercado de ações (Dataset Dante).

## Requerimentos

Python >= 3.7

## Como usar

Execute o seguinte comando para instalar as dependências e instalar o pacote `dante_tokenizer`.

```bash
make install
```

O pacote será adicionado ao seu ambiente python. Para tokenizar textos, basta seguir os seguintes passos:

```python
>>> from dante_tokenizer.tokenizer import DanteTokenizer
>>> tokenizer = DanteTokenizer()
>>> tokenizer.tokenize("A DANT3 está em alta!")
['A', 'DANT3', 'está', 'em', 'alta', '!']
```

O método `tokenize` irá retornar uma lista de strings contendo os respectivos tokens detectados. 

# DanteTokenizer

O DanteTokenizer é uma modificação do [TweetTokenizer](https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.casual) do pacote nltk. Adicionando regras para comportar as variedades de tokens existentes nos tweets relacionados ao mercado de ações.

Obs: Como a classe atual do TweetTokenizer não permite uma extensão de forma fácil, o código foi extraído e modificado dentro do `dante_tokenizer`.

## Agradecimentos

Ao Prof. Thiago A. S. Pardo pela orientação no programa de mestrado, à Profa. Ariani Di Felippo por definir as regras de tokenização e à Dra. Lucelene Lopes pelas contribuições técnicas. 
