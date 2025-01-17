from http.server import SimpleHTTPRequestHandler, HTTPServer
import os


class ReactHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve index.html for all unknown paths
        static_dir = os.path.join(os.path.dirname(__file__), "static")
        requested_path = os.path.join(static_dir, self.path.lstrip("/"))

        # Check if the requested path is a file
        if not os.path.isfile(requested_path):
            self.path = "/index.html"

        return super().do_GET()


def serve(port=3000):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    os.chdir(static_dir)  # Change directory to static files

    handler = ReactHandler
    server = HTTPServer(("localhost", port), handler)
    print(f"Serving React app at http://localhost:{port}")
    server.serve_forever()
