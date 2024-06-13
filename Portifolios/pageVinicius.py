import cherrypy
import os

#Chega em \CherryPy-Site
abs_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class PaginaVinicius():
    conteudo = open(abs_dir + "\\Site\\Portifolios\\Vinicius\\trabalho.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        html = self.conteudo

        return html