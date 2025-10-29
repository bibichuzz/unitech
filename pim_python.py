import json, re, hashlib, os, sys, string, random, datetime, subprocess

def senha_encode(senha):
    senha_hash = hashlib.sha256()
    senha_hash.update(senha.encode())
    return senha_hash.hexdigest()

def validar_email():
    while True:
            email = input("Digite seu e-mail: ")
            padrao_email = r"^\S+@\S+\.\S+$"
            
            for usuario in dados_users:
                if dados_users[usuario]["email"] == email:
                    print("Esse e-mail já pertence a outro usuário. Não gostaria de fazer seu log-in?")
                    raise Exception
                
            if re.match(padrao_email, email) == None:
                print("E-mail inválido!")
            else:
                return email
            
def show_professor_disc(disciplina_cadastrada_par):
    professor_disciplina = dados_disciplinas[disciplina_cadastrada_par]["professor"]
    if professor_disciplina != None:
        professor_disciplina_user = dados_users[professor_disciplina]["nome"]
        print(f"ID {disciplina_cadastrada_par}: {dados_disciplinas[disciplina_cadastrada_par]["nome"].capitalize()}: Curso {dados_disciplinas[disciplina_cadastrada_par]["curso"].capitalize()}, {dados_disciplinas[disciplina_cadastrada_par]["semestre"]}º semestre, Prof. {professor_disciplina_user}")
    else:
        print(f"ID {disciplina_cadastrada_par}: {dados_disciplinas[disciplina_cadastrada_par]["nome"]}: Curso {dados_disciplinas[disciplina_cadastrada_par]["curso"].capitalize()}, {dados_disciplinas[disciplina_cadastrada_par]["semestre"]}º semestre")

def show_atividade(atv_visualizar):
    print(f"\n----- {dados_atividades[atv_visualizar]["titulo"]} -----")
    print(f"{dados_atividades[atv_visualizar]["conteudo"]}")
    if dados_atividades[atv_visualizar]["tipo"] == "A":
        print(f"Prazo para entrega: {dados_atividades[atv_visualizar]["prazo"]}")


caminho_users = os.path.join(os.path.dirname(__file__), "database_users.json")
caminho_disciplinas = os.path.join(os.path.dirname(__file__), "database_disciplinas.json")
caminho_atividades = os.path.join(os.path.dirname(__file__), "database_atividades.json")
caminho_turmas = os.path.join(os.path.dirname(__file__), "database_turmas.json")

# Abre arquivo e lê os dados que tem nele
try:
    # Usuários
    with open(caminho_users, "r", encoding='utf-8') as arquivo_leitura_user:
        dados_users = json.load(arquivo_leitura_user)
    print("Dados de usuário carregados!")
except:
    # Se arquivo estiver vazio
    dados_users = {}
    print("Não há dados de usuários cadastrados.")

try:
    # Disciplinas
    with open(caminho_disciplinas, "r", encoding='utf-8') as arquivo_leitura_disc:
        dados_disciplinas = json.load(arquivo_leitura_disc)
    print("Dados de disciplinas carregados!")
except:
    # Se arquivo estiver vazio
    dados_disciplinas = {}
    print("Não há dados de disciplinas cadastrados.")

try:
    # Atividades
    with open(caminho_atividades, "r", encoding='utf-8') as arquivo_leitura_atv:
        dados_atividades = json.load(arquivo_leitura_atv)
    print("Dados de atividades carregados!")
except:
    # Se arquivo estiver vazio
    dados_atividades = {}
    print("Não há dados de atividades cadastrados.")

try:
    # Turmas
    with open(caminho_turmas, "r", encoding='utf-8') as arquivo_leitura_tur:
        dados_turmas = json.load(arquivo_leitura_tur)
    print("Dados de atividades carregados!")
except:
    # Se arquivo estiver vazio
    dados_turmas = {}
    print("Não há dados de atividades cadastrados.")

