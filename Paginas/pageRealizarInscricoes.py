import cherrypy
import os

#Chega em \CherryPy-Site
abs_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from classes.formulario import Formulario

class PaginaInscricao():
    topo = open(abs_dir + "\\Site\\cabecalho.html", encoding='utf-8').read()
    #conteudo = open(abs_dir + "\\Site\\Page02.html", encoding='utf-8').read()
    rodape = open(abs_dir + "\\Site\\rodape.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        return self.montaFormulario()
    
    def montaFormulario(self, pId = 0, pNome = '', pIdade = ''):
        html = self.topo
        # Formulario
        html += """
                <div class="Menu-Conteudo FlexSpaceBetween">

                    <div class="Menu FlexColumnSpaceBetween" style="overflow: auto;">
                        <div class="Voltar" style="background-color: #ffffff;">
                            <h2 class="AnularMargem"><a href="/">Voltar</a></h2>
                        </div>
                    </div>

                    <div class="Conteudo">

                        <h1 style="display: flex; justify-content: center; align-items: center;">Formulario</h1>

                        <div class="evento">
                            <form name="inscircao" action="gravarFormulario" method="post">
                                <div class="FlexColumnSpaceBetween">

                                    <div style="margin: auto;">
                                        <h3>Dados pessoais:</h3>
                                    </div>
                                    </br>

                                    <input type="hidden" id="txtId" name="txtId" value="%s"/>
                                    <div class="FlexSpaceBetween">

                                        <div style="margin-right: 50px;">
                                            <label for="txtNome">Nome: </label>
                                            <input type="text" id="txtNome" name="txtNome" value="%s" size="30" maxlength="30">
                                        </div>
                                        
                                        <div>
                                            <label for="txtIdade">Idade: </label>
                                            <input type="text" id="txtIdade" name="txtIdade" value="%s" size="30" maxlength="30">
                                        </div>

                                    </div>
                                    </br>

                                    <div style="margin: auto;">
                                        <div>
                                            Telefone: <input type="tel" id="telefone">
                                        </div>
                                    </div>
                                    </br>
                                    
                                </div>
                                </br>

                                <div class="FlexColumnSpaceBetween">

                                    <div style="margin: auto;">
                                        <h3>Seção de endereço:</h3>
                                    </div>
                                    </br>

                                    <div style="margin: auto;">
                                        <div>
                                            Cidade: <input type="text" id="cidade">
                                        </div>
                                    </div>
                                    </br>

                                    <div style="margin: auto;">
                                        <div>
                                            Endereço <input type="text" id="rua">
                                        </div>
                                    </div>
                                    </br>

                                </div>
                                </br>

                                <div class="FlexColumnSpaceBetween">

                                    <div style="margin: auto;">
                                        <h3>Participação do evento:</h3>
                                    </div>
                                    </br>

                                    <div style="margin: auto;">
                                        Instituição de ensino: <input type="text" id="ensino">
                                    </div>
                                    </br>

                                </div>
                                </br>

                                <div class="buttons">

                                    <div>
                                        <input type="submit" id="btnGravar" name="btnGravar" value="Gravar">
                                    </div>
                                    </br>

                                    <div>
                                        <input type="reset" value="Limpar" id="btnLimpar">
                                    </div>

                                </div>
                            </form>
                        </div>
                """ % (pId, pNome, pIdade)
        html += self.montaTabela()
        html += self.rodape
        return html
    
    def montaTabela(self):
        html =  """
                <br>
                <h1 style="display: flex; justify-content: center; align-items: center;">SQL</h1>
                <table class="evento" style="width: fit-content;margin: auto;">
                    <tbody style="width: 100%; margin: auto;"><tr>
                        <th> Código </th>
                        <th> Nome </th>
                        <th> Idade </th>
                        <th> Telefone </th>
                        <th> Cidade  </th>
                        <th> Endereço </th>
                        <th> Instituição de Ensino </th>
                    </tr>
                """
        objForm = Formulario() # Criar um objeto do tipo Formulario (Instanciar um objeto)
        dados = objForm.obterRegistros() # Retorna uma lista de tuplas com todos os registros gravados no banco de dados
        for reg in dados: # Percorre a lista e gerar o HTML de cada linha da tabela com os dados
            html += """
                    <tr>
                        <td> %s </td>
                        <td> %s </td>
                        <td> %s </td>
                        <td>  </td>
                        <td>  </td>
                        <td>  </td>
                        <td>  </td>
                        <td style="text-align:center">
                            <a href="excluirFormulario?idFor=%s">[Excluir]</a>
                            <a href="alterarFormulario?idFor=%s">[Alterar]</a>
                        </td>
                    </tr>
                    """ % (reg['FORM_ID'], reg['FORM_Nome'], reg['FORM_Idade'], reg['FORM_ID'], reg['FORM_ID'])

        html += """
                        </table><br><br><br>
                    </div>
                </div>
                """

        return html

    @cherrypy.expose()
    def gravarFormulario(self, txtId, txtNome, txtIdade, btnGravar):
        if len(txtNome) > 0: # A descrição não está vazia
            objForm = Formulario()
            objForm.set_nome(txtNome)
            objForm.set_idade(txtIdade)
            
            retorno = 0 # Variável para controlar se o comando foi executado com sucesso!!
            if int(txtId) == 0: # É um novo registro no banco
                retorno = objForm.gravar()
            else: # Registro já existe na tabela, fazer apenas a alteração
                objForm.set_id(int(txtId))
                retorno = objForm.alterar()
            if retorno > 0: # Gravação no banco OK
                return  """
                        <h2>O Cadastro <b>%s</b> foi gravado com sucesso!!</h2>
                        <a href="/rotaInscricao">voltar</a>
                        """ % (txtNome)
            else:
                return  """
                        <h2>Erro ao gravar o Form <b>%s</b></h2>
                        <a href="/rotaInscricao">voltar</a>
                        """ % (txtNome)
        else: # descrição está vazia
            return  """
                    <h2>O Nome precisa ser informado!!</h2>
                    <a href="/rotaInscricao">voltar</a>
                    """
        
    @cherrypy.expose()
    def excluirFormulario(self, idFor):
        objForm = Formulario()
        objForm.set_id(int(idFor))
        if objForm.excluir() > 0:
            raise cherrypy.HTTPRedirect('/rotaInscricao')
        else:
            return  """
                    <h2> Não foi possível excluir a espécie! </h2>
                    <a href="/rotaInscricao"> voltar </a>
                    """

    @cherrypy.expose()
    def alterarFormulario(self, idFor):
        objForm = Formulario()
        # Buscar no banco de dados a espécie com o id que foi selecinada na tabela
        dadosFormularioSelect = objForm.obterRegistroE(idFor)
        # Colocar os dados que retornaram do SQL nos inputs do formuário
        return self.montaFormulario(dadosFormularioSelect[0]['FORM_ID'], dadosFormularioSelect[0]['FORM_Nome'], dadosFormularioSelect[0]['FORM_Idade'])