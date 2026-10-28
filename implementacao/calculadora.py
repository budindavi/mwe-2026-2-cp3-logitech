from abc import ABC, abstractmethod

class RegraCalculo(ABC):
    @abstractmethod
    def calcular(self, atraso_horas: float, valor_frete: float) -> float:
        pass

class RegraVarejo(RegraCalculo):
    def calcular(self, atraso_horas: float, valor_frete: float) -> float:
        if atraso_horas <= 2: return 0.0
        elif atraso_horas <= 24: credito = valor_frete * 0.10
        elif atraso_horas <= 72: credito = valor_frete * 0.25
        else: credito = valor_frete * 0.50
        return min(credito, 500.0)

class RegraCorporativo(RegraCalculo):
    def calcular(self, atraso_horas: float, valor_frete: float) -> float:
        if atraso_horas <= 2: return 0.0
        elif atraso_horas <= 24: credito = valor_frete * 0.20
        elif atraso_horas <= 72: credito = valor_frete * 0.50
        else: credito = valor_frete * 1.00
        return min(credito, 2000.0)

class RegraCortesia(RegraCalculo):
    def calcular(self, atraso_horas: float, valor_frete: float) -> float:
        return 0.0

class CalculadoraGarantia:
    def __init__(self):
        self.regras = {
            'VAREJO': RegraVarejo(),
            'CORPORATIVO': RegraCorporativo(),
            'CORTESIA': RegraCortesia()
        }

    def calcular(self, tipo_cliente: str, atraso_horas: float, valor_frete: float) -> float:
        regra = self.regras.get(tipo_cliente.upper())
        if not regra:
            raise ValueError("Tipo de cliente desconhecido")
        return regra.calcular(atraso_horas, valor_frete)
