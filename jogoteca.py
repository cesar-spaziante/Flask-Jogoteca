#render_template renderiza nossos arquivos .HTML
#request coleta as informações do nosso formulário

from flask import Flask, redirect, render_template, request, redirect

#Criando uma classe para os jogos
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

#Deixando a lista de jogos global para todas as funções usarem
jogo1=Jogo('The Witcher 3','Action RPG','PS4')
jogo2=Jogo('Little Big Planet 3','Adventure','PS4')
jogo3=Jogo('Prey','FPS','PS5')
lista_jogos = [jogo1,jogo2,jogo3]

#Criando o aoo em Flask
app = Flask(__name__) #__name__ se refere ao proprio arquivo

#Rota padrão
@app.route('/')
def index():
    
    return render_template('lista.html', titulo='Lista de Jogos', jogos=lista_jogos) #O Flask ja sabe que o arquivo esta na pasta templates por padronização da ferramenta


#Form de novo jogo
@app.route('/novo')
def novo():
    return render_template('novo_jogo.html', titulo='Cadastro de Jogo')

#Criação de um novo jogo
@app.route('/criar', methods=['POST',]) #Especificamos que aceita POST
def criar():

    nome = request.form['nome'] #Capturando os dados do formulario com request
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria,console) #Chamando a classe Jogo para cirar um novo jogo
    lista_jogos.append(jogo) #Append do novo jogo criado para a lista de jogos
    return redirect('/') #Redireciona para a rota "/"

app.run(debug=True) #debug faz com que nossa aplicação entende e atualize alterações em tempo real