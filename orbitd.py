#!/usr/bin/env python3
# coding: utf-8

import park
import uuid
import socket
import sys
import socketserver
import subprocess
import cmd


class Orbit(object):
    def __init__(self):
        self.kv = park.SQLiteStore("orbitd.db")
        if (self.kv.get("local/device_uuid") == None):
            self.kv.put("local/device_uuid", str(uuid.uuid4()))

    def set_root(self, root):
        self.kv.put("global/orbit_root", root);

    def get_device_uuid(self):
        return self.kv.get("local/device_uuid")

    def get_root(self):
        return self.kv.get("global/orbit_root")


#class OrbitServerRequestHandler(socketserver.BaseRequestHandler):
#    def handle(self):
#        # self.request is the TCP socket connected to the client
#        self.data = self.request.recv(1024).strip()
#        print("{} wrote:".format(self.client_address[0]))
#        print(self.data)
#        # just send back the same data, but upper-cased
#        self.request.sendall(self.data.upper())
#        print(self.server.kv.get("local/device_uuid"))


#class OrbitServer(Orbit, socketserver.TCPServer):
#    def __init__(self):
#        Orbit.__init__(self)
#        socketserver.TCPServer.__init__(self, ("", 3302), OrbitServerRequestHandler)


#o = OrbitServer()
#o.serve_forever()


class OrbitShell(cmd.Cmd):
    intro = "Welcome to orbitd shell. See help for all commands available"
    prompt = "> "
    orbit = Orbit()

    def do_getUUID(self, arg):
        print(self.orbit.get_device_uuid())

    def do_getRoot(self, arg):
        print(self.orbit.get_root())

    def do_exit(self,arg):
        sys.exit(0)


if __name__ == '__main__':
    if( len(sys.argv) == 2 and sys.argv[1] == "shell"):
        OrbitShell().cmdloop()
