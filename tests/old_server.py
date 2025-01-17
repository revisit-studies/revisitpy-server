import os
import importlib.resources as resources
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading


class ReactHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Access static files inside the package using importlib.resources
        static_dir = os.path.join(os.path.dirname(__file__), "static")

        # Attempt to serve requested file from the static directory
        requested_path = os.path.join(static_dir, self.path.lstrip("/"))
        if not os.path.isfile(requested_path):
            # If the requested file doesn't exist, serve index.html
            self.path = "/index.html"

        return super().do_GET()


def serve(port=3000):
    def run_server():
        # Use importlib.resources to access files from within the package
        static_dir = os.path.join(os.path.dirname(__file__), "static")

        # If the static directory doesn't exist, we'll create it at runtime for local use
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)

        # Load static files into the package (if needed)
        with resources.path(__package__, 'static') as static_path:
            print(f"Static files served from {static_path}")

        os.chdir(static_dir)  # Change directory to static files for serving
        handler = ReactHandler
        server = HTTPServer(("localhost", port), handler)
        print(f"Serving React app at http://localhost:{port}")
        server.serve_forever()  # Block here for the server

    # Create a thread to run the server in the background
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # Optional: allows the thread to exit when the main program exits
    server_thread.start()

    print("Server started in the background!")
