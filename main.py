import pandas as pd
import random as rand
from caso import Cardapio

arquivos = ["BaseDados/alimento_nut_all.xlsx", "BaseDados/alimentos.xlsx", "BaseDados/grupos.xlsx"]

alimentos_nut_arq = arquivos[0]
alimentos_arq = arquivos[1]
grupos_arq = arquivos[2]

alimentos = pd.read_excel(alimentos_arq)
alimentos_nut = pd.read_excel(alimentos_nut_arq)
grupos = pd.read_excel(grupos_arq)
## Tabela dos alimentos com nutrientes conhecidos (inicia vazia)
conhecidos = pd.read_excel("conhecidos.xlsx") # print("\nalimentos\n")# print(alimentos)# print("\nalimentoss_nut\n")# print(alimentoss_nut)# print("\ngrupos\n")# print(grupos)
casos = []

## Determina o tipo do alimento entre: 
## [Carboidrato, Proteina, Gordura, Fruta, Vegetal, Bebida, Sobremesa, Industrial, Outros]
def determinar_tipo(nome, grupo):
  match grupo:
  ## N?mero em colchetes por causa do formato na tabela.
    case 65:                                          # print("Cereais e derivados")
      return "Carboidrato"
    case 66:                                          # print("Vegetais e derivados")
      if "batata" in nome:
        return "Carboidrato"
      else:
        return "Vegetal"
    case 67:                                          # print("Frutas e derivados")
      if "suco" in nome:
        return "Bebida"
      return "Fruta"
    case 68:                                          # print("Gorduras e ?leos")
      return "Gordura" 
    case 69:                                          # print("Pescados e frutos do mar")
      return "Proteina"
    case 70:                                          # print("Carnes e derivados")
      return "Proteina"
    case 71:                                          # print("Leite e derivados")
      return "Sobremesa"
    case 72:                                          # print("Bebidas ")
      return "Bebida"
    case 74:                                          # print("Ovos e derivados")
      return "Proteina"
    case 75:                                          # print("A??cares e doces")
      return "Sobremesa"
    case 76:                                          # print("Miscel?neas")
      if "Sundae" in nome:
        return "Sobremesa"
      else:
        return "Carboidrato"
    case 77:                                          # print("Fast food")
      if "batata" in nome:
        return "Carboidrato"
      else:
        return "Proteina" 
    case 78:                                          # print("Alimentos para fins especiais")
      if "chocolate" in nome:
        return "Sobremesa"
      if "gelatina" in nome:
        return "Sobremesa"
      return "Outros" 
    case 82:                                          # print("Alimentos industrializados")
      return "Industrial"
    case 84:                                          # print("Leguminosas e derivados")
      return "Vegetal"
    case 85:                                          # print("Nozes e sementes")
      return "Vegetal"
    case _:
      print("*************Erro ao buscar grupo da tabela*********************")
      return "Desconhecido"
    
## Troca valores nulos por "0" e retira valores negativos.
def retirar_ruido(linha_base):
  lista_sem_null = []
  for i in range(len(linha_base)):
    if linha_base.iloc[i]:
      ## As colunas alternam entre int e String, ?ndice par = "String", ?mpar = "int"
      if i % 2 != 0:
        if linha_base.iloc[i] >= 0:
          lista_sem_null.append(linha_base.iloc[i])
        else:
          lista_sem_null.append(0)
      else:
        lista_sem_null.append(linha_base.iloc[i])
    else:
      lista_sem_null.append(0)
  return lista_sem_null

