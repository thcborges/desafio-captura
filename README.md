# Crawler para o site [epocacosmeticos.com.br](https://www.epocacosmeticos.com.br)

Este projeto acessa o site [http://www.epocacosmeticos.com.br](http://www.epocacosmeticos.com.br)
e acessa todas as suas páginas a fim de buscar por produtos. Estes serão salvos em 
um arquivo `.csv` com campos relativos ao nome do produto, título da página do 
produto e a url da página do produto.


- Projeto desenvolvido em Python 3.6

- Dependências: BeautifoulSoup4

## Instalação
Basta clonar o repositório e fazer a intalação das dependências.
```commandline
git clone https://github.com/thcborges/desafio-captura.git
pip install -r requirements.pip
```

## Execução
Para executar o programa em busca dos produtos disponíveis no site 
[epocacosmeticos.com.br](https://www.epocacosmeticos.com.br), basta executar a 
seguinte linha de comando.
```commandline
python main.py
```
Será feita, então, uma busca por todos os links do site. Serão verificados se
os links são internos ou externos, excluindo os externos de serem acessados.

Todos os links internos do site serão acessados e salvos em um banco de dados 
local. Toda vez que uma url for acessada, o seu status no banco é alterado 
para visitada, fazendo com que aquela url não seja mais visitada.

Um padrão para as urls de produtos foi estipulado e a prioridade é o acesso 
às urls de produtos. Ou seja, sempre que houver uma url de produto não acessada
ela será acessada primeiro antes das demais urls.

Toda vez que uma url de produto for acessada, será salvo no arquivo `.csv` as 
informações pedidas no desafio: nome do produto, título da página e url.

O programa pode ser interrompido a qualquer momento, com uma instrução de 
interrupção do teclado `CTRL+C`. Ao retornar a sua execução a busca pelo site 
retornará exatamente de onde parou, pois seu estado atual está salvo no banco 
de dados.

 Ao finalizar o programa questionará o usuário se o mesmo deseja apagar o 
 banco de dados.
 
 
 ## Respostas
 - Agora você tem de capturar dados de outros 100 sites. Quais seriam suas 
 estratégias para escalar a aplicação?
    
    - A partir do conhecimento do padrão da url dos produtos de cada site,
    seria possível transformar `MAIN` (dicionário com chaves sendo `url` e 
    `product_pattern` do arquivo `main.py`) em uma lista de dicionários com
     chaves  `url` e `product_pattern`. 
     Tendo feito isso, eu precisaria verificar o DOM de cada novo site, para verificar
     se a forma como eu capturo o nome do produto continua válido.

 - Alguns sites carregam o preço através de JavaScript. Como faria para
 capturar esse valor.
 
    - Primeiro eu entraria na página de um produto do site e abriria a 
    inspeção de página. Uma vez nela, a guia `Network` possui todas as 
    chamadas feitas ao servidor pela página aberta no browser. Então,
    eu reconheceria a chamada feita onde o preço foi obtido. A partir daí
    é possível repetir a chamada ao servidor obtendo como respota o mesmo `JSON`
    ou `XML` (este último é bem difícil de ser usado atualmente). Após obter
    a resposta desse chamado, usaria bibliotecas como `json` ou `beautifoulsoup`
    para pegar o preço dos produtos.
    
 - Alguns sites podem bloquear a captura por interpretar seus acessos como um 
 ataque DDOS. Como lidaria com essa situação?
 
    - Eu usaria a função `sleep()` da lib `time` para criar uma pausa entre as 
    requisições feitas.
    
 - Um cliente liga reclamando que está fazendo muitos acessos ao seu site e 
 aumentando seus custos com infra. Como resolveria esse problema?
 
    - Se isso é um problema para o meu cliente, eu preciso diminuir a quantidade
    de acessos que faço ao site dele. Para isso eu usaria a mesma abrodagem para
    solucionar o problema a cima, utilizaria a função `sleep()` da lib `time`, 
    aumentando o intervalo de acesso a página do cliente. 
    
