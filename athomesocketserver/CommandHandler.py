#
# AtHomeSocketServer
# Copyright (C) 2016  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

import os
import glob
import json
from collections import OrderedDict

class CommandHandler:
    """
    Handles commands sent by a network client.

    The protocol is very simple (loosely based on the mpd (music player daemon) protocol).
    The client sends a command line terminated by a newline (\n). In this case, the command line
    consists of a command and any number of operands.
    The command handler parses the command line into into its constituent parts.
    The command handler executes the command a returns a JSON formatted response.
    The response is one line, terminated with a newline.
    The JSON payload is a dictionary. The following properties appear in all responses.
        command: the command for which the response was generated
        result: OK or ERROR
    The remainder of the response is command dependent.

    Examples
    Client sends:
        scriptfiles\n
    Server responds:
        {"command": "scriptfiles", "result": "OK", "scriptfiles": ["definitions.dmx", "test-end.dmx", "test.dmx"]}\n

    Client sends:
        bad-command\n
    Server responds:
        {"command": "bad-command", "result": "ERROR", "messages": ["Unrecognized command"]}\n

    The easiest way to experiment with the client is to use telnet. Simply open
    a connection and type commands.
        telnet server host
    """

    # Protocol constants
    OK_RESPONSE = "OK"
    ERROR_RESPONSE = "ERROR"
    END_RESPONSE_DELIMITER = "\n"

    class Response:
        def __init__(self, command, result=None, state=None):
            self._response = OrderedDict()
            self._response["command"] = command
            if result:
                self._response["result"] = result
            if state:
                self._response["state"] = state

        def set_result(self, result):
            self._response["result"] = result

        def set_state(self, state):
            self._response["state"] = state

        def set_value(self, key, value):
            self._response[key] = value

        def __str__(self):
            return json.dumps(self._response) + CommandHandler.END_RESPONSE_DELIMITER

    def __init__(self):
        """
        Constructor for an instance of CommandHandler
        """
        # Valid commands and their handlers
        self._valid_commands = {
        }

    def execute_command(self, raw_command):
        """
        Execute a client command/request.
        :param raw_command:
        :return:
        """
        tokens = raw_command.lower().split()
        if (len(tokens) >= 1) and (tokens[0] in self._valid_commands):
            if self._valid_commands[tokens[0]]:
                response = self._valid_commands[tokens[0]](tokens, raw_command)
            else:
                r = CommandHandler.Response(tokens[0], result=CommandHandler.ERROR_RESPONSE)
                r.set_value("messages", "Command not implemented")
                response = str(r)
        else:
            r = CommandHandler.Response(tokens[0], result=CommandHandler.ERROR_RESPONSE)
            r.set_value("messages", "Unrecognized command")
            response = str(r)

        # Return the command generated response with the end of response
        # delimiter tacked on.
        return response
