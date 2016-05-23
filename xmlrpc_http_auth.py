#!/usr/local/bin/python3


import argparse
import xmlrpc.client
from base64 import b64decode
from xmlrpc.server import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler

class SecureXMLRPCServer(SimpleXMLRPCServer):
    def __init__(self,host,port,username,password,*args,**kargs):
        self.username = username
        self.password = password

        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
            def parse_request(request):
                if SimpleXMLRPCRequestHandler.parse_request(request):
                    if self.authenticate(request.headers):
                        return True

                    else:
                        request.send_error(401,'Authentication failed,try again')
                return False

        SimpleXMLRPCServer.__init__(self,(host,port),requestHandler = VerifyingRequestHandler,*args,**kargs)

    def authenticate(self,headers):
        headers = headers.get('Authorization').split()
        basic,encode = headers[0],headers[1]
        if basic != 'Basic':
            print('Only basic authentication supported')
            return False
        secret = (encode).split(':')
        username,password = secret[0],secret[1]
        return True if (username == self.username and password == self.password) else False


def run_server(host,port,username,password):
    server = SecureXMLRPCServer(host,port,username,password)
    def echo(msg):
        reply = msg.upper()
        print("client said: %s.So we echo that in uppercase: %s" %(msg,reply))
        return reply

    print("Running a HTTP auth enabledXMLRPC server on %s:%s..." % (host,port))
    server.serve_forever()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="multithread multicall XMLRPC SERVER")

    parser.add_argument('--host' ,action='store',dest='host',default='localhost')
    parser.add_argument('--port',action='store',dest='port',default=8000,type=int)
    parser.add_argument('--username',action='store',dest='username',default='user')
    parser.add_argument('--password',action='store',dest='password',default='pass')
    given_args = parser.parse_args()
    host,port = given_args.host,given_args.port
    username,password = given_args.username,given_args.password
    run_server(host,port,username,password)
