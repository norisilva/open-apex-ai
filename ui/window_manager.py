import keyboard
from ui.edge_trigger import EdgeTrigger

class WindowState:
    EXPANDED = "EXPANDED"
    HIDDEN = "HIDDEN"

class WindowManager:
    """
    Segregation Principle: Isola a logica de controle de estado, visibilidade, 
    hotkeys e foco da janela principal.
    """
    def __init__(self, root, hotkey='f4'):
        self.root = root
        self.state = WindowState.EXPANDED
        self.edge_trigger = None
        self.retract_timer = None
        self.hotkey = hotkey

        # Registrar eventos
        self.root.bind("<FocusOut>", self._on_focus_out)
        
        try:
            keyboard.add_hotkey(self.hotkey, self._trigger_hotkey)
        except Exception as e:
            print(f"Aviso: Erro ao registrar hotkey global: {e}")

    def _trigger_hotkey(self):
        # A API do keyboard chama callbacks em background thread.
        # O after(0) injeta de volta na thread segura do tkinter
        self.root.after(0, self.toggle)

    def toggle(self):
        """Alterna estritamente entre os estados expandido e oculto."""
        if self.state == WindowState.HIDDEN:
            self.expand()
        else:
            self.retract()

    def expand(self):
        """Expande a janela, define topmost e forca o foco."""
        if self.state == WindowState.EXPANDED:
            return
            
        self.state = WindowState.EXPANDED
        
        if self.edge_trigger and self.edge_trigger.winfo_exists():
            self.edge_trigger.destroy()
            self.edge_trigger = None
            
        if self.retract_timer:
            self.root.after_cancel(self.retract_timer)
            self.retract_timer = None
            
        self.root.deiconify()
        # Garante que vai aparecer em cima do F1 (fundamental)
        self.root.attributes("-topmost", True)
        self.root.focus_force()

    def retract(self):
        """Oculta a janela principal e ativa o trigger flutuante."""
        if self.state == WindowState.HIDDEN:
            return
            
        self.state = WindowState.HIDDEN
        
        self.root.attributes("-topmost", False)
        self.root.withdraw()
        
        if self.edge_trigger is None or not self.edge_trigger.winfo_exists():
            self.edge_trigger = EdgeTrigger(self._trigger_hotkey)

    def _on_focus_out(self, event):
        """Controla a perda de foco."""
        # Se a propria janela perder foco, checamos para recolher.
        if event.widget == self.root and self.state == WindowState.EXPANDED:
            # Debounce timer para evitar glitchs de perda de foco do OS
            if self.retract_timer:
                self.root.after_cancel(self.retract_timer)
            self.retract_timer = self.root.after(200, self._do_retract_if_unfocused)

    def _do_retract_if_unfocused(self):
        """Se apos 200ms a janela continuar sem foco do OS, recolhemos."""
        if self.state == WindowState.EXPANDED:
            # Se for None, significa que nenhum componente da nossa interface tem o foco
            if self.root.focus_displayof() is None:
                self.retract()
            
    def destroy(self):
        """Limpa as hotkeys globais ao fechar o app."""
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