## Adiciona uma nova linha na tabela de conhecido com base nos dados das tabelas "alimento" e "alimento_nut_all"
def adicionar_conhecido(tabela_conhecidos, linha_alimento, linha_nutrientes): 
  tipo = determinar_tipo(linha_alimento.iloc[1], linha_alimento.iloc[2])
  lista_nut = retirar_ruido(linha_nutrientes)
  nova_linha = pd.DataFrame({'id': linha_alimento.iloc[0],'nome': linha_alimento.iloc[1], 'grupo': linha_alimento.iloc[2], 'tipo': [tipo], 'energia': lista_nut[3], 'carboidratos': lista_nut[7], 'proteinas': lista_nut[11], 'lipidios': lista_nut[13],
                             'fibras': lista_nut[15], 'alcool': lista_nut[17], 'colesterol': lista_nut[19], 'calcio': lista_nut[21], 'ferro': lista_nut[23],
                             'sodio': lista_nut[25], 'potassio': lista_nut[27], 'vitamina_D': lista_nut[29], 'vitamina_E': lista_nut[31], 'vitamina_C': lista_nut[33]},)

  if tabela_conhecidos.empty:
    tabela_conhecidos = nova_linha.copy()
  else:
    tabela_conhecidos = pd.concat([tabela_conhecidos, nova_linha], ignore_index=True)
  # print(nova_linha)
  return tabela_conhecidos

## Procura na tabela "alimentos" os membros que existem em "alimentos_nut_all" e adicona dados importantes na tabela "conhecidos"
def procurar_codigos(alimentos, alimentos_nut, conhecidos):                 # counter = 0
  for i in range(len(alimentos_nut)):                                       # print(f"\nLinha {i}")
    codigo = alimentos_nut.iloc[i,0]                                        # print(codigo)
    for j in range(len(alimentos)):
      if codigo in alimentos.iloc[j,0]:                                     # print(alimentos.iloc[j]) # counter += 1
        ## Manda por param?tro a linha de alimento e alimento_nut para adicionar os elementos a tabela
        conhecidos = adicionar_conhecido(conhecidos, alimentos.iloc[j], alimentos_nut.iloc[i])
        break
    # print(f"\n{conhecidos.iloc[i]}")
  return conhecidos
  # print(conhecidos)# print(f"\n{counter}")
def pegar_ordenados_alimentos(conhecidos, tipo):
  lista = conhecidos[conhecidos['tipo'] == tipo]
  lista = lista.sort_values(by='energia', ascending=True)
  return lista

#1 proteina, 2 vegetais ou mais, 1 carboidrato ou mais, 1 bebida
def criar_cardapio(energia_total, limiar):
    cardapio = []
    energia_min = energia_total - limiar
    energia_max = energia_total + limiar
    # print(f"Energia total desejada: {energia_total}")    # print(f"Limiar: {limiar} (Intervalo: {energia_min} a {energia_max})\n")
    energia_usada = 0
    # Listas de alimentos ordenadas por energia
    lista_carboidrato = pegar_ordenados_alimentos(conhecidos, "Carboidrato")
    lista_proteina = pegar_ordenados_alimentos(conhecidos, "Proteina")
    lista_bebida = pegar_ordenados_alimentos(conhecidos, "Bebida")
    lista_vegetal = pegar_ordenados_alimentos(conhecidos, "Vegetal")

    # Adicionar alimentos obrigatórios
    def adicionar_ao_cardapio(descricao):
      lista = []
      match descricao:
        case "Proteina":
            lista = lista_proteina
        case "Vegetal":
            lista = lista_vegetal
        case "Carboidrato":
            lista = lista_carboidrato
        case "Bebida":
            lista = lista_bebida
      nonlocal energia_usada
      if len(lista) == 0:
          # print(f"Não há itens disponíveis para {descricao}.")
          return
      item = lista.iloc[rand.randrange(0, len(lista))]
      energia_item = float(item.iloc[4])  # Certifique-se de que seja um número válido
      if energia_usada + energia_item <= energia_max:  # Verifique se não ultrapassa o limite
          energia_usada += energia_item
          cardapio.append(item)
          # print(f"{descricao}: {item.iloc[1]} (Energia: {energia_item})")
      # else:
      #     print(f"Item {descricao} ignorado para não ultrapassar o limite.")
    # adicionar_ao_cardapio("Proteína")    # adicionar_ao_cardapio(lista_vegetal, "Vegetal")    # adicionar_ao_cardapio(lista_vegetal, "Vegetal")    # adicionar_ao_cardapio(lista_carboidrato, "Carboidrato")    # adicionar_ao_cardapio(lista_bebida, "Bebida")
    adicionar_ao_cardapio("Proteina")
    adicionar_ao_cardapio("Vegetal")
    adicionar_ao_cardapio("Vegetal")
    adicionar_ao_cardapio("Carboidrato")
    adicionar_ao_cardapio("Bebida")
    # print(f"\nEnergia usada após itens obrigatórios: {energia_usada}")
    ## Ajuste para energia dentro do intervalo
    while energia_usada < energia_min:
        item = lista_carboidrato.iloc[rand.randrange(0, len(lista_carboidrato))]
        energia_item = float(item.iloc[4])
        if energia_usada + energia_item <= energia_max:
            energia_usada += energia_item
            cardapio.append(item)
            # print(f"Adicionado ao cardápio: {item.iloc[1]} (Energia: {energia_item})")
        # else:
            # print(f"Item ignorado para não ultrapassar o limite.")

    ## Consolidar itens iguais no cardápio
    cardapio_consolidado = {}
    for item in cardapio:
        nome = item.iloc[1]
        energia_item = float(item.iloc[4])
        if nome in cardapio_consolidado:
            cardapio_consolidado[nome]["quantidade"] += 1
        else:
            cardapio_consolidado[nome] = {"energia": energia_item, "quantidade": 1}

    ## Imprimir cardápio final consolidado
    print("Itens no cardápio:")
    for nome, info in cardapio_consolidado.items():
        print(f"- {nome} (Energia: {info['energia']}) (Quantidade: {info['quantidade']})")
    # print(f"\nEnergia total usada: {energia_usada}\n")
    caso = Cardapio(energia_total,limiar,cardapio,energia_usada)
    casos.append(caso)
    caso.mostrar_tabela()
    return cardapio

