import random #importa módulo random de python

def configuracion(): #establece configuración de la máquina. Pendiente meterle parámetros, pero habría que cambiar el código de la función
    rotoresDefault = {'I':'EKMFLGDQVZNTOWYHXUSPAIBRCJ','II':'AJDKSIRUXBLHWTMCQGZNPYFVOE','III':'BDFHJLCPRTXVZNYEIWGAKMUSQO','IV':'ESOVPZJAYQUIRHXLNFTGKDCMWB','V':'VZBRGITYUPSDNHLXAWMJQOFECK'}
    rotores = [] #crea una lista vacía para meter los rotores
    reflector = [] #crea una lista vacía para meter el reflector
    valid = False
    
    while not valid: #mientras valid es falso
        default = input('Rotores y Reflector por defecto de la Enigma I o aleatorios? (D/A) ')
        valid = True #pone valid a verdadero y lo pondrá a falso si falla algo
        if default.isalpha and default.upper() == 'A': #rodillos aleatorios
            rotorNum = input ('Cuantos rotores? ')
            if not rotorNum.isnumeric(): #si no es un número invalida
                valid = False
            abecedario = creaABC() #crea abecedario
            if (len(abecedario) % 2) != 0: #comprueba si el número de letras del abecedario es par, debe serlo para usar el reflector, que se empareja consigo mismo
                abecedario += '@' #si no es par añade el caracter @
            abecedarioLista = list(abecedario) #convierte a lista la cadena abecedario
            for _ in range(int(rotorNum)): #para el número de rotores
                rotor = abecedarioLista.copy() #copia lista abecedario a rotor
                random.shuffle(rotor) #reorganiza rotor al azar
                rotores.append(rotor) #añade rotor a la lista de rotores
            random.shuffle(abecedarioLista) #reorganiza abecedario al azar
            while len(abecedarioLista) > 0: #mientras queden letras sin emparejar en diccionario
                reflector.append((abecedarioLista[:1],abecedarioLista[-1:])) #añade pareja de la primera y la última letra de abecedario randomizado
                abecedarioLista.pop(0) #elimina la primera letra de abecedario, ya añadida a reflector
                abecedarioLista.pop(len(abecedarioLista)-1) #elimina la última letra de abecedario, ya añadida a reflector
            
        elif default.isalpha and default.upper() == 'D': #si rodillos por defecto
            abecedario = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #abecedario por defecto, sin Ñ
            reflector = [('A','E'),('B','J'),('C','M'),('D','Z'),('F','L'),('G','Y'),('H','X'),('I','V'),('K','W'),('N','R'),('O','Q'),('P','U'),('S','T')] #reflector A de Enigma I
            rotorNum = 3 #número de rotores por defecto
            for _ in range(rotorNum): #para cada rotor
                rotorName = input ('Elige el rotor 1 (I II III IV V): ')
                if rotorName.isalpha and rotoresDefault[rotorName.upper()]: #si es un rotor válido
                    rotores.append(rotoresDefault[rotorName.upper()]) #añade rotor correspondiente del diccionario por defecto
                else:
                    valid = False
    abecedario = abecedario.upper() #asegura que el diccionario está en mayúsculas
    rotorNum = int(rotorNum) #asegura que el número de rotores es entero
    config = (abecedario,reflector,rotores) #crea un tupla con la configuración
    return config

def creaABC(): #crea abecedario
    abecedario = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ' #abecedario por defecto
    valid = False
    while not valid: #mientras valid es falso y los rotores aleatorios permite elegir diccionario
        print('abecedario predeterminado =',abecedario) #muestra abecedario por defecto
        default = input('Quieres usar el diccionario predeterminado? (S/N) ')
        if default.isalpha and default.upper() == 'N': #si no quiere usar el abecedario por defecto
            valid = True #pone valid a verdadero
            abcAux = input ('Introduce el abecedario: ')
            for letra in abcAux: #recorre todas las letras del abecedario
                if not letra.isalpha() or abcAux.count(letra) > 1: #si no es letra o la letra se repite vuelve a poner valid a falso, en otro caso se mantiene verdadero
                    valid = False
            if valid: #si el abecedario introducido es válido lo copia a la variable por defecto
                abecedario = abcAux
        elif default.isalpha and default.upper() == 'S': #si quiere usar el abecedario por defecto pone valid a True
            valid = True
    return abecedario

def inputMensaje(): #introducir mensaje
    valid = False
    while not valid: #mientras valid es falso
        valid = True #pone valid a verdadero
        msg = input ('Introduce el mensaje: ')
        for letra in msg: #recorre todas las letras del mensaje
            if not letra.isalpha() and letra != ' ' and letra != '.': #si no es letra, espacio o punto vuelve a poner valid a falso, si no se mantiene verdadero
                valid = False
    return msg.upper() #pone el mensaje en mayúsculas para evitar que no coincida luego al comparar

