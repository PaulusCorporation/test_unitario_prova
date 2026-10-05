def calcular_desconto(valor_compra, tipo_cliente):
    # Validação das entradas
    if valor_compra < 0:
        raise ValueError("valor_compra não pode ser negativo")

    tipo_cliente = str(tipo_cliente).strip().upper()   # CORREÇÃO 2: case-insensitive
    if tipo_cliente not in ("VIP", "COMUM"):
        raise ValueError("tipo_cliente deve ser 'VIP' ou 'COMUM'")

    desconto = 0

    # Validação do desconto base
    if valor_compra >= 100 and valor_compra < 500:      # CORREÇÃO 1: >= 100
        desconto = 0.10
    elif valor_compra >= 500:
        desconto = 0.20

    # Validação do cliente VIP
    if tipo_cliente == "VIP":
        desconto += 0.05

    valor_desconto = valor_compra * desconto

    # Regra do Teto de R$ 200,00
    if valor_desconto > 200:
        valor_desconto = 200

    return round(valor_desconto, 2)
