import tkinter as tk
import customtkinter as ctk

class BlackWindowReader(ctk.CTk):
    """
    Classe principal que une a janela customizada com a guia de leitura.
    """
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO DA JANELA E TRANSPARÊNCIA ---
        self.initial_width = 600
        self.initial_height = 600
        self.geometry(f"{self.initial_width}x{self.initial_height}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        self.transparent_color = 'white'
        self.configure(fg_color=self.transparent_color)
        self.attributes("-transparentcolor", self.transparent_color)
        
        self.resizing = False
        self.x_offset, self.y_offset = 0, 0
        
        # --- BARRA DE TÍTULO ---
        fonte = "Trebuchet MS"
        self.title_bar = tk.Frame(self, bg="black", relief="raised", bd=0)
        self.title_bar.pack(fill=tk.X)
        
        self.title_label = tk.Label(self.title_bar, text="The Dark Reader by masTHIERRYi", fg="#1F1F1F", 
                                      bg="black", font=(fonte, 10, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=10, pady=4)
        
        self.close_button = ctk.CTkButton(self.title_bar, text="X", width=24, height=10,
                                          command=self.destroy, font=(fonte, 12, "bold"), text_color="#383838", fg_color="black", hover_color="#1c1c1c")
        self.close_button.pack(side=tk.RIGHT, padx=6, pady=5)
        
        self.title_bar.bind("<B1-Motion>", self.move_window)
        self.title_bar.bind("<Button-1>", self.get_pos)

        # --- CANVAS PARA A GUIA DE LEITURA ---
        self.canvas = tk.Canvas(self, bg=self.transparent_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # --- PROPRIEDADES DA GUIA DE LEITURA ---
        self.hole_width = 500
        self.hole_height = 50
        self.hole_x = (self.initial_width - self.hole_width) // 2
        self.hole_y = 40
        self.scroll_step = 10
        self.resize_step = 10

        # --- ÁREA DE REDIMENSIONAMENTO ---
        self.grip = tk.Frame(self, bg='black', cursor="bottom_right_corner")
        self.grip.place(relx=1.0, rely=1.0, anchor="se", width=15, height=15)
        self.grip.bind("<ButtonPress-1>", self.start_resize)
        self.grip.bind("<B1-Motion>", self.do_resize)

        # --- VINCULAÇÃO DE EVENTOS ---
        self.bind_events()
        self.bind("<Configure>", self.on_window_configure)

        # --- GUIA DE USO INICIAL ---
        self.show_instructions()

    def show_instructions(self):
        """Exibe as instruções de uso no centro do canvas."""
        instruction_text = (
            "\n"
            "GUIDE\n\n\n\n\n\n"
            "position: scroll or drag\n"
            "V-size: ^ / v\n"
            "H-size: < / >\n\n"
            "Close: Press 'ESC' or 'X' button"
        )
        self.canvas.create_text(
            self.initial_width / 2, 90, text=instruction_text, fill="grey",
            font=("Arial", 11), justify=tk.CENTER, tag="instructions"
        )
        # As instruções desaparecem após 8 segundos
        self.after(8000, self.hide_instructions)

    def hide_instructions(self):
        """Apaga as instruções da tela."""
        self.canvas.delete("instructions")

    def on_window_configure(self, event=None):
        self.draw_guide()
        self.grip.place(relx=1.0, rely=1.0, anchor="se", width=15, height=15)
        self.grip.lift()

    def draw_guide(self):
        self.canvas.delete("guide")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1: return
        
        # Desenha 4 retângulos pretos baseados na posição e tamanho da fenda
        self.canvas.create_rectangle(0, 0, canvas_width, self.hole_y, fill='black', outline='black', tag="guide")
        self.canvas.create_rectangle(0, self.hole_y + self.hole_height, canvas_width, canvas_height, fill='black', outline='black', tag="guide")
        self.canvas.create_rectangle(0, self.hole_y, self.hole_x, self.hole_y + self.hole_height, fill='black', outline='black', tag="guide")
        self.canvas.create_rectangle(self.hole_x + self.hole_width, self.hole_y, canvas_width, self.hole_y + self.hole_height, fill='black', outline='black', tag="guide")
        self.canvas.lift("instructions") # Garante que as instruções fiquem no topo
        
    def bind_events(self):
        """Vincula todos os eventos do mouse e teclado."""
        self.bind("<MouseWheel>", self.on_mouse_scroll)
        self.bind("<Button-4>", self.on_mouse_scroll)
        self.bind("<Button-5>", self.on_mouse_scroll)
        self.bind("<Up>", self.decrease_hole_height)
        self.bind("<Down>", self.increase_hole_height)
        self.bind("<Left>", self.decrease_hole_width)
        self.bind("<Right>", self.increase_hole_width)
        self.bind("<Escape>", lambda e: self.destroy())
        # Adiciona o bind para arrastar a fenda no canvas
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)

    def on_mouse_scroll(self, event):
        delta = 0
        if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0): delta = -self.scroll_step
        elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0): delta = self.scroll_step
        if delta != 0: self.hole_y += delta; self.clamp_hole_position(); self.draw_guide()

    # --- NOVOS MÉTODOS PARA CONTROLE HORIZONTAL ---
    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_drag(self, event):
        dx, dy = event.x - self._drag_start_x, event.y - self._drag_start_y
        self.hole_x += dx
        self.hole_y += dy
        self._drag_start_x, self._drag_start_y = event.x, event.y
        self.clamp_hole_position()
        self.draw_guide()
        
    def increase_hole_width(self, event=None):
        self.hole_width += self.resize_step; self.clamp_hole_position(); self.draw_guide()

    def decrease_hole_width(self, event=None):
        if self.hole_width > self.resize_step * 2: self.hole_width -= self.resize_step
        self.clamp_hole_position(); self.draw_guide()

    def increase_hole_height(self, event=None):
        self.hole_height += self.resize_step; self.clamp_hole_position(); self.draw_guide()

    def decrease_hole_height(self, event=None):        
        if self.hole_height > self.resize_step: self.hole_height -= self.resize_step
        self.clamp_hole_position(); self.draw_guide()
        
    def clamp_hole_position(self):
        """Garante que a fenda não saia dos limites da janela (agora em X e Y)."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # Limites horizontais (X)
        if self.hole_x < 0: self.hole_x = 0
        if self.hole_x + self.hole_width > canvas_width: self.hole_x = canvas_width - self.hole_width
        # Limites verticais (Y)
        if self.hole_y < 0: self.hole_y = 0
        if self.hole_y + self.hole_height > canvas_height: self.hole_y = canvas_height - self.hole_height
    
    # --- MÉTODOS ORIGINAIS DE MOVIMENTO E REDIMENSIONAMENTO DA JANELA ---
    def get_pos(self, event): self.x_offset, self.y_offset = event.x, event.y
    def move_window(self, event): self.geometry(f"+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}")
        
    def start_resize(self, event):
        self.resizing = True
        self.x_start, self.y_start = event.x_root, event.y_root
        self.width_start, self.height_start = self.winfo_width(), self.winfo_height()

    def do_resize(self, event):
        if self.resizing:
            new_width = self.width_start + (event.x_root - self.x_start)
            new_height = self.height_start + (event.y_root - self.y_start)
            if new_width > 200 and new_height > 100: self.geometry(f"{new_width}x{new_height}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = BlackWindowReader()
    app.mainloop()
