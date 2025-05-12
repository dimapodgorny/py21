import asyncio

class Network():    
    server = None
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info("peername")
        await writer.drain()
        writer.close()
        
    async def host_lobby(self, ADDR: str, PORT: int):
        try:            
            self.server = await asyncio.start_server(
                self.handle_client,
                host = ADDR,
                port = PORT
            )
            addr = self.server.sockets[0].getsockname()
            
        except OSError as err:
            pass
        
    async def join_lobby(self, ADDR: str, PORT: int):
        try:
            reader, writer = await asyncio.open_connection(ADDR, PORT)
            data = await reader.readline()
            writer.close()
            await writer.wait_closed()
            
        except Exception:
            pass
        
        
global Multiplayer
Multiplayer = Network()