from random import shuffle, randrange
import entry
import tkinter as tk
import random


def make_maze(w, h):
    """ Cria uma matriz com valores aleatorios de acordo com os parametros w e h.
        Parâmetros:
            w - o número de colunas do labirinto (padrão: 16)
            h - o número de linhas do labirinto (padrão: 8)
    """

    matrizConvertida = [
        [random.randint(1, 9) for _ in range(w*2)] for i in range(h*2)]

    return matrizConvertida


def draw_grid(container, height, width):
    """
    Cria uma celula para cada medida H e W
    """
    for x in range(width+1):
        row = []
        for y in range(height+1):
            cell = tk.Entry(container, width=6)
            cell.grid(row=x, column=y)
            row.append(cell)


def paint_outline(matriz, container):
    # Preenche verticalmente
    for h in range((len(matriz))):
        # Define o cabecalho com as cordenadas
        entry.change_entry_text(container, h+1, 0, h)
        entry.change_entry_color(container, h+1, 0, "aquamarine1")

    # Preenche horizontalmente
    for w in range(len(matriz[0])):
        # Define o cabecalho com as cordenadas
        entry.change_entry_text(container, 0, w+1, w)
        entry.change_entry_color(container, 0, w+1, "aquamarine1")


def paint_maze(matriz, container):
    rowCount = 0
    idCont = 0
    for row in matriz:
        colCount = 0
        for char in row:
            entry.change_entry_text(
                container, rowCount+1, colCount+1, str(idCont)+" - "+str(char))
            idCont = idCont+1
            colCount = colCount+1
        rowCount = rowCount+1


def paint_path(visitadoArray, container, matriz):
    for count, cell in enumerate(visitadoArray, 0):
        x, y = encontrar_posicao(cell, matriz)
        # Para o primeiro e ultimo resultado, define uma cor diferente
        if (count == 0):
            entry.change_entry_color(container, y+1, x+1,  "tomato1")
        elif (count == len(visitadoArray)-1):
            entry.change_entry_color(container, y+1, x+1,  "lawngreen")
        else:
            entry.change_entry_color(container, y+1, x+1, "steelblue1")


def encontrar_id(y, x, matriz):
    # Subtrai 1 de X e Y para ajustar para índices baseados em 0
    id = x * len(matriz) + y
    return int(id)


def encontrar_posicao(id, matriz):
    x = (id) % len(matriz)
    y = (id) // len(matriz)
    return x, y
