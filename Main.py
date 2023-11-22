import tkinter as tk
from tkinter import messagebox
import unittest


# Clase principal del juego
class NumberLinkGame:
    # Constructor: inicializa el juego con el tablero proporcionado
    def __init__(self, board):
        self.board = board # Tablero del juego
        self.root = tk.Tk()  # Ventana principal del juego
        self.root.title("NumberLink/FreeFlow")
        self.selected = None # Número actualmente seleccionado
        self.path = [] # Camino actual entre dos números
        self.caminos = set()
        self.size = len(board)

        # Mostrar el tablero en la interfaz
        self.buttons = [[None for _ in row] for row in board]
        for i in range(len(board)):
            for j in range(len(board[0])):
                text = board[i][j] if board[i][j] != 0 else ""
                btn = tk.Button(self.root, text=str(text), width=5, height=2)
                btn.grid(row=i, column=j)
                btn.bind("<Button-1>", lambda event, x=i, y=j: self.on_click(x, y))
                btn.bind("<Button-3>", lambda event, x=i, y=j: self.undo(x, y))
                self.buttons[i][j] = btn

    # Función llamada cuando se hace clic en una casilla
    def on_click(self, x, y):
        # Si el usuario hace clic en una casilla vacía y ya ha seleccionado un número:
        if self.board[x][y] == 0 and self.selected:
            # Marcar la casilla como parte del camino actual.
            # Check that the move is not diagonal
            if self.path:
                last_x, last_y = self.path[-1]
                if abs(last_x - x) + abs(last_y - y) != 1:
                    return
            self.path.append((x, y))
            # Cambiar el color de fondo de la casilla para mostrar que es parte del camino.
            self.buttons[x][y].config(bg="gray")

        # Si el usuario hace clic en una casilla con un número:
        elif self.board[x][y] != 0:
            # Si no hay un número seleccionado previamente:
            if not self.selected:
                # Establecer el número como seleccionado.
                self.selected = (x, y)
                # Iniciar un nuevo camino desde este número.
                self.path = [(x, y)]
                # Cambiar el color de fondo del número seleccionado.
                self.buttons[x][y].config(bg="green")

            # Si ya hay un número seleccionado previamente:
            else:
                # Verificar si el número en la casilla actual coincide con el número seleccionado
                # y que no sea la misma casilla que se seleccionó inicialmente:
                if self.board[x][y] == self.board[self.selected[0]][self.selected[1]] and (x, y) != self.selected:
                    # Finalizar el camino en el número actual.
                    self.path.append((x, y))
                    # Recorrer cada casilla en el camino y configurar su valor y color.
                    for px, py in self.path:
                        self.board[px][py] = self.board[self.selected[0]][self.selected[1]]
                        self.buttons[px][py].config(bg="yellow")
                    # Resetear las variables de selección y camino.
                    self.selected = None
                    self.path = []
                    # Verificar si el juego ha sido completado.
                    self.check_game_completion()
                # Si el usuario selecciona un número diferente al seleccionado inicialmente:
                else:
                    # Resetear el camino anterior.
                    for px, py in self.path:
                        self.buttons[px][py].config(bg="white")
                    # Establecer el nuevo número como seleccionado.
                    self.selected = (x, y)
                    # Iniciar un nuevo camino desde este número.
                    self.path = [(x, y)]
                    # Cambiar el color de fondo del número seleccionado.
                    self.buttons[x][y].config(bg="green")

    # Función para deshacer el camino seleccionado
    def undo(self, x, y):
        # Allow undo only for the cells in the current path
        # Obtener el número de la casilla en la que se hizo clic derecho (para deshacer).
        if (x, y) in self.path:
            number = self.board[x][y]
            # If the undone cell contains a number, clear the entire path for that number, but keep the number
            # Si la casilla seleccionada ya es parte de un camino existente (y no es el camino actual):
            # Encontrar los puntos iniciales y finales de ese número.
            starting_points = []
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == number:
                        starting_points.append((i, j))


            # Deshacer_todo el camino de ese número, excepto los puntos iniciales y finales.
            if number != 0 and (x, y) != self.selected:
                for i in range(len(self.board)):
                    for j in range(len(self.board[0])):
                        if self.board[i][j] == number and (i, j) != self.selected:
                            self.board[i][j] = 0
                            self.buttons[i][j].config(bg="white", text="")
                self.selected = None
                self.path = []
            elif (x, y) == self.selected:
                # If only the selected number is clicked, just deselect it
                self.selected = None
                self.path = []
                self.buttons[x][y].config(bg="white")
            else:
                self.path.remove((x, y))
                self.buttons[x][y].config(bg="white", text="")
                self.board[x][y] = 0

    # Verificar si el juego ha sido completado
    def check_game_completion(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return
        messagebox.showinfo("Felicitaciones!", "Has completadoo el juego")

    # Función para iniciar y mostrar el juego
    def run(self):
        self.root.mainloop()
    
    #corregido?
    def contarParesNumeros(self):
        conteo_numeros={}
        for fila in self.board:
            for celda in fila:
                if celda != 0:
                    conteo_numeros[celda]=conteo_numeros.get(celda,0)+1
        for numero, conteo in conteo_numeros.items():
            if conteo != 2:
                raise ValueError("El numero "+str(numero)+" no tiene dos pares")
        return len(conteo_numeros)
    
    def imprimirTablero(self):
        for fila in self.board:
            fila_para_imprimir=' '.join(str(celda) if celda != 0 else '.' for celda in fila)
            print(fila_para_imprimir)

    def obtenerTodosLosNumeros(self):
        numeros=set()
        for fila in self.board:
            for celda in fila:
                if celda != 0:
                    numeros.add(celda)
        return numeros
    
    def encontrarNumero(self, num):
        for i, fila in enumerate(self.board):
            for j, celda in enumerate(fila):
                if celda == num:
                    return i, j
        return None
    
    #Corregido?
    def verificarCamino(self, inicio, numero, caminos):
        visitados = set([inicio])
        stack = [inicio]
        
        while stack:
            x, y = stack.pop()
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Direcciones de movimiento permitidas
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]):  # Asegurar que estamos dentro del tablero
                    if (nx, ny) not in visitados:
                        if self.board[nx][ny] == 0 or self.board[nx][ny] == numero:
                            visitados.add((nx, ny))
                            stack.append((nx, ny))
        
        # Al final, necesitas verificar que el conjunto visitados contiene las dos celdas con el número dado
        # y que estas celdas son los únicos lugares donde aparece el número en el camino.
        posiciones_numero = [(i, j) for i, fila in enumerate(self.board) for j, valor in enumerate(fila) if valor == numero]
        return all(pos in visitados for pos in posiciones_numero) and len(posiciones_numero) == 2




    ### corregido?
    #### en desuso actualmente ####
    def movimientoValidado(self, x, y, numero, visitados, caminos):
        if not (0 <= x < len(self.board) and 0 <= y < len(self.board[0])):
            return False
        
        if (x, y) in visitados or (x, y) in caminos:
            return False
        
        # La celda está vacía o contiene el número que queremos mover.
        return self.board[x][y] in (0, numero)


    
    #corregido?
    def validarSolucionCompleta(self):
        numeros = self.obtenerTodosLosNumeros()
        caminos=set()
        
        for num in numeros:
            inicio = self.encontrarNumero(num)
            if not inicio or not self.verificarCamino(inicio, num, caminos):
                return False
            
        if any(self.board[i][j] == 0 for i, fila in enumerate(self.board) for j, celda in enumerate(fila) if (i, j) not in caminos):
            return False
        return True
    ####################################################################
    #Backtracking
    def resolver(self):
        self.caminos = set()

        numero_para_resolver = self.obtenerSiguienteNumero()
        if numero_para_resolver is None:
            return True
        
        inicio = self.encontrarNumero(numero_para_resolver)

        return self.intentarResolverDesde(inicio, numero_para_resolver)

    def intentarResolverDesde(self, inicio, numero):
        x,y = inicio

        if self.board[x][y] == numero and (x,y) != inicio:
            return True
        
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if self.movimientoValido(nx, ny, numero):
                self.hacerMovimiento(nx, ny, numero)
                self.marcarCamino(nx, ny, numero)
                if self.intentarResolverDesde((nx,ny), numero):
                    return True
                self.deshacerMovimiento(nx, ny, numero)
        
        return False
    
    def esNumeroConectado(self, numero):
        posiciones = [pos for  pos, val in self.enumerarTablero() if val == numero]
        if len(posiciones) != 2:
            return False
        return all(pos in self.caminos for pos in posiciones)
    
    def enumerarTablero(self):
        for i, fila in enumerate(self.board):
            for j, celda in enumerate(fila):
                yield (i, j), celda

    def movimientoValido(self, x, y, numero, visitados=None, caminos=None):
        # Verifica si la posición está dentro de los límites del tablero.
        if not (0 <= x < len(self.board) and 0 <= y < len(self.board)):
            return False
        # Verifica si la celda está ocupada por un número diferente.
        if self.board[x][y] not in (0, numero):
            return False
        # Si se proporcionan, verifica si la celda ya ha sido visitada o está en los caminos.
        if visitados is not None and (x, y) in visitados:
            return False
        if caminos is not None and (x, y) in caminos:
            return False
        # Si todas las comprobaciones pasan, el movimiento es válido.
        return True
    

    def movimientoValido2(self, x, y, numero, visitados=None, caminos=None):
        # Verifica si la posición está dentro de los límites del tablero.
        if not (0 <= x < len(self.board) and 0 <= y < len(self.board)):
            return False
        # Verifica si la celda está ocupada por un número diferente.
        if self.board[x][y] not in (0, numero):
            return False
        
        # Si todas las comprobaciones pasan, el movimiento es válido.
        return True

    
    def hacerMovimiento(self, x,y, numero):
        self.board[x][y] = "#"
        self.caminos.add((x,y))

    def deshacerMovimiento(self, x,y, numero):
        self.board[x][y] = 0
        self.caminos.remove((x,y))

    def marcarCamino(self, x,y, numero):
        self.caminos.add((x,y))
        self.board[x][y] = numero

    #corregido?
    def obtenerSiguienteNumero(self):
        for numero in sorted(self.obtenerTodosLosNumeros()):
            if not self.esNumeroConectado(numero):
                return numero
        return None

    

    ####################################################################
    #en desuso actualmente
    def verificarCaminoCompleto(self, numero, visitados):
        return sum(1 for x, y in visitados if self.board[x][y] == numero) == 2
    

    ####################################################################
    #### heuristicas ####

    ### mal
    instacia_tablero = [[]]
    #tupla de visitados        
    l_tupla = ()
    punto0 = (0,0)
    
    def resolver_tablero(self):
        
          
        cortos = self.priorizar_cortos()
        lista2 = []
        lista_tuplas2 = []
        for i , enumerable in enumerate(cortos):
            lista2.append(cortos[i][0])
            lista_tuplas2.append(cortos[i][1][0])


        lista_tuplas3 = set()
        #con este for lo podemos jugar para cada numero 
        global instacia_tablero 
        instacia_tablero = self.board  
        global l_tupla  
        l_tupla = self.caminos 
        global punto0
        print("XXXXXXXXXXXXXXXXXXXXX")
        [print(" ".join(map(str, fila))) for fila in instacia_tablero]
        for i , j in zip(lista2, lista_tuplas2):
            print("ENTRA")
            
            print(i,j)
            #función que guarde la instancia del tablero 
            
            
            punto0 = j
            if (self.resolver_numero(j, i,set(), self.board) == True):                
                self.board = instacia_tablero
                lista_tuplas3 = self.caminos | lista_tuplas3
                self.caminos= lista_tuplas3   
                
            else:
                print("este es el else")
                [print(" ".join(map(str, fila))) for fila in instacia_tablero]

            

         
            

            
            
            
        print("mapa resuelto")    
        [print(" ".join(map(str, fila))) for fila in instacia_tablero]
        print(self.caminos)
        print("----------------")
        
        
        return True
        
        #siclo que me llame la función resolver numero para cada una de estas 
        # resolver_numero(self, 1(x,y), 1, visitados=None)

        #lo que saca la función es la matriz modificada y el valor de self.caminos con los espacios invalidos 
    
    ### mal
    def resolver_numero(self, inicio, numero, visitados, boards):
        validar = False
        print("entramos en esta función")
        
        #se entra a camino solo cuando se conecta , esto me gusta 
        self.caminos = visitados
        if visitados is None:
            visitados = set()
            print("entramos a opción 1")
        if self.esNumeroConectado(numero):
            print("----------------hola---------------")
            print("entramos a opción 2")
            return True

        
        else:
            print("entramos a opción 3")
            validar1 = False
            validad2 = False
            x,y = inicio
            visitados.add((x,y))
            print(f"Iniciando desde {inicio}") 
            


            #estos dos son los for que hacen el movimento desde el punto inicio 
            
            #for que ve que no lo tenga de vecino  este for actua hasta llegar a la solución o un punto encerrado
            for dx, dy in [(x,(y+1)),((x+1),y),(x, (y-1)),((x-1),y)]:
                if (dx, dy) not in visitados and self.movimientoValido(dx, dy, numero):
                    print("entramos a opción 3,1")
                    if self.board[dx][dy] == numero :
                            print("entramos a opción 3,1,1")
                            visitados.add((dx,dy))
                            print(self.caminos)
                            validar1 = True
                            print("CONECTADO")
                            global instacia_tablero
                            instacia_tablero = self.board
                            global l_tupla  
                            l_tupla = self.caminos 
                            global punto0
                            punto0 = (dx,dy)
                            [print(" ".join(map(str, fila))) for fila in instacia_tablero]
                            print("XXXXXXXXXXXXXXXXXXXXX")
                            return True
                    else:
                        print("entramos a opción 3,1,2")
                else:
                    print("entramos a opción 3,2")

            #for para hacer movimiento, este es complejo    
            for dx, dy in [(x,(y+1)),((x+1),y),(x, (y-1)),((x-1),y)]:
                if ((dx, dy) not in visitados and self.movimientoValido(dx, dy, numero) and validar1 == False):
                    print("entramos a opción 4,1")
                    if ( (self.esNumeroConectado(numero) == False) and self.movimientoValido(dx, dy, numero)):
                        validad2 = True
                        self.hacerMovimiento(dx, dy, numero)
                        print(x,y)
                        print(f"Movimiento realizado a {(dx, dy)}")
                        
                        self.resolver_numero( (dx,dy), numero, visitados, self.board)
                        #[print(" ".join(map(str, fila))) for fila in self.board]
                        print("entramos a opción 4,1,1")
                    else:
                        print("entramos a opción 4,1,2")
                """elif((dx, dy) not in visitados and self.movimientoValido2(dx, dy, numero) and validar1 == False):
                    print("entramos a opción 4,2")
                    if ( (self.esNumeroConectado(numero) == False) and self.movimientoValido(dx, dy, numero)):
                        self.resolver_numero(punto0 ,numero , l_tupla ,instacia_tablero)  
                        validad2 = True
                        self.hacerMovimiento(dx, dy, numero)
                        print(x,y)
                        print(f"Movimiento realizado a {(dx, dy)}")
                        
                        self.resolver_numero( (dx,dy), numero, visitados, self.board)
                        #[print(" ".join(map(str, fila))) for fila in self.board]
                        print("entramos a opción 4,2,1")
                    elif((self.esNumeroConectado(numero) == False) ):
                        validad2 = True
                        self.hacerMovimiento(dx, dy, numero)
                        print(x,y)
                        print(f"Movimiento realizado a {(dx, dy)}")
                        
                        self.resolver_numero( (dx,dy), numero, visitados, self.board)
                       #[print(" ".join(map(str, fila))) for fila in self.board]
                        print("entramos a opción 4,2,2")
                        self.resolver_numero(punto0 ,numero , l_tupla ,instacia_tablero)  
                    else:
                        
                        print("entramos a opción 4,2,3")
                else:
                    print("entramos a opción 4,3")    """

        
        if validad2 == False:
            print("AAAAAAAAAAAAA")
            
            print("este es el else")
            print(punto0)
            print(numero)
            #el problema esta en el valor visitados 
            #ya esta no mover l_tupla 
            print(l_tupla)
            print(type(l_tupla))
            print(visitados)
            print(type(visitados))
            print(self.caminos)
            print(type(self.caminos))
            [print(" ".join(map(str, fila))) for fila in instacia_tablero]
            #self.resolver_numero(punto0 ,numero , l_tupla ,instacia_tablero)   
        
        print(f"No se encontró solución desde {inicio}, visitados: {visitados}")
        return False


    def obtener_direcciones(self):
        return [(0,1),(0,-1),(1,0),(-1,0)]
    

   
    def encontrar_pares(self):
        pares ={} 
        for i, fila in enumerate(self.board):
            for j, numero in enumerate(fila):
                if numero != 0: # Si el valor no es 0, es decir no es espacio vacio
                    if numero in pares: # Si el valor no está aun en el diccionario de pares
                        pares[numero].append((i,j)) # Inicializar la entrada en el diccionario con la primera coordenada
                    else:
                        pares[numero] = [(i,j)]  # Agregar la segunda coordenada al valor existente en el diccionario
        return pares

    def distancia(self, punto1, punto2):
        return abs(punto1[0] - punto2[0]) + abs(punto1[1] - punto2[1])


    def priorizar_cortos(self):
        pares = self.encontrar_pares()
        pares_ordenados = [(numero, (coord1, coord2)) for numero, (coord1, coord2) in sorted(pares.items(), key=lambda par: self.distancia(par[1][0], par[1][1]))]
        #pares_ordenados = sorted(pares.items(), key=lambda par: self.distancia(par[1][0], par[1][1]))
        return pares_ordenados 


    def priorizar_largos(self):
        pares = self.encontrar_pares()  # Llama a la función que encuentra los pares y los guarda en 'pares'.
        pares_ordenados = [(numero, (coord1, coord2)) for numero, (coord1, coord2) in sorted(pares.items(), key=lambda par: self.distancia(par[1][0], par[1][1]), reverse=True)]
        #pares_ordenados = sorted(pares.items(), key=lambda par: self.distancia(par[1][0], par[1][1]), reverse=True)
        return pares_ordenados  # Devuelve la lista de pares ordenados por la distancia más larga primero.


