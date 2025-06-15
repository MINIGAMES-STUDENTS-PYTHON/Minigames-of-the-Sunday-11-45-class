import random
from collections import deque

# Configuración del juego
FILAS = 8
COLUMNAS = 8
MINAS = 10

class Tablero:
    def __init__(self, filas, columnas, minas):
        self.filas = filas
        self.columnas = columnas
        self.minas = minas
        self.tablero = self._crear_tablero()
        self.visible = self._crear_tablero()
        self.minas_colocadas = False

    def _crear_tablero(self, valor=' '):
        return [[valor for _ in range(self.columnas)] for _ in range(self.filas)]

    def _colocar_minas(self, primera_fila, primera_col):
        colocadas = 0
        while colocadas < self.minas:
            f = random.randint(0, self.filas - 1)
            c = random.randint(0, self.columnas - 1)
            if self.tablero[f][c] != 'M' and (f != primera_fila or c != primera_col):
                self.tablero[f][c] = 'M'
                colocadas += 1
        self.minas_colocadas = True

    def contar_minas_alrededor(self, fila, col):
        direcciones = [(-1, -1), (-1, 0), (-1, 1),
                       (0, -1),          (0, 1),
                       (1, -1), (1, 0),  (1, 1)]
        total = 0
        for df, dc in direcciones:
            nf, nc = fila + df, col + dc
            if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                if self.tablero[nf][nc] == 'M':
                    total += 1
        return total

    def descubrir(self, fila, col):
        if not self.minas_colocadas:
            self._colocar_minas(fila, col)

        if self.tablero[fila][col] == 'M':
            self.visible[fila][col] = 'M'
            return False  # Perdiste

        visitado = set()
        cola = deque([(fila, col)])

        while cola:
            f, c = cola.popleft()
            if (f, c) in visitado or self.visible[f][c] != ' ':
                continue

            visitado.add((f, c))
            minas = self.contar_minas_alrededor(f, c)
            self.visible[f][c] = ' ' if minas == 0 else str(minas)

            if minas == 0:
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf, nc = f + df, c + dc
                        if 0 <= nf < self.filas and 0 <= nc < self.columnas:
                            cola.append((nf, nc))

        return True  # Continuar jugando

    def marcar(self, fila, col):
        if self.visible[fila][col] == ' ':
            self.visible[fila][col] = 'F'
        elif self.visible[fila][col] == 'F':
            self.visible[fila][col] = ' '

    def mostrar_tablero(self, tablero):
        print("     " + " ".join(f"{i:2}" for i in range(self.columnas)))
        print("    " + "---" * self.columnas)
        for idx, fila in enumerate(tablero):
            print(f"{idx:2} | " + " ".join(f"{celda:2}" for celda in fila))

    def ha_ganado(self):
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.tablero[f][c] != 'M' and self.visible[f][c] == ' ':
                    return False
        return True

    def mostrar_tablero_completo(self):
        self.mostrar_tablero(self.tablero)

    def mostrar_tablero_visible(self):
        self.mostrar_tablero(self.visible)


class Juego:
    def __init__(self, filas, columnas, minas):
        self.tablero = Tablero(filas, columnas, minas)
        self.jugando = True

    def turno(self):
        self.tablero.mostrar_tablero_visible()
        accion = input("Acción (d para descubrir, m para marcar): ").strip().lower()
        try:
            fila = int(input("Fila: "))
            col = int(input("Columna: "))
        except ValueError:
            print("Coordenadas inválidas.")
            return

        if not (0 <= fila < self.tablero.filas and 0 <= col < self.tablero.columnas):
            print("Coordenadas fuera del tablero.")
            return

        if accion == 'm':
            self.tablero.marcar(fila, col)
        elif accion == 'd':
            resultado = self.tablero.descubrir(fila, col)
            if not resultado:
                self.tablero.mostrar_tablero_completo()
                print("💥 ¡Pisaste una mina! Fin del juego.")
                self.jugando = False
            elif self.tablero.ha_ganado():
                self.tablero.mostrar_tablero_visible()
                print("🎉 ¡Felicidades, ganaste!")
                self.jugando = False
        else:
            print("Acción no reconocida.")


def main():
    juego = Juego(FILAS, COLUMNAS, MINAS)
    while juego.jugando:
        juego.turno()


if __name__ == "__main__":
    main()
