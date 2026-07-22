# IMC Calculator 

Calculadora de IMC que vai além do cálculo tradicional: para menores de 18 anos, usa a referência oficial da OMS (IMC-para-idade, 2007) para classificar o resultado considerando idade e sexo — em vez de aplicar cegamente os pontos de corte pensados para adultos.

## Por que este projeto existe

O IMC clássico (abaixo do peso / normal / sobrepeso / obesidade) foi desenhado para adultos. Aplicado a um adolescente, pode gerar uma classificação enganosa, já que o corpo em desenvolvimento tem uma distribuição de IMC diferente a cada idade. Este projeto resolve isso consultando a tabela oficial da OMS (LMS, referência 2007, 5 a 19 anos) e calculando o escore-Z do IMC para a idade e sexo da pessoa.

## Funcionalidades

- Cálculo de IMC a partir de peso e altura
- Classificação por idade e sexo (OMS) para menores de 18 anos, com escore-Z visível
- Classificação clássica + faixa de peso ideal para adultos (18+)
- Interface gráfica moderna (CustomTkinter)
- Aviso claro quando a idade está fora da faixa coberta pela tabela (menores de 5 anos)

## Como rodar

```bash
pip install -r requirements.txt
python main.py
```

## Estrutura do projeto

IMC-Calculator/
├── main.py # Ponto de entrada
├── interface.py # Interface gráfica (CustomTkinter)
├── calculos.py # Lógica de cálculo (IMC, adulto, OMS)
├── utils.py # Validações (data, números, texto)
├── data/
│ ├── bmi_meninos.csv
│ └── bmi_meninas.csv
└── requirements.txt

## Fonte dos dados

Os dados de referência (L, M, S por mês, 5 a 19 anos) vêm da [WHO Growth Reference 2007](https://www.who.int/tools/growth-reference-data-for-5to19-years).

## Aviso

Este programa é uma ferramenta educacional/informativa e não substitui avaliação médica profissional.