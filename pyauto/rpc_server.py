import pyautogui
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import socket

# Restrict to a specific path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def start_server(host='0.0.0.0', port=8000):
    print(f"Starting PyAutoGUI RPC Server on {host}:{port}...")
    
    with SimpleXMLRPCServer((host, port), requestHandler=RequestHandler, allow_none=True) as server:
        server.register_introspection_functions()
        
        # Register wrappers to return basic types (XML-RPC doesn't like named tuples)
        def get_position():
            return tuple(pyautogui.position())
        server.register_function(get_position, 'position')

        def get_size():
            return tuple(pyautogui.size())
        server.register_function(get_size, 'size')

        # Helper to check aliveness
        def ping():
            return "pong"
        server.register_function(ping, 'ping')

        # Track already registered functions so we don't overwrite wrappers
        registered = {'position', 'size', 'ping'}

        # Dynamically register all other public callable functions from pyautogui
        for name in dir(pyautogui):
            if name.startswith('_') or name in registered:
                continue
            
            func = getattr(pyautogui, name)
            if callable(func):
                try:
                    server.register_function(func, name)
                    # print(f"Registered: {name}") 
                except Exception:
                    pass

        print(f"Server is ready. Listening...")
        print(f"Local IP likely: {socket.gethostbyname(socket.gethostname())}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopping...")

if __name__ == "__main__":
    # You can change the port if needed
    start_server()
