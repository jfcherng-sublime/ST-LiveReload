#!/usr/bin/python
try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import SimpleHTTPRequestHandler

import LiveReload

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import sys

# HTTP handler with WebSocket upgrade support


class WSRequestHandler(SimpleHTTPRequestHandler):

    def __init__(
        self,
        req,
        addr,
        ):

        SimpleHTTPRequestHandler.__init__(self, req, addr, object())

        self.server_version = 'LiveReload/1.0'

    def do_GET(self):
        if self.headers.get('upgrade') and self.headers.get('upgrade').lower() == 'websocket':

            if self.headers.get('sec-websocket-key1') or self.headers.get('websocket-key1'):

                # For Hixie-76 read out the key hash

                self.headers.__setitem__('key3', self.rfile.read(8))

            # Just indicate that an WebSocket upgrade is needed

            self.last_code = 101
            self.last_message = '101 Switching Protocols'
        else:
            req = urlparse(self.path)
            file = LiveReload.API.has_file(req.path)
            httpcallback = LiveReload.API.has_callback(req.path)
            if httpcallback:
                try:
                    plugin = sys.modules['LiveReload'].PluginAPI.PluginFactory.getPlugin(LiveReload.Plugin, httpcallback['cls'])
                    func = getattr(plugin, httpcallback['name'], None)
                    if func:
                        res = func(req)
                        self.send_response(200, res)
                    else:
                        res = "Callback method not found"
                        self.send_response(404, 'Not Found')
                except Exception as e:
                    self.send_response(500, 'Error')
                    res = e

                self.send_header('Content-type', 'text/plain')
                self.send_header('Content-Length', len(res))
                self.end_headers()
                self.wfile.write(bytes(res.encode("UTF-8")))
                return
            if file:
                buffer = file['buffer'].read() if hasattr(file['buffer'], 'read') else file['buffer']

                self.send_response(200, 'OK')
                self.send_header('Content-type', file['content_type'])
                self.send_header('Content-Length', len(buffer))
                self.end_headers()
                self.wfile.write(bytes(buffer.encode("UTF-8")))
                return

            # Disable other requests
            notallowed = "Method not allowed"

            self.send_response(405, notallowed)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-Length', len(notallowed))
            self.end_headers()
            self.wfile.write(bytes(notallowed.encode("utf-8")))
            return

    def send_response(self, code, message=None):

        # Save the status code

        self.last_code = code
        SimpleHTTPRequestHandler.send_response(self, code, message)

    def log_message(self, f, *args):

        # Save instead of printing

        self.last_message = f % args
