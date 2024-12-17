class Cardapio:
    alimentos = []
    tabela = {}
    
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
        
    def mostrar_alimentos(self):
      cardapio_consolidado = {}
      for item in self.alimentos:
          nome = item.iloc[1]
          energia_item = float(item.iloc[4])
          if nome in cardapio_consolidado:
              cardapio_consolidado[nome]["quantidade"] += 1
          else:
              cardapio_consolidado[nome] = {"energia": energia_item, "quantidade": 1}

    def mostrar_tabela(self):
      tabela = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      linha = 1
      while linha < len(self.alimentos):
        item = (self.alimentos[linha])
        linha += 1
        index = 4
        while index < (len(item)):
          tabela[index-4] += item.iloc[index]
          index += 1
      print("\nTabela Nutricional ::\n")
      print(f"Total de Energia = {tabela[0]}")
      print(f"Total de Proteina = {tabela[1]}")	
      print(f"Total de Lipidios = {tabela[2]}")	
      print(f"Total de Fibras = {tabela[3]}")	
      print(f"Total de Alcool = {tabela[4]}")	
      print(f"Total de Colesterol = {tabela[5]}")	
      print(f"Total de Calcio = {tabela[6]}")	
      print(f"Total de Ferro = {tabela[7]}")
      print(f"Total de Sodio = {tabela[8]}")	
      print(f"Total de Potassio = {tabela[9]}")	
      print(f"Total de Vitamina_D = {tabela[10]}")	
      print(f"Total de Vitamina_E = {tabela[11]}")	
      print(f"Total de Vitamina_C = {tabela[12]}")