####################################################################
#pruebas de auxiliares de backtracking
# Asumiendo que tenemos definida la clase NumberLinkGame con todas las funciones mencionadas.

class TestNumberLinkGame(unittest.TestCase):
    def setUp(self):
        # Esta función se ejecuta antes de cada prueba.
        self.game = NumberLinkGame([[1, 1], [2, 2]])


    def test_contarParesNumeros(self):
        self.game.board = [[1, 2], [2, 1]]
        self.assertEqual(self.game.contarParesNumeros(), 2)


    def test_obtenerTodosLosNumeros(self):
        self.game.board = [[1, 2], [3, 4]]
        self.assertSetEqual(self.game.obtenerTodosLosNumeros(), {1, 2, 3, 4})

    def test_encontrarNumero(self):
        self.game.board = [[1, 0], [0, 2]]
        self.assertEqual(self.game.encontrarNumero(1), (0, 0))

    def test_verificarCamino(self):
        self.game.board = [[1, 1], [0, 0]]  # Un camino directo para el número 1.
        caminos = set()  # Inicialmente vacío, ya que es construido por verificarCamino.
        self.assertTrue(self.game.verificarCamino((0, 0), 1, caminos))



    def test_movimientoValidado(self):
        self.game.board = [[0, 0], [0, 0]]
        visitados = set()
        caminos = set()
        self.assertTrue(self.game.movimientoValidado(1, 0, 1, visitados, caminos))

    def test_validarSolucionCompleta(self):
        self.game.board = [[1, 1], [2, 2]]  # Asumiendo que este es un tablero resuelto válido.
        self.game.caminos = {(0, 0), (0, 1), (1, 0), (1, 1)}  # Caminos que reflejan una solución completa.
        self.assertTrue(self.game.validarSolucionCompleta())



    def test_esNumeroConectado(self):
        self.game.board = [[1, 0], [0, 1]]
        self.game.caminos = {(0, 0), (1, 1)}  # Asumimos que estos representan un camino conectado para el número 1.
        self.assertTrue(self.game.esNumeroConectado(1))
        self.assertFalse(self.game.esNumeroConectado(2))  # No hay caminos para el número 2.



    def test_marcarCamino(self):
        self.game.marcarCamino(0, 0, 1)
        self.assertIn((0, 0), self.game.caminos)

    def test_obtenerSiguienteNumero(self):
        # Configuramos un tablero donde 1 y 2 están conectados por caminos válidos.
        self.game.board = [[1, 1], [2, 2]]
        # Asumimos que estos caminos representan una conexión válida para el número 1 y 2.
        self.game.caminos = {(0, 0), (0, 1), (1, 0), (1, 1)}  # Caminos para 1 y 2
        self.assertIsNone(self.game.obtenerSiguienteNumero())  # Todos los números están conectados

    def test_resolver_tablero(self):
        self.game.board = [
            [1, 0, 0, 0, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0],
            [5, 0, 5, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1]
        ]
        # Configura un tablero que necesita resolver
        self.assertTrue(self.game.resolver_tablero())#toca cambiar esto
        # Verifica que el tablero se resuelve correctamente

    def test_resolver_numero(self):
        self.game.board = [[1, 0, 0 ,0,0], [0, 0, 0, 0,0] , [0, 0, 0, 0,0], [0, 0, 0, 0,0],[0, 0, 0, 0,1]]
        self.assertTrue(self.game.resolver_numero((0, 0), 1, set(),self.game.board))

    def test_obtener_direcciones(self):
        esperado = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.assertEqual(self.game.obtener_direcciones(), esperado)
        # Verifica que las direcciones obtenidas son las correctas

    def test_actualizacion_caminos(self):
        self.game.board = [[1, 0], [0, 1]]
        self.game.hacerMovimiento(0, 1, 1)
        self.assertIn((0, 1), self.game.caminos)
        # Verifica que hacerMovimiento actualiza self.caminos

        self.game.deshacerMovimiento(0, 1, 1)
        self.assertNotIn((0, 1), self.game.caminos)
        # Verifica que deshacerMovimiento actualiza self.caminos


    # Más métodos de prueba...



# Función para leer el archivo de entrada y cargar el tablero
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n, m = map(int, lines[0].split(','))
        board = [[0 for _ in range(m)] for _ in range(n)]
        for line in lines[1:]:
            x, y, value = map(int, line.split(','))
            board[x-1][y-1] = value
    return board

# Punto de entrada principal
if __name__ == "__main__":
    #board = read_input_file("juego.txt")  # Replace con el archivo del juego
    #game = NumberLinkGame(board)
    #game.run()
    unittest.main()