from calculadora import CalculadoraGarantia

def test_ct01_varejo_atraso_2h_credito_zero():
    calc = CalculadoraGarantia()
    assert calc.calcular('VAREJO', 2.0, 100.0) == 0.0

def test_ct02_varejo_atraso_2h01_credito_10_porcento():
    calc = CalculadoraGarantia()
    assert calc.calcular('VAREJO', 2.1, 100.0) == 10.0

def test_ct03_varejo_atraso_24h01_credito_25_porcento():
    calc = CalculadoraGarantia()
    assert calc.calcular('VAREJO', 24.1, 100.0) == 25.0

def test_ct04_varejo_teto_500():
    calc = CalculadoraGarantia()
    assert calc.calcular('VAREJO', 73.0, 2500.0) == 500.0

def test_ct05_corporativo_atraso_2h01_credito_20_porcento():
    calc = CalculadoraGarantia()
    assert calc.calcular('CORPORATIVO', 2.1, 100.0) == 20.0

def test_ct06_corporativo_teto_2000():
    calc = CalculadoraGarantia()
    assert calc.calcular('CORPORATIVO', 73.0, 5000.0) == 2000.0

def test_ct07_cortesia_credito_zero():
    calc = CalculadoraGarantia()
    assert calc.calcular('CORTESIA', 48.0, 0.0) == 0.0
