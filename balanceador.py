import matplotlib.pyplot as plt
import math

class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

def simplificar_extensiones(expresion):
    resultado = ""
    i = 0
    while i < len(expresion):
        c = expresion[i]
        if c == '+':
            anterior = resultado[-1]
            if anterior == ')':
                count = 0
                j = len(resultado) - 1
                while j >= 0:
                    if resultado[j] == ')':
                        count += 1
                    elif resultado[j] == '(':
                        count -= 1
                    if count == 0:
                        break
                    j -= 1
                grupo = resultado[j:]
                resultado = resultado[:j] + grupo + grupo + '*'
            else:
                resultado += anterior + '*'
        elif c == '?':
            anterior = resultado[-1]
            if anterior == ')':
                count = 0
                j = len(resultado) - 1
                while j >= 0:
                    if resultado[j] == ')':
                        count += 1
                    elif resultado[j] == '(':
                        count -= 1
                    if count == 0:
                        break
                    j -= 1
                grupo = resultado[j:]
                resultado = resultado[:j] + '(' + grupo + '|ε)'
            else:
                resultado = resultado[:-1] + '(' + anterior + '|ε)'
        else:
            resultado += c
        i += 1
    return resultado

def agregar_concatenacion(expresion):
    resultado = ""
    for i in range(len(expresion) - 1):
        c1 = expresion[i]
        c2 = expresion[i + 1]
        resultado += c1
        if (
            c1 not in '(|' and
            c2 not in '|)*+?)'
        ):
            resultado += '.'
    resultado += expresion[-1]
    return resultado

def infix_a_postfix(expresion):
    precedencia = {'*': 3, '.': 2, '|': 1}
    salida = []
    pila = []

    for c in expresion:
        if c.isalnum() or c == 'ε':
            salida.append(c)
        elif c == '(':
            pila.append(c)
        elif c == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()  # sacar '('
        else:
            while pila and pila[-1] != '(' and precedencia.get(pila[-1], 0) >= precedencia.get(c, 0):
                salida.append(pila.pop())
            pila.append(c)

    while pila:
        salida.append(pila.pop())

    return ''.join(salida)

def postfix_a_arbol(postfix):
    stack = []
    for simbolo in postfix:
        if simbolo == '*':
            hijo = stack.pop()
            nodo = Nodo(simbolo, izquierdo=hijo)
            stack.append(nodo)
        elif simbolo in {'.', '|'}:
            derecho = stack.pop()
            izquierdo = stack.pop()
            nodo = Nodo(simbolo, izquierdo=izquierdo, derecho=derecho)
            stack.append(nodo)
        else:
            stack.append(Nodo(simbolo))
    return stack.pop() if stack else None

def asignar_posiciones(nodo, x=0, y=0, dx=1.5, posiciones=None, lineas=None):
    if posiciones is None:
        posiciones = {}
    if lineas is None:
        lineas = []

    posiciones[nodo] = (x, y)

    if nodo.izquierdo:
        lineas.append(((x, y), (x - dx, y - 1)))
        asignar_posiciones(nodo.izquierdo, x - dx, y - 1, dx / 1.5, posiciones, lineas)
    if nodo.derecho:
        lineas.append(((x, y), (x + dx, y - 1)))
        asignar_posiciones(nodo.derecho, x + dx, y - 1, dx / 1.5, posiciones, lineas)

    return posiciones, lineas

def dibujar_arbol(raiz, nombre='árbol'):
    if raiz is None:
        print("Árbol vacío.")
        return

    posiciones, lineas = asignar_posiciones(raiz)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    radio = 0.3
    for (x1, y1), (x2, y2) in lineas:
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        offset_x = dx * radio / dist
        offset_y = dy * radio / dist
        ax.plot([x1 + offset_x, x2 - offset_x], [y1 + offset_y, y2 - offset_y], 'k-')

    for nodo, (x, y) in posiciones.items():
        ax.add_patch(plt.Circle((x, y), radio, color='lightblue', ec='black'))
        ax.text(x, y, nodo.valor, ha='center', va='center', fontsize=10)

    plt.title(nombre)
    plt.show()

def procesar_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding="utf-8")as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            expresion = linea.strip()
            print(f"\nLínea {numero_linea}: {expresion}")

            simplificada = simplificar_extensiones(expresion)
            print("  Simplificada (+ y ?):", simplificada)

            con_concat = agregar_concatenacion(simplificada)
            print("  Con concatenación explícita:", con_concat)

            postfix = infix_a_postfix(con_concat)
            print("  Postfix:", postfix)

            raiz = postfix_a_arbol(postfix)
            dibujar_arbol(raiz, nombre=f"Árbol sintáctico - Línea {numero_linea}")

if __name__ == "__main__":
    archivo = "expresiones.txt"
    print(f"Procesando archivo: {archivo}")
    procesar_archivo(archivo)
