import cherrypy
import os

# Chega em \CherryPy-Site
abs_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class PaginaVisto():
    topo = open(abs_dir + "\\Site\\cabecalho.html", encoding='utf-8').read()
    conteudo = open(abs_dir + "\\Site\\Page04.html", encoding='utf-8').read()
    rodape = open(abs_dir + "\\Site\\rodape.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        html = self.topo
        html += self.conteudo
        html += self.rodape

        return html