class Carro(object):

    cambio = ""
    combustivel = ""
    direcao = ""
    potencia = ""
    quilometragem = ""
    portas = ""
    airbag = ""
    alarme = ""
    arcondicionado = ""
    trava_eletrica = ""
    vidro_eletrico = ""
    sensor_re = ""
    cam_re = ""
    cor = ""

    
    #Atributos n/selecionados: Tipo_veiculo, ipva_pago, fim_placa, som, marca, versao.
    def __init__(self, id, modelo, ano, cor, portas, pot, comb, km, dir, camb, preco):
        self.modelo = modelo
        self.ano = ano
        self.preco = preco
