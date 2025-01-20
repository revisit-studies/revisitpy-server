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
            print(self.path)

        return super().do_GET()


def run_server(port):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    handler = ReactHandler
    os.chdir(static_dir)
    server = HTTPServer(("localhost", port), handler)
    server.serve_forever()


if __name__ == "__main__":
    run_server(port=8080)
