import random
import time
import os
import re
while True:
    print("Menu Automata/Gramatica")
    print("Elija la opcion que desea hacer")
    print("A. Automatas")
    print("B. Gramaticas")
    print("C. Salir")
    opcion = input("Ingrese una opcion: ").upper()
    if opcion == "A":
        while True:
            os.system("cls")
            print("Automata")
            def lectura_Automata(archivo):
                with open(archivo, 'r') as f:
                    estados = int(f.readline().strip())
                    print(f"Numero de Estados -> {estados}")
                    sigma = int(f.readline().strip())
                    print(f"Tamaño de sigma -> {sigma}")
                    finales = int(f.readline().strip())
                    print(f"Tamaño de Estados Finales -> {finales}")
                    datos_sig = f.readline().strip().split()
                    sin_n = datos_sig[0].split("Sig")
                    sig = sin_n[1].strip("{}").split(",")
                    print(f"Valores de Sigma -> {sig}")
                    datos_f = f.readline().strip().split()
                    sin_t = datos_f[0].split("F")
                    fd = sin_t[1].strip("{}").split(",")
                    print(f"Valores de Estados Finales -> {fd}")
                    alcanzables = f.readlines()
                    acumulador = ""
                    for restantes_estados in alcanzables:
                        acumulador = acumulador + restantes_estados.strip()
                        patron = r">(.*?)(,|\})"
                        resultados = re.finditer(patron, acumulador)
                        valores = []
                    for aux in resultados:
                        valores.append(aux.group(1).strip().split(" | "))
                    print(f"Transiciones -> {valores}")
                    return sig, fd, valores
            def matriz_to_Dict(matriz, Sigma):
                tabla_transiciones = {}
                for i in range(len(matriz)):
                    estado = str(i)
                    transiciones = {}
                    for j in range(len(Sigma)):
                        simbolo = Sigma[j]
                        estado_destino = matriz[i][j] if i < len(matriz) and j < len(matriz[i]) else None
                        transiciones[simbolo] = estado_destino
                    tabla_transiciones[estado] = transiciones
                return tabla_transiciones
            def minimizacion(Sigma, Estados, Estado_inicial, Estados_finales, Transiciones):
                n = len(Estados)
                band = False
                for x in Transiciones.values():
                    for xy in x.values():
                        if len(xy) != 1 and xy != 'NULL':
                            band = True
                            break
                    if band:
                        break
                if band:
                    print("El autómata es no determinista, no se puede realizar la minimización.")
                    return
                particion_actual = [set(Estados_finales), set(Estados) - set(Estados_finales)]
                particion_anterior = []
                while particion_actual != particion_anterior:
                    particion_anterior = particion_actual.copy()
                    for i, particion in enumerate(particion_actual):
                        for simbolo in Sigma:
                            transiciones = {}
                            for estado in particion:
                                if Transiciones[estado].get(simbolo) is None:
                                   estado_destino = None
                                else:
                                   estado_destino = Transiciones[estado][simbolo]
                                if estado_destino in transiciones:
                                   transiciones[estado_destino].add(estado)
                                else:
                                   transiciones[estado_destino] = {estado}
                            particion_actual[i] = set.union(particion_actual[i], *[particion_actual[j] for j in range(len(particion_actual)) if transiciones.get(
                                list(particion_actual[j])[0]) is not None and len(particion_actual[j] & transiciones[list(particion_actual[j])[0]]) > 0])
                            particion_actual.extend([particion_actual[j] & transiciones[list(particion_actual[j])[0]] for j in range(len(particion_actual)) if transiciones.get(list(
                                particion_actual[j])[0]) is not None and len(particion_actual[j] & transiciones[list(particion_actual[j])[0]]) > 0 and particion_actual[j] not in particion_actual])
                tabla_transiciones_minimizada = {}
                for particion in particion_actual:
                    estado = list(particion)[0]
                    tabla_transiciones_minimizada[estado] = {}
                    for simbolo in Sigma:
                        estado_destino = None
                        for estado_en_particion in particion:
                            if Transiciones[estado_en_particion].get(simbolo) is not None:
                                estado_destino = Transiciones[estado_en_particion][simbolo]
                                break
                        for particion_destino in particion_actual:
                            if estado_destino in particion_destino:
                                tabla_transiciones_minimizada[estado][simbolo] = list(particion_destino)[0]
                                break
                print(f"Matriz de transiciones minimizada: {tabla_transiciones_minimizada}")
                for estado, transiciones in tabla_transiciones_minimizada.items():
                    for simbolo, estado_destino in transiciones.items():
                        print(f"{estado} > {simbolo} | {estado_destino}")
                estados_minimizados = list(particion_actual)
                estados_finales_minimizados = [particion for particion in particion_actual if particion & set(Estados_finales)]
                estado_inicial_minimizado = [list(particion)[0] for particion in particion_actual if Estado_inicial in particion]
                print("Estados minimizados:", estados_minimizados)
                print("Estados finales minimizados:", estados_finales_minimizados)
                print("Estado inicial minimizado:", estado_inicial_minimizado)
                print("Autómata minimizado:")
                for i, estado_minimizado in enumerate(estados_minimizados):
                    print(f"{i} : {estado_minimizado}")
                    if estado_minimizado in estados_finales_minimizados:
                        print(f"{i} Es estado final")
                    if estado_minimizado == estado_inicial_minimizado:
                        print(f"{i} Es estado inicial")
                    for simbolo in Sigma:
                        estado_destino_minimizado = tabla_transiciones_minimizada[list(estado_minimizado)[0]].get(simbolo)
                        for j, estado_minimizado_destino in enumerate(estados_minimizados):
                            if estado_destino_minimizado in estado_minimizado_destino:
                                print(f"{i} --{simbolo}--> {j}")
                                break
            def conseguir_estados(transicionesDict):
                estados = []
                for estado in transicionesDict:
                    estados.append(estado)
                    return estados
            estados_diferentes = []
            def buscar_diferentes(valores):
                for x in valores:
                    for xy in x:
                        if len(xy) != 1 and xy != 'NULL':
                            if xy not in estados_diferentes:
                                estados_diferentes.append(xy)
                return estados_diferentes
            def transiciones(valores, estados_afnd, sig):
                interaccion = []
                datos_leidos = []
                for valor_sigma in sig:
                    for j in estados_afnd:
                        interaccion = []
                        for i in j:
                            if i < len(valores) and sig.index(valor_sigma) < len(valores[i]):
                                interaccion.append(valores[i][sig.index(valor_sigma)])
                                datos_leidos.append(interaccion)
                return datos_leidos
            def convertir_afnd_a_afd(sig, fd, valores):
                nuevos_valores2 = []
                band = False
                for x in valores:
                    for xy in x:
                        if len(xy) != 1 and xy != 'NULL':
                            band = True
                            break
                    if band:
                        break
                if band:
                    time.sleep(5)
                    os.system("cls")
                    print("No es determinista")
                    nuevos_valores = buscar_diferentes(valores)
                    nuevos_valores2 = []
                    for num in nuevos_valores:
                        digitos = []
                        for digito in num:
                            if str(digito).isdigit():
                                digitos.append(int(digito))
                        nuevos_valores2.append(digitos)
                    fin = False
                    while fin == False:
                        nuevos_estados = transiciones(valores, nuevos_valores2, sig)
                        lista_final = []
                        for sublista in nuevos_estados:
                            nueva_sublista = []
                            valores_agregados = set()
                            for elemento in sublista:
                                for caracter in list(str(elemento)):
                                    if (
                                        caracter.isdigit()
                                        and caracter not in valores_agregados
                                        and caracter != 'N'
                                        and caracter != 'U'
                                        and caracter != 'L'
                                    ):
                                        nueva_sublista.append(int(caracter))
                                        valores_agregados.add(caracter)
                            lista_final.append(nueva_sublista)
                        for inser in nuevos_valores2:
                            lista_final.append(inser)
                        set_lista_final = set(map(tuple, lista_final))
                        set_nuevos_valores2 = set(map(tuple, nuevos_valores2))
                        resultado = set_lista_final.symmetric_difference(set_nuevos_valores2)
                        resultado = list(map(list, resultado))
                        if resultado == []:
                            fin = True
                        else:
                            for dar in resultado:
                                nuevos_valores2.append(dar)
                    nuevos_finales = set()
                    for x in range(len(valores)):
                        for y in range(len(valores[x])):
                            if valores[x][y] in fd:
                                nuevos_finales.add(valores[x][y])
                    temp_set = set()
                    for orden2 in nuevos_valores2:
                        orden2_ordenada = sorted(orden2)
                        tupla = tuple(orden2_ordenada)
                        temp_set.add(tupla)
                    nuevos_valores2 = [list(tupla) for tupla in temp_set]
                    nuevos_valores2.sort()
                    print("Nuevos Estados: ", nuevos_valores2)
                    print("Transiciones: ", set_lista_final)
                    print("Estados Finales: ", nuevos_finales)
                else:
                    print("Este Automata es determnista")
                return nuevos_valores2
            def generate_random_string(input_alphabet, max_length):
                return ''.join(random.choice(input_alphabet) for _ in range(random.randint(1, max_length)))
            def verificar_cadena(archivo):
                with open(archivo, 'r') as f: 
                    automaton_lines = f.readlines()
                    num_states = int(automaton_lines[0])
                    num_input_symbols = int(automaton_lines[1])
                    num_accept_states = int(automaton_lines[2])
                    input_alphabet = set(automaton_lines[3].strip().split('{')[1].split('}')[0].split(','))
                    accept_states = set(automaton_lines[4].strip().split('{')[1].split('}')[0].split(','))
                    transitions = {}
                for line in automaton_lines[5:]:
                 transitions_data = line.strip().split(',')
                 state = transitions_data[0].strip()
                for transition in transitions_data[1:]:
                    symbol, next_state = transition.strip().split(' | ')
                    transitions[(state, symbol)] = next_state
                print(f"Estados de Aceptacion {input_alphabet}")
                cad_val = False
                cad_eva = []
                while not cad_val:
                    input_string = input("Ingresa cadena: ")
                    if all(simbols in input_alphabet for simbols in input_string):
                        cad_eva = list(input_string)
                        cad_val = True
                        break
                    else:
                        cad_val = False
                        break
                if cad_val:
                    print(f"La cadena {input_string} es valida")   
                else:
                    print(f"La cadena {input_string} no es valida")    
            if __name__ == "__main__":
                Texto = str(input("Ingrese nombre del archivo: "))
                acep = True
                secuencia_aut = r'Aut[1-9]\.txt$'
                while acep == False:
                    if Texto == "" or re.match(secuencia_aut, Texto) == None:
                        print("No ingrese un archivo valido o ingreso nada")
                        Texto = str(input("Ingrese nombre del archivo: "))
                        acep = True
                        if acep == False:
                            pass
                        else:
                            break
                while True:
                    os.system("cls")
                    print("1) Conversion")
                    print("2) Minimizacion")
                    print("3) Verificar cadena")
                    print("4) Salir")
                    opcion = (input("Ingrese una opcion: "))
                    if opcion == '1':
                        os.system("cls")
                        sig, fd, valores = lectura_Automata(Texto)
                        convertir_afnd_a_afd(sig, fd, valores)
                        time.sleep(11)
                    elif opcion == '2':
                        os.system("cls")
                        sig, fd, valores = lectura_Automata(Texto)
                        Estado_inicial = sig[0]
                        diccionario_transiciones = matriz_to_Dict(valores, sig)
                        estados = conseguir_estados(diccionario_transiciones)
                        minimizacion(sig, estados, Estado_inicial, fd, diccionario_transiciones)
                        time.sleep(22)
                    elif opcion == '3':
                        os.system("cls")
                        verificar_cadena(Texto)
                        time.sleep(5)
                    elif opcion == '4':
                        os.system("cls")
                        exit()
                    else:
                        os.system("cls")
                        print("Opcion invalida")
                        time.sleep(5)
                    os.system("cls")
                    print("¿Seguimos con el mismo automata?")
                    print("1) Si")
                    print("2) No")
                    opc = input("Ingrese su opcion: ").upper()
                    while opc != '1' and opc != '2':
                        opc = input("Ingrese su opcion nuevamente: ").upper()
                    if opc == '2':
                       Texto = str(input("Ingrese nombre del archivo: "))                          
    elif opcion == "B":
        while True:
            os.system("cls")
            print("Gramatica")
            def StringstoString(lista):
                palabra = ""
                for i in range(len(lista)):
                    palabra += lista[i]
                return palabra
            def cargar_gramatica():
                Texto = str(input("Ingrese nombre del archivo: "))
                acep = True
                secuencia_aut = r'Gram[1-4]\.txt$'
                while acep == False:
                    if Texto == "" or re.match(secuencia_aut, Texto) == None:
                        print("No ingrese un archivo valido o ingreso nada")
                        Texto = str(input("Ingrese nombre del archivo: "))
                        acep = True
                        if acep == False:
                            pass
                        else:
                            break
                with open(Texto, "r") as tex:
                    T, NT, Filas, Columnas = [int(tex.readline().strip()) for _ in range(4)]
                    NT = list(tex.readline().replace('N{', '').replace('}', '').replace(',', '').strip())
                    T = list(tex.readline().replace('T{', '').replace('}', '').replace(',', '').strip())
                    texto = tex.read()
                    matriz = {}
                    for auxiliar in texto.split('{')[-1].split('}')[0].split(','):
                        auxiliar2, auxiliar3 = auxiliar.strip().split('>')
                        matriz[auxiliar2.strip()] = list({auxiliar3.strip() for auxiliar4 in auxiliar3.strip('|')})
                    NuevaMatriz = []
                    NuevaMatriz.extend(matriz.values())
                    NuevaMatriz2 = []
                    for i in range(len(NuevaMatriz)):
                        NuevaMatriz2.append(NuevaMatriz[i])
                    print("Vector No terminales: ", NT)
                    print("Vector Terminales: ", T)
                    print("Tamaño de matriz de solucion", len(NuevaMatriz2))
                    print("Matriz de solucion:")
                    for i in range(len(NuevaMatriz2)):
                       auxiliar = NuevaMatriz2[i][0]
                       auxiliar = auxiliar.split(' | ')
                       print(auxiliar)
                return NuevaMatriz2, NT, T
            def generar_cadenas_aleatorias(NuevaMatriz2, NT, T):
                Matriz_corregida = []
                for i in range(0, len(NuevaMatriz2)):
                    auxiliar = NuevaMatriz2[i][0]
                    auxiliar = auxiliar.split(' | ')
                    Matriz_corregida.append(auxiliar)
                generador = Matriz_corregida[0][random.randint(0, len(Matriz_corregida[0]) - 1)]
                print(generador)
                while True:
                    for i in range(len(generador)):
                        for j in range(len(NT)):
                            print(generador)
                            if NT[j] in generador[i]:
                                Z = random.randint(0, len(Matriz_corregida[j]) - 1)
                                generador2 = Matriz_corregida[j][Z]
                                generador = list(generador)
                                generador.pop(i)
                                generador.insert(i, generador2)
                                generador = StringstoString(generador)
                                generador = list(generador)
                                cont = 0
                                for k in range(len(T)):
                                    cont += generador.count(T[k])
                                if cont == len(StringstoString(generador)):
                                    generador = StringstoString(generador)
                                    print(generador)
                                    return
                                else:
                                    generador = StringstoString(generador)
                    break
            def reglas_recursivas(NuevaMatriz2, NT):
                for i in range(len(NuevaMatriz2)):
                    auxiliar = NuevaMatriz2[i][0]
                    auxiliar = auxiliar.split(' | ')
                n = 0
                recursion = 0
                while n <= len(NuevaMatriz2) - 1:
                    j = 0
                    while j <= len(NuevaMatriz2[n]) - 1:
                        a = NuevaMatriz2[n][j]
                        b = NT[n]
                        if b in a:
                            print(f"La recursión {NT[n]} se encuentra en {NuevaMatriz2[n][j]}")
                            recursion = recursion + 1
                        j = j + 1
                    n = n + 1
                print("Recursiones encontradas:", recursion)
            def menu():
                gramatica_cargada = False
                NuevaMatriz2 = []
                NT = []
                T = []
                while True:
                    os.system("cls")
                    print("1. Cargar Gramática")
                    print("2. Generar Cadenas Aleatorias")
                    print("3. Reglas Recursivas")
                    print("4. Salir")
                    opcion = input("Selecciona una opción: ")
                    if opcion == "1":
                        NuevaMatriz2, NT, T = cargar_gramatica()
                        gramatica_cargada = True
                        input("Gramática cargada. Presione Enter para continuar")
                    elif opcion == "2":
                        if not gramatica_cargada:
                            print("No se ha cargado ninguna gramática. Por favor, carga una gramática primero.")
                            time.sleep(2)
                            continue
                        generar_cadenas_aleatorias(NuevaMatriz2, NT, T)
                        pregunta = input("¿Quieres seguir trabajando con esta gramática? (s/n): ")
                        if pregunta.lower() != "s":
                            gramatica_cargada = False
                    elif opcion == "3":
                        if not gramatica_cargada:
                            print("No se ha cargado ninguna gramática. Por favor, carga una gramática primero.")
                            time.sleep(2)
                            continue
                        reglas_recursivas(NuevaMatriz2, NT)
                        pregunta = input("¿Quieres seguir trabajando con esta gramática? (s/n): ")
                        if pregunta.lower() != "s":
                            gramatica_cargada = False
                    elif opcion == "4":
                        exit()
                        break
                    else:
                        print("Opción inválida. Por favor, selecciona una opción válida.")
                        time.sleep(2)
            menu()    
    elif opcion == "C":
        exit()
        break                
