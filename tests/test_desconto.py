import pytest
from src.tech.desconto import calcular_desconto


# ---- Faixas de desconto base (cliente COMUM) ----
@pytest.mark.parametrize("valor, esperado", [
    (0, 0),            # mínimo
    (50, 0),           # abaixo de 100
    (99.99, 0),        # limite inferior da faixa 0%
    (100, 10),         # limite: exatamente 100 -> 10%
    (100.01, 10.00),
    (300, 30),         # o "teste de cabeça" do Dev Jr.
    (499.99, 50.00),   # limite superior da faixa 10%
    (500, 100),        # limite: exatamente 500 -> 20%
    (700, 140),
])
def test_cliente_comum_faixas(valor, esperado):
    assert calcular_desconto(valor, "COMUM") == pytest.approx(esperado, abs=0.01)


# ---- Cliente VIP (+5%) ----
@pytest.mark.parametrize("valor, esperado", [
    (50, 2.50),        # 0% -> 5%
    (99.99, 5.00),
    (100, 15),         # 10% -> 15%
    (300, 45),
    (500, 125),        # 20% -> 25%
    (700, 175),
])
def test_cliente_vip_adicional(valor, esperado):
    assert calcular_desconto(valor, "VIP") == pytest.approx(esperado, abs=0.01)


# ---- Case-insensitive ----
@pytest.mark.parametrize("tipo", ["VIP", "vip", "Vip", " vip "])
def test_vip_ignora_maiusculas_minusculas(tipo):
    assert calcular_desconto(100, tipo) == pytest.approx(15)


@pytest.mark.parametrize("tipo", ["COMUM", "comum", "Comum"])
def test_comum_ignora_maiusculas_minusculas(tipo):
    assert calcular_desconto(100, tipo) == pytest.approx(10)


# ---- Teto de R$ 200 ----
def test_teto_vip_acima_do_limite():
    assert calcular_desconto(1000, "VIP") == 200      # 25% = 250 -> teto 200


def test_teto_comum_acima_do_limite():
    assert calcular_desconto(2000, "COMUM") == 200    # 20% = 400 -> teto 200


def test_teto_exato():
    assert calcular_desconto(1000, "COMUM") == 200    # 20% = 200 exatos


def test_logo_abaixo_do_teto():
    assert calcular_desconto(999.99, "COMUM") == pytest.approx(200.00, abs=0.01)
    assert calcular_desconto(799.99, "VIP") == pytest.approx(200.00, abs=0.01)  # 25% = 199.9975


# ---- Entradas inválidas ----
def test_valor_negativo():
    with pytest.raises(ValueError):
        calcular_desconto(-10, "COMUM")


def test_tipo_cliente_invalido():
    with pytest.raises(ValueError):
        calcular_desconto(100, "PREMIUM")