try:
    # Opções da plataforma
    print("---------- UNITECH ----------")
    print("Olá, bem vindo(a) à UniTech! O que você deseja?")
    print("1. Cadastrar novo usuário")
    print("2. Fazer log-in")
    print("3. Sair")
    resposta = int(input("Digite a opção desejada: "))

    # CADASTRO DE USUÁRIO
    if resposta == 1:
        os.system('cls')
        # Pede informações do novo usuário
        print("\n---------- CADASTRO DE USUÁRIO ----------")
        print("Boa! Vamos cadastrar um novo usuário...")

        while True:
            id = f"{''.join(random.choices(string.ascii_letters.upper(),k=3))}{''.join(random.choices("0123456789",k=4))}"
            if id not in dados_users.keys():
                break

        # Nome
        nome = input("Digite seu nome: ")

        # Cargo: 
        while True:
            print("Você é aluno ou professor? Digite o número que corresponde ao seu cargo:")
            print("1. Aluno")
            print("2. Professor")
            cargoEscolha = int(input())
            if cargoEscolha == 1:
                cargo = "aluno"
                break
            elif cargoEscolha == 2:
                cargo = "professor"
                break
            else:
                print("\n Escolha uma opção válida!")

        # Matrícula
        while True:
            matricula = input("Digite a sua matrícula (apenas letras e números): ").upper()
            for usuario in dados_users:
                if dados_users[usuario]["matricula"] == matricula:
                    print("Esta matrícula já está cadastrado! Por favor, entre em contato com a administração.")
                    raise Exception

            if len(matricula) == 7 and matricula[0].isalpha() and matricula[-1].isdigit():
                break
            else:
                print("Digite uma matrícula válida!")

        # CPF
        while True:
            cpf = input("Digite seu CPF (apenas números): ")
            # Se CPF já existir
            for usuario in dados_users:
                if dados_users[usuario]["cpf"] == cpf:
                    print("Este CPF já está cadastrado! Por favor, entre em contato com a administração.")
                    raise Exception

            soma_cpf = 0
            index_cpf = 0

            for i in range(10,1,-1):
                soma_cpf += int(cpf[index_cpf])*i
                index_cpf += 1
            if soma_cpf % 11 < 2:
                digito_1 = 0
            else:
                digito_1 = 11 - soma_cpf % 11

            index_cpf = 0
            soma_cpf = 0
            for i in range(11,1,-1):
                soma_cpf += int(cpf[index_cpf])*i
                index_cpf += 1
            if soma_cpf % 11 < 2:
                digito_2 = 0
            else:
                digito_2 = 11 - soma_cpf % 11
                
            if len(cpf) == 11 and int(cpf[9]) == digito_1 and int(cpf[10]) == digito_2:
                break
            else:
                print("Digite um CPF válido!")

        # Data de nascimento
        while True:
            data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ")
            padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"

            if re.match(padrao_data, data_nascimento):
                break
            else:
                print("Digite uma data válida!")

        if cargo == "aluno":
            while True:
                turma = input("Digite sua turma: ").upper()
                if turma[0:2].isalpha() and turma[2].isdigit() and turma[3].isalpha() and turma[4:6].isdigit() and len(turma)==6:
                    break
                else:
                    print("Digite uma turma válida!")
        else:
            turma = None

        # Validação de e-mail
        email = validar_email()

        # Criptografando a senha do usuário
        senha_input = input("Digite sua nova senha: ")
        senha = senha_encode(senha_input)
        
        # Cria um novo usuário, adicionando-o ao dicionário JSON
        user = {
            "nome": nome,
            "cargo": cargo,
            "matricula": matricula,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "email": email,
            "senha": senha,
            "turma": turma,
            "aprovado": None,
            "admin": False
        }
        dados_users[id] = user
        with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
            json.dump(dados_users, arquivo_escrita, ensure_ascii=False)

        print("Usuário cadastrado com sucesso!")

    elif resposta == 2:
        # LOGANDO O USUÁRIO NA PLATAFORMA
        os.system('cls')
        print("\n---------- LOG-IN ----------")
        print("Boa! Vamos fazer seu log-in...")
        matricula_usuario = input("Digite a matrícula cadastrada: ").upper()
        senha_usuario = input("Digite a sua senha: ")

        # Codificando senha inserida
        senha_usuario_hash = senha_encode(senha_usuario)

        # Comparando os dados com a database JSON
        for usuario in dados_users:
            # Checar se a matrícula cadastrada já foi aprovada pelo administrador
            if dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["aprovado"] == None:
                print("Sua matrícula ainda está em análise. Por favor, tente novamente mais tarde.")
                raise Exception
            
            elif dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["aprovado"] == False:
                print("Sua matrícula foi reprovada. Por favor, entre em contato com a administração.")
                raise Exception

            # Se matrícula e senha estiverem corretos
            elif dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["senha"] == senha_usuario_hash and dados_users[usuario]["aprovado"] == True:
                os.system('cls')
                print(f"----- {dados_users[usuario]["nome"]}, BEM VINDO(A)! -----")
                usuario_sistema = dados_users[usuario]
                break

            # Se matrícula estiver correto, e senha estiver errada
            elif dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["senha"] != senha_usuario_hash:
                print("Senha incorreta. Tente novamente!")
                raise Exception
                
            # Se a matrícula não for encontrado
            elif usuario == list(dados_users)[-1]:
                print("Não foi possível identificar sua matrícula. Não se esqueça de fazer seu cadastro!")
                raise Exception
            
        # Quando usuário estiver logado:
        while True: 
            print("\nO que você gostaria de fazer?")
            print("1. Visualizar minhas informações")
            print("2. Atualizar minhas informações")
            print("3. Excluir meu usuário")
            print("4. Disciplinas")
            if usuario_sistema["admin"] == True:
                print("5. Lista de aprovação")
                print("6. Administrar turmas")
                print("7. Administrar disciplinas")
                print("8. Sair")
            else:
                print("5. Sair")
            resposta_login = int(input("Digite a opção desejada: "))

            if resposta_login == 1:
                cpf_user = usuario_sistema["cpf"]
                os.system('cls')
                print(f"----- USUÁRIO: {usuario_sistema["nome"]} -----")
                print(f"Email: {usuario_sistema["email"]}")
                print(f"Matrícula: {usuario_sistema["matricula"]}")
                print(f"Cargo: {usuario_sistema["cargo"]}")
                print(f"Data de nascimento: {usuario_sistema["data_nascimento"]}")
                print(f"CPF: {cpf_user[0:3]}.{cpf_user[3:6]}.{cpf_user[6:9]}-{cpf_user[9:10]}")
                print(f"Turma: {usuario_sistema["turma"]}")
                #print(f"Curso: {dados_turma[turma]["curso"]}")
                print(f"----------------------------------------")
                continue

            elif resposta_login == 2:
                # Atualizar informações
                os.system('cls')
                print(f"----- ATUALIZANDO INFORMAÇÕES -----")
                print("\nQual informação você gostaria de atualizar?")
                print("1. E-mail")
                print("2. Senha")
                print("3. Voltar")
                resposta_update = int(input("Digite a opção desejada: "))

                if resposta_update == 1:
                    # Novo e-mail
                    email_novo = validar_email()
                    usuario_sistema["email"] = email_novo
                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                    print("E-mail atualizado!")
                    continue

                elif resposta_update == 2:
                    # Nova senha
                    senha_atual = input("Confirme sua senha: ")
                    senha_atual_encode = senha_encode(senha_atual)
                    if senha_atual_encode != usuario_sistema["senha"]:
                        print("Senha inválida! Tente novamente.")
                        continue

                    senha_nova = input("Digite sua nova senha: ")
                    usuario_sistema["senha"] = senha_encode(senha_nova)
                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                    print("Senha atualizada!")
                    continue

                elif resposta_update == 3:
                    continue

                else:
                    raise ValueError

            elif resposta_login == 3:
                os.system('cls')
                print(f"----- EXCLUIR USUÁRIO -----")
                excluir_confirmar = input("Você tem certeza que deseja deletar seu usuário? Você perderá todo o seu progresso nas disciplinas! (S / N) ")
                if excluir_confirmar.lower() == "s" or excluir_confirmar.lower() == "sim":
                    del usuario_sistema
                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                    print("Usuário excluído, até mais!")
                    break
                else:
                    continue




            # Visualizar disciplinas
            elif resposta_login == 4:
                os.system('cls')
                print("----- DISCIPLINAS -----")
                print("\nQual disciplina você gostaria de acessar?")

                if usuario_sistema["cargo"] == "aluno":
                    turma_aluno = usuario_sistema["turma"]
                    for disciplina_aluno in dados_disciplinas:
                        if dados_turmas[turma_aluno]["semestre"] == dados_disciplinas[disciplina_aluno]["semestre"] and dados_turmas[turma_aluno]["curso"] == dados_disciplinas[disciplina_aluno]["curso"]:
                            show_professor_disc(disciplina_aluno)
                    print("< Voltar")

                elif usuario_sistema["cargo"] == "professor":
                    for id_prof, info_usuario in dados_users.items():
                        if info_usuario == usuario_sistema:
                            id_prof_logado = id_prof
                            break # ID encontrado, podemos sair do loop
                    for disciplina_prof in dados_disciplinas:
                        if id_prof_logado == dados_disciplinas[disciplina_prof]["professor"]:
                            show_professor_disc(disciplina_prof)
                    print("< Voltar")

                elif usuario_sistema["admin"] == True:
                    for disciplina_adm in dados_disciplinas:
                        show_professor_disc(disciplina_adm)
                    print("< Voltar")
                
                if usuario_sistema["cargo"] == "professor":
                    resposta_disciplinas = input("\nDigite o ID da disciplina desejada ou + para gerar um relatório de presença: ").upper()
                else:
                    resposta_disciplinas = input("Digite o ID da disciplina desejada: ").upper()
                if resposta_disciplinas == "<":
                    continue
                
                elif resposta_disciplinas == "+" and usuario_sistema["cargo"] == "professor":
                    os.system("cls")
                    print("\n--- RELATÓRIO DE PRESENÇA ---")
                    
                    for id_prof, info_usuario in dados_users.items():
                        if info_usuario == usuario_sistema:
                            id_prof_logado = id_prof
                            break # ID encontrado, podemos sair do loop
                    for disciplina_prof in dados_disciplinas:
                        if id_prof_logado == dados_disciplinas[disciplina_prof]["professor"]:
                            show_professor_disc(disciplina_prof)
                    print("< Voltar")
                    disc_relatorio = input("\nDigite o ID da disciplina a ser impressa: ").upper()
            
                    if disc_relatorio in dados_disciplinas:
                        turmas_disciplina = []
                        for turma_cadastrada in dados_turmas:
                                if dados_turmas[turma_cadastrada]["curso"] == dados_disciplinas[disc_relatorio]["curso"]:
                                    turmas_disciplina.append(turma_cadastrada)

                        if len(turmas_disciplina) > 0:
                            print("\nTurmas cadastradas:")
                            for turma_cadastrada in dados_turmas:
                                if dados_turmas[turma_cadastrada]["curso"] == dados_disciplinas[disc_relatorio]["curso"]:
                                    print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].capitalize()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                            turma_relatorio = input("\nDigite o nome da turma a ser impressa: ").upper()

                            if turma_relatorio in dados_turmas:
                                print(f"\nTurma {turma_relatorio}: {dados_turmas[turma_relatorio]["curso"].capitalize()}, {dados_turmas[turma_relatorio]["semestre"]}º semestre.")
                                while True:
                                    data_presenca = input("Digite a data do relatório (dd/mm/aaaa): ")
                                    padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"

                                    if re.match(padrao_data, data_presenca):
                                        break
                                    else:
                                        print("Digite uma data válida!")
                                print("Imprimindo relatório...")
                                alunos_turma_relatorio = []
                                alunos_turma_relatorio.append(data_presenca)
                                for aluno_turma in dados_users:
                                    if dados_users[aluno_turma]["turma"] == turma_relatorio and dados_users[aluno_turma]["cargo"] == "aluno":
                                        alunos_turma_relatorio.append(f"{dados_users[aluno_turma]["nome"]} - {dados_users[aluno_turma]["matricula"]}")
                                alunos_turma_relatorio.sort()
                                alunos_turma_relatorio.append(f"Turma {turma_relatorio}, curso {dados_turmas[turma_relatorio]["curso"].capitalize()}, {dados_turmas[turma_relatorio]["semestre"]}º semestre")
                                alunos_turma_relatorio.append(f"{turma_relatorio}_{data_presenca.replace("/","")}")
                                subprocess.run(["output/relatorio_presenca.exe"] + alunos_turma_relatorio)
                            else:
                                print("Digite uma turma válida!")
                        else:
                            print("Não há nenhuma turma cadastrada!")
                    else:
                        ("Digite uma disciplina válida!")


                elif resposta_disciplinas in dados_disciplinas:
                    os.system("cls")
                    print(f"----- {dados_disciplinas[resposta_disciplinas]["nome"].upper()} -----")
                    print("Atividades:")

                    if len(dados_atividades) > 0:
                        for atividade in dados_atividades:
                            print(f"ID {atividade}: {dados_atividades[atividade]["titulo"]}")
                    else:
                        print("Não há nenhuma atividade ainda!")  

                    if usuario_sistema["cargo"] == "professor":
                        if len(dados_atividades) > 0:
                            respost_prof_atv = input("\nigite o ID da atividade para acessá-la ou + para adicionar uma atividade: ").upper()
                        else:
                            respost_prof_atv = input("\nAperte enter para voltar ou + para adicionar uma atividade: ").upper()

                        if respost_prof_atv == "+":
                            print("\n--- ADICIONAR POSTAGEM ---")
                            while True:
                                id_atv = f"{''.join(random.choices(string.ascii_letters.upper(),k=3))}{''.join(random.choices("0123456789",k=4))}"
                                if id_atv not in dados_atividades.keys():
                                    break
                            while True:
                                tipo_atv = input("Digite C para cadastrar um CONTEÚDO DE AULA e A para cadastrar uma ATIVIDADE: ").upper()
                                if tipo_atv == "C" or tipo_atv == "A":
                                    break
                                else:
                                    print("Digite um tipo de postagem!")
                            titulo_atv = input("Digite o título da postagem: ")
                            conteudo_atv = input("Digite o conteúdo/explicação da postagem: ")
                            if tipo_atv == "A":
                                while True:
                                    prazo_atv = input("Digite o prazo da atividade (dd/mm/aaaa): ")
                                    padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
                                    if re.match(padrao_data, prazo_atv):
                                        break
                                    else:
                                        print("Digite uma data válida!")
                            else:
                                prazo_atv = None

                            atividade_cadastrar = {
                                "titulo": titulo_atv,
                                "conteudo": conteudo_atv,
                                "prazo": prazo_atv,
                                "tipo": tipo_atv,
                                "disciplina": resposta_disciplinas
                            }
                            dados_atividades[id_atv] = atividade_cadastrar
                            with open(caminho_atividades, "w", encoding='utf-8') as arquivo_escrita:
                                json.dump(dados_atividades, arquivo_escrita, ensure_ascii=False)

                            print("Atividade cadastrada com sucesso!")

                            
                        elif respost_prof_atv in dados_atividades:
                            show_atividade(respost_prof_atv)
                            resposta_atv_edit = input("\nAperte enter para continuar, + para editar a atividade e - para excluí-la. ")

                            if resposta_atv_edit == "-":
                                resposta_atv_exc = input("Tem certeza que deseja excluir essa atividade? (s/n) ").lower()
                                if resposta_atv_exc == "s" or resposta_atv_exc == "sim":
                                    del dados_atividades[respost_prof_atv]
                                    with open(caminho_atividades, "w", encoding='utf-8') as arquivo_escrita:
                                        json.dump(dados_atividades, arquivo_escrita, ensure_ascii=False)
                                    print("Atividade excluída!")
                                else:
                                    continue

                            if resposta_atv_edit == "+":
                                novo_titulo_atv = input("Digite o novo título da atividade: ")
                                novo_conteudo_atv = input("Digite o novo conteúdo da atividade: ")
                                if dados_atividades[respost_prof_atv]["prazo"] == "A":
                                    while True:
                                        novo_prazo_atv = input("Digite o prazo da atividade (dd/mm/aaaa): ")
                                        novo_padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
                                        if re.match(novo_padrao_data, novo_prazo_atv):
                                            break
                                        else:
                                            print("Digite uma data válida!")
                                else:
                                    novo_prazo_atv = None
                                dados_atividades[respost_prof_atv]["titulo"] = novo_titulo_atv
                                dados_atividades[respost_prof_atv]["conteudo"] = novo_conteudo_atv
                                dados_atividades[respost_prof_atv]["prazo"] = novo_prazo_atv
                                with open(caminho_atividades, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_atividades, arquivo_escrita, ensure_ascii=False)
                                print("Dados da atividade atualizados!")
                                
                            
                        else:
                            print("Digite uma atividade válida!")

                    if usuario_sistema["cargo"] == "aluno" and len(dados_atividades) > 0:
                        respost_aluno_atv = input("Digite o ID da atividade para acessá-la: ").upper()
                        if respost_aluno_atv in dados_atividades:
                            show_atividade(respost_aluno_atv)
                            if dados_atividades[respost_aluno_atv]["tipo"] == "A":
                                aluno_atv_resp = input("Deseja fazer a entrega desta atividade? (s/n) ").lower()
                                if aluno_atv_resp == "s":
                                    aluno_atividade_entrega = input("Escreva a sua resposta para a atividade acima: ")
                                    aluno_atv_array = []
                                    aluno_atv_array.append(respost_aluno_atv)
                                    aluno_atv_array.append(dados_atividades[respost_aluno_atv]["titulo"])
                                    aluno_atv_array.append(dados_atividades[respost_aluno_atv]["conteudo"])
                                    aluno_atv_array.append(usuario_sistema["nome"])
                                    aluno_atv_array.append(usuario_sistema["matricula"])
                                    aluno_atv_array.append(aluno_atividade_entrega)
                                    aluno_atv_array.append(dados_disciplinas[resposta_disciplinas]["nome"].capitalize())
                                    subprocess.run(["output/atividade_aluno.exe"] + aluno_atv_array)
                                    
                        else:
                            print("Digite uma atividade válida!")

                else:
                    print("Digite uma disciplina válida!") 


            elif resposta_login == 5 and usuario_sistema["admin"] != True:
                print("\nSem problemas! Parando a execução...")
                break




            # LISTA DE APROVAÇÕES
            elif resposta_login == 5 and usuario_sistema["admin"] == True:
                os.system("cls")
                
                while True:
                    print("----- LISTA DE APROVAÇÕES -----")                
                    for usuario in dados_users:
                        if dados_users[usuario]["aprovado"] == None:
                            print(f"ID {usuario}: {dados_users[usuario]["nome"]}")
                    print("< Sair")
                    resposta_aprovacao = input("\nEscolha qual usuário você seja avaliar (digite o ID): ").upper()

                    if resposta_aprovacao == "<":
                        break       


                    os.system('cls')
                    for usuario_aprovar in dados_users:
                        if usuario_aprovar == resposta_aprovacao:
                            while True:
                                cpf_user = dados_users[usuario_aprovar]["cpf"]
                                print(f"----- USUÁRIO: {dados_users[usuario_aprovar]["nome"]} -----")
                                print(f"Email: {dados_users[usuario_aprovar]["email"]}")
                                print(f"Matrícula: {dados_users[usuario_aprovar]["matricula"]}")
                                print(f"Cargo: {dados_users[usuario_aprovar]["cargo"]}")
                                print(f"Data de nascimento: {dados_users[usuario_aprovar]["data_nascimento"]}")
                                print(f"CPF: {cpf_user[0:3]}.{cpf_user[3:6]}.{cpf_user[6:9]}-{cpf_user[9:10]}")
                                print(f"Turma: {dados_users[usuario_aprovar]["turma"]}")
                                #print(f"Curso: {dados_turma[turma]["curso"]}")
                                print(f"----------------------------------------")
                                resposta_user_aprovacao = int(input("\nDigite 1 para aprovar e 2 para reprovar: "))

                                if resposta_user_aprovacao == 1:
                                    dados_users[usuario_aprovar]["aprovado"] = True
                                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                                        os.system("cls")
                                        print("Usuário aprovado!\n")
                                        break

                                elif resposta_user_aprovacao == 2:
                                    dados_users[usuario_aprovar]["aprovado"] = False
                                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                                        os.system("cls")
                                        print("Usuário reprovado!\n")
                                        break
                                    
                                else:
                                    os.system("cls")
                                    print("ERRO: digite uma resposta válida! 1\n")
                                    continue
                            break

                        elif usuario_aprovar == list(dados_users)[-1]:
                            print("ERRO: digite uma resposta válida! 2\n")
                            continue

            # TURMAS
            elif resposta_login == 6 and dados_users[usuario]["admin"] == True:
                os.system("cls")
                print("--- CONSULTA DE TURMAS ---")
                print("1. Visualizar turmas")
                print("2. Cadastrar turmas")
                print("3. Atualizar turmas")
                print("4. Excluir turmas")
                print("5. Voltar")
                resposta_turmas = int(input("Digite a opção desejada: "))

                if resposta_turmas == 1:
                    os.system("cls")
                    if len(dados_turmas) > 0:
                        print("\nTurmas já cadastradas:")
                        for turma_cadastrada in dados_turmas:
                            print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].capitalize()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                    else:
                        print("Não há nenhuma turma cadastrada!")
                    
                if resposta_turmas == 2:
                    os.system("cls")
                    print("\n--- CADASTRAR NOVA TURMA ---")

                    while True:
                        nome_turma_cadastro = input("Digite o nome da turma no sistema: ").upper()
                        if nome_turma_cadastro in dados_turmas:
                            print("Essa turma já existe! Digite uma turma nova.")
                        elif nome_turma_cadastro[0:2].isalpha() and nome_turma_cadastro[2].isdigit() and nome_turma_cadastro[3].isalpha() and nome_turma_cadastro[4:6].isdigit():
                            break
                        else:
                            print("Digite uma turma válida!")

                    curso_turma_cadastro = input(f"Digite o curso respectivo da turma {nome_turma_cadastro}: ").lower()
                    semestre_turma_cadastro = int(input(f"Digite o número do respectivo semestre da turma {nome_turma_cadastro}: "))

                    turma_cadastrar = {
                        "curso": curso_turma_cadastro,
                        "semestre": semestre_turma_cadastro
                    }
                    dados_turmas[nome_turma_cadastro] = turma_cadastrar
                    with open(caminho_turmas, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_turmas, arquivo_escrita, ensure_ascii=False)

                    print("Turma cadastrada com sucesso!")

                if resposta_turmas == 3:
                    os.system("cls")
                    print("\n--- ATUALIZAR TURMA ---")
                    if len(dados_turmas) > 0:
                        print("\nTurmas cadastradas:")
                        for turma_cadastrada in dados_turmas:
                            print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].capitalize()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                        print("< Voltar")
                        turma_update = input("\nDigite o nome da turma a ser atualizada: ").upper()

                        if turma_update == "<":
                            continue

                        elif turma_update in dados_turmas:
                            print(f"\nTurma {turma_update}: {dados_turmas[turma_update]["curso"].capitalize()}, {dados_turmas[turma_update]["semestre"]}º semestre.")
                            turma_update_semestre = int(input("Digite o número do novo semestre da turma: "))
                            dados_turmas[turma_update]["semestre"] = turma_update_semestre
                            with open(caminho_turmas, "w", encoding='utf-8') as arquivo_escrita:
                                json.dump(dados_turmas, arquivo_escrita, ensure_ascii=False)
                            print("Dados atualizados!")
                                
                        else:
                            print("Digite uma turma válida!")
                    else:
                        print("Não há nenhuma turma cadastrada!")

                if resposta_turmas == 4:
                    os.system("cls")
                    print("\n--- EXCLUIR TURMA ---")
                    if len(dados_turmas) > 0:
                        print("\nTurmas cadastradas:")
                        for turma_cadastrada in dados_turmas:
                            print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].capitalize()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                        print("< Voltar")
                        turma_excluir = input("\nDigite o nome da turma a ser excluída: ").upper()

                        if turma_excluir == "<":
                            continue

                        elif turma_excluir in dados_turmas:
                            print(f"\nTurma {turma_excluir}: {dados_turmas[turma_excluir]["curso"].capitalize()}, {dados_turmas[turma_excluir]["semestre"]}º semestre.")
                            turma_excluir_confirmar = input("Tem certeza que deseja excluir essa turma? (s/n) ").upper()
                            if turma_excluir_confirmar == "S":
                                del dados_turmas[turma_excluir]
                                with open(caminho_turmas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_turmas, arquivo_escrita, ensure_ascii=False)
                                print("Turma excluída!")
                                
                        else:
                            print("Digite uma turma válida!")

                    else:
                        print("Não há nenhuma turma cadastrada!")


            # DISCIPLINAS
            elif resposta_login == 7 and dados_users[usuario]["admin"] == True:
                os.system("cls")
                print("\n--- CONSULTA DE DISCIPLINAS ---")
                print("1. Visualizar disciplinas")
                print("2. Cadastrar disciplinas")
                print("3. Atualizar disciplinas")
                print("4. Excluir disciplinas")
                print("5. Voltar")
                resposta_disciplinas_admin = int(input("Digite a opção desejada: "))

                if resposta_disciplinas_admin == 1:
                    os.system("cls")
                    if len(dados_disciplinas) > 0:
                        print("\nDisciplinas já cadastradas:")
                        for disciplina_cadastrada in dados_disciplinas:
                            show_professor_disc(disciplina_cadastrada)
                    else:
                        print("Não há nenhuma disciplina cadastrada!")

                elif resposta_disciplinas_admin == 2:
                    os.system("cls")
                    print("\n--- CADASTRAR NOVA DISCIPLINA ---")

                    while True:
                        id_disciplina = f"{''.join(random.choices(string.ascii_letters.upper(),k=3))}{''.join(random.choices("0123456789",k=4))}"
                        if id_disciplina not in dados_disciplinas.keys():
                            break

                    nome_disc_cadastro = input("Digite o nome da nova disciplina: ").lower()
                    curso_disc_cadastro = input("Digite o nome do curso que a disciplina faz parte: ").lower()
                    sem_disc_cadastro = int(input("Digite o número do semestre que a disciplina deve ser cursada: "))

                    print("\nProfessores disponíveis:")
                    for usuario_disc in dados_users:
                        if dados_users[usuario_disc]["cargo"] == "professor":
                            print(f"{usuario_disc}: Prof. {dados_users[usuario_disc]["nome"]}")
                    prof_disc_cadastro_input = input("\nSe já houver cadastro, digite o ID do professor responsável: ").upper()
                    for usuario_disc in dados_users:
                        if dados_users[usuario_disc]["cargo"] == "professor" and usuario_disc == prof_disc_cadastro_input:
                            prof_disc_cadastro = prof_disc_cadastro_input
                            break
                        else:
                            prof_disc_cadastro = None

                    disciplina_cadastrar = {
                        "nome": nome_disc_cadastro,
                        "curso": curso_disc_cadastro,
                        "semestre": sem_disc_cadastro,
                        "professor": prof_disc_cadastro
                    }
                    dados_disciplinas[id_disciplina] = disciplina_cadastrar
                    with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)

                    print("Disciplina cadastrada com sucesso!")

                elif resposta_disciplinas_admin == 3:
                    os.system("cls")
                    print("\n--- ATUALIZAR DISCIPLINA ---")

                    if len(dados_disciplinas) > 0:
                        print("\nDisciplinas já cadastradas:")
                        for disciplina_cadastrada in dados_disciplinas:
                            show_professor_disc(disciplina_cadastrada)
                        print("< Voltar")
                        disc_update = input("\nDigite o ID da disciplina a ser atualizada: ").upper()

                        if disc_update == "<":
                            continue

                        elif disc_update in dados_disciplinas:
                            print(f"ID {disc_update}: {dados_disciplinas[disc_update]["nome"]}: Curso {dados_disciplinas[disc_update]["curso"].capitalize()}, {dados_disciplinas[disc_update]["semestre"]}º semestre, Prof. {dados_disciplinas[disc_update]["professor"].capitalize()}")
                            print("1. Alterar nome")
                            print("2. Alterar curso")
                            print("3. Alterar professor")
                            print("4. Alterar semestre")
                            print("< Voltar")
                            disc_update_input = int(input("\nO que você gostaria de alterar? "))

                            if disc_update_input == "<":
                                continue

                            elif disc_update_input == 1:
                                nome_novo_disc = input("\nDigite o novo nome da disciplina: ").lower()
                                dados_disciplinas[disc_update]["nome"] = nome_novo_disc
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")

                            elif disc_update_input == 2:
                                curso_novo_disc = input("\nDigite o novo curso da disciplina: ").lower()
                                dados_disciplinas[disc_update]["curso"] = curso_novo_disc
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")

                            elif disc_update_input == 3:
                                print("\nProfessores disponíveis:")
                                for usuario_disc in dados_users:
                                    if dados_users[usuario_disc]["cargo"] == "professor":
                                        print(f"{dados_users[usuario_disc]["matricula"]}: Prof. {dados_users[usuario_disc]["nome"]}")
                                prof_disc_novo = input("\nSe já houver cadastro, digite a matrícula do novo professor responsável: ").upper()
                                if prof_disc_novo not in dados_users.values():
                                    prof_disc_novo = None
                                dados_disciplinas[disc_update]["professor"] = prof_disc_novo
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")

                            elif disc_update_input == 4:
                                sem_novo_disc = int(input("\nDigite o novo semestre da disciplina: "))
                                dados_disciplinas[disc_update]["semestre"] = sem_novo_disc
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")
                                
                        else:
                            print("Digite uma disciplina válida!")
                    else:
                        print("Não há nenhuma disciplina cadastrada!")

                elif resposta_disciplinas_admin == 4:
                    os.system("cls")
                    print("\n--- EXCLUIR DISCIPLINA ---")
                    if len(dados_turmas) > 0:
                        for disciplina_cadastrada in dados_disciplinas:
                            show_professor_disc(disciplina_cadastrada)
                        print("< Voltar")
                        disc_delete = input("\nDigite o ID da disciplina a ser excluída: ").upper()

                        if disc_delete == "<":
                            continue

                        elif disc_delete in dados_disciplinas:
                            show_professor_disc(disciplina_cadastrada)
                            disc_excluir_confirmar = input("Tem certeza que deseja excluir essa turma? (s/n) ").upper()
                            if disc_excluir_confirmar == "S":
                                del dados_disciplinas[disc_delete]
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Disciplina excluída!")
                                
                        else:
                            print("Digite uma disciplina válida!")

                    else:
                        print("Não há nenhuma disciplina cadastrada!")

                else:
                    continue

            elif resposta_login == 8 and usuario_sistema["admin"] == True:
                print("\nSem problemas! Parando a execução...")
                break

            else:
                print("ERRO: Digite uma resposta válida!")

    else:
        print("\nSem problemas! Parando a execução...")
        sys.exit()

except ValueError:
    # Se idade não for um número inteiro
    print("Erro: digite uma resposta válida.")
#except:
    # Se algo der errado durante o cadastro ou log-in
    #print("Erro de processamento, tente novamente mais tarde.")