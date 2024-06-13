import cherrypy
import os

from pageDetalhesDoEvento import PaginaDetalhes
from pageRealizarInscricoes import PaginaInscricao
from pageEventosJaRealizados import PaginaEventos
from pageVistoEmAula import PaginaVisto

from pageMateus import PaginaMateus
from pageVinicius import PaginaVinicius
from pageEduardo import PaginaEduardo
from pageIgor import PaginaIgor
from pageKaiky import PaginaKaiky

local_dir = os.path.dirname(__file__)

class Principal():
    topo = open(local_dir + "\\Site\\cabecalho.html", encoding='utf-8').read()
    conteudo = open(local_dir + "\\Site\\conteudo.html", encoding='utf-8').read()
    rodape = open(local_dir + "\\Site\\rodape.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        html = self.topo
        html = html + self.conteudo
        html = html + self.rodape

        return html
    
server_config = {
    "server.socket_host": "127.0.0.1",
    "server.socket_port": 80
}

cherrypy.config.update(server_config)

#Para que o cherrypy possa encontrar os arquivos dentro do diretório da aplicação
local_config = {
    "/": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": local_dir
    },
}

#objetos utilizados para rota de navegação
root = Principal() #rota principal "/"

root.rotaDetalhes = PaginaDetalhes() # criação da rota da página
root.rotaInscricao = PaginaInscricao() 
root.rotaEventos = PaginaEventos()
root.rotaVisto = PaginaVisto()

root.rotaMateus = PaginaMateus()
root.rotaVinicius = PaginaVinicius()
root.rotaEduardo = PaginaEduardo()
root.rotaIgor = PaginaIgor()
root.rotaIgor = PaginaIgor()
root.rotaKaiky = PaginaKaiky()

cherrypy.quickstart(root,config=local_config)