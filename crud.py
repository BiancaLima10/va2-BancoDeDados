#coding: utf-8

from appJar import gui
import MySQLdb

conexao = MySQLdb.connect("192.168.56.101", "va1_user", "va1_user", "mundo")
print conexao
cursor = conexao.cursor()
print cursor


#cursor.execute("SELECT * FROM Pais;")
# pegar o primeiro resultado
# result1 = cursor.fetchone()
# pegar todos os resultados
# result = cursor.fetchall()
app = gui("CRUD de MySQL", "600x300")



def usando(btn):
	pass
	#app.infoBox("Mensagem de aviso!", "Você me usou. Vou-lhe usar!")

#def name(btn):
	#cod = app.textBox("Seus dados", "Digite seu nome:", parent=None)
	#print cod


def pesquisar(btn):
	termo = app.getEntry("txtBusca")
	if termo == '':
		app.errorBox("Erro", 'Informe um termo para pesquisar!')
	else:
		#SELECT * FROM Cidade WHERE NomeCidade LIKE '%Belo%'
		cursor.execute("SELECT c.NomeCidade, e.NomeEstado FROM Cidade c"+
			" INNER JOIN Estado e ON e.id = c.idEstado " +
			" WHERE c.NomeCidade LIKE '%" + termo + "%'")
		rs = cursor.fetchall()

		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca", x[0] + ' - ' + x[1])
			#app.addListItems("Busca", rs)


def exibir(btn):
	cursor.execute(
		"SELECT c.NomeCidade, e.NomeEstado, p.NomePais FROM Cidade c" +
		"INNER JOIN Estado e ON c.idEstado = idEstado " +
		"INNER JOIN Pais ON Estado.idPais = idPais;"
	)
	rs = cursor.fetchall()

	app.clearListBox("lBusca")

	for x in rs:
		app.addListItem("lBusca", x[0] + ' - ' + x[1] + ' - ' + x[2])



def inserir(btn):
	app.showSubWindow('janela-inserir')


def salvar_estado(btn):
	cidade = app.getEntry('txtcidade')
	idestado = app.getEntry('txtestado')
	cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('{}',{})".format(cidade,idestado))
	#cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('%s',%s)" % (cidade,idestado))
	conexao.commit()
	
	app.clearListBox("lBusca")
	app.addListItem("lBusca", "Cidade " + cidade + " foi inserida!")

	app.hideSubWindow('janela_inserir')



def deletar(btn):
	app.showSubWindow("delete_cidade")



def deletar_estado(btn):
	nome_cidade_delete = app.getEntry("cidade2")
	cursor.execute(
		"SELECT idEstado, NomeEstado FROM Cidade WHERE NomeCidade LIKE '%" + nome_cidade_delete + "%'"
	)
	rs = None
	rs = cursor.fetchone()
	app.clearListBox("lBusca")
	app.addListItem("lBusca", "A" + rs[1] + " foi deletada!")
	cursor.execute(
		"DELETE FROM Cidade WHERE idEstado = %s" % (rs[0])
	)
	conexao.commit()
	app.hideSubWindow("delete_cidade")



def atualizar(btn):
	app.showSubWindow("atualizar_cidade")



def atualizar_estado(btn):
	nome = app.getEntry("nome")
	nome_novo = app.getEntry("nome_novo")
	id_novo = app.getEntry("id_novo")

	cursor.execute(
		"SELECT idEstado, nomeEstado FROM Cidade WHERE nomeEstado LIKE '%" + nome + "%'"
	)
	rs = cursor.fetchone()
	app.clearListBox("lBusca")
	app.addListItem("lBusca", "A cidade " + rs[1] + " foi atualizada para " + nome_novo + " com o ID " + id_novo + " !")
	cursor.execute(
		"UPDATE Cidade "+
		"SET idEstado = " + id_novo + ", Nome = '" + nome_novo + "'"
		"WHERE idCidade = " + str(rs[0])
	)
	conexao.commit()
	app.hideSubWindow("atualizar_cidade")


def main(btn):
    if btn == "Cancel":
        app.stop()
    else:
        usuario = app.getEntry("Usuario")
        senha = app.getEntry("Senha")
        print("Usuario:", usr, "Senha:", senha)


app.startSubWindow("janela-main", modal=True)
app.addLabel("lmain, Inserindo nome/senha...")
app.addEntry('Host')
app.addEntry('Usuario')
app.addEntry('Senha')
app.stopSubWindow()


app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Inserindo dados...")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton('Salvar cidade',salvar_estado)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da cidade")
app.stopSubWindow()


app.startSubWindow("delete_cidade", modal=True)
app.addLabel("lDelete", "Deletar cidade: ")
app.addEntry("cidade2")
app.addButton("Deletar Cidade", deletar_estado)
app.setEntryDefault("cidade2", "Nome Cidade")
app.stopSubWindow()


app.startSubWindow("atualizar_cidade", modal=True)
app.addLabel("lUpdate", "Atualizar cidade: ")
app.addEntry("nome_antigo")
app.addEntry("nome_novo")
app.addEntry("id_novo")
app.addButton("Atualizar Cidade", atualizar_estado)
app.setEntryDefault("nome_antigo", "Nome Antigo")
app.setEntryDefault("nome_novo", "Nome Novo")
app.setEntryDefault("id_novo", "Novo ID")
app.stopSubWindow()


app.addLabel("lNome", '', 0, 0, 2)
app.addButton("Exibir dados", exibir, 1, 0)
app.addButton("Inserir dados", inserir, 1, 1)
app.addButton("Atualizar dados", atualizar, 2, 0)
app.addButton("Excluir dados", deletar, 2, 1)
app.addEntry("txtBusca", 3, 0, 2)
app.setEntryDefault("txtBusca", "Digite o termo...")
app.addButton("Pesquisar", pesquisar, 4, 0, 2)
app.addListBox("lBusca", [], 5, 0, 2)
app.setListBoxRows("lBusca", 5)

#x = app.textBox("NOme", "Informe seu nome")
#app.setLabel("lNome", "Bem-vindo "+x)
app.go()

