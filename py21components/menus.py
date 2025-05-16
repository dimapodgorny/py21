from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.widgets import Button, Label, Input, ListView, ListItem
from textual.containers import Container, Vertical, Horizontal

import asyncio

from _network_ import Client


class MainMenu(Screen):
    from py21components.ascii_strings import MAINMENU
        
    CSS_PATH = "../styles/mainmenu.tcss"
    
    def on_mount(self) -> None:
        self.call_later(lambda: self.app.set_focus(None))
        
    def compose(self) -> ComposeResult:
        with Container(id="MainMenuContainer"):
            yield Label(self.MAINMENU.TITLE, id="MainMenuTitle")
            
            with Horizontal(id="MainMenuButtons"):
                yield Button(self.MAINMENU.BUTTONS["play"], name="button_play")
                yield Button(self.MAINMENU.BUTTONS["config"], name="button_config")
                yield Button(self.MAINMENU.BUTTONS["credits"], name="button_credits")
                yield Button(self.MAINMENU.BUTTONS["exit"], name="button_exit")
        
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

###

class Lobby(Screen):
    CSS_PATH = "../styles/lobby.tcss"
  
    def on_mount(self) -> None:
        self.app.push_screen(FindLobby())
        self.app.server.client_connected.connect(self.refresh_peers_list)
        self.app.server.client_disconnected.connect(self.refresh_peers_list)
    
    def compose(self) -> ComposeResult:
        with Container(id="LobbyContainer"):
            self.PeersList : ListView = ListView()
            with Vertical():
                yield self.PeersList

    def refresh_peers_list(self) -> None:
        self.PeersList.clear()                                 # wipe old entries
        for idx, client_sock in enumerate(self.app.server.clients, 1):
            addr = client_sock.getpeername()
            item = ListItem(Label(f"{idx}. {addr[0]}:{addr[1]}")) 
            self.PeersList.append(item)
        
        self.call_later(self.recompose)
            
#

class FindLobby(ModalScreen):
    def on_mount(self) -> None:
        self.app.server.server_started.connect(self.on_server_creation_successful)

    
    def compose(self) -> ComposeResult:
        with Vertical(id="FindLobbyContainer"):
            with Horizontal():
                yield Input(placeholder="ip address", type="text", id="lobby_input_address")
                yield Input(placeholder="port", type="number", max_length=5, id="lobby_input_port")
            
            with Horizontal():
                yield Button("Host", name="button_host")
                yield Button("Join", name="button_join")

            
            yield Label("hi", id="cool_label")
            
            
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        addr_input = self.query_one("#lobby_input_address", Input)
        port_input = self.query_one("#lobby_input_port", Input)
        match event.button.name:
            case "button_host":
                if (addr_input.value, port_input.value):
                    self.app.server.host = str(addr_input.value)
                    self.app.server.port = int(port_input.value)

                    def spawn_host_client() -> None:
                        self.app.client.host = self.app.server.host
                        self.app.client.port = self.app.server.port
                        
                        self.app.client.connect()
                        
                    self.app.server.server_started.disconnect(spawn_host_client)
                    self.app.server.server_started.connect(spawn_host_client)
                    

                    self.run_worker(
                        lambda: self.app.server.start(),
                        thread=True
                    )

            case "button_join":
                if (addr_input.value and port_input.value):
                    self.app.client.host = str(addr_input.value)
                    self.app.client.port = int(port_input.value)

                        # Optional: start receiving in background if needed
                        # client.receive(lambda data: print("Received:", data))
                    try:
                        self.app.pop_screen()  # Close the modal
                    except Exception as e:
                        self.query_one("#cool_label", Label).update("Failed to join")
                        print("Join error:", e)

    
    #
    def on_server_creation_successful(self) -> None:
        self.app.pop_screen()
        
    
    def on_server_creation_failed(self) -> None:
        self.query_one("#cool_label", Label).update("failed to create server")
        
        