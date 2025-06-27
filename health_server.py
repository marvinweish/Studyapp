#!/usr/bin/env python3
"""
Health check server for AWS ECS deployment
Runs alongside the main Flet app to provide health endpoints
"""

import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            health_data = {
                'status': 'healthy',
                'timestamp': int(time.time()),
                'port': os.environ.get('PORT', '8080'),
                'environment': os.environ.get('ENVIRONMENT', 'production'),
                'version': '1.0.0'
            }
            
            self.wfile.write(json.dumps(health_data).encode())
            
        elif self.path == '/ready':
            # Readiness probe - check if app is ready to serve traffic
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            ready_data = {
                'status': 'ready',
                'timestamp': int(time.time())
            }
            
            self.wfile.write(json.dumps(ready_data).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass

def start_health_server(port=8080):
    """Start health check server on the same port as main app"""
    class ThreadedHTTPServer(HTTPServer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.daemon_threads = True
    
    try:
        # Start health server on port + 1 to avoid conflicts
        health_port = port + 1000  # Use a different port range
        server = ThreadedHTTPServer(('0.0.0.0', health_port), HealthCheckHandler)
        print(f"🏥 Health check server starting on port {health_port}")
        
        # Run in daemon thread so it doesn't block main app
        health_thread = threading.Thread(target=server.serve_forever, daemon=True)
        health_thread.start()
        
        return server
    except Exception as e:
        print(f"⚠️ Could not start health server: {e}")
        return None

if __name__ == "__main__":
    # For testing the health server standalone
    port = int(os.environ.get('PORT', 8080))
    server = start_health_server(port)
    
    if server:
        print("Health check server running. Press Ctrl+C to stop.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down health check server...")
            server.shutdown()
