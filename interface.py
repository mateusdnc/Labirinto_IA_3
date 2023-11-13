import tkinter as tk
import Grid
import entry
import maze
import time

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

        # Find path container
        container_find_path = tk.Frame(
            master, height=200, borderwidth=2, relief="groove")
        container_find_path.pack(fill=tk.X, padx=5, pady=5)

        # Coordenate X
        container_cordy = tk.Frame(
            container_find_path, height=200, borderwidth=2)
        container_cordy.pack(fill=tk.X, padx=5, pady=5)

        text_end = tk.Label(container_cordy, text="Coordinate X",)
        text_end.pack(side=tk.LEFT)

        self.entry_end = tk.Entry(container_cordy)
        self.entry_end.pack(side=tk.RIGHT)

        # Coordenate Y
        container_cordx = tk.Frame(
            container_find_path, height=200, borderwidth=2)
        container_cordx.pack(fill=tk.X, padx=5, pady=5)

        text_end1 = tk.Label(container_cordx, text="Coordinate Y",)
        text_end1.pack(side=tk.LEFT)

        self.entry_end1 = tk.Entry(container_cordx)
        self.entry_end1.pack(side=tk.RIGHT)

        # # Limit field
        # container_limit = tk.Frame(
        #     container_find_path, height=200, borderwidth=2)
        # container_limit.pack(fill=tk.X, padx=5, pady=5)

        # text_limit = tk.Label(
        #     container_limit, text="Limit (AIA*)",)
        # text_limit.pack(side=tk.LEFT)

        # self.text_limit = tk.Entry(container_limit)
        # self.text_limit.pack(side=tk.RIGHT)

        container_maze = tk.Frame(master, borderwidth=2, relief="groove")
        # Button Make Maze
        button_make = tk.Button(
            text="Make Maze", command=lambda: self.generate_maze(container_maze))
        button_make.pack()

        # Subida de Encosta
        button_find_path_amplitude = tk.Button(
            text="Subida de Encosta", command=lambda: self.activate_uniform_cost(container_maze))
        button_find_path_amplitude.pack()

        # Subida de Encosta Alterada
        button_find_path_profundidade = tk.Button(
            text="Subida de Encosta Alterada", command=lambda: self.activate_greedy(container_maze))
        button_find_path_profundidade.pack()

        # Tempera Simulada
        button_find_path_limitada = tk.Button(
            text="Tempera Simulada", command=lambda: self.activate_a(container_maze))
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
        self.grafo, self.nos = maze.convertAndSetMatrixToGraph(self.MATRIZ)
        self.h = maze.gera_H(self.grafo,self.nos,self.h,len(self.nos), self.nos, self.MATRIZ)
        print("Heuristica\n")
        print(self.h)
        print("Mapa Valores\n")
        print(self.MATRIZ)



    def reset_maze_container(self, matriz, container):
        # Limpa o container container_maze se já houver widgets
        self.clean_maze_container(container)
        Grid.draw_grid(container, len(matriz), len(matriz[0]))
        Grid.paint_maze(matriz, container)
        Grid.paint_outline(matriz, container)

    def activate_uniform_cost(self, container):
        # Start timer
        start_time = time.perf_counter()

        self.reset_maze_container(self.MATRIZ, container)
        fim = Grid.encontrar_id(int(
            self.entry_end1.get()), int(self.entry_end.get()),self.MATRIZ)
        output = maze.busca.custo_uniforme(self,self.grafo,self.nos,self.h, self.inicio,fim)
        Grid.paint_path(output[0], container, self.MATRIZ)

        # End timer
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        # Insere o valor do custo e tempo de processamento no label text_cost
        entry.change_text_by_entry(
            self.text_cost, "Custo: "+str(output[1])+" \nTempo de processamento: "+str("{:.4f}".format(elapsed_time)) + " secs")

    def activate_greedy(self, container):
        # Start timer
        start_time = time.perf_counter()

        self.reset_maze_container(self.MATRIZ, container)
        fim = Grid.encontrar_id(int(
            self.entry_end1.get()), int(self.entry_end.get()),self.MATRIZ)
        output = maze.busca.greedy(self.grafo,self.nos,self.h, self.inicio,fim)
        Grid.paint_path(output[0], container, self.MATRIZ)

        # End timer
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        # Insere o valor do custo e tempo de processamento no label text_cost
        entry.change_text_by_entry(
            self.text_cost, "Custo: "+str(output[1])+" \nTempo de processamento: "+str("{:.4f}".format(elapsed_time)) + " secs")

    def activate_a(self, container):
        # Start timer
        start_time = time.perf_counter()

        self.reset_maze_container(self.MATRIZ, container)
        fim = Grid.encontrar_id(int(
            self.entry_end1.get()), int(self.entry_end.get()),self.MATRIZ)
        output = maze.busca.a_estrela(self.grafo,self.nos,self.h, self.inicio,fim)
        Grid.paint_path(output[0], container, self.MATRIZ)

        # End timer
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        # Insere o valor do custo e tempo de processamento no label text_cost
        entry.change_text_by_entry(
            self.text_cost, "Custo: "+str(output[1])+" \nTempo de processamento: "+str("{:.4f}".format(elapsed_time)) + " secs")

    def activate_aia(self, container):
        # Start timer
        start_time = time.perf_counter()

        self.reset_maze_container(self.MATRIZ, container)
        fim = Grid.encontrar_id(int(
            self.entry_end1.get()), int(self.entry_end.get()),self.MATRIZ)
        output = maze.busca.aia_estrela(self.grafo,self.nos,self.h, self.inicio,fim)
        Grid.paint_path(output[0], container, self.MATRIZ)

        # End timer
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        # Insere o valor do custo e tempo de processamento no label text_cost
        entry.change_text_by_entry(
            self.text_cost, "Custo: "+str(output[1])+" \nTempo de processamento: "+str("{:.4f}".format(elapsed_time)) + " secs")

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