def criar_cardapio_usuario(energia_total,limiar):
  cardapio = []
  energia_min = energia_total - limiar
  energia_max = energia_total + limiar
  energia_usada = 0
  ## Listas de alimentos ordenadas por energia
  lista_carboidrato = pegar_ordenados_alimentos(conhecidos, "Carboidrato")
  lista_proteina = pegar_ordenados_alimentos(conhecidos, "Proteina")
  lista_bebida = pegar_ordenados_alimentos(conhecidos, "Bebida")
  lista_vegetal = pegar_ordenados_alimentos(conhecidos, "Vegetal")

  ## Adicionar alimentos obrigatórios
  def adicionar_ao_cardapio(descricao, tentativas, opcional):
      if tentativas > 900:
        return # print(f"Nao foi possivel encontrar {descricao} que coubesse no limiar")
      lista = []
      match descricao:
        case "Proteina":
            lista = lista_proteina
        case "Vegetal":
            lista = lista_vegetal
        case "Carboidrato":
            lista = lista_carboidrato
        case "Bebida":
            lista = lista_bebida
        case "Fruta":
            lista = lista_fruta
        case "Industrial":
            lista = lista_industrial
        case "Outros":
            lista = lista_outros
        case "Sobremesa":
            lista = lista_sobremesa
      nonlocal energia_usada
      if len(lista) == 0:
          print(f"Não há itens disponíveis para {descricao}.")
          return
      item = lista.iloc[rand.randrange(0, len(lista))]
      energia_item = float(item.iloc[4])  ## Certifique-se de que seja um número válido
      if energia_usada + energia_item <= energia_max:  ## Verifique se não ultrapassa o limite 
          energia_usada += energia_item
          cardapio.append(item)          # print(f"{descricao}: {item.iloc[1]} (Energia: {energia_item})")
          return item
      else:
          tentativas += 1
          if opcional:
             adicionar_ao_cardapio(descricao, tentativas, True)
             return
          if len(cardapio) > 0:
            cardapio.sort(key=lambda x: x.iloc[4])   
            # print(cardapio)
            ultimo = cardapio.pop()
            energia_usada -= ultimo.iloc[4]
            # print(cardapio)
            ultimo_nome = ultimo.iloc[1]            # print("ID grupo = ")            # print(ultimo.iloc[2])
            ultimo_grupo = determinar_tipo(ultimo_nome, ultimo.iloc[2])            # print(ultimo_grupo)
            adicionar_ao_cardapio(ultimo_grupo, tentativas, False)
            tentativas += 1
            adicionar_ao_cardapio(descricao, tentativas, False)
            return
          else:
            adicionar_ao_cardapio(descricao, tentativas, False)
            return False

  adicionar_ao_cardapio("Proteina", 0, False)
  adicionar_ao_cardapio("Vegetal", 0, False)
  adicionar_ao_cardapio("Vegetal", 0, False)
  adicionar_ao_cardapio("Carboidrato", 0, False)
  adicionar_ao_cardapio("Bebida", 0, False)

  # print(f"\nEnergia usada após itens obrigatórios: {energia_usada}\n")
  lista_sobremesa = pegar_ordenados_alimentos(conhecidos, "Sobremesa")
  lista_fruta = pegar_ordenados_alimentos(conhecidos, "Fruta")
  lista_industrial = pegar_ordenados_alimentos(conhecidos, "Industrial")
  lista_outros = pegar_ordenados_alimentos(conhecidos, "Outros")
  
  ## Ajuste para energia dentro do intervalo
  tentativas = 0
  opcoes = ["Carboidrato","Vegetal","Sobremesa","Fruta","Industrial","Outros"]
  
  while energia_usada < energia_min:
      tipo = rand.choice(opcoes)
      adicionar_ao_cardapio(tipo, 0, True)
      tentativas += 1
      if (tentativas > 900):
        break
  ## Consolidar itens iguais no cardápio
  cardapio_consolidado = {}
  for item in cardapio:
      nome = item.iloc[1]
      energia_item = float(item.iloc[4])
      if nome in cardapio_consolidado:
          cardapio_consolidado[nome]["quantidade"] += 1
      else:
          cardapio_consolidado[nome] = {"energia": energia_item, "quantidade": 1}
  ## Imprimir cardápio final consolidado
  print("Itens no cardápio:")
  for nome, info in cardapio_consolidado.items():
      print(f"- {nome} (Energia: {info['energia']}) (Quantidade: {info['quantidade']})")

  print(f"\nEnergia total usada: {energia_usada}")
  return cardapio

