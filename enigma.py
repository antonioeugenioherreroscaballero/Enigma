import random

class Reflector():
    def __init__(self,abecedario,conf=''):
        if conf == '':
            reflejo = ''
            reflejoLista = list(abecedario)
            random.shuffle(abecedario)
            for letra in reflejoLista:
                reflejo += letra
            self.configuracion = (abecedario,reflejo)
        else:
            reflejoLista = list(conf)
            for letra in abecedario:
                if letra in conf:
                    reflejoLista.remove(letra)
            if len(reflejoLista) > 0:
                print('Sobran letras en el bastidor derecho')
            else:
                self.configuracion = (abecedario,conf)

    def refleja(self,indice):
        letra = self.configuracion[0][indice]
        return self.configuracion[1].index(letra)

class Rotor():
    def __init__(self,abecedario,conexiones=''):
        self.abecedario = abecedario
        self.conexiones = conexiones
        self._idx_ini = None
        self._idx_salto = None
        self.salto = False
    
    def inicializa(self):
        self.abecedario = self.abecedario[self._idx_ini:] + self.abecedario[:self._idx_ini]
        self.conexiones = self.conexiones[self._idx_ini:] + self.conexiones[:self._idx_ini]
        self._idx_salto = self._idx_ini

    def avanza(self):
        self.abecedario = self.abecedario[1:] + self.abecedario[:1]
        self.conexiones = self.conexiones[1:] + self.conexiones[:1]
        if self.abecedario.index(self.abecedario[0]) == self._idx_salto:
            self.salto = True

    def codifica(self, indice):
        letra = self.abecedario[indice]
        indice_izda = self.conexiones.index(letra)
        return indice_izda

    def decodifica(self, indice):
        letra = self.conexiones[indice]
        indice_dcha = self.abecedario.index(letra)
        return indice_dcha

    @property
    def idx_ini(self):
        return self._idx_ini

    @idx_ini.setter
    def idx_ini(self, value):
        self._idx_ini = self.abecedario.index(value)

    '''
        TODO:
            - Conexion: Lista de cadenas (abecedario, cortocircuito) que 
              determina la entrada y salida según el caracter de salida o entrada
            - Posicion: Indice/caracter en posición cero de la conexión
            - Pasos ¿?: Número de pasos girados desde que empezamos a codificar
            - Salto: Indice, caracter de abecedario en que se obliga al salto del 
              siguiente rotor si lo hubiera
            - swSalto ¿?: True o False
            - codifica(indice): Devuelve el pin de salida
            - decodifica(indice): Devuelve el pin de entrada
            - avanza(): Rota una posición la conexión. Comprueba si debe activar swSalto 
    '''

