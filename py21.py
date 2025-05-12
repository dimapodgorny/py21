from textual.app import App
from textual.events import MouseEvent

from py21components.menus import MainMenu
from scripts.network import Network



class Py21App(App):
    CSS_PATH = "styles\\py21.tcss"
    BINDINGS = [
        ("0", "exit_app", "Exit app")
        ]
    
    def on_mount(self) -> None:
        self.push_screen(MainMenu())
        
    ## Method binds
    def action_exit_app(self) -> None:
        self.exit()
        
    
    async def on_event(self, event) -> None:
        if isinstance(event, MouseEvent):
            event.stop()
        else:
            return await super().on_event(event)


if __name__ == "__main__":
    app = Py21App()
    app.run()