def iniciar_casos(quant_pratos):
    print("\nCriando Cardápio Base\n")
    energia = 500
    i = 0
    while i < quant_pratos:
      print(f"\nCardápio Base {i+1}")
      i += 1
      energia += 400
      cardapio = criar_cardapio(energia, 200)

def adaptar_caso(caso, energia_min, energia_max):
  # print(f"energia_min = {energia_min}")  # print(f"energia_max = {energia_max}")
  lista_carboidrato = pegar_ordenados_alimentos(conhecidos, "Carboidrato")
  lista_proteina = pegar_ordenados_alimentos(conhecidos, "Proteina")
  lista_bebida = pegar_ordenados_alimentos(conhecidos, "Bebida")
  lista_vegetal = pegar_ordenados_alimentos(conhecidos, "Vegetal")
  lista_sobremesa = pegar_ordenados_alimentos(conhecidos, "Sobremesa")
  lista_fruta = pegar_ordenados_alimentos(conhecidos, "Fruta")
  lista_industrial = pegar_ordenados_alimentos(conhecidos, "Industrial")
  lista_outros = pegar_ordenados_alimentos(conhecidos, "Outros")

  opcoes = ["Carboidrato", "Proteina", "Bebida", "Vegetal", "Sobremesa", "Fruta", "Industrial", "Outros"]
  itens_mudados = 0
  tentativas = 0
  while tentativas < 100:
    if (itens_mudados != 0) & (energia_min <= caso.energia_total <= energia_max):
       print("\n Modificacoes necessarias feitas")
       break
    esperanca = True
    lista = []
    tentativas += 1
    tipo = rand.choice(opcoes)
    ##Verifica??o de tentativa e itens mudados
    if (tentativas > 90) & (esperanca):
      caso.alimentos.sort(key=lambda x: x.iloc[4])   
      ultimo = caso.alimentos.pop()
      print(f"{ultimo.iloc[1]} removido")
      caso.energia_total -= ultimo.iloc[4]
      ultimo_nome = ultimo.iloc[1] 
      ultimo_grupo = determinar_tipo(ultimo_nome, ultimo.iloc[2])
      tipo = ultimo_grupo
      esperanca = False
    match tipo:
      case "Proteina":
          lista = lista_proteina
      case "Vegetal":
          lista = lista_vegetal
      case "Carboidrato":
          lista = lista_carboidrato
      case "Bebida":
          lista = lista_bebida
      case "Fruta":
          lista = lista_fruta
      case "Industrial":
          lista = lista_industrial
      case "Outros":
          lista = lista_outros
      case "Sobremesa":
          lista = lista_sobremesa
    if esperanca == False:
      item = lista.iloc[0]
      esperanca = True
    else:
      item = lista.iloc[rand.randrange(0, len(lista))]
    energia_item = float(item.iloc[4])  ## Certifique-se de que seja um número válido
    if (caso.energia_total + energia_item) <= energia_max:  ## Verifique se não ultrapassa o limite 
      caso.energia_total += energia_item
      caso.adicionar_item(item)  
      itens_mudados += 1      
      print(f"Item {item.iloc[1]} adicionado para chegar no limar")

  cardapio_consolidado = {}
  for item in caso.alimentos:
      nome = item.iloc[1]
      energia_item = float(item.iloc[4])
      if nome in cardapio_consolidado:
          cardapio_consolidado[nome]["quantidade"] += 1
      else:
          cardapio_consolidado[nome] = {"energia": energia_item, "quantidade": 1}
  ## Imprimir cardápio final consolidado
  print("\nItens no cardápio:")
  for nome, info in cardapio_consolidado.items():
      print(f"- {nome} (Energia: {info['energia']}) (Quantidade: {info['quantidade']})")

  caso.mostrar_tabela()
  return caso

