import json
from plugin import Plugin
from exceptions import APIError



def main():

    # User name and password for the dummyjson API
    username = "emilys"
    password = "emilyspass"
    
    try:
        plugin = Plugin(username, password)
        
        if not plugin.test_connectivity():
            print("Error: Failed to establish connection with the API")
            exit(1)
            
        evidence = plugin.collect_evidence()
        
        print(json.dumps(evidence, indent=4))
        
    except APIError as e:
        print(f"Error: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 