# Socket Server with Command-Line-Like API - test program
# Copyright 2016  Dave Hocker (email: AtHomeX10@gmail.com)
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

import athomesocketserver.SocketServerThread as SocketServerThread
import athomesocketserver.CommandHandler as CommandHandler
import time
import sys

# This accepts connections from any network interface.
HOST, PORT = "0.0.0.0", 5050

# Create the socket server on its own thread.
# This is done so that we can handle the kill signal which
# arrives on the main thread. If we didn't put the socket server
# on its own thread we would not be able to shut it down in
# an orderly fashion.
print "Creating a SocketServerThread instance"
server = SocketServerThread.SocketServerThread(HOST, PORT, CommandHandler)
print server

# Launch the socket server
try:
    # This runs "forever", until ctrl-c or killed
    print "Press Ctrl-C to terminate..."
    server.Start()
    terminate_service = False
    while not terminate_service:
        # We do a lot of sleeping to avoid using too much CPU :-)
        time.sleep(1)
except KeyboardInterrupt:
    print "\nCtrl-C received"
    print "AtHomePowerlineServer shutting down..."
except Exception as e:
    print e.strerror
    print sys.exc_info()[0]
finally:
    # We actually get here through ctrl-c or process kill (SIGTERM)
    # TODO This needs to move to the clean up function
    server.Stop()
