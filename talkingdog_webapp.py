#!/usr/bin/python3

import cherrypy
import config
import io
from cherrypy.process.plugins import Daemonizer

PRESSES_FILE = '/home/pi/talkingdog/presses.html'

class MainPage(object):

    # Show the list.
    @cherrypy.expose
    def index(self):
        html  = '<h1>Talking Dog Project</h1>'
        html += '<h2>' + config.dog_name + ' said:</h2>'
        html += '<a href="clear">Clear</a><br/><br/>'
        html += '<table>'
        arr = []
        with open(PRESSES_FILE) as f:
            arr = f.readlines()
            arr.reverse()
            for row in arr:
                html += row
        html += '</table>'
        return html

    # Clear the list.
    @cherrypy.expose
    def clear(self):
        try:
            html  = '<h1>Talking Dog Project</h1>'
            with open(PRESSES_FILE, 'w') as f:
                f.write('')
                html = 'Cleared.<br/><br/>'
                html += '<a href="/">Back</a>'
            return html
        except io.UnsupportedOperation:
            print('Error writing file.')

if __name__ == '__main__':
    # Fork.
    #d = Daemonizer(cherrypy.engine)
    #d.subscribe()

    # Set listen address and port.
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 80})

    # Start the web server.
    cherrypy.quickstart(MainPage())
