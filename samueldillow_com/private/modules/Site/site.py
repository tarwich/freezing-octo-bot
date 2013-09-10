import pprint
import cgi
import os
import jinja2

class Site():
    def index(self, jackal, uri):
        jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
            extensions=['jinja2.ext.autoescape']
            )
        template = jinja.get_template("index.html")
        jackal.response.write(str(template.render()))

        