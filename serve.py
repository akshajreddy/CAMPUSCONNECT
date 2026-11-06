#!/usr/bin/env python3
"""
CampusConnect - Local Development Server
Launches a lightweight HTTP server to preview the landing page.
Usage:
    python serve.py [port]
"""

import http.server
import socketserver
import sys
import webbrowser
import os

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DEFAULT_PORT = 3000

def find_available_port(start_port):
    port = start_port
    while port < start_port + 50:
        try:
            with socketserver.TCPServer(("", port), None) as s:
                return port
        except OSError:
            port += 1
    return start_port

def run_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port '{sys.argv[1]}', using default {DEFAULT_PORT}")
            
    port = find_available_port(port)
    handler = http.server.SimpleHTTPRequestHandler
    
    # Enable friendly MIME types
    handler.extensions_map.update({
        '.js': 'application/javascript',
        '.jsx': 'text/jsx',
        '.css': 'text/css',
        '.html': 'text/html',
        '.svg': 'image/svg+xml',
    })

    print("-" * 60)
    print(" [*] CampusConnect Landing Page Server")
    print(f" [*] Serving live at: http://localhost:{port}")
    print(f" [*] Root directory:  {os.getcwd()}")
    print(" [*] Press Ctrl+C to stop the server")
    print("-" * 60)

    try:
        webbrowser.open(f"http://localhost:{port}")
    except Exception:
        pass

    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped gracefully.")

if __name__ == "__main__":
    run_server()
