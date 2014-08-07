from bottle import ServerAdapter


class SSLCherryPy(ServerAdapter):
    """
    SSLCherryPy

    Extends the base class ServerAdapter with CherryPy as a WSGI capable server
    for SSL support in Bottle.

    Attributes:
        cert: The SSL certificate.
        key: The key corresponding to the SSL certificate.
    """
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

