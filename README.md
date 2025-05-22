# py21
### To-do:
- [ ] game
- [X] Network script
- [ ] Functioning network script
- [ ] Networking script that works
- [X] Good enough networking script

---

# Installation
Step by step guide on how to install the project :)

## 1. **Clone the repository**
```bash
git clone https://github.com/dimapodgorny/py21.git
cd py21
```

## 2. **Create the virtual environment and give it the name `py21env`**
```bash
python.exe -m venv py21env
```

## 3. **Activate the virtual environment**
On powershell:
```ps1
Set-ExecutionPolicy Unrestricted -Scope Process
py21env\Scripts\Activate.ps1
```

## 4. **Run app.py**
```bash
/py21env/Scripts/python.exe -m pip install -r requirements.exe
```

# Running the project 
You can either run the project normally, or by running the network script for debugging.

## Running it normally (LOBBY BROKEN)
Assuming you already have app.py open, (if you don't, run `python.exe ./app.py`)

This is pretty much it, as for example if you try hosting or joining a server it will break or crash for now.

Congratulations you've run the app.

---

## Running the network module
#### Host:
1. Start the script `python.exe ./_network_.py`

2. You will be prompted to either host or join a server, enter `host`

3. Enter the desired IP address when prompted to. Your server will be hosted on this address.

4. Enter the desired port when prompted to.

#### Client:
1. Start the script `python.exe ./_network_.py`

2. You will be prompted to either host or join a server, enter `join`

3. When prompted to, enter the IP address the server is hosted on.

4. Enter the port of the server when prompted to.

Congratulations! You can now send messages by writing a something and pressing enter. The message will be broadcasted to everyone other client. Or alternatively you can use commands by prefixing it's "id" with `/`. Use `/help` for a list of commands.
