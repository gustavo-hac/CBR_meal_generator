class Cardapio:
    alimentos = []
    
    def __init__(self, energia_recebida, limiar, alimentos, energia_total):
        self.id = id
        self.energia_recebida = energia_recebida
        self.limiar = limiar
        self.limiar_inf = energia_recebida - limiar
        self.limiar_sup = energia_recebida + limiar
        self.alimentos = alimentos
        self.energia_total = energia_total
    
    def adaptar(self):
        novos_alimentos = self.alimentos
        novos_alimentos.append(self.alimentos[1])
        nova_energia = self.energia_total + self.alimentos[1].iloc[4]
        novo_cardapio = Cardapio(self.energia_recebida, self.limiar, novos_alimentos, nova_energia)
        return novo_cardapio
    
    def adicionar_item(self, item):
        self.alimentos.append(item)