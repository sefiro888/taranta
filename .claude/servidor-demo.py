"""Servidor local solo para revisar la demo (desactiva la cache del navegador)."""
import http.server, functools, os

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, max-age=0')
        super().end_headers()

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
http.server.ThreadingHTTPServer(('127.0.0.1', 8123), H).serve_forever()
