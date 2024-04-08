def imc_classify(imc: float):
    if imc < 18.5:
        return "Abaixo do peso", 'normal-weight'
    elif imc < 25:
        return "Peso normal", 'normal-weight'
    elif imc < 30:
        return "Sobrepeso", 'above-weight'
    elif imc < 35:
        return "Obesidade grau I", 'over-weight'
    elif imc < 40:
        return "Obesidade grau II", 'over-weight'
    else:
        return "Obesidade grau III (mórbida)", 'over-weight'
