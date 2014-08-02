from bottle import server_names, ServerAdapter


class SSLCherryPy(ServerAdapter):
    def __init__(self, cert=None, key=None, ** kwargs):
        """Create an SSL capable Bottle ServerAdapter with CherryPy"""
        super(SSLCherryPy, self).__init__(** kwargs)
        self.cert = cert
        self.key = key

    def run(self, app):
        """Initialize and start the SSL Capable CherryPy Server"""
        from cherrypy import wsgiserver
        from cherrypy.wsgiserver import CherryPyWSGIServer, ssl_builtin

        server = CherryPyWSGIServer((self.host, self.port), app)
        server.ssl_adapter = ssl_builtin.BuiltinSSLAdapter(self.cert, self.key)
        try:
            server.start()
        finally:
            server.stop()

# register SSLCherryPy as a wsgi capable server
server_names['sslcherrypy'] = SSLCherryPy
