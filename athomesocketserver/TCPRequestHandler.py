#
# AtHomeSocketServer
# Copyright (C) 2016  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# See the LICENSE file for more details.
#

import SocketServer

class TCPRequestHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    call_sequence = 1

    # The command_handler_class is injected by the user of this class
    # See dmx_client.py for an example implementation.
    command_handler_class = None

    @classmethod
    def set_command_handler_class(cls, command_handler_to_use, connection_time_out=5.0):
        """
        Command handler injection
        :param command_handler_to_use: A class that implements a
        Response class and an execute_command method.
        :param connection_time_out:
        :return:
        """
        cls.command_handler_class = command_handler_to_use
        cls.connection_time_out = connection_time_out

    """
    This handler uses raw data from the SocketServer.TCPServer class.
    """

    def handle(self):
        print "Connection from {0}".format(self.client_address[0])

        # Do until close is received
        connection_open = True
        while connection_open:
            # self.request is the TCP socket connected to the client
            raw_command = self.read_command()

            if raw_command and len(raw_command) > 0:
                try:
                    print "Request: {0}, on socket: {1}".format(raw_command, self.request.getsockname())
                    raw_command = raw_command.lower()

                    # The command handler generates the response
                    if TCPRequestHandler.command_handler_class:
                        # Create an instance of the command handler
                        handler = TCPRequestHandler.command_handler_class()
                        # Pass the command string to the command handler
                        response = handler.execute_command(self.request.getsockname()[1], raw_command)
                    else:
                        r = TCPRequestHandler.command_handler_class.Response(raw_command,
                            result=TCPRequestHandler.command_handler_class.ERROR_RESPONSE)
                        r.set_value("message", "No command handler")
                        response = r

                    print "Request completed"
                except Exception as ex:
                    print "Exception occurred while handling request"
                    print str(ex)
                    print raw_command
                    r = TCPRequestHandler.command_handler_class.Response(raw_command,
                        result=TCPRequestHandler.command_handler_class.ERROR_RESPONSE)
                    r.set_value("message", "ERROR Exception occurred while handling request")
                    response = r
                finally:
                    pass

                # Note that session end is detected by convention. Any command that
                # starts with close or quit will end the session.
                # if raw_command.startswith("close") or raw_command.startswith("quit"):
                connection_open = not response.is_closed()

                TCPRequestHandler.call_sequence += 1
            else:
                r = TCPRequestHandler.command_handler_class.Response(raw_command,
                                                                     result=TCPRequestHandler.command_handler_class.ERROR_RESPONSE)
                if raw_command:
                    r.set_value("message", "Empty command ignored")
                else:
                    r.set_value("message", "Connection timed out")
                response = r
                # We consider this an error, so we force close the socket
                connection_open = False

            # Return the response to the client
            self.request.sendall(str(response))

        print "Socket {0} closed".format(self.client_address[0])

    def read_command(self):
        """
        Read a command from a socket
        """
        command = ""
        # Time out. This will close the connection.
        self.request.settimeout(TCPRequestHandler.connection_time_out)

        try:
            c = self.request.recv(1)
            while c != "\n":
                if c != "\r":
                    command += c
                c = self.request.recv(1)

        except Exception as ex:
            command = None

        return command
