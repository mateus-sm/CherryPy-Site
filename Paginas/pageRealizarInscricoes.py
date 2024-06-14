import cherrypy
import os

# Chega em \CherryPy-Site #https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory?noredirect=1&lq=1
abs_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from classes.formulario import Formulario

class PaginaInscricao():
    topo = open(abs_dir + "\\Site\\cabecalho.html", encoding='utf-8').read()
    conteudo = open(abs_dir + "\\Site\\Page02.html", encoding='utf-8').read()
    rodape = open(abs_dir + "\\Site\\rodape.html", encoding='utf-8').read()
    cadastro = open(abs_dir + "\\Site\\confirmacao.html", encoding='utf-8').read()

    @cherrypy.expose()
    def index(self):
        return self.montaFormulario()
    
    def montaFormulario(self, pId = 0, pNome = "", pIdade = "", pTelefone = "", pCidade = "", pEndereco = "", pInstituicao = ""):
        html = self.topo
        # Formulario
        html += self.conteudo.replace("{ID}", str(pId)).replace("{Nome}", pNome).replace("{Idade}", str(pIdade)).replace("{Telefone}", pTelefone).replace("{Cidade}", pCidade).replace("{Endereco}", pEndereco).replace("{Instituicao}", pInstituicao)
        # Tabela
        html += self.montaTabela()
        html += self.rodape
        return html
    
    def montaTabela(self):
        html =  """
                <br>
                <h1 style="display: flex; justify-content: center; align-items: center;">SQL</h1>
                <table class="evento" style="width: fit-content; margin: auto;">
                    <tbody style="width: 100%; margin: auto;"><tr>
                        <th> Código </th>
                        <th> Nome </th>
                        <th> Idade </th>
                        <th> Telefone </th>
                        <th> Cidade  </th>
                        <th> Endereço </th>
                        <th> Instituição de Ensino </th>
                        <th> Opções </th>
                    </tr>
                """
        objForm = Formulario() # Criar um objeto do tipo Formulario (Instanciar um objeto)
        dados = objForm.obterRegistros() # Retorna uma lista de tuplas com todos os registros gravados no banco de dados
        for reg in dados: # Percorre a lista e gerar o HTML de cada linha da tabela com os dados
            html += f"""
                    <tr>
                        <td style="text-align: center;"> {reg["FORM_ID"]} </td>
                        <td> {reg["FORM_Nome"]} </td>
                        <td style="text-align: center;"> {reg["FORM_Idade"]} </td>
                        <td> {reg["FORM_Telefone"]} </td>
                        <td> {reg["FORM_Cidade"]} </td>
                        <td> {reg["FORM_Endereco"]} </td>
                        <td style="text-align: center;"> {reg["FORM_Instituicao"]} </td>
                        <td style="text-align:center">
                            <a href="excluirFormulario?idFor={reg["FORM_ID"]}">[Excluir]</a>
                            <a href="alterarFormulario?idFor={reg["FORM_ID"]}">[Alterar]</a>
                        </td>
                    </tr>
                    """

        html += """
                        </table><br><br><br>
                    </div>
                </div>
                """

        return html

    @cherrypy.expose()
    def gravarFormulario(self, txtId, txtNome, txtIdade, txtTelefone, txtCidade, txtEndereco, txtInstituicao, btnGravar):
        if len(txtNome) > 0:
            # A descrição não está vazia e os int são validos
            objForm = Formulario()
            objForm.set_nome(txtNome)
            objForm.set_idade(txtIdade)
            objForm.set_telefone(txtTelefone)
            objForm.set_cidade(txtCidade)
            objForm.set_endereco(txtEndereco)
            objForm.set_instituicao(txtInstituicao)
            
            retorno = 0 # Variável para controlar se o comando foi executado com sucesso
            
            if int(txtId) == 0: # É um novo registro no banco
                retorno = objForm.gravar()
            else: # Registro já existe na tabela, fazer apenas a alteração
                objForm.set_id(int(txtId))
                retorno = objForm.alterar()
            if retorno > 0: # Gravação no banco OK
                return self.cadastro
            else:
                return self.cadastro.replace("<h2>Cadastro concluído com sucesso!</h2>", "<h2>Erro ao gravar o Registro</h2>")
        else: # Nome está vazio
            return self.cadastro.replace("<h2>Cadastro concluído com sucesso!</h2>", "<h2>O Nome precisa ser informado!!</h2>")
        
    @cherrypy.expose()
    def excluirFormulario(self, idFor):
        objForm = Formulario()
        objForm.set_id(int(idFor))
        if objForm.excluir() > 0:
            raise cherrypy.HTTPRedirect('/rotaInscricao')
        else:
            return self.cadastro.replace("<h2>Cadastro concluído com sucesso!</h2>", "<h2> Não foi possível excluir o Registro! </h2>")

    @cherrypy.expose()
    def alterarFormulario(self, idFor):
        objForm = Formulario()
        # Buscar no banco de dados a espécie com o ID que foi selecinada na tabela
        dadosFormularioSelect = objForm.obterRegistroE(idFor)
        # Colocar os dados que retornaram do SQL nos inputs do formuário
        return self.montaFormulario(dadosFormularioSelect[0]["FORM_ID"], dadosFormularioSelect[0]["FORM_Nome"], dadosFormularioSelect[0]["FORM_Idade"], dadosFormularioSelect[0]["FORM_Telefone"], dadosFormularioSelect[0]["FORM_Cidade"], dadosFormularioSelect[0]["FORM_Endereco"], dadosFormularioSelect[0]["FORM_Instituicao"])
    
    @cherrypy.expose()
    def limparFormulario(self):
        return self.montaFormulario(0, "", "", "", "", "", "")