import keyboard
import logging
from ui.edge_trigger import EdgeTrigger

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class WindowState:
    EXPANDED = "EXPANDED"
    HIDDEN = "HIDDEN"

class WindowManager:
    """
    Segregation Principle: Isolates the logic of state control, visibility,
    hotkeys and focus of the main window.
    """
    def __init__(self, root, hotkey='f4'):
        self.root = root
        self.state = WindowState.EXPANDED
        self.edge_trigger = None
        self.retract_timer = None
        self.hotkey = hotkey

        # Register events
        self.root.bind("<FocusOut>", self._on_focus_out)
        
        try:
            keyboard.add_hotkey(self.hotkey, self._trigger_hotkey)
        except Exception as e:
            print(f"Warning: Error registering global hotkey: {e}")

    def _trigger_hotkey(self):
        logging.debug("[WindowManager] _trigger_hotkey called")
        # The keyboard API calls callbacks in a background thread.
        # after(0) injects back into the tkinter thread
        self.root.after(0, self.toggle)

    def toggle(self):
        """Strictly alternates between expanded and hidden states."""
        logging.debug(f"[WindowManager] toggle called. Current state: {self.state}")
        if self.state == WindowState.HIDDEN:
            self.expand()
        else:
            self.retract()

    def expand(self):
        """Expands the window, sets topmost and forces focus."""
        logging.debug(f"[WindowManager] expand called. State was: {self.state}")
        if self.state == WindowState.EXPANDED:
            logging.debug("[WindowManager] expand ignored: already expanded")
            return
            
        self.state = WindowState.EXPANDED
        
        if self.edge_trigger and self.edge_trigger.winfo_exists():
            self.edge_trigger.destroy()
            self.edge_trigger = None
            
        if self.retract_timer:
            self.root.after_cancel(self.retract_timer)
            self.retract_timer = None
            
        self.root.deiconify()
        # Ensures it will appear on top of F1 (fundamental)
        self.root.attributes("-topmost", True)
        self.root.focus_force()
        
        # Ignores spurious FocusOut events from OS due to edge trigger destruction
        self._ignore_focus = True
        self.root.after(500, lambda: setattr(self, '_ignore_focus', False))
        logging.debug("[WindowManager] Window expanded successfully.")

    def retract(self):
        """Hides the main window and activates the floating trigger."""
        logging.debug(f"[WindowManager] retract called. State was: {self.state}")
        if self.state == WindowState.HIDDEN:
            logging.debug("[WindowManager] retract ignored: already hidden")
            return
            
        self.state = WindowState.HIDDEN
        
        self.root.attributes("-topmost", False)
        self.root.withdraw()
        
        if self.edge_trigger is None or not self.edge_trigger.winfo_exists():
            self.edge_trigger = EdgeTrigger(self._trigger_hotkey)
        logging.debug("[WindowManager] Window retracted successfully.")

    def _on_focus_out(self, event):
        """Handles focus loss."""
        if getattr(self, '_ignore_focus', False):
            logging.debug(f"[WindowManager] FocusOut ignored by _ignore_focus shield on: {event.widget}")
            return
            
        # If the window itself loses focus, we check to retract.
        if event.widget == self.root and self.state == WindowState.EXPANDED:
            logging.debug("[WindowManager] FocusOut on root received, scheduling retract...")
            # Debounce timer to avoid OS focus loss glitches
            if self.retract_timer:
                self.root.after_cancel(self.retract_timer)
            self.retract_timer = self.root.after(200, self._do_retract_if_unfocused)

    def _do_retract_if_unfocused(self):
        """If after 200ms the window remains without OS focus, we retract."""
        logging.debug("[WindowManager] Executing validation of _do_retract_if_unfocused")
        if self.state == WindowState.EXPANDED:
            # If None, it means no component of our interface has focus
            focus_val = self.root.focus_displayof()
            logging.debug(f"[WindowManager] Current focus is: {focus_val}")
            if focus_val is None:
                logging.debug("[WindowManager] Focus lost confirmed. Executing retract.")
                self.retract()
            
    def destroy(self):
        """Clears global hotkeys when closing the app."""
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
