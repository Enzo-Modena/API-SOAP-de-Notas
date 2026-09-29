from decimal import Decimal, ROUND_HALF_UP

def calcular_media(nota1: float, nota2: float) -> float:
    d1 = Decimal(str(nota1))
    d2 = Decimal(str(nota2))
    media = (d1 * Decimal('0.4')) + (d2 * Decimal('0.6'))
    return float(media.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

def determinar_situacao(media: float) -> str:
    if media >= 7.0:
        return "Aprovado"
    elif media >= 5.0:
        return "Recuperação"
    else:
        return "Reprovado"

def validar_notas(nota1: float, nota2: float) -> None:
    if not (0.0 <= nota1 <= 10.0):
        raise ValueError("Nota 1 deve estar entre 0.0 e 10.0")
    if not (0.0 <= nota2 <= 10.0):
        raise ValueError("Nota 2 deve estar entre 0.0 e 10.0")
