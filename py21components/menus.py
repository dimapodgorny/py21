from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Button, Label, Input
from textual.containers import Container, Vertical, Horizontal

from scripts.network import Network

class MainMenu(Screen):
    def __init__(self, name = None, id = None, classes = None):
        super().__init__(id="MainMenuScreen")
        
    from py21components.ascii_strings import MAINMENU
    
    
    def on_mount(self) -> None:
        self.call_later(lambda: self.app.set_focus(None))
        
    def compose(self) -> ComposeResult:
        yield Container(
            Label(self.MAINMENU.TITLE, id="MainMenuTitle"),
            
            Horizontal(
                Button(self.MAINMENU.BUTTONS["play"], name="button_play"),
                Button(self.MAINMENU.BUTTONS["config"], name="button_config"),
                Button(self.MAINMENU.BUTTONS["credits"], name="button_credits"),
                Button(self.MAINMENU.BUTTONS["exit"], name="button_exit"),

                id="MainMenuButtons",
            ),
            id="MainMenuContainer",
        )
        
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.name:
            case "button_play":
                self.app.push_screen(Lobby())
                
            case "button_config":
                self.app.console.log("wip")

            case "button_credits":
                self.app.console.log("wip")

            case "button_exit":
                self.app.exit() 


class Lobby(Screen):
    CSS_PATH = "..\\styles\\lobby.tcss"
  
    def on_mount(self) -> None:
        pass
        self.app.push_screen(FindLobby())
    
    def compose(self):
        yield Label("lobby")
        
        
class FindLobby(ModalScreen):
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button("Host", name="button_host")
            yield Button("Join", name="button_join")
            yield Horizontal(
                Input(placeholder="ip address", type="text", id="lobby_input_address"),
                Input(placeholder="port", type="number", id="lobby_input_port")
            )
            
    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.name:
            case "button_host":
                addr_input = self.query_one("#lobby_input_address", Input)
                port_input = self.query_one("#lobby_input_port", Input)

                Network.Multiplayer.host_lobby(
                    ADDR=addr_input.value,
                    PORT=port_input.value
                    )

            case "button_join":
                pass