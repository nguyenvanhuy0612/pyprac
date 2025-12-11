import xmlrpc.client
import time

# Configuration
# Replace 'localhost' with the IP address of your REMOTE machine.
# Example: REMOTE_IP = '192.168.1.105'
REMOTE_IP = 'localhost' 
PORT = 8000

def run_remote_actions():
    url = f'http://{REMOTE_IP}:{PORT}'
    print(f"Connecting to {url}...")
    
    # Create proxy
    remote = xmlrpc.client.ServerProxy(url)
    
    try:
        # Check connection
        print(f"Server says: {remote.ping()}")
        
        # Get remote screen size
        width, height = remote.size()
        print(f"Remote Screen Size: {width}x{height}")
        
        # Get current position
        x, y = remote.position()
        print(f"Current Remote Position: ({x}, {y})")
        
        print("Moving mouse remotely in 2 seconds...")
        time.sleep(2)
        
        # Move mouse relative
        remote.move(100, 100) # Move right-down 100px
        
        # Move mouse absolute
        remote.moveTo(width // 2, height // 2) # Center
        
        print("Clicking center...")
        # remote.click() # Uncomment to click
        
        print("Typing hello...")
        # remote.write("hello from local", 0.1) # Uncomment to type
        
        print("Done.")
        
    except ConnectionRefusedError:
        print(f"Error: Could not connect to {url}. Make sure rpc_server.py is running on the remote machine.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_remote_actions()
