import csv
import math
import os


def calcular_imc(peso_kg: float, altura_m: float) -> float:
    """Calcula o IMC a partir do peso (kg) e da altura (m)."""
    return peso_kg / (altura_m ** 2)


def classificar_imc_adulto(imc: float) -> str:
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    elif imc < 35:
        return "Obesidade Grau I"
    elif imc < 40:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"

def faixa_peso_ideal_adulto(altura_m):
    peso_min = 18.5 * (altura_m ** 2)
    peso_max = 24.9 * (altura_m ** 2)
    return peso_min, peso_max

def carregar_tabela(caminho_csv):
    tabela = []
    with open(caminho_csv, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            tabela.append((
                int(linha["mes"]),
                float(linha["L"]),
                float(linha["M"]),
                float(linha["S"]),
            ))
    return tabela


def tabela_para_sexo(sexo):
    sexo_normalizado = sexo.strip().lower()
    if sexo_normalizado.startswith("m"):
        return TABELA_MENINOS
    return TABELA_MENINAS


def buscar_linha_lms(idade_meses, tabela):
    idade_meses = round(idade_meses)
    idade_meses = max(61, min(228, idade_meses))  # trava dentro do intervalo da OMS

    for mes, L, M, S in tabela:
        if mes == idade_meses:
            return L, M, S

    return None  # não deveria acontecer, mas é uma segurança

def calcular_zscore(imc, L, M, S):
    if abs(L) < 1e-8:  # praticamente zero
        return math.log(imc / M) / S
    return ((imc / M) ** L - 1) / (L * S)


def classificar_zscore_oms(z):
    if z < -3:
        return "Magreza acentuada"
    elif z < -2:
        return "Magreza"
    elif z <= 1:
        return "Peso adequado para a idade"
    elif z <= 2:
        return "Sobrepeso"
    else:
        return "Obesidade"

def calcular_resultado(peso_kg, altura_cm, idade_meses, sexo):
    altura_m = altura_cm / 100
    imc = calcular_imc(peso_kg, altura_m)

    if idade_meses >= 216:  # 18 anos * 12 meses
        classificacao = classificar_imc_adulto(imc)
        peso_min, peso_max = faixa_peso_ideal_adulto(altura_m)
        return {
            "imc": imc,
            "classificacao": classificacao,
            "fonte": "OMS — critério para adultos",
            "peso_min_saudavel": peso_min,
            "peso_max_saudavel": peso_max,
        }

    if idade_meses < 61:
        return {
            "imc": imc,
            "classificacao": "Fora da faixa coberta (consulte um pediatra)",
            "fonte": "Sem tabela oficial disponível para menores de 5 anos neste programa",
        }

    tabela = tabela_para_sexo(sexo)
    L, M, S = buscar_linha_lms(idade_meses, tabela)
    z = calcular_zscore(imc, L, M, S)
    classificacao = classificar_zscore_oms(z)

    return {
        "imc": imc,
        "classificacao": classificacao,
        "fonte": "OMS (WHO) — IMC-para-idade, referência 2007",
        "z_score": z,
    }

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MENINOS = os.path.join(BASE_DIR, "data", "bmi_meninos.csv")
CAMINHO_MENINAS = os.path.join(BASE_DIR, "data", "bmi_meninas.csv")

TABELA_MENINOS = carregar_tabela(CAMINHO_MENINOS)
TABELA_MENINAS = carregar_tabela(CAMINHO_MENINAS)

if __name__ == "__main__":
    resultado = calcular_resultado(peso_kg=15, altura_cm=95, idade_meses=36, sexo="Feminino")
    print(resultado)