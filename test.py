import unittest
import enigma

class ABCTest(unittest.TestCase):
    def setUp(self):
        self.abecedario = enigma.creaABC()

    def test_ABC_AlphaOK(self):
        self.assertTrue(self.abecedario.isalpha)

    def test_ABC_UpperOK(self):
        self.assertTrue(self.abecedario.upper)

class ReflectorTest(unittest.TestCase):
    def test_reflejaOK(self):
        reflector = enigma.Reflector(['ABCDEFGHIJKLMNÑOPQRSTUVWXYZ','ZYXWVUTSRQPOÑNMLKJIHGFEDCBA'])
        self.assertEqual(reflector.refleja('A'), 'Z')
        
class RotorTest(unittest.TestCase):
    def setUp(self): 
        self.rotor = enigma.Rotor('ABCDEFG', 'CFAGBDE')

    def test_RotorConstruyeOK(self):
        self.assertEqual(self.rotor.conexion, ['ABCDEFG', 'CFAGBDE'])

    def test_RotorCodificaOK(self):
        self.assertEqual(self.rotor.codifica(0), 2)
        self.assertEqual(self.rotor.decodifica(4), 1)

    def test_RotorCodificaOK_con_pos_ini(self):
        self.rotor.pos_ini = 'C'
        self.assertEqual(self.rotor.pos_ini, 2)
        self.assertEqual(self.rotor.codifica(0), 5)
        self.assertEqual(self.rotor.decodifica(4), 2)

class EnigmaTest(unittest.TestCase):
    def setUp(self):
        self.mensaje = 'rosa'
    
    def test_codifica(self):
        pass
        #self.assertEqual(enigma.Enigma.codifica(self.mensaje),'FFEK')

if __name__ == '__main__':
    unittest.main()