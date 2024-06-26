import sqlite3
import os

# Chega em \CherryPy-Site
abs_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Executar todas as rotinas necessárias para abrir e fechar conexão, emitir instruções SQL para o BD
class Banco():

    def __init__(self): # Construtor
        self.__conexao = None
        self.__cursor = None

    def __abrirConexao(self):
        self.__conexao = sqlite3.connect(abs_dir + "\\DB\\Formulario.db")
        self.__conexao.row_factory = sqlite3.Row # Acessar os dados pelos nomes dos atributos da tabela e não somente pela posição que eles se encontram
        self.__cursor = self.__conexao.cursor()

    def __fecharConexao(self):
        self.__cursor.close()
        self.__conexao.close()

    def executarInsertUpdateDelete(self, sql):
        # Quando não recebeu o comando de SQL para ser executado
        linhasAfetadas = -10 # Variável de controle de erro...
        if len(sql) > 0:
            self.__abrirConexao()
            self.__cursor.execute(sql) # Executar no banco
            linhasAfetadas = self.__cursor.rowcount # Número de linhas afetadas pelo SQL
            self.__conexao.commit() # Efetuar SQL
            self.__fecharConexao()
        return linhasAfetadas

    def executarSelect(self, sql):
        dados = ''
        if len(sql) > 0:
            self.__abrirConexao()

            self.__cursor.execute(sql)
            dados = self.__cursor.fetchall() # Colocar os dados que vieram do BD no dados (retorna o resultado do select) - Lista

            self.__fecharConexao()
        return dados