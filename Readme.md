# Socket Server with Command-Line-Like API
Copyright © 2016, 2018 by Dave Hocker (AtHomeX10@gmail.com)

## Overview
This package implements a simple TCP socket based client-server
interface using the SocketServer/socketserver package.
The client opens a session with the server (basically
a telnet kind of session). It sends commands to the server and
the server returns responses in JSON format.

This package is used in the AtHomeDMX and AtHomeLED projects.

## Compatibility
This package is Python 2/3 compatible. It has been tested on
Python 2.7 and 3.6.

## Classes
### ThreadedTCPServer
This class is simply derived from the SocketServer.ThreadingMixIn
and SocketServer.TCPServer classes. A new instance of this class takes
a host address, port number and command handler class. The command
handler class is a class that implements the following:

* A Response class
* An execute_command method

The CommandHandler file provides an example of a command handler
class.

### CommandHandler and Response
The Response class is implemented within the command handler class. It
must implement the following methods.

* set_result
* set_state
* set_value
* is_closed
* __str__ (converts response to JSON string)

The CommandHandler file provides an example of a Response class.

### SocketServerThread
Runs an instance of the SocketServer class on a spawned thread.

### TCPReqestHandler
Handles command requests coming through the TCP session.

## Files
### test.py
This file shows how to create an instance of the SocketServerThread
class.

## References
1. [AtHomeDMX Lighting Control Server](http://dhocker.github.io/projects/athomedmx.html)
