import cherrypy
import os

local_dir = os.path.dirname(__file__)

class PaginaKaiky():
    conteudo = open(local_dir + "\\Site\\Portifolios\\Kaiky\\definitivo.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        html = self.conteudo

        return html