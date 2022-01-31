import mysql.connector
import time




def criar_conexao(host, usuario, senha, banco):
    return mysql.connector.connect(host=host, user=usuario,password = senha, database= banco )

def fechar_conexao(con):
    return con.close()

def insere_usuario(con, nome, idade, email, cpf, senha):
    cursor = con.cursor()
    sql = 'INSERT INTO usuario(nome, idade, email, cpf, senha) values (%s, %s, %s, %s, %s)'
    valores = (nome, idade, email, cpf, senha)
    cursor.execute(sql, valores)
    cursor.close()

def delete_usuario(con, nome, cpf):
    cursor = con.cursor()
    sql = 'DELETE FROM usuario where nome = %s and cpf = %s'
    valores = (nome, cpf)
    cursor.execute(sql, valores)
    cursor.close()

def select_usuarios(con):
    cursor = con.cursor()
    sql = 'SELECT nome, idade, email, cpf FROM usuario'
    cursor.execute(sql)
    for (nome, idade, email, cpf) in cursor:
        print(f'{nome}  |   {idade}    |   {email}  |   {cpf}')
    cursor.close()


def update_senha(con, senha, nome, cpf):
    cursor = con.cursor()
    sql = 'UPDATE usuario SET senha = %s WHERE nome = %s AND cpf = %s'
    valor = (senha, nome, cpf)
    cursor.execute(sql, valor)
    cursor.close()

def update_email(con, email, nome, cpf):
    cursor = con.cursor()
    sql = 'UPDATE usuario SET email = %s WHERE nome = %s AND cpf = %s'
    valor = (email, nome, cpf)
    cursor.execute(sql, valor)
    cursor.close()

def update_tudo(con, email, senha, nome, cpf):
    cursor = con.cursor()
    sql = 'UPDATE usuario SET email = %s, senha = %s WHERE nome = %s AND cpf = %s'
    valores = (email, senha, nome, cpf)
    cursor.execute(sql, valores)
    cursor.close()


def verifica_usuario(con, nome, cpf):
    global cadastrado
    cadastrado = 0
    cursor = con.cursor()
    sql = 'select nome from usuario where nome = %s AND cpf = %s'
    valores = (nome, cpf)
    cursor.execute(sql, valores)
    resultado = cursor.fetchall()
    if len(resultado) != 0:
        time.sleep(1)
        print('USUÁRIO EXISTE')
        sql = 'select nome, idade, email, cpf from usuario where nome = %s AND cpf = %s'
        valores = (nome, cpf)
        cursor.execute(sql, valores)

        for (nome, idade, email, cpf) in cursor:
            print('  NOME   |   IDADE  |     EMAIL     |    CPF ')
            print(f'{nome}  |   {idade}    |   {email}  |   {cpf}')
        cadastrado = 1
        time.sleep(2)

    else:
        print('USUÁRIO NÃO CADASTRADO')
        cadastrado = 0
        time.sleep(1)

    cursor.close()