def inicializa(rotores,abecedario): #inicializa el rotor en la letra seleccionada
    valid = False
    while not valid: #mientras valid es falso
        valid = True
        for rotorNum,rotor in enumerate(rotores):
            letra = input('Introduce una letra para establecer la posición inicial del rotor: ')
            if len(letra) == 1 and letra.isalpha() and letra.upper() in abecedario: #si la letra de inicialización es válida y se encuentra en abecedario devolverla
                pos = rotor.index(letra.upper()) #posición de la letra en el rotor
                rotores[rotorNum] = (rotor[pos:] + rotor[:pos]) #ponemos el rotor a 0 a la altura de la letra inicial y lo añadimos a la lista auxiliar
            else:
                valid = False
    return rotores

def avanza(rotores,pasos): #avanza los rotores en número de pasos acumulado
    caracteres = len(rotores[0]) #asigna el número de caracteres del rotor a la variable
    for rotorNum,rotor in enumerate(rotores): #mueve los rotores un número de pasos que depende del punto del mensaje en que nos encontremos
        while pasos > 0: #mientras queden pasos por recorrer
            vueltas = pasos // caracteres #saca las vueltas recorridas
            posicion = pasos % caracteres #calcula la posición en el rotor actual
            rotores[rotorNum] = rotor[pasos:] + rotor[:pasos] #coge desde la posición actual del rotor hasta el final y le suma lo anterior
            pasos = vueltas #reinicia pasos restantes para el siguiente rotor
            print('rotor {} posicion {} pasos restantes {}'.format(rotorNum+1,posicion,pasos)) #comprobación debug
            print(rotores[rotorNum][posicion]) #comprobación debug
    return rotores

def cruzaRotores(rotores,pos,reverse=False): #avanza a través del rotor
    if reverse: #invierte la lista de rotores si cruza en orden inverso
        rotores = reversed(list(rotores))
    for rotor in rotores:
        letra = rotor[pos] #según la posición de la letra en el avance anterior (abecedario para el 1º y último) elige la letra correspondiente en el rotor
        print('tras rotor:',letra,rotor.index(letra)) #comprobación debug
    return letra

def cruzaReflector(reflector,letra): #avanza a través de los rotores
    for pareja in reflector: #para cada pareja de letras del reflector
        if pareja[0].count(letra) > 0 or pareja[1].count(letra) > 0: #si encuentra la letra
            print('pareja reflector',pareja) #comprobación debug
            if pareja[0] == letra: #devuelve la derecha si está en el lado izquierdo
                letraCod = pareja[1]
            else: #devuelve la izquierda si está en el lado derecho
                letraCod = pareja[0]
    return letraCod

#donde ponga "#comprobación debug" es un print de variables para entender mejor qué está ocurriendo, eliminar # del inicio de línea para que lo muestre en consola
if __name__ == '__main__': #si se ejecuta directamente el programa en lugar de llamarlo desde otro hacer esto
    config = configuracion() #archivo de configuración para elegir número de rotores, cuáles o que los genere de forma aleatoria y el abecedario
    abecedario = config[0]  #recupera el diccionario creado en la configuración
    reflector = config[1] #recupera el reflector creado en la configuración

    while True: #bucle general del programa, es infinito, para romper "CTRL + C" en Windows, "command + ." en Mac
        rotoresInit = inicializa(config[2],abecedario) #pide letra para inicializar el rotor y crea una copia en el punto de inicio
        print(rotoresInit) #comprobación debug
        pasos = 1 #crea una variable para saber cuantos pasos debe avanzar los rotores, en el método avanza está implementada la lógica estilo cuentakilómetros
        mensajeCod = '' #define variable donde guardar el mensaje codificado
        mensaje = inputMensaje() #pide el mensaje a codificar, que está en una función aparte para incluir la validación
        #if mensaje !='': #si hay mensaje ejecuta código (sin implementar, para poder reiniciar la máquina)
        for letra in mensaje: #recorre cada letra del mensaje
            if letra != ' ' and letra != '.': #si no es espacio ni punto
                rotores = avanza(rotoresInit,pasos) #avanza rotores
                pasos += 1 #añade 1 paso por el avance del rotor
                posLetra = abecedario.index(letra) #saca su posición en la lista abecedario
                print('Letra pulsada:',letra,posLetra) #comprobación debug
                letraCod = cruzaRotores(rotores,posLetra) #según la posición de la letra en la lista devuelve la codificada
                letraCod = cruzaReflector(reflector,letraCod) #devuelve la pareja conectada mediante el reflector
                posLetra = rotores[len(rotores)-1].index(letraCod) #saca la posición en el rotor de la letra devuelta por el reflector
                inverted = True #pone la variable a True para que cruce los rotores en sentido inverso
                letraCod = cruzaRotores(rotores,posLetra,inverted) #según la posición de la letra en la lista devuelve la codificada (con un rotor es irrelevante)
                bombilla = abecedario[posLetra] #devuelve la letra codificada que corresponde a la posición del rotor en el abecedario
                print('bombilla:',bombilla,posLetra) #comprobación debug
            else: #si es espacio o punto lo añade directamente
                bombilla = letra
            mensajeCod += bombilla #añade la letra codificada a través de los rotores al mensaje
        print(mensajeCod) #imprime mensaje codificado