from classes.banco import Banco

class Formulario():
    '''Documentação da classe
    - aqui devemos descrever os objetivos da classe e suas funcionalidades
    - toda classe deve ter uma responsabilidade única (PGR) e possui propriedades e métodos
    '''
    # toda classe precisa ter o construtor
    def __init__(self):
        # propriedades públicas
        # propriedades privadas
        self.__id = 0
        self.__descricao = ''
        self.__banco = Banco() # essa propriedade é responsável por manter a conexão com o banco de dados especificamente com a tabela Especies

    # métodos da classe
    # métodos getters e setters

    #Setters
    def set_id(self, pId):
        if pId > 0:
            self.__id = pId

    def set_nome(self, pNome):
        if len(pNome) > 0:
            self.__nome = pNome

    #Getters
    def get_id(self):
        return self.__id
    
    def get_nome(self):
        return self.__nome

    # devolver todas as espécies cadastradas no banco de dados
    def obterRegistros(self):
        sql ='''
            select * from DB_Formulario
            order by FORM_Nome
        '''
        return self.__banco.executarSelect(sql)

    def obterRegistroE(self, id=0):
        if id != 0:
            self.__id = id # a gente vai colocar no objeto o id da linha que foi selecionada na tabela
        sql ='''
            select * from DB_Formulario
            where FORM_ID = #id
        '''
        sql = sql.replace('#id', str(self.__id))
        return self.__banco.executarSelect(sql)

    def gravar(self): # vai pegar os dados do objeto e gravar no banco de dados
        sql ='''
            insert into DB_Formulario (FORM_Nome)
            VALUES ("#nome")
        '''
        sql = sql.replace('#nome', self.__nome)
        return self.__banco.executarInsertUpdateDelete(sql)

    def excluir(self): # vai exluir o id que está no objeto do banco de dados
        sql = 'delete from DB_Formulario where FORM_ID = #id'
        sql = sql.replace('#id',str(self.__id))
        return self.__banco.executarInsertUpdateDelete(sql)

    def alterar(self):
        sql ='''
            update DB_Formulario
            set FORM_Nome = "#nome"
            where FORM_ID = #id
        '''
        sql = sql.replace('#id',str(self.__id))
        sql = sql.replace('#nome',self.__nome)
        return self.__banco.executarInsertUpdateDelete(sql)


