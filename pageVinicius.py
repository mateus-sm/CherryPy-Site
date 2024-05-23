import cherrypy
import os

local_dir = os.path.dirname(__file__)

class PaginaVinicius():
    conteudo = open(local_dir + "\\Site\\Portifolios\\Vinicius\\trabalho.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        html = self.conteudo

        return html