import os
import subprocess
import sys



venv_name : str = "py21env"

python_path = os.path.join(os.getcwd(), venv_name, "Scripts", "python.exe")

def ensure_venv() -> bool:
    print("Ensuring virtual environment...")
    if not os.path.exists(venv_name):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_name])
        print(f"Created environment '{venv_name}'")
    else:
        print("Virtual environment already exists.")
        

def ensure_all_packages() -> None:
    subprocess.check_call(
        [python_path, "-m", "pip", "install", "-r", "requirements.txt"]
    )

def update_requirements_file():
    print("Updating requirements.txt...")
    
    subprocess.check_call(
        [python_path, "-m", "pip", "freeze"],
    )
    
    with open("requirements.txt", "w") as f:
        subprocess.check_call(
            [python_path, "-m", "pip", "freeze"],
            stdout=f
        )

ensure_all_packages()
update_requirements_file()

#

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


if __name__ == "__main__":
    app = Py21App()
    app.run()
