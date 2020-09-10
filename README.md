# API de Consulta de dados abertos da SINESP
Esta API viabiliza o acesso à Informações Públicas sobre Ocorrências Criminais em todo o brasil disponibilizado pelo Sistema Nacional de Estatística de Segurança Pública e Justiça Criminal (SINESP)

A base de dados pode ser consultada clicando [aqui](http://dados.gov.br/dataset/sistema-nacional-de-estatisticas-de-seguranca-publica).

## Como Consultar 

- A busca deve ser feita através de um único endpoint utilizando [Parâmetros de Requisição](https://en.wikipedia.org/wiki/Query_string) para a filtragem dos dados
- Por questões de desempenho, as consultas são limitadas à 1000 por página.

**URL:** 
- Produção: `http://ec2-54-174-4-15.compute-1.amazonaws.com/api`
- Desenvolvimento: `http://localhost:5000/api`

**Método:** `GET`

**Parâmetros de Consulta** :

Todos os filtros são opcionais e podem ser combinados da forma que for mais conveniente:

> Todos os parâmetros passam por uma camada de validação. Caso um dado seja informado incorretamente, o parâmetro será desconsiderado  

| Parâmetro        | Observação                                                      |Exemplo                |
| ---------------- | --------------------------------------------------------------- | --------------------- |
| regiao           | Região do Brasil [Ver Todas](#Regiões)                          | `ne`                  |
| uf               | Estado [Ver Todas](#estados-uf)                                 | `ce`                  |
| municipio        | Cidade                                                          | `sobral`              |
| crime            | Tipo de Crime [1-9] [Ver Todos](#tipos-de-crimes)               | `2`                   |
| ano              | Ano ou Intervalo de Anos                                        | `2015` ou `2017-2020` |
| mes              | Mês ou intervalo de Meses                                       | `mar` ou `jun-nov`    |
| per_page         | Numero de itens exibidos por página (Limite: 1000, Padrão: 100) | `500`                 |
| page             | Indice de Navegação por Página (Padrão: 1)                      | `2`                   |

**Exemplo**: 
- Url com todos os filtros: 

`http://localhost:5000/api?ano=2017-2020&crime=7&mes=jun-nov&municipio=Sobral&regiao=ne&uf=ce&per_page=50&page=1`

- Curl: 

```curl
curl --request GET \
  --url 'http://localhost:5000/api?ano=2017-2020&crime=7&mes=jun-nov&municipio=Sobral&regiao=ne&uf=ce&per_page=50&page=1'
```

**Consulta com Sucesso**
```json
{
    "page": 1,
    "results_per_page": 50,
    "total_results": 5,
    "total_ocorrencias": 618,
    "data": [
        {
            "ano": "2018",
            "crime": "1",
            "mes": "jan",
            "municipio": "fortaleza",
            "ocorrencias": "144.0",
            "regiao": "ne",
            "uf": "ce",
            "vitimas": "",
            "vitimas_municipio": "157"
        },
        {
            "ano": "2018",
            "crime": "1",
            "mes": "fev",
            "municipio": "fortaleza",
            "ocorrencias": "92.0",
            "regiao": "ne",
            "uf": "ce",
            "vitimas": "",
            "vitimas_municipio": "120"
        },
        ...
    ]
}
```

**Consulta Inválida**
```json
{
  "page": 1,
  "results_per_page": 50,
  "total_results": 0,
  "total_ocorrencias": 0,
  "data": []
}
```

#### Regiões
A Região pode ser informados por siglas com 2 caracteres [case-insensitive](https://pt.wiktionary.org/wiki/case_insensitive)

| Nome da Região | Parâmetro |
| -------------- | --------- |
| Norte          | `no`      |
| Nordeste       | `ne`      |
| Centro-Oeste   | `co`      |
| Sudeste        | `se`      |
| Sul            | `su`      |


#### Estados UF
O estado podem ser informados por siglas com 2 caracteres [case-insensitive](https://pt.wiktionary.org/wiki/case_insensitive)

| Estado              | Parâmetro |
| ------------------- | --------- |
| Acre                | `ac`      |
| Alagoas             | `al`      |
| Amapá               | `ap`      |
| Amazonas            | `am`      |
| Bahia               | `ba`      |
| Ceará               | `ce`      |
| Distrito Federal    | `df`      |
| Espírito Santo      | `es`      |
| Goiás               | `go`      |
| Maranhão            | `ma`      |
| Mato Grosso         | `mt`      |
| Mato Grosso do Sul  | `ms`      |
| Minas Gerais        | `mg`      |
| Pará                | `pa`      |
| Paraíba             | `pb`      |
| Paraná              | `pr`      |
| Pernambuco          | `pe`      |
| Piauí               | `pi`      |
| Rio de Janeiro      | `rj`      |
| Rio Grande do Norte | `rn`      |
| Rio Grande do Sul   | `rs`      |
| Rondônia            | `ro`      |
| Roraima             | `rr`      |
| Santa Catarina      | `sc`      |
| São Paulo           | `sp`      |
| Sergipe             | `se`      |
| Tocantins           | `to`      |


#### Município
O Município pode ser consultado através de seu nome por extenso. A API realizará os seguintes tratamentos:
 - Remoção de Espaços
 - Remoção de acentos
 - Conversão do nome em letra minúscula

portanto a busca por `São José dos Campos` será entendida como `saojosedoscampos`

#### Tipos de Crimes 
A Base de Dados categoriza 9 tipos de crimes que deverão ser consultados através do seu valor numérico

| Nome do Crime                       | Parâmetro |
| ----------------------------------- | --------- |
| Estupro                             | `1`       |
| Furto de veículo                    | `2`       |
| Homicídio doloso                    | `3`       |
| Lesão corporal seguida de morte     | `4`       |
| Roubo a instituição financeira      | `5`       |
| Roubo de carga                      | `6`       |
| Roubo de veículo                    | `7`       |
| Roubo seguido de morte (latrocínio) | `8`       |
| Tentativa de homicídio              | `9`       |

## Ambiente de Desenvolvimento
> Todos os comandos devem ser executados no diretório raiz deste projeto

Para conexão com o banco de dados [MongoDB] é necessário um arquivo .env com a variável de ambiente que contém a chave da API do pymongo, o arquivo deve conter o conteúdo neste formato: 

```
MONGO_URI="mongodb+srv://<username>:<password>@<cluster_name>.mongodb.net/<dbname>?retryWrites=true&w=majority"
``` 
#### Instalação
- [Python3](https://www.python.org/downloads/)
- Gerenciador de dependências [python3-pip ou pip3](https://packaging.python.org/guides/installing-using-linux-tools/#debian-ubuntu)

`sudo apt install python3 && sudo apt install python3-pip && sudo apt install python3-venv`

#### Criando ambiente virtal
- `python3 -m venv <nome_do_ambiente>`

#### Ativando ambiente virtual
- `source <nome_do_ambiente>/bin/activate`

#### Instalação de dependências
`pip3 install -r requirements.txt`

#### Execução do projeto
`python3 app.py`

## Agradecimentos
[@lucifernandes](https://github.com/lucifernandes) - Padronização e organização da base de dados

[@doissegundos](https://github.com/doissegundos) - Deploy da aplicação