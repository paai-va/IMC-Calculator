from datetime import date


def validar_data_nascimento(texto: str) -> date | None:
    """
    Converte uma string 'DD/MM/AAAA' em um objeto date.
    Retorna None se o formato for inválido, a data não existir
    ou for uma data no futuro.
    """
    texto = texto.strip()

    try:
        dia, mes, ano = texto.split("/")
        nascimento = date(int(ano), int(mes), int(dia))
    except (ValueError, AttributeError):
        return None

    if nascimento > date.today():
        return None

    return nascimento


def calcular_idade_em_meses(nascimento: date) -> int:
    """Calcula a idade total, em meses completos, a partir da data de nascimento."""
    hoje = date.today()

    idade_meses_total = (hoje.year - nascimento.year) * 12 + (hoje.month - nascimento.month)

    if hoje.day < nascimento.day:
        idade_meses_total -= 1

    return idade_meses_total


def meses_para_anos_e_meses(idade_meses_total: int) -> tuple[int, int]:
    """Converte um total de meses em (anos_completos, meses_restantes)."""
    anos_completos = idade_meses_total // 12
    meses_restantes = idade_meses_total % 12
    return anos_completos, meses_restantes

def validar_float(valor: str) -> float | None:
    """
    Converte uma string (aceitando vírgula ou ponto decimal) em float.
    Retorna None se o valor não puder ser convertido ou for <= 0.
    """
    valor = valor.strip().replace(",", ".")

    try:
        numero = float(valor)
    except ValueError:
        return None

    if numero <= 0:
        return None

    return numero

def validar_texto(valor: str) -> str:
    """Remove espaços extras e formata um nome com iniciais maiúsculas."""
    return valor.strip().title()

if __name__ == "__main__":
    data = validar_data_nascimento("15/03/2008")
    print("Data válida:", data.strftime("%d/%m/%Y") if data else "None")

    if data:
        meses = calcular_idade_em_meses(data)
        print("Idade em meses:", meses)
        print("Anos e meses:", meses_para_anos_e_meses(meses))

    # Testando uma data inválida de propósito
    print("Data inválida (deve ser None):", validar_data_nascimento("32/13/2008"))