def escolher_prato(energia,limiar):
  energia_min = energia - limiar
  energia_max = energia + limiar  # print(f"Energia total desejada: {energia}")  # print(f"Limiar: {limiar} (Intervalo: {energia_min} a {energia_max})\n")
  i = 0
  lista_cardapio = []
  while i < 2:
    i += 1
    print(f"\nCardapio {i}:")
    lista_cardapio.append(criar_cardapio_usuario(energia, limiar))
  novo_caso = casos[0]
  i = 0
  for caso in casos:
    if caso.energia_total > energia:
      if energia_min < caso.energia_total < energia_max:
        novo_caso = caso
      else:
        break
    else:
      novo_caso = caso
    i += 1
  print(f"\nAdaptando caso do Cardapio Base {i}\n")
  caso_adaptado = adaptar_caso(novo_caso, energia_min, energia_max)
  lista_cardapio.append(caso_adaptado)
  return [lista_cardapio,i]
## Fun??o principal que inicia o programa
def start():
  while True:
    print("\n1: Pedir um prato ")
    print("0: Sair")
    opcao = int(input("\nDigite a opcao desejada: "))
    match opcao:
      case 0:
        return
      case 1:
        energia = int(input("\nDigite a energia m?dia desejada: "))
        limiar = int(input("Digite o limiar: "))
        informacao = escolher_prato(energia,limiar)
        lista_cardapio = informacao[0]
        indice = informacao[1]
        entrada_incorreta = True
        while entrada_incorreta:
          cardapio_num = int(input("\nDigite o n?mero do Cardapio desejado ou \"0\" para sair: "))
          if 1 <= cardapio_num < (len(lista_cardapio) + 1):
            entrada_incorreta = False
            print(f"\nCardapio {cardapio_num} escolhido")
            if{cardapio_num == 3}:
              casos.pop(indice)     
              casos.append(lista_cardapio[cardapio_num-1])
              print(f"\nCardapio Base {indice} modificado na base de dados")
            else:
              casos.append(lista_cardapio[cardapio_num-1])
              print(f"\nCardapio {cardapio_num} adicionado a base de casos")
          else:
            if 0 == cardapio_num:
              print(f"Nenhum Cardapio selecionado")
              entrada_incorreta = False
            else:
              entrada_incorreta = True
      case _:
        print("\nDigite um numero valido")

conhecidos = procurar_codigos(alimentos, alimentos_nut, conhecidos) # print(conhecidos)
iniciar_casos(10)
start()