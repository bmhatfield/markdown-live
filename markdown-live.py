import os
import time
import optparse

# Included with project, but full source found here --
# https://github.com/trentm/python-markdown2
import markdown2

# Included with project, full docs found here --
# https://github.com/defnull/bottle
from bottle import route, run, template, abort, static_file

# Create markdown processor object
mdp = markdown2.Markdown()

# Read command line arguments
parser = optparse.OptionParser()
parser.add_option('--host', dest='host', default='localhost', help='IP Address for Bottle to bind to')
parser.add_option('--port', dest='port', default=8080, help='Port for Bottle to bind to')
parser.add_option('--path', dest='path', default='.', help='Provide path to where Markdown files can be found')
parser.add_option('--content', dest='content', default='static', help='Provide path to where static files (like CSS) can be found')
parser.add_option('--reloader', dest='reloader', default=False, action='store_true', help='Enable bottle reloader mode')
parser.add_option('--debug', dest='debug', default=False, action='store_true', help='Enable bottle debug mode')
options, args = parser.parse_args()

html_start = '<html>\n<head>\n<link rel="stylesheet" href="/static/markdown-simple.css" type="text/css">\n</head>\n<body>\n'
html_end = '</body>\n</html>'

@route('/:name')
def index(name):
    markdown_file = os.path.join(options.path, "%s.md" % (name))

    if os.path.isfile(markdown_file):
        if options.debug:
            t1 = time.time()
        with open(markdown_file, 'r') as mdfh:
            raw_markdown = mdfh.read()
            md_html = mdp.convert(raw_markdown)

            if options.debug:
                print "Markdown conversion time: %0.3fs" % (time.time() - t1)

            return template(html_start + md_html + html_end)
    else:
        abort(404, "No markdown found.")

@route('/static/<filename:path>')
def sfile(filename):
    return static_file(filename, root=options.content)

run(host=options.host, port=options.port, reloader=options.reloader, debug=options.debug)