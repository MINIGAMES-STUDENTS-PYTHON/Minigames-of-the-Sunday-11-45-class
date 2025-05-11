import random

# Parámetros del juego
FILAS = 8
COLUMNAS = 8
MINAS = 10

# Crear el tablero vacío
def crear_tablero(filas, columnas, valor=' '):
    return [[valor for _ in range(columnas)] for _ in range(filas)]

# Colocar minas aleatoriamente
def colocar_minas(tablero, minas):
    colocadas = 0
    while colocadas < minas:
        f = random.randint(0, FILAS - 1)
        c = random.randint(0, COLUMNAS - 1)
        if tablero[f][c] != 'M':
            tablero[f][c] = 'M'
            colocadas += 1

# Contar minas alrededor de una celda
def contar_minas_alrededor(tablero, fila, col):
    direcciones = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1),  (1, 0), (1, 1)]
    total = 0
    for df, dc in direcciones:
        nf, nc = fila + df, col + dc
        if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
            if tablero[nf][nc] == 'M':
                total += 1
    return total

# Descubrir celdas 
def descubrir(tablero, visible, fila, col):
    if visible[fila][col] != ' ':
        return
    if tablero[fila][col] == 'M':
        visible[fila][col] = 'M'
        return
    minas = contar_minas_alrededor(tablero, fila, col)
    visible[fila][col] = str(minas) if minas > 0 else '0'
    if minas == 0:
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nf, nc = fila + df, col + dc
                if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                    descubrir(tablero, visible, nf, nc)

# Mostrar el tablero visible
def mostrar_tablero(tablero):
    print("   " + " ".join([str(i) for i in range(COLUMNAS)]))
    for idx, fila in enumerate(tablero):
        print(f"{idx:2} " + " ".join(fila))

# Comprobar victoria
def ha_ganado(tablero, visible):
    for f in range(FILAS):
        for c in range(COLUMNAS):
            if tablero[f][c] != 'M' and visible[f][c] == ' ':
                return False
    return True

# Juego principal
def jugar():
    tablero = crear_tablero(FILAS, COLUMNAS)
    visible = crear_tablero(FILAS, COLUMNAS)
    colocar_minas(tablero, MINAS)

    while True:
        mostrar_tablero(visible)
        accion = input("Acción (d para descubrir, m para marcar): ").strip().lower()
        try:
            fila = int(input("Fila: "))
            col = int(input("Columna: "))
        except ValueError:
            print("Coordenadas inválidas.")
            continue

        if not (0 <= fila < FILAS and 0 <= col < COLUMNAS):
            print("Coordenadas fuera del tablero.")
            continue

        if accion == 'm':
            visible[fila][col] = 'F' if visible[fila][col] != 'F' else ' '
        elif accion == 'd':
            if tablero[fila][col] == 'M':
                mostrar_tablero(tablero)
                print(" ¡Pisaste una mina! Fin del juego.")
                break
            descubrir(tablero, visible, fila, col)
            if ha_ganado(tablero, visible):
                mostrar_tablero(visible)
                print("🎉 ¡Felicidades, ganaste!")
                break
        else:
            print("Acción no reconocida.")

# Ejecutar el juego
if __name__ == "__main__":
    jugar()

