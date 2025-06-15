def crear_tablero():
    return [
        ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
        ["♟"] * 8,
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        ["♙"] * 8,
        ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
    ]

def mostrar_tablero(tablero):
    print("  a b c d e f g h")
    for i, fila in enumerate(tablero):
        print(8 - i, end=" ")
        for pieza in fila:
            print(pieza, end=" ")
        print(8 - i)
    print("  a b c d e f g h\n")

def convertir_pos(pos):
    if len(pos) != 2: return None
    col = ord(pos[0].lower()) - ord('a')
    row = 8 - int(pos[1])
    return (row, col) if 0 <= row < 8 and 0 <= col < 8 else None

def pieza_es_blanca(p): return p in "♙♖♘♗♕♔"
def pieza_es_negra(p): return p in "♟♜♞♝♛♚"

def es_turno_correcto(pieza, turno):
    if pieza == " ": return False
    return pieza_es_blanca(pieza) if turno == "blancas" else pieza_es_negra(pieza)

def es_enemigo(pieza_origen, pieza_destino):
    if pieza_destino == " ": return False
    return (pieza_es_blanca(pieza_origen) and pieza_es_negra(pieza_destino)) or \
           (pieza_es_negra(pieza_origen) and pieza_es_blanca(pieza_destino))

# Ejemplo: solo movimientos válidos de peón y caballo (puedes expandir con más piezas)
def movimiento_valido(tablero, f1, c1, f2, c2):
    pieza = tablero[f1][c1]
    destino = tablero[f2][c2]
    
    if not es_enemigo(pieza, destino) and destino != " ":
        print("No puedes capturar tus propias piezas.")
        return False
    
    df, dc = f2 - f1, c2 - c1

    if pieza == "♙":  # Peón blanco
        if c1 == c2 and tablero[f2][c2] == " ":
            return df == -1 or (df == -2 and f1 == 6 and tablero[f1-1][c1] == " ")
        if abs(dc) == 1 and df == -1 and pieza_es_negra(destino):
            return True

    if pieza == "♟":  # Peón negro
        if c1 == c2 and tablero[f2][c2] == " ":
            return df == 1 or (df == 2 and f1 == 1 and tablero[f1+1][c1] == " ")
        if abs(dc) == 1 and df == 1 and pieza_es_blanca(destino):
            return True

    if pieza in ["♘", "♞"]:  # Caballos
        return (abs(df), abs(dc)) in [(2, 1), (1, 2)]

    return False  # Para otras piezas, aún no implementado

def mover_pieza(tablero, desde, hasta, turno):
    pos1 = convertir_pos(desde)
    pos2 = convertir_pos(hasta)
    if not pos1 or not pos2:
        print("Coordenadas inválidas.")
        return False

    f1, c1 = pos1
    f2, c2 = pos2
    pieza = tablero[f1][c1]

    if not es_turno_correcto(pieza, turno):
        print(f"No puedes mover esa pieza. Es el turno de las {turno}.")
        return False

    if not movimiento_valido(tablero, f1, c1, f2, c2):
        print("Movimiento no válido.")
        return False

    tablero[f2][c2] = pieza
    tablero[f1][c1] = " "
    return True

def jugar():
    tablero = crear_tablero()
    turno = "blancas"
    while True:
        mostrar_tablero(tablero)
        print(f"Turno de las {turno}")
        desde = input("Desde (e2): ").strip()
        if desde.lower() == "salir": break
        hasta = input("Hasta (e4): ").strip()
        if hasta.lower() == "salir": break
        if mover_pieza(tablero, desde, hasta, turno):
            turno = "negras" if turno == "blancas" else "blancas"

jugar()
