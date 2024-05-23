import cherrypy
import os

local_dir = os.path.dirname(__file__)

class PaginaEventos():
    topo = open(local_dir + "\\Site\\cabecalho.html", encoding='utf-8').read()
    conteudo = open(local_dir + "\\Site\\Page03.html", encoding='utf-8').read()
    rodape = open(local_dir + "\\Site\\rodape.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        html = self.topo
        html += self.conteudo
        html += self.rodape

        return html