def menu_principal(con):

    perg = ''
    while perg != 6:
        perg = int(input('''
    ------ MENU PRINCIPAL ---------------------
    [ 1 ] FAZER O CADASTRO
    [ 2 ] VERIFICAR SE EXISTE CADASTRO
    [ 3 ] ALTERAR O CADASTRO
    [ 4 ] DELETAR O CADASTRO
    [ 5 ] EXIBIR AS PESSOAS JÁ CADASTRADAS
    [ 6 ] ENCERRAR O SISTEMA DE CADASTROS
    
    --------------------------------------------
    O QUE DESEJA FAZER?  
        '''))

        if perg == 1:
            nome = input('DIGITE SEU NOME: ')
            idade = int(input('DIGITE SUA IDADE: '))
            email = input('DIGITE SEU EMAIL: ')
            senha = input('DIGITE SUA SENHA: ')
            cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')
            while len(cpf) != 11:
                print('CPF INVÁLIDO.')
                cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')
            print('CADASTRANDO USUÁRIO...')
            time.sleep(1)
            insere_usuario(con, nome, idade, email, cpf, senha)
            print('USUÁRIO CADASTRADO COM SUCESSO')
            time.sleep(2)

        elif perg == 2:
            print('DIGITE O NOME E O CPF DE QUEM DESEJA VERIFICAR O CADASTRO')
            nome = input('DIGITE SEU NOME: ')
            cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')
            while len(cpf) != 11:
                print('CPF INVÁLIDO.')
                cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')
            print('VAMOS PROCURAR NO SISTEMA...')
            verifica_usuario(con, nome, cpf)

        elif perg == 3:

            print('DIGITE O NOME E O CPF DE QUEM DESEJA ALTERAR O CADASTRO')
            nome = input('DIGITE SEU NOME: ')
            cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')
            while len(cpf) != 11:
                print('CPF INVÁLIDO.')
                cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')
            print('VAMOS PROCURAR NO SISTEMA...')

            verifica_usuario(con, nome, cpf)

            if cadastrado == 0:
                print('NÃO FOI POSSIVEL ALTERAR O USUÁRIO POIS ELE NÃO ESTA CADASTRADO')
            elif cadastrado == 1:
                time.sleep(1)
                menu_alterar = int(input('''
                SELECIONE QUAL ITEM DESEJA ALTERAR
                [ 1 ] EMAIL
                [ 2 ] SENHA
                [ 3 ] AMBOS
                '''))
                if menu_alterar == 1:
                    email = input('DIGITE O NOVO EMAIL: ')
                    update_email(con, email, nome, cpf)
                    time.sleep(1)
                    print('EMAIL ALTERADO COM SUCESSO')

                elif menu_alterar == 2:
                    senha = input('DIGITE A NOVA SENHA: ')
                    senha_confirma = input('CONFIRME A NOVA SENHA: ')
                    while senha != senha_confirma:
                        print('OCORREU ALGUM ERRO AO DIGITAR A SENHA. TENTE NOVAMENTE')
                        senha = input('DIGITE A NOVA SENHA: ')
                        senha_confirma = input('CONFIRME A NOVA SENHA: ')
                    update_senha(con, senha, nome, cpf)
                    time.sleep(1)
                    print('SENHA ALTERADA COM SUCESSO')

                elif menu_alterar == 3:
                    email = input('DIGITE O NOVO EMAIL: ')
                    senha = input('DIGITE A NOVA SENHA: ')
                    senha_confirma = input('CONFIRME A NOVA SENHA: ')
                    while senha != senha_confirma:
                        print('OCORREU ALGUM ERRO AO DIGITAR A SENHA. TENTE NOVAMENTE')
                        senha = input('DIGITE A NOVA SENHA: ')
                        senha_confirma = input('CONFIRME A NOVA SENHA: ')
                    update_tudo(con, email, senha, nome, cpf)
                    time.sleep(1)
                    print('EMAIL E SENHA ALTERADOS COM SUCESSO')
                else:
                    print('COMANDO INVÁLIDO')
            else:
                print('ERRO')

        elif perg == 4:
            print('DIGITE O NOME E O CPF DE QUEM DESEJA DELETAR O CADASTRO')
            nome = input('DIGITE SEU NOME: ')
            cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')
            while len(cpf) != 11:
                print('CPF INVÁLIDO.')
                cpf = input('DIGITE SEU CPF SEM A PONTUAÇÃO: ')

            verifica_usuario(con, nome, cpf)
            if cadastrado == 0:
                print('NÃO FOI POSSÍVEL EXCLUIR O USUÁRIO POIS ELE NÃO SE ENCONTRA NO BANCO DE DADOS')
            elif cadastrado == 1:
                print('DELETANDO USUÁRIO...')
                delete_usuario(con, nome, cpf)
                time.sleep(1)
                print('USUÁRIO DELETADO COM SUCESSO')
                time.sleep(2)
            else:
                print('ERRO')


        elif perg == 5:
            print('AS PESSOAS JÁ CADASTRADAS EM NOSSO SISTEMA SÃO...')
            time.sleep(1)
            print('NOME  |  IDADE   |     EMAIL     |     CPF   ')
            select_usuarios(con)

            time.sleep(2)


        elif perg == 6:
            print('O PROGRAMA SERÁ ENCERRADO')
            break

        else:
            print('COMANDO INVÁLIDO')



def main():
    global con
    con = criar_conexao('localhost', 'root', '', 'cadastro')
    menu_principal(con)
    fechar_conexao(con)


if __name__ == '__main__':
    main()



