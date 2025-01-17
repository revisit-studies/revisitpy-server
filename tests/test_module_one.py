import src.revisit_server.server as rs
import os

if __name__ == "__main__":
    print(os.getcwd())
    process = rs.serve()
    print(os.getcwd())
