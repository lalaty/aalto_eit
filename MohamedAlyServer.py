from __future__ import print_function
#######################################

# Created by Mohamed Aly Bou Hanana on 24.03.2016.

######################################
__author__ = 'Mohamed Aly Bou Hanana'
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import argparse
import re
import cgi
# import urlparse
from urllib.parse import urlparse, parse_qsl, parse_qs
from tools import subbprocessCommand
import json
import os, sys, subprocess
from run import api
import socket
# from sdn import createBasicIntentP2P

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

serverPath = os.path.dirname(os.path.realpath(__file__))


def fwRule(rule):
    subbprocessCommand(rule.split())



def snortRule(rule, file= '/etc/snort/rules/local.rules'):
    subbprocessCommand(['echo', rule, '>>', file])
    restartSnort()



def startSnort():
    subbprocessCommand(['systemctl', 'start', 'snortd'])

def stopSnort():
    subbprocessCommand(['systemctl', 'stop', 'snortd'])

def restartSnort():
    subbprocessCommand(['systemctl', 'restart', 'snortd'])

def restartFirewall():
    subbprocessCommand(['systemctl', 'restart', 'snortd'])

class HTTPRequestHandler(BaseHTTPRequestHandler):
    alert = False
    def do_POST(self):
        if None != re.search('/api/v1/addrecord/*', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'application/json':
                length = int(self.headers.getheader('content-length'))
                data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                recordID = self.path.split('/')[-1]
                LocalData.records[recordID] = data
                print("record %s is added successfully" % recordID)
            else:
                data = {}
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = dict(parse_qsl(parsed_path.query))
        try:

            if query['type'] == 'snort':
                if query['action'] == 'start':
                    try:
                        startSnort()
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')

                        self.end_headers()
                        self.wfile.write(bytes(str('{"result": "ok", "message": "Everything is Ok"}'), "utf-8"))
                    except Exception as e:
                        print('Calling Snort exception:' + str(e))
                        # receiveSnort(out)
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')

                        self.end_headers()
                        self.wfile.write(
                            bytes(str('{"result": "no", "message": "Error: Uncaught snort Exception ' + str(e) + '"}'),
                                  "utf-8"))
                elif query['action'] == 'rule':
                    try:
                        snortRule(query['rule'])
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')

                        self.end_headers()
                        self.wfile.write(bytes(str('{"result": "ok", "message": "Everything is Ok"}'), "utf-8"))
                    except Exception as e:
                        print('Calling Snort exception:' + str(e))
                        # receiveSnort(out)
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')

                        self.end_headers()
                        self.wfile.write(
                            bytes(str('{"result": "no", "message": "Error: Uncaught snort Exception ' + str(e) + '"}'),
                                  "utf-8"))



            elif query['type'] == 'fw':
                if query['action'] == 'rule':
                    try:
                        fwRule(query['rule'])
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')

                        self.end_headers()
                        self.wfile.write(bytes(str('{"result": "ok", "message": "Everything is Ok"}'), "utf-8"))
                    except Exception as e:
                        print('Calling fw exception:' + str(e))
                        # receiveSnort(out)
                        self.send_response(200)
                        self.send_header('Access-Control-Allow-Origin', '*')

                        self.end_headers()
                        self.wfile.write(
                            bytes(str('{"result": "no", "message": "Error: Uncaught fw Exception ' + str(e) + '"}'),
                                  "utf-8"))
        except Exception as e:

            print('not snort exc:' + str(e))

            self.send_response(403)

            self.send_header('Content-Type', 'application/json')

            self.end_headers()

        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()

        HTTPServer.shutdown(self)


class SimpleHttpServer():
    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.server_thread.daemon = True

        self.server_thread.start()

    def waitForThread(self):
        self.server_thread.join()

    def addRecord(self, recordID, jsonEncodedRecord):
        LocalData.records[recordID] = jsonEncodedRecord

    def stop(self):
        self.server.shutdown()

        self.waitForThread()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='HTTP Server')

    # parser.add_argument('port', type=int, help='Listening port for HTTP Server')

    # parser.add_argument('ip', help='HTTP Server IP')

    # args = parser.parse_args()

    # server = SimpleHttpServer(args.ip, args.port)

    ##server = SimpleHttpServer('195.148.125.46', 801)

    server = SimpleHttpServer(getIp(), 801)

    print('HTTP Server Running...........')

    server.start()

    server.waitForThread()
