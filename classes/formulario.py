from classes.banco import Banco

class Formulario():
    """Documentação da classe
    - aqui devemos descrever os objetivos da classe e suas funcionalidades
    - toda classe deve ter uma responsabilidade única (PGR) e possui propriedades e métodos
    """
    # Toda classe precisa ter o construtor
    def __init__(self):
        # Propriedades públicas
        # Propriedades privadas
        self.__id = 0
        self.__nome = ""
        self.__idade = ""
        self.__banco = Banco() # Essa propriedade é responsável por manter a conexão com o banco de dados especificamente com a tabela Formulario

    # Métodos da classe
    # Métodos getters e setters

    # Setters
    def set_id(self, pId):
        if pId > 0:
            self.__id = pId

    def set_nome(self, pNome):
        if len(pNome) > 0:
            self.__nome = pNome

    def set_idade(self, pIdade):
        if len(pIdade) >= 0:
            self.__idade = pIdade

    def set_telefone(self, pTelefone):
        if len(pTelefone) >= 0:
            self.__telefone = pTelefone

    # Getters
    def get_id(self):
        return self.__id
    
    def get_nome(self):
        return self.__nome
    
    def get_idade(self):
        return self.__idade
    
    def get_telefone(self):
        return self.__telefone

    # Devolver todas as espécies cadastradas no banco de dados
    def obterRegistros(self):
        sql =   """
                select * from DB_Formulario
                order by FORM_Nome
                """
        return self.__banco.executarSelect(sql)

    def obterRegistroE(self, id=0):
        if id != 0:
            self.__id = id # Colocar no objeto o id da linha que foi selecionada na tabela
        sql =   """
                select * from DB_Formulario
                where FORM_ID = {}
                """.format(str(self.__id))
        return self.__banco.executarSelect(sql)

    def gravar(self): # Pegar os dados do objeto e gravar no banco de dados
        sql =   """
                insert into DB_Formulario (FORM_Nome, FORM_Idade, FORM_Telefone)
                VALUES ("{}", "{}", "{}")
                """.format(self.__nome, self.__idade, self.__telefone)
        return self.__banco.executarInsertUpdateDelete(sql)

    def excluir(self): # Exluir o id que está no objeto do banco de dados
        sql = f"delete from DB_Formulario where FORM_ID = {str(self.__id)}"
        return self.__banco.executarInsertUpdateDelete(sql)

    def alterar(self):
        sql =   """
                update DB_Formulario
                set FORM_Nome = "{}", FORM_Idade = "{}", FORM_Telefone = "{}"
                where FORM_ID = {}
                """.format(self.__nome, self.__idade, self.__telefone, self.__id)
        return self.__banco.executarInsertUpdateDelete(sql)


