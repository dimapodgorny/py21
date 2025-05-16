from textual.app import App
from textual.events import MouseEvent

from py21components.menus import MainMenu

from _network_ import Server, Client

class Py21App(App):
    CSS_PATH = "styles/py21.tcss"
    BINDINGS = [
        ("0", "exit_app", "Exit app")
        ]
    
    def __init__(self):
        super().__init__()
        self.server = Server()
        self.client = Client()
        self.is_host : bool = False
        
    
    def on_mount(self) -> None:
        self.push_screen(MainMenu())
        
    def action_exit_app(self) -> None:
        self.exit()
        
    
    async def on_event(self, event) -> None:
        if isinstance(event, MouseEvent):
            event.stop()
        else:
            return await super().on_event(event)

app = Py21App()

if __name__ == "__main__":
    app.run()