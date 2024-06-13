import cherrypy
import os

local_dir = os.path.dirname(__file__)

from classes.formulario import Formulario

class PaginaInscricao():
    topo = open(local_dir + "\\Site\\cabecalho.html", encoding='utf-8').read()
    conteudo = open(local_dir + "\\Site\\Page02.html", encoding='utf-8').read()
    rodape = open(local_dir + "\\Site\\rodape.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        return self.montaFormulario()
    
    def montaFormulario(self, pId=0, pNome=''):
        html = self.topo
        #formulario
        html += '''
            <div class="Menu-Conteudo FlexSpaceBetween">

                <div class="Menu FlexColumnSpaceBetween">                  
                    <div class="Voltar" style="background-color: #ffffff;">
                        <h2 class="AnularMargem"><a href="/">Voltar</a></h2>
                    </div>
                </div>

                <div class="Conteudo">

                    <div class="evento">
                        <form name="inscircao" action="gravarFormulario" method="post">
                            <div class="pessoal">
                                <div class="p0">
                                    <h3>Dados pessoais:</h3>
                                    </br></br>
                                </div>
                                <input type="hidden" id="txtId" name="txtId" value="%s"/>
                                <div class="p1">
                                    <div class="pnome">
                                        <label for="txtNome">Nome: </label> 
                                        <input type="text" id="txtNome" name="txtNome" value="%s" size="30" maxlength="30">
                                    </div>
                                    </br>
                                    <div class="pidade">
                                        Idade: <input type="text" id="idade">
                                    </div>
                                </div>
                                </br>
                                <div class="p2">
                                    <div class="ptel">
                                        Telefone: <input type="tel" id="telefone">
                                    </div>
                                </div>
                                </br>
                            </div>
                            <div class="endereco">
                                <div class="e0">
                                    <h3>Seção de endereço:</h3>
                                </div>
                                <div class="e1">
                                    <div class="ecid">
                                        Cidade: <input type="text" id="cidade">
                                    </div>
                                </div>
                                <div class="e2">
                                    <div class="eend">
                                        Endereço <input type="text" id="rua">
                                    </div>
                                </div>
                            </div>
                            <div class="part">
                                <div class="part0">
                                    <h3>Participação do evento:</h3>
                                </div>
                                <div class="part1">
                                    Instituição de ensino: <input type="text" id="ensino">
                                </div>
                                </br>
                            </div>

                            <div class="buttons">
                                <div class="b0">
                                    <input type="submit" id="btnGravar" name="btnGravar" value="Gravar">
                                </div>
                                </br>
                                <div class="b1">
                                    <input type="reset" value="Limpar" id="b1">
                                </div>
                            </div>
                            
                        </form>
                    </div>
                     

            ''' % (pId, pNome)
        html += self.montaTabela()
        html += self.rodape
        return html
    
    def montaTabela(self):
        html = '''<table class="alinha">
                     <tr>
                        <th> Código </th>
                        <th> Nome </th>
                        <th> Idade </th>
                        <th> Telefone </th>
                        <th> Cidade  </th>
                        <th> Endereço </th>
                        <th> Instituição de Ensino </th>
                     </tr>  '''
        objForm = Formulario() # estamos criando um objeto do tipo Espécie (Instanciar um objeto)
        dados = objForm.obterRegistros() # vai retornar uma lista de tuplas com todos os registros gravados no banco de dados
        for reg in dados: # percorrer a lista e gerar o html de cada linha da tabela com os dados
            html += ('''<tr>
                        <td> %s </td>
                        <td> %s </td>
                        <td style="text-align:center">
                          <a href="excluirFormulario?idFor=%s">[Excluir]</a>
                          <a href="alterarFormulario?idFor=%s">[Alterar]</a>
                        </td>
                       </tr>  ''' % (reg['FORM_ID'], reg['FORM_Nome'], reg['FORM_ID'], reg['FORM_ID']))      
#<td> %s </td>
#<td> %s </td>
#<td> %s </td>
#<td> %s </td>
#<td> %s </td>

        html += """
                        </table><br><br><br>
                    </div>
                </div>
            """
        return html
    
    @cherrypy.expose()
    def gravarFormulario(self, txtId, txtNome, btnGravar):
        if len(txtNome) > 0: # a descrição não está vazia!!
            objForm = Formulario()
            objForm.set_nome(txtNome)
            retorno = 0 # variável para controlar se o comando foi executado com sucesso!!
            if int(txtId) == 0: # é um novo registro no banco
                retorno = objForm.gravar()
            else: # neste caso o registro já existe na tabela, a gente vai fazer apenas a alteração
                objForm.set_id(int(txtId))
                retorno = objForm.alterar()
            if retorno > 0: # deu certo a gravação no banco
                return '''
                   <h2>O Form <b>%s</b> foi gravado com sucesso!!</h2>
                   <a href="/rotaInscricao">voltar</a>
                    ''' % (txtNome)
            else:
                return '''
                   <h2>Erro ao gravar o Form <b>%s</b></h2>
                   <a href="/rotaInscricao">voltar</a>
                    ''' % (txtNome)
        else: # descrição está vazia
            return '''<h2>O Form precisa ser informado!!</h2>
                     <a href="/rotaInscricao">voltar</a>'''
        
    @cherrypy.expose()
    def excluirFormulario(self, idFor):
        objForm = Formulario()
        objForm.set_id(int(idFor))
        if objForm.excluir() >0:
            raise cherrypy.HTTPRedirect('/rotaInscricao')
        else:
            return '''
                  <h2> Não foi possível excluir a espécie! </h2>
                  <a href="/rotaInscricao"> voltar </a>
                  '''
        
    @cherrypy.expose()
    def alterarFormulario(self, idFor):
        objForm = Formulario()
        # vamos buscar no banco de dados a espécie com o id que foi selecinada na tabela
        dadosFormularioSelect = objForm.obterRegistroE(idFor)
        # vamos colocar os dados que retornaram do SQL nos inputs do formuário
        return self.montaFormulario(dadosFormularioSelect[0]['FORM_ID'], dadosFormularioSelect[0]['FORM_Nome'])