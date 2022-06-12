#render_template renderiza nossos arquivos .HTML
#request coleta as informações do nosso formulário
#session permite que retenhamos informações pelos cookies do navegador
#flash serve para mostramos mensagens na tela para o usuário
#url_for dinamiza as nossas referencias às rotas


from unicodedata import category
from flask import Flask, flash, redirect, render_template, request, redirect, session, flash, url_for

#Criando uma classe para os jogos
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

#Criando uma classe para os usuarios
class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome=nome
        self.nickname=nickname
        self.senha=senha

usuario1 = Usuario('Geralt', 'lobo_branco', 'alohomora')
usuario2 = Usuario('Yennefer', 'yen', 'teste')
usuario3 = Usuario('Ciri', 'cintra_leon', 'winter')
usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

#Deixando a lista de jogos global para todas as funções usarem
jogo1=Jogo('The Witcher 3','Action RPG','PS4')
jogo2=Jogo('Little Big Planet 3','Adventure','PS4')
jogo3=Jogo('Prey','FPS','PS5')
lista_jogos = [jogo1,jogo2,jogo3]

#Criando o aoo em Flask
app = Flask(__name__) #__name__ se refere ao proprio arquivo

#Criando criptrografia do site
app.secret_key = "A1ur4"


#Rota padrão
@app.route('/')
def index():
    
    return render_template('lista.html', titulo='Lista de Jogos', jogos=lista_jogos) #O Flask ja sabe que o arquivo esta na pasta templates por padronização da ferramenta


#Form de novo jogo
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo_jogo.html', titulo='Cadastro de Jogo')

#Criação de um novo jogo
@app.route('/criar', methods=['POST',]) #Especificamos que aceita POST
def criar():

    nome = request.form['nome'] #Capturando os dados do formulario com request
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome,categoria,console) #Chamando a classe Jogo para cirar um novo jogo
    lista_jogos.append(jogo) #Append do novo jogo criado para a lista de jogos
    return redirect(url_for('index')) #Redireciona para a rota "/"


@app.route('/login', methods=['GET',])
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Faça se Login', proxima=proxima)    

@app.route('/autenticar', methods=['POST',])
def autenticar():

    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash('Bem-vindo {}!'.format(session['usuario_logado']), 'alert alert-success')
            proxima_pag = request.form['proxima']
            return redirect(proxima_pag)

    else:
        flash('{} não existe!'.format(request.form['usuario']), 'alert alert-warning')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None 
    flash('Logout efetuado com sucesso!', 'alert alert-success')
    return redirect(url_for('login'))

app.run(debug=True) #debug faz com que nossa aplicação entende e atualize alterações em tempo real