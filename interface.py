import tkinter as tk
import Grid
import entry
import maze
import time
import main

# Variaveis do tamanho da janela do Tkinter
window_height = 600
window_width = 600

root = tk.Tk()


class Application(tk.Frame):
    MATRIZ = []
    h=[]
    nos=[]
    grafo =[]
    inicio=0

    entry_width = None
    entry_height = None

    n = 35
    minimo = 20
    maximo = 50

    # GERA PROBLEMA - MATRIZ DE ADJACÊNCIAS
    matriz = main.gera_Ambiente(minimo,maximo,n)

    qt = 50
    ga1 = 0
    ga2 = 0
    ga3 = 0

    sf = 0
    vf=0

    # GERA SOLUÇÃO INICIAL ALEATÓRIA
    si = main.solucao_Inicial(n)

    # AVALIA SOLUÇÃO INICIAL
    vi = main.avalia_Solucao(si,matriz,n)


    def __init__(self, master=None):
        # Container to shelter container_width and container_height
        container_options = tk.Frame(
            master, height=200, borderwidth=2, relief="groove")
        container_options.pack(fill=tk.X, padx=5, pady=5)

        # Width
        container_width = tk.Frame(
            container_options, height=200, borderwidth=2)
        container_width.pack(fill=tk.X, padx=5, pady=5)

        text_width = tk.Label(container_width, text="Width",)
        text_width.pack(side=tk.LEFT)

        self.entry_width = tk.Entry(container_width)
        self.entry_width.pack(side=tk.RIGHT)

        # Height
        container_height = tk.Frame(
            container_options, height=200, borderwidth=2)
        container_height.pack(fill=tk.X, padx=5, pady=5)

        text_height = tk.Label(container_height, text="Height",)
        text_height.pack(side=tk.LEFT)

        self.entry_height = tk.Entry(container_height)
        self.entry_height.pack(side=tk.RIGHT)

        container_maze = tk.Frame(master, borderwidth=2, relief="groove")
        # Button Make Maze
        button_make = tk.Button(
            text="Make Maze", command=lambda: self.generate_maze(container_maze))
        button_make.pack()

        # Subida de Encosta
        button_find_path_amplitude = tk.Button(
            text="Subida de Encosta", command=lambda: self.activate_subida_enconsta(container_maze))
        button_find_path_amplitude.pack()

        # Subida de Encosta Alterada
        button_find_path_profundidade = tk.Button(
            text="Subida de Encosta Alterada", command=lambda: self.activate_subida_encosta_a(container_maze))
        button_find_path_profundidade.pack()

        # Tempera Simulada
        button_find_path_limitada = tk.Button(
            text="Tempera Simulada", command=lambda: self.activate_tempera_simulada(container_maze))
        button_find_path_limitada.pack()

        container_maze.pack(fill=tk.X, pady=10, padx=5)

        self.text_cost = tk.Label(
            master, text="Cost: ",)
        self.text_cost.pack(side=tk.TOP)

    def generate_maze(self, container):
        # Obtem matriz com cordenadas do grid
        self.MATRIZ = Grid.make_maze(
            int(self.entry_height.get()), int(self.entry_width.get()))
        self.reset_maze_container(self.MATRIZ, container)



    def reset_maze_container(self, matriz, container):
        # Limpa o container container_maze se já houver widgets
        self.clean_maze_container(container)
        Grid.draw_grid(container, len(matriz), len(matriz[0]))
        Grid.paint_maze(matriz, container)
        Grid.paint_outline(matriz, container)

    def activate_subida_enconsta(self, container):
        # EXECUTA - SUBIDA DE ENCOSTA
        self.sf, self.vf = main.encosta(self.si,self.vi,self.matriz,self.n)
        self.ga1 += (self.vi - self.vf)/self.vi
        print("Ganho - Subida de Encosta....: ",100*self.ga1/self.qt)


    def activate_subida_encosta_a(self, container):
        # EXECUTA - SUBIDA DE ENCOSTA ALTERADA
        self.tmax = self.n-1
        self.sf, vf = main.encosta_alt(self.si,self.vi,self.matriz,self.n,self.tmax)
        self.ga2 += (self.vi - vf)/self.vi
        print("Ganho - Subida de Encosta_A..: ",100*self.ga2/self.qt)


    def activate_tempera_simulada(self, container):
        # EXECUTA - TEMPERA SIMULADA
        self.t_ini  = 800
        self.t_fim  = 0.01
        self.ft_red = 0.95
        self.sf, self.vf = main.tempera(self.si,self.vi,self.matriz,self.t_ini,self.t_fim,self.ft_red)
        self.ga3 += (self.vi - self.vf)/self.vi
        print("Ganho - Têmpera Simulada.....: ",100*self.ga3/self.qt)


    def clean_maze_container(self, container):
        # Itere sobre os widgets no container e destrua-os
        for widget in container.winfo_children():
            widget.destroy()


# Altera o posicionamento da tela para o meio do monitor principal
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width,
              window_height, x_cordinate, y_cordinate))

Application(root)
root.title("Labirinto IA - 2")
# Impede o redimensionamento horizontal e vertical
# root.resizable(False, False)
root.mainloop()