class Enigma():
    abecedario = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    def __init__(self):
        self.reflectorConf = ('ZYXWVUTSRQPOÑNMLKJIHGFEDCBA')
        self.reflector = ()
        self.rotoresConf = ('ÑMHCKWNOJFZEPSUBGRXAIQTVYLD',)
        self.rotores = ()
        self.mensaje = ''
        self.mensajeCod = ''

    def configura(self): #establece configuración de la máquina.
        self.abecedario = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #ETW abecedario por defecto Enigma I
        reflectoresDefault = {'A':'EJMZALYXVBWFCRQUONTSPIKHGD','B':'YRUHQSLDPXNGOKMIEBFZCWVJAT','C':'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
        rotoresDefault = {'I':'EKMFLGDQVZNTOWYHXUSPAIBRCJ','II':'AJDKSIRUXBLHWTMCQGZNPYFVOE','III':'BDFHJLCPRTXVZNYEIWGAKMUSQO', #Enigma I (1930)
        'IV':'ESOVPZJAYQUIRHXLNFTGKDCMWB','V':'VZBRGITYUPSDNHLXAWMJQOFECK', #M3 Army (DEC 1938)
        'VI':'JPGVOUMFYQBENHZRDKASXLICTW','VII':'NZJHGRCXMYSWBOUFAIVLPEKQDT','VIII':'FKQHTLXOCBJSPDZRAMEWNIUYGV'} #M3 (1939) & M4 Naval (FEB 1942)
        rotorNum = 3
        rotorCon = ''
        rotores = []
        valid = False

        while not valid: #mientras valid es falso
            default = input('Rotores y Reflector por defecto de la Enigma I (I), M3Army (M), M4Naval (N) o aleatorios? ')
            valid = True #pone valid a verdadero y lo pondrá a falso si falla algo  

            if default.isalpha and default.upper() == 'I': #si es Enigma I abecedario por defecto, reflector A, 3 rotores
                self.reflectorConf = (reflectoresDefault['A'])
                rotorName = ('I','II','III')
                for rotor in range(rotorNum):
                    rotores.append(rotoresDefault[rotorName[rotor]]) #añade rotor correspondiente de rotoresDefault
                    rotorIni = input ('Elige la letra para la posicion inicial del rotor {}: '.format(rotor+1))
                    if rotorIni.isalpha and rotorIni.upper() in self.abecedario: #si la letra está en el abecedario
                        self.rotor.idx_ini = rotorIni
                        rotorName[rotor].inicializa()
                        
                    else:
                        valid = False

                    self.rotoresConf = (rotoresDefault[rotorName[rotor]])

            elif default.isalpha and default.upper() == 'M': #si es M3Army abecedario por defecto, reflector A, 3 rotores de 5
                self.reflectorConf = (reflectoresDefault['A'])
                for rotor in range(rotorNum): #para cada rotor
                    rotorName = input ('Elige el rotor', rotor+1 ,'(I II III IV V): ')
                    if rotorName.isalpha and rotorName.upper() in ('I','II','III','IV','V'): #si es un rotor válido del I al V
                        rotores.append(rotoresDefault[rotorName.upper()]) #añade rotor correspondiente de rotoresDefault
                    else:
                        valid = False

            elif default.isalpha and default.upper() == 'N': #si es M4Navy abecedario por defecto, reflector A, 3 rotores de 8
                self.reflectorConf = (reflectoresDefault['A'])
                for rotor in range(rotorNum):
                    rotorName = input ('Elige el rotor', rotor+1 ,'(I II III IV V VI VII VIII): ')
                    if rotorName.isalpha and rotorName.upper() in rotoresDefault: #si es un rotor válido en rotoresDefault
                        rotores.append(rotoresDefault[rotorName.upper()]) #añade rotor correspondiente
                    else:
                        valid = False

            else: #en cualquier otro caso reflector y rotores aleatorios
                abecedario = creaABC() #crea abecedario
                self.abecedario = abecedario
                self.reflectorConf = None
                numeroRotores = input ('Cuantos rotores? ')
                if not numeroRotores.isnumeric(): #si no es número pone valid a False
                    valid = False
                else:
                    rotorNum = int(numeroRotores)
                for rotor in range(rotorNum):
                    rotorConList = list(abecedario)
                    random.shuffle(rotorConList) #reorganiza rotor al azar
                    for letra in rotorCon:
                        rotorCon += letra
                    rotores.append(rotorCon) #añade rotor correspondiente
        self.rotoresConf = tuple(rotores)
        
    def codifica(self,mensaje):
        mensajeCod = ''
        self.reflector = Reflector(self.abecedario,self.reflectorConf)
        self.rotores = []
        for rotor in range(len(self.rotoresConf)):
            self.rotor = Rotor(self.abecedario,self.rotoresConf[rotor])
            rotorIni = input ('Elige la letra para la posicion inicial del rotor {}: '.format(rotor+1))
            if rotorIni.isalpha and rotorIni.upper() in self.abecedario: #si la letra está en el abecedario
                self.rotor.idx_ini = rotorIni.upper()
                self.rotor.inicializa()
            self.rotores.append(self.rotor)

        print(self.abecedario)
        for letra in mensaje:
            print('letra: {} {}'.format(letra,self.abecedario.index(letra))) #comprobación debug
            for rotorNum,rotor in enumerate(self.rotores):
                if rotorNum == 0:
                    rotor.avanza()
                else:
                    if self.rotores[rotorNum-1].salto == True:
                        rotor.avanza()
                indiceCod = rotor.codifica(self.abecedario.index(letra))
                print('tras rotor: {} {}'.format(self.abecedario[indiceCod],indiceCod)) #comprobación debug
            indiceCod = self.reflector.refleja(indiceCod)
            print('tras reflector: {} {}'.format(self.abecedario[indiceCod],indiceCod)) #comprobación debug
            for rotorNum,rotor in enumerate(self.rotores):
                indiceCod = self.rotor.decodifica(indiceCod)
                letraCod = self.abecedario[indiceCod]
                print('tras rotor_back: {} {}'.format(letraCod,indiceCod)) #comprobación debug
            mensajeCod += letraCod
        print(mensajeCod)
        '''
        TODO:
            - reflector: su configuración prefijada en principio
            - rotor: su conexión prefijada en principio
            - posi_inicial: Letra inicial del rotor (indice?)
            - codifica(mensaje): Transforma el mensaje en uno nuevo. Solo hay una dirección.
            Si se pasa la salida de codifica como entrada volviendo la posi_inicial. Obtenemos
            la otra entrada. 
        '''

def creaABC():
    abecedario = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ' #abecedario por defecto
    valid = False
    while not valid: #mientras valid es falso solicita diccionario
        print('abecedario español predeterminado =',abecedario) #muestra abecedario por defecto
        default = input('Quieres usar el diccionario español predeterminado? (S/N) ')
        if default.isalpha and default.upper() == 'S': #si usa abecedario por defecto pone valid a True y sale del bucle
            valid = True
        elif default.isalpha and default.upper() == 'N': #si no quiere usar el abecedario por defecto
            valid = True #pone valid a verdadero y cambiará si hay errores
            abcAux = input ('Introduce el abecedario: ')
            for letra in abcAux: #recorre las letras del abecedario recién creado
                if not letra.isalpha() or abcAux.count(letra) > 1: #si no es letra o ésta se repite pone valid a falso
                    valid = False
            if valid: #si el abecedario introducido es válido lo copia a la variable por defecto en mayúsculas
                abecedario = abcAux.upper()
    return abecedario
    
def inputMensaje():
    valid = False
    while not valid: #mientras valid es falso solicita mensaje
        valid = True #pone valid a verdadero y cambiará en caso de error
        msg = input ('Introduce el mensaje: ')
        for letra in msg: #recorre las letras del mensaje
            if not letra.isalpha() and letra != ' ' and letra != '.' and letra != ',': #si no es una letra, espacio, punto o coma, valid es falso
                valid = False
    return msg.upper() #devuelve el mensaje en mayúsculas para evitar que no coincida al comparar las letras en enigma

if __name__ == '__main__':
    enigma = Enigma() #crea una máquina Enigma
    conf = input('Quieres usar la Enigma por defecto del excel de Manuel (M) o configurarla? ')
    if not conf.isalpha() or conf.upper() != 'M':
        enigma.configura() #configura la máquina
    while True: #bucle general del programa, es infinito, para romper "CTRL + C" en Windows, "command + ." en Mac
        mensaje = inputMensaje() #guarda el mensaje a codificar, llama a una función aparte para incluir la validación
        enigma.codifica(mensaje) #llama a Enigma para iniciar la codificación/decodificación