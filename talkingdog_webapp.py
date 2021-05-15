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
        html = self.htmlHeader()
        html += '<h2>' + config.dog_name + ' said:</h2>'
        arr = []
        with open(PRESSES_FILE) as f:
            arr = f.readlines()
            if len(arr) > 0:
                arr.reverse()
                html += '<table>'
                for row in arr:
                    html += row
                html += '</table>'
            else:
                html += '<i>Nothing yet.</i>'
        html += '<br/><br/>'
        html += '<a href="clear">Clear</a>'
        html += self.htmlFooter()
        return html

    # Clear the list.
    @cherrypy.expose
    def clear(self):
        html = self.htmlHeader()
        try:
            with open(PRESSES_FILE, 'w') as f:
                f.write('')
                html = 'Cleared.<br/><br/>'
                html += '<a href="/">Back</a>'
        except io.UnsupportedOperation:
            print('Error writing file.')
        html += self.htmlFooter()
        return html

    def htmlHeader(self):
        html = '<html><head><title>Talking Dog Project</title><style>'
        html += 'body {font-family: sans-serif}'
        html += 'table {background-color: #eee; border-spacing: 5px;}'
        html += '.timestamp-td {color: #666}'
        html += '.text-td {font-weight: bold}'
        html += '</style></head>'
        html += '<body>'
        html += '<h1>Talking Dog Project</h1>'
        return html

    def htmlFooter(self):
        html = '</body></html>'
        return html

if __name__ == '__main__':
    # Fork.
    #d = Daemonizer(cherrypy.engine)
    #d.subscribe()

    # Set listen address and port.
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 80})

    # Start the web server.
    cherrypy.quickstart(MainPage())
