"""
================================================================================
SISTEMA UNITECH - PLATAFORMA DE GESTÃO ACADÊMICA
================================================================================

DESCRIÇÃO GERAL:
Este é o arquivo principal do Sistema UniTech, uma plataforma completa para
gestão acadêmica de uma faculdade de tecnologia. O sistema permite que alunos,
professores e administradores gerenciem disciplinas, atividades, turmas e
informações acadêmicas.

FUNCIONALIDADES PRINCIPAIS:
- Cadastro e autenticação de usuários (alunos e professores)
- Sistema de aprovação de cadastros por administradores
- Gestão de disciplinas e turmas
- Publicação de conteúdos de aula e atividades
- Entrega de atividades por alunos
- Geração de relatórios de presença

ARQUITETURA:
O sistema usa arquivos JSON como banco de dados para armazenar:
- Usuários (database_users.json)
- Disciplinas (database_disciplinas.json)
- Atividades (database_atividades.json)
- Turmas (database_turmas.json)

DEPENDÊNCIAS EXTERNAS:
- Programas compilados em C (atividade_aluno.exe, relatorio_presenca.exe)
  para geração de arquivos de entrega e relatórios
================================================================================
"""

# Importações de bibliotecas necessárias
import json       # Manipulação de arquivos JSON (banco de dados)
import re         # Expressões regulares para validações (e-mail, CPF, datas)
import hashlib    # Criptografia de senhas usando SHA-256
import os         # Operações do sistema operacional (limpar tela, caminhos)
import sys        # Funções do sistema (saída do programa)
import string     # Constantes de strings (letras, números)
import random     # Geração de IDs aleatórios
import datetime   # Manipulação de datas e horários
import subprocess # Execução de programas externos (arquivos .exe em C)

# ================================================================================
# FUNÇÕES UTILITÁRIAS
# ================================================================================

def senha_encode(senha):
    """
    Criptografa uma senha usando o algoritmo SHA-256.
    
    PARÂMETROS:
        senha (str): Senha em texto puro a ser criptografada
    
    RETORNA:
        str: Hash hexadecimal da senha (64 caracteres)
    
    FUNCIONAMENTO:
        1. Cria um objeto hash SHA-256
        2. Converte a senha para bytes e atualiza o hash
        3. Retorna a representação hexadecimal do hash
    
    SEGURANÇA:
        - SHA-256 é uma função hash unidirecional (não pode ser revertida)
        - O mesmo texto sempre gera o mesmo hash
        - Impossível descobrir a senha original a partir do hash
    """
    senha_hash = hashlib.sha256()
    senha_hash.update(senha.encode())
    return senha_hash.hexdigest()

def validar_email():
    """
    Valida e verifica a unicidade de um e-mail no sistema.
    
    RETORNA:
        str: E-mail válido e não cadastrado
    
    FUNCIONAMENTO:
        1. Solicita e-mail ao usuário
        2. Verifica se o e-mail já está cadastrado no sistema
        3. Valida o formato usando expressão regular
        4. Retorna o e-mail se válido, ou repete o processo
    
    VALIDAÇÕES:
        - Formato básico: texto@texto.texto
        - Unicidade: e-mail não pode estar em uso por outro usuário
    
    REGEX UTILIZADO:
        ^\S+@\S+\.\S+$
        - ^\S+ = Um ou mais caracteres não-brancos no início
        - @ = Obrigatório arroba
        - \S+ = Um ou mais caracteres não-brancos
        - \. = Ponto obrigatório
        - \S+$ = Um ou mais caracteres não-brancos no final
    
    EXCEÇÕES:
        Lança Exception se o e-mail já estiver cadastrado
    """
    while True:
            email = input("Digite seu e-mail: ")
            # Padrão simples de validação de e-mail
            padrao_email = r"^\S+@\S+\.\S+$"
            
            # Verifica se o e-mail já está cadastrado no sistema
            for usuario in dados_users:
                if dados_users[usuario]["email"] == email:
                    print("Esse e-mail já pertence a outro usuário. Não gostaria de fazer seu log-in?")
                    raise Exception
                
            # Valida o formato do e-mail usando regex
            if re.match(padrao_email, email) == None:
                print("E-mail inválido!")
            else:
                return email
            
def show_professor_disc(disciplina_cadastrada_par):
    """
    Exibe informações formatadas de uma disciplina, incluindo o professor responsável.
    
    PARÂMETROS:
        disciplina_cadastrada_par (str): ID da disciplina a ser exibida
    
    FORMATO DE EXIBIÇÃO:
        Com professor: ID ABC1234: Programação I: Curso Sistemas de Informação, 1º semestre, Prof. João Silva
        Sem professor: ID ABC1234: Programação I: Curso Sistemas de Informação, 1º semestre
    
    FUNCIONAMENTO:
        1. Busca o ID do professor na disciplina
        2. Se houver professor, busca o nome do professor nos dados de usuários
        3. Exibe as informações formatadas com ou sem o nome do professor
    """
    # Busca o ID do professor responsável pela disciplina
    professor_disciplina = dados_disciplinas[disciplina_cadastrada_par]["professor"]
    
    # Se houver professor atribuído
    if professor_disciplina != None:
        # Busca o nome do professor nos dados de usuários
        professor_disciplina_user = dados_users[professor_disciplina]["nome"]
        # Exibe disciplina COM professor
        print(f"ID {disciplina_cadastrada_par}: {dados_disciplinas[disciplina_cadastrada_par]["nome"].title()}: Curso {dados_disciplinas[disciplina_cadastrada_par]["curso"].title()}, {dados_disciplinas[disciplina_cadastrada_par]["semestre"]}º semestre, Prof. {professor_disciplina_user}")
    else:
        # Exibe disciplina SEM professor (ainda não atribuído)
        print(f"ID {disciplina_cadastrada_par}: {dados_disciplinas[disciplina_cadastrada_par]["nome"].title()}: Curso {dados_disciplinas[disciplina_cadastrada_par]["curso"].title()}, {dados_disciplinas[disciplina_cadastrada_par]["semestre"]}º semestre")

def show_atividade(atv_visualizar):
    """
    Exibe os detalhes de uma atividade ou conteúdo de aula.
    
    PARÂMETROS:
        atv_visualizar (str): ID da atividade a ser exibida
    
    TIPOS DE POSTAGEM:
        "C" = Conteúdo de aula (sem prazo de entrega)
        "A" = Atividade (com prazo de entrega)
    
    FORMATO DE EXIBIÇÃO:
        ----- Título da Atividade -----
        Descrição ou conteúdo da atividade...
        Prazo para entrega: dd/mm/aaaa (apenas se for tipo "A")
    """
    # Exibe o cabeçalho com o título da atividade
    print(f"\n----- {dados_atividades[atv_visualizar]["titulo"]} -----")
    
    # Exibe o conteúdo/descrição da atividade
    print(f"{dados_atividades[atv_visualizar]["conteudo"]}")
    
    # Se for uma ATIVIDADE (tipo "A"), exibe o prazo de entrega
    # Conteúdos de aula (tipo "C") não têm prazo
    if dados_atividades[atv_visualizar]["tipo"] == "A":
        print(f"Prazo para entrega: {dados_atividades[atv_visualizar]["prazo"]}")


# ================================================================================
# CONFIGURAÇÃO E CARREGAMENTO DO BANCO DE DADOS (ARQUIVOS JSON)
# ================================================================================

"""
ESTRUTURA DO BANCO DE DADOS:
O sistema utiliza 4 arquivos JSON como banco de dados:

1. database_users.json - Armazena informações de todos os usuários
   Estrutura: {
       "ID_USUARIO": {
           "nome": str,
           "cargo": "aluno" | "professor",
           "matricula": str,
           "cpf": str,
           "data_nascimento": str,
           "email": str,
           "senha": str (hash SHA-256),
           "turma": str | None,
           "aprovado": True | False | None,
           "admin": bool
       }
   }

2. database_disciplinas.json - Armazena informações das disciplinas
   Estrutura: {
       "ID_DISCIPLINA": {
           "nome": str,
           "curso": str,
           "semestre": int,
           "professor": str (ID do professor) | None
       }
   }

3. database_atividades.json - Armazena atividades e conteúdos de aula
   Estrutura: {
       "ID_ATIVIDADE": {
           "titulo": str,
           "conteudo": str,
           "prazo": str | None,
           "tipo": "A" | "C",
           "disciplina": str (ID da disciplina)
       }
   }

4. database_turmas.json - Armazena informações das turmas
   Estrutura: {
       "CODIGO_TURMA": {
           "curso": str,
           "semestre": int
       }
   }
"""

# Define os caminhos completos para os arquivos JSON
# os.path.dirname(__file__) obtém o diretório onde este script está localizado
caminho_users = os.path.join(os.path.dirname(__file__), "database_users.json")
caminho_disciplinas = os.path.join(os.path.dirname(__file__), "database_disciplinas.json")
caminho_atividades = os.path.join(os.path.dirname(__file__), "database_atividades.json")
caminho_turmas = os.path.join(os.path.dirname(__file__), "database_turmas.json")

# ================================================================================
# CARREGAMENTO DOS DADOS DE USUÁRIOS
# ================================================================================
try:
    # Tenta abrir e carregar o arquivo de usuários
    with open(caminho_users, "r", encoding='utf-8') as arquivo_leitura_user:
        dados_users = json.load(arquivo_leitura_user)
    print("Dados de usuário carregados!")
except:
    # Se o arquivo não existir ou estiver vazio, inicializa dicionário vazio
    dados_users = {}
    print("Não há dados de usuários cadastrados.")

# ================================================================================
# CARREGAMENTO DOS DADOS DE DISCIPLINAS
# ================================================================================
try:
    # Tenta abrir e carregar o arquivo de disciplinas
    with open(caminho_disciplinas, "r", encoding='utf-8') as arquivo_leitura_disc:
        dados_disciplinas = json.load(arquivo_leitura_disc)
    print("Dados de disciplinas carregados!")
except:
    # Se o arquivo não existir ou estiver vazio, inicializa dicionário vazio
    dados_disciplinas = {}
    print("Não há dados de disciplinas cadastrados.")

# ================================================================================
# CARREGAMENTO DOS DADOS DE ATIVIDADES
# ================================================================================
try:
    # Tenta abrir e carregar o arquivo de atividades
    with open(caminho_atividades, "r", encoding='utf-8') as arquivo_leitura_atv:
        dados_atividades = json.load(arquivo_leitura_atv)
    print("Dados de atividades carregados!")
except:
    # Se o arquivo não existir ou estiver vazio, inicializa dicionário vazio
    dados_atividades = {}
    print("Não há dados de atividades cadastrados.")

# ================================================================================
# CARREGAMENTO DOS DADOS DE TURMAS
# ================================================================================
try:
    # Tenta abrir e carregar o arquivo de turmas
    with open(caminho_turmas, "r", encoding='utf-8') as arquivo_leitura_tur:
        dados_turmas = json.load(arquivo_leitura_tur)
    print("Dados de turmas carregados!") 
except:
    # Se o arquivo não existir ou estiver vazio, inicializa dicionário vazio
    dados_turmas = {}
    print("Não há dados de turmas cadastrados.")

# ================================================================================
# BLOCO PRINCIPAL DO SISTEMA - MENU INICIAL
# ================================================================================

"""
FLUXO GERAL DO SISTEMA:
1. Menu Inicial: Cadastro, Login ou Sair
2. Se Cadastro: Coleta dados → Aguarda aprovação
3. Se Login: Valida credenciais → Menu do usuário (Aluno/Professor/Admin)
4. Menu do Usuário: Funcionalidades específicas por tipo de usuário

TRATAMENTO DE ERROS:
O sistema usa try/except para capturar erros gerais.
"""

try:
    # ================================================================================
    # TELA INICIAL - OPÇÕES PRINCIPAIS
    # ================================================================================
    
    print("---------- UNITECH ----------")
    print("Olá, bem vindo(a) à UniTech! O que você deseja?")
    print("1. Cadastrar novo usuário")
    print("2. Fazer log-in")
    print("3. Sair")
    resposta = int(input("Digite a opção desejada: "))

    # ================================================================================
    # OPÇÃO 1: CADASTRO DE NOVO USUÁRIO
    # ================================================================================
    
    """
    PROCESSO DE CADASTRO:
    1. Gera ID único automaticamente
    2. Coleta informações pessoais (nome, CPF, data nascimento, etc)
    3. Valida cada informação conforme regras específicas
    4. Diferencia cadastro de aluno (requer turma) e professor
    5. Criptografa a senha com SHA-256
    6. Salva no banco de dados com status "aprovado = None" (aguardando)
    7. Administrador precisa aprovar antes do usuário poder fazer login
    
    VALIDAÇÕES IMPLEMENTADAS:
    - Matrícula: 7 caracteres (1 letra + 5 números + 1 letra)
    - CPF: 11 dígitos numéricos com validação de dígitos verificadores
    - Data: formato dd/mm/aaaa
    - Turma (alunos): 6 caracteres (2 letras + 1 número + 1 letra + 2 números)
    - E-mail: formato básico com @ e domínio
    """
    
    if resposta == 1:
        os.system('cls')  # Limpa a tela (cls no Windows, clear no Linux/Mac)
        
        print("\n---------- CADASTRO DE USUÁRIO ----------")
        print("Boa! Vamos cadastrar um novo usuário...")

        # ========================================================================
        # GERAÇÃO DE ID ÚNICO
        # ========================================================================
        # Gera um ID aleatório no formato: ABC1234 (3 letras maiúsculas + 4 números)
        # Continua gerando até encontrar um ID que não exista no banco de dados
        while True:
            # Gera 3 letras maiúsculas aleatórias
            id = f"{''.join(random.choices(string.ascii_letters.upper(),k=3))}"
            # Concatena com 4 números aleatórios
            id += f"{''.join(random.choices("0123456789",k=4))}"
            # Verifica se o ID já existe
            if id not in dados_users.keys():
                break  # ID único encontrado, sai do loop

        # COLETA DE INFORMAÇÕES - NOME
        nome = input("Digite seu nome: ")

        # ========================================================================
        # COLETA DE INFORMAÇÕES - CARGO (ALUNO OU PROFESSOR)
        # ========================================================================
        # O sistema diferencia entre alunos e professores
        # Alunos: precisam informar turma, veem disciplinas da turma
        # Professores: não têm turma, veem apenas disciplinas que lecionam
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

        # ========================================================================
        # VALIDAÇÃO DE MATRÍCULA
        # ========================================================================
        # Formato esperado: 7 caracteres (1 letra + 5 números + 1 letra)
        # Exemplo: A12345B
        while True:
            matricula = input("Digite a sua matrícula (apenas letras e números): ").upper()
            
            # Verifica se a matrícula já está cadastrada no sistema
            for usuario in dados_users:
                if dados_users[usuario]["matricula"] == matricula:
                    print("Esta matrícula já está cadastrada! Por favor, entre em contato com a administração.")
                    raise Exception

            # Valida o formato da matrícula:
            # - Deve ter exatamente 7 caracteres
            # - Primeiro caractere deve ser letra
            # - Último caractere deve ser número
            if len(matricula) == 7 and matricula[0].isalpha() and matricula[-1].isdigit():
                break
            else:
                print("Digite uma matrícula válida!")

        # ========================================================================
        # VALIDAÇÃO DE CPF
        # ========================================================================
        # Implementa o algoritmo oficial de validação de CPF brasileiro
        # CPF deve ter 11 dígitos, onde os 2 últimos são dígitos verificadores
        # 
        # ALGORITMO DE VALIDAÇÃO:
        # 1º dígito verificador:
        #   - Multiplica os 9 primeiros dígitos por 10, 9, 8, ..., 2
        #   - Soma os resultados
        #   - Calcula o resto da divisão por 11
        #   - Se resto < 2, dígito = 0; senão dígito = 11 - resto
        # 
        # 2º dígito verificador:
        #   - Multiplica os 10 primeiros dígitos por 11, 10, 9, ..., 2
        #   - Segue a mesma lógica do 1º dígito
        while True:
            cpf = input("Digite seu CPF (apenas números): ")
            
            # Verifica se o CPF já está cadastrado
            for usuario in dados_users:
                if dados_users[usuario]["cpf"] == cpf:
                    print("Este CPF já está cadastrado! Por favor, entre em contato com a administração.")
                    raise Exception

            # ---- CÁLCULO DO PRIMEIRO DÍGITO VERIFICADOR ----
            soma_cpf = 0
            index_cpf = 0

            # Multiplica os 9 primeiros dígitos por 10, 9, 8, ..., 2
            for i in range(10,1,-1):
                soma_cpf += int(cpf[index_cpf])*i
                index_cpf += 1
            
            # Calcula o primeiro dígito verificador
            if soma_cpf % 11 < 2:
                digito_1 = 0
            else:
                digito_1 = 11 - soma_cpf % 11

            # ---- CÁLCULO DO SEGUNDO DÍGITO VERIFICADOR ----
            index_cpf = 0
            soma_cpf = 0
            
            # Multiplica os 10 primeiros dígitos por 11, 10, 9, ..., 2
            for i in range(11,1,-1):
                soma_cpf += int(cpf[index_cpf])*i
                index_cpf += 1
            
            # Calcula o segundo dígito verificador
            if soma_cpf % 11 < 2:
                digito_2 = 0
            else:
                digito_2 = 11 - soma_cpf % 11
            
            # ---- VALIDAÇÃO FINAL ----
            # Verifica se o CPF tem 11 dígitos e se os dígitos verificadores estão corretos
            if len(cpf) == 11 and int(cpf[9]) == digito_1 and int(cpf[10]) == digito_2:
                break
            else:
                print("Digite um CPF válido!")

        # ========================================================================
        # VALIDAÇÃO DE DATA DE NASCIMENTO
        # ========================================================================
        # Formato esperado: dd/mm/aaaa (dia com 2 dígitos, mês com 2, ano com 4)
        # Regex valida:
        #   - Dias: 01-31 (0[1-9]|[12][0-9]|3[01])
        #   - Meses: 01-12 (0[1-9]|1[0-2])
        #   - Ano: 4 dígitos (\d{4})
        # 
        # NOTA: Não valida datas impossíveis como 31/02 ou 30/02
        while True:
            data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ")
            padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"

            if re.match(padrao_data, data_nascimento):
                break
            else:
                print("Digite uma data válida!")

        # ========================================================================
        # VALIDAÇÃO DE TURMA (APENAS PARA ALUNOS)
        # ========================================================================
        # Formato esperado: 6 caracteres (2 letras + 1 número + 1 letra + 2 números)
        # Exemplo: SI1A23 = Sistemas de Informação, 1º semestre, turma A, ano 2023
        # 
        # Professores não têm turma (valor None)
        if cargo == "aluno":
            while True:
                turma = input("Digite sua turma: ").upper()
                # Valida posição por posição:
                # [0:2] = 2 letras (código do curso)
                # [2] = 1 número (semestre)
                # [3] = 1 letra (identificação da turma)
                # [4:6] = 2 números (ano)
                if turma[0:2].isalpha() and turma[2].isdigit() and turma[3].isalpha() and turma[4:6].isdigit() and len(turma)==6:
                    break
                else:
                    print("Digite uma turma válida!")
        else:
            turma = None  # Professores não pertencem a turmas

        # VALIDAÇÃO DE E-MAIL
        # Chama a função validar_email() que verifica formato e unicidade
        email = validar_email()

        # ========================================================================
        # CRIPTOGRAFIA DA SENHA
        # ========================================================================
        # A senha é criptografada usando SHA-256 antes de ser armazenada
        # Isso garante que mesmo administradores não consigam ver senhas reais
        senha_input = input("Digite sua nova senha: ")
        senha = senha_encode(senha_input)  # Converte senha em hash SHA-256
        
        # ========================================================================
        # CRIAÇÃO DO OBJETO USUÁRIO
        # ========================================================================
        # Cria um dicionário com todas as informações do usuário
        # CAMPOS:
        #   - nome: Nome completo
        #   - cargo: "aluno" ou "professor"
        #   - matricula: Identificação única na faculdade
        #   - cpf: CPF validado
        #   - data_nascimento: Data no formato dd/mm/aaaa
        #   - email: E-mail único e válido
        #   - senha: Hash SHA-256 da senha
        #   - turma: Código da turma (alunos) ou None (professores)
        #   - aprovado: None (aguardando), True (aprovado), False (reprovado)
        #   - admin: Se o usuário tem permissões de administrador
        user = {
            "nome": nome,
            "cargo": cargo,
            "matricula": matricula,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "email": email,
            "senha": senha,
            "turma": turma,
            "aprovado": None,  # Novo usuário aguarda aprovação
            "admin": False     # Por padrão, usuários não são administradores
        }
        
        # ========================================================================
        # SALVAMENTO NO BANCO DE DADOS
        # ========================================================================
        # Adiciona o novo usuário ao dicionário de usuários
        dados_users[id] = user
        
        # Salva o dicionário atualizado no arquivo JSON
        with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
            json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
            # ensure_ascii=False permite caracteres especiais (acentos, ç, etc)

        print("Usuário cadastrado com sucesso!")
        print("Aguarde a aprovação do administrador para fazer login.")

    # ================================================================================
    # OPÇÃO 2: LOGIN (AUTENTICAÇÃO DE USUÁRIO)
    # ================================================================================
    
        """
    PROCESSO DE LOGIN:
    1. Usuário digita matrícula e senha
    2. Sistema criptografa a senha digitada com SHA-256
    3. Busca a matrícula no banco de dados
    4. Verifica o status de aprovação do cadastro
    5. Compara a senha criptografada com a armazenada
    6. Se tudo estiver correto, autoriza o acesso
    
    VALIDAÇÕES DE SEGURANÇA:
    - Verifica se o cadastro foi aprovado pelo administrador
    - Compara hashes de senha (não armazena senhas em texto puro)
    - Diferencia erros de matrícula não encontrada vs senha incorreta
    
    POSSÍVEIS MENSAGENS DE ERRO:
    - "Matrícula em análise": Cadastro ainda não foi aprovado
    - "Matrícula reprovada": Cadastro foi rejeitado
    - "Senha incorreta": Matrícula existe, mas senha está errada
    - "Matrícula não encontrada": Usuário não está cadastrado
        """
    
    elif resposta == 2:
        os.system('cls')  # Limpa a tela
        print("\n---------- LOG-IN ----------")
        print("Boa! Vamos fazer seu log-in...")
        
        # Solicita credenciais do usuário
        matricula_usuario = input("Digite a matrícula cadastrada: ").upper()
        senha_usuario = input("Digite a sua senha: ")

        # Criptografa a senha digitada usando SHA-256 para comparar com o hash armazenado
        senha_usuario_hash = senha_encode(senha_usuario)

        # ========================================================================
        # PROCESSO DE AUTENTICAÇÃO
        # ========================================================================
        # Percorre todos os usuários cadastrados para encontrar a matrícula
        for usuario in dados_users:
            # ---- VERIFICAÇÃO 1: Matrícula em análise (aguardando aprovação) ----
            if dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["aprovado"] == None:
                print("Sua matrícula ainda está em análise. Por favor, tente novamente mais tarde.")
                raise Exception
            
            # ---- VERIFICAÇÃO 2: Matrícula reprovada pelo administrador ----
            elif dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["aprovado"] == False:
                print("Sua matrícula foi reprovada. Por favor, entre em contato com a administração.")
                raise Exception

            # ---- VERIFICAÇÃO 3: Matrícula e senha corretas + cadastro aprovado ----
            # Esta é a condição de sucesso do login
            elif dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["senha"] == senha_usuario_hash and dados_users[usuario]["aprovado"] == True:
                os.system('cls')  # Limpa a tela
                print(f"----- {dados_users[usuario]["nome"]}, BEM VINDO(A)! -----")
                
                # Armazena os dados do usuário logado em uma variável global
                # Esta variável será usada em todo o sistema para identificar o usuário
                usuario_sistema = dados_users[usuario]
                break  # Sai do loop, login bem-sucedido

            # ---- VERIFICAÇÃO 4: Matrícula correta, mas senha incorreta ----
            elif dados_users[usuario]["matricula"] == matricula_usuario and dados_users[usuario]["senha"] != senha_usuario_hash:
                print("Senha incorreta. Tente novamente!")
                raise Exception
                
            # ---- VERIFICAÇÃO 5: Matrícula não encontrada no sistema ----
            # Se chegou ao último usuário e não encontrou a matrícula
            elif usuario == list(dados_users)[-1]:
                print("Não foi possível identificar sua matrícula. Não se esqueça de fazer seu cadastro!")
                raise Exception
            
        # ========================================================================
        # MENU PRINCIPAL DO USUÁRIO LOGADO
        # ========================================================================
        
        """
        ESTRUTURA DO MENU:
        O menu é diferente para usuários comuns (alunos/professores) e administradores.
        
        OPÇÕES PARA TODOS OS USUÁRIOS (1-5):
        1. Visualizar informações pessoais (nome, e-mail, CPF, etc)
        2. Atualizar informações (e-mail e senha)
        3. Excluir conta do sistema
        4. Acessar disciplinas (ver conteúdos, atividades, etc)
        5. Sair do sistema
        
        OPÇÕES EXCLUSIVAS PARA ADMINISTRADORES (5-8):
        5. Lista de aprovação (aprovar/reprovar novos cadastros)
        6. Administrar turmas (criar, editar, excluir turmas)
        7. Administrar disciplinas (criar, editar, excluir, atribuir professores)
        8. Sair do sistema
        
        O loop continua até o usuário escolher sair (opção 5 ou 8).
        """
        
        while True: 
            print("\nO que você gostaria de fazer?")
            print("1. Visualizar minhas informações")
            print("2. Atualizar minhas informações")
            print("3. Excluir meu usuário")
            print("4. Disciplinas")
            
            # Menu adicional para administradores
            if usuario_sistema["admin"] == True:
                print("5. Lista de aprovação")
                print("6. Administrar turmas")
                print("7. Administrar disciplinas")
                print("8. Sair")
            else:
                print("5. Sair")
            
            resposta_login = int(input("Digite a opção desejada: "))

            # ================================================================
            # OPÇÃO 1: VISUALIZAR INFORMAÇÕES PESSOAIS
            # ================================================================
            # Exibe todos os dados do usuário logado
            if resposta_login == 1:
                cpf_user = usuario_sistema["cpf"]
                os.system('cls')
                
                print(f"----- USUÁRIO: {usuario_sistema["nome"]} -----")
                print(f"Email: {usuario_sistema["email"]}")
                print(f"Matrícula: {usuario_sistema["matricula"]}")
                print(f"Cargo: {usuario_sistema["cargo"]}")
                print(f"Data de nascimento: {usuario_sistema["data_nascimento"]}")
                print(f"CPF: {cpf_user[0:3]}.{cpf_user[3:6]}.{cpf_user[6:9]}-{cpf_user[9:11]}")
                if usuario_sistema["cargo"] == "aluno":
                    print(f"Turma: {usuario_sistema["turma"]}")
                    try:
                        print(f"Curso: {dados_turmas[dados_users[usuario_aprovar]["turma"]]["curso"]}")
                    except:
                        print(f"Curso: Turma ainda não cadastrada")

                print(f"----------------------------------------")
                continue

            # ================================================================
            # OPÇÃO 2: ATUALIZAR INFORMAÇÕES
            # ================================================================
            # Permite ao usuário atualizar e-mail ou senha
            # NOTA: Não permite alterar outros dados (nome, CPF, matrícula, etc)
            # Para alterar esses dados, é necessário entrar em contato com a administração
            elif resposta_login == 2:
                os.system('cls')
                print(f"----- ATUALIZANDO INFORMAÇÕES -----")
                print("\nQual informação você gostaria de atualizar?")
                print("1. E-mail")
                print("2. Senha")
                print("3. Voltar")
                resposta_update = int(input("Digite a opção desejada: "))

                if resposta_update == 1:
                    # ---- ATUALIZAR E-MAIL ----
                    # Valida o novo e-mail (formato e unicidade)
                    email_novo = validar_email()
                    usuario_sistema["email"] = email_novo
                    
                    # Salva a alteração no banco de dados
                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                    print("E-mail atualizado!")
                    continue

                elif resposta_update == 2:
                    # ---- ATUALIZAR SENHA ----
                    # Por segurança, exige que o usuário confirme a senha atual
                    senha_atual = input("Confirme sua senha: ")
                    senha_atual_encode = senha_encode(senha_atual)
                    
                    # Verifica se a senha atual está correta
                    if senha_atual_encode != usuario_sistema["senha"]:
                        print("Senha inválida! Tente novamente.")
                        continue

                    # Se senha atual estiver correta, permite definir nova senha
                    senha_nova = input("Digite sua nova senha: ")
                    usuario_sistema["senha"] = senha_encode(senha_nova)  # Criptografa nova senha
                    
                    # Salva a alteração no banco de dados
                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                    print("Senha atualizada!")
                    continue

                elif resposta_update == 3:
                    continue

                else:
                    raise ValueError

            elif resposta_login == 3:
                # EXCLUIR USUÁRIO
                os.system('cls')
                print(f"----- EXCLUIR USUÁRIO -----")
                # Pede confirmação do usuário para excluir a conta de maneira definitiva
                excluir_confirmar = input("Você tem certeza que deseja deletar seu usuário? Você perderá todo o seu progresso nas disciplinas! (S / N) ")
                if excluir_confirmar.lower() == "s" or excluir_confirmar.lower() == "sim":
                    del usuario_sistema
                    # Salva a alteração no banco de dados
                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                    print("Usuário excluído, até mais!")
                    break
                else:
                    continue




            # ================================================================
            # OPÇÃO 4: ACESSAR DISCIPLINAS
            # ================================================================
            # Funcionalidade diferente para cada tipo de usuário:
            # - ALUNOS: Veem disciplinas da sua turma e semestre
            # - PROFESSORES: Veem apenas disciplinas que lecionam
            # - ADMINISTRADORES: Veem todas as disciplinas do sistema
            elif resposta_login == 4:
                os.system('cls')
                print("----- DISCIPLINAS -----")
                print("\nQual disciplina você gostaria de acessar?")

                # ---- VISUALIZAÇÃO PARA ALUNOS ----
                # Filtra disciplinas por turma e semestre do aluno
                if usuario_sistema["cargo"] == "aluno":
                    turma_aluno = usuario_sistema["turma"]
                    
                    # Busca disciplinas que correspondem ao curso e semestre da turma do aluno
                    for disciplina_aluno in dados_disciplinas:
                        if dados_turmas[turma_aluno]["semestre"] == dados_disciplinas[disciplina_aluno]["semestre"] and dados_turmas[turma_aluno]["curso"] == dados_disciplinas[disciplina_aluno]["curso"]:
                            show_professor_disc(disciplina_aluno)
                    print("< Voltar")

                # ---- VISUALIZAÇÃO PARA PROFESSORES ----
                # Mostra apenas as disciplinas que o professor leciona
                elif usuario_sistema["cargo"] == "professor":
                    # Primeiro, encontra o ID do professor logado
                    for id_prof, info_usuario in dados_users.items():
                        if info_usuario == usuario_sistema:
                            id_prof_logado = id_prof
                            break  # ID encontrado, podemos sair do loop
                    
                    # Busca disciplinas onde o professor é o responsável
                    for disciplina_prof in dados_disciplinas:
                        if id_prof_logado == dados_disciplinas[disciplina_prof]["professor"]:
                            show_professor_disc(disciplina_prof)
                    print("< Voltar")

                # ---- VISUALIZAÇÃO PARA ADMINISTRADORES ----
                # Administradores veem TODAS as disciplinas cadastradas
                elif usuario_sistema["admin"] == True:
                    for disciplina_adm in dados_disciplinas:
                        show_professor_disc(disciplina_adm)
                    print("< Voltar")
                
                # ---- ESCOLHA DA DISCIPLINA OU GERAÇÃO DE RELATÓRIO ----
                # Professores têm opção adicional de gerar relatórios de presença (símbolo +)
                if usuario_sistema["cargo"] == "professor":
                    resposta_disciplinas = input("\nDigite o ID da disciplina desejada ou + para gerar um relatório de presença: ").upper()
                else:
                    resposta_disciplinas = input("Digite o ID da disciplina desejada: ").upper()
                
                # Opção para voltar ao menu anterior
                if resposta_disciplinas == "<":
                    continue
                
                # ================================================================
                # GERAÇÃO DE RELATÓRIO DE PRESENÇA (EXCLUSIVO PARA PROFESSORES)
                # ================================================================
                # Cria um arquivo .txt com lista de alunos para marcar presença
                # Utiliza o programa externo relatorio_presenca.exe (escrito em C)
                elif resposta_disciplinas == "+" and usuario_sistema["cargo"] == "professor":
                    os.system("cls")
                    print("\n--- RELATÓRIO DE PRESENÇA ---")
                    
                    # Encontra o ID do professor logado
                    for id_prof, info_usuario in dados_users.items():
                        if info_usuario == usuario_sistema:
                            id_prof_logado = id_prof
                            break # ID encontrado, podemos sair do loop
                    
                    # Busca disciplinas onde o professor é o responsável
                    for disciplina_prof in dados_disciplinas:
                        if id_prof_logado == dados_disciplinas[disciplina_prof]["professor"]:
                            show_professor_disc(disciplina_prof)
                    print("< Voltar")
                    disc_relatorio = input("\nDigite o ID da disciplina a ser impressa: ").upper()
            
                    if disc_relatorio in dados_disciplinas:
                        # Busca turmas que correspondem ao curso da disciplina
                        turmas_disciplina = []
                        for turma_cadastrada in dados_turmas:
                                if dados_turmas[turma_cadastrada]["curso"] == dados_disciplinas[disc_relatorio]["curso"]:
                                    turmas_disciplina.append(turma_cadastrada)

                        if len(turmas_disciplina) > 0:
                            print("\nTurmas cadastradas:")
                            # Mostra as turmas cadastradas para o professor
                            for turma_cadastrada in dados_turmas:
                                if dados_turmas[turma_cadastrada]["curso"] == dados_disciplinas[disc_relatorio]["curso"]:
                                    print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].title()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                            turma_relatorio = input("\nDigite o nome da turma a ser impressa: ").upper()

                            # Verifica se a turma existe
                            if turma_relatorio in dados_turmas:
                                # Mostra os detalhes da turma
                                print(f"\nTurma {turma_relatorio}: {dados_turmas[turma_relatorio]["curso"].title()}, {dados_turmas[turma_relatorio]["semestre"]}º semestre.")
                                # Solicita a data do relatório
                                while True:
                                    data_presenca = input("Digite a data do relatório (dd/mm/aaaa): ")
                                    padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"

                                    # Verifica se a data está no formato correto
                                    if re.match(padrao_data, data_presenca):
                                        break
                                    else:
                                        print("Digite uma data válida!")
                                print("Imprimindo relatório...")
                                alunos_turma_relatorio = []
                                alunos_turma_relatorio.append(data_presenca)
                                # Busca alunos que correspondem à turma
                                for aluno_turma in dados_users:
                                    # Verifica se o aluno está na turma e é aluno
                                    if dados_users[aluno_turma]["turma"] == turma_relatorio and dados_users[aluno_turma]["cargo"] == "aluno":
                                        alunos_turma_relatorio.append(f"{dados_users[aluno_turma]["nome"]} - {dados_users[aluno_turma]["matricula"]}")
                                # Ordena a lista de alunos
                                alunos_turma_relatorio.sort()
                                # Adiciona o nome da turma e a data do relatório
                                alunos_turma_relatorio.append(f"Turma {turma_relatorio}, curso {dados_turmas[turma_relatorio]["curso"].title()}, {dados_turmas[turma_relatorio]["semestre"]}º semestre")
                                # Adiciona nome do professor
                                alunos_turma_relatorio.append(usuario_sistema["nome"])
                                # Adiciona o nome da turma e a data do relatório
                                alunos_turma_relatorio.append(f"{turma_relatorio}_{data_presenca.replace("/","")}")
                                # Executa o programa externo relatorio_presenca.exe
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
                    # Mostra as atividades cadastradas para o professor
                    print("Atividades:")

                    if len(dados_atividades) > 0:
                        # Mostra as atividades cadastradas para o professor
                        for atividade in dados_atividades:
                            if dados_atividades[atividade]["disciplina"] == resposta_disciplinas:
                                print(f"ID {atividade}: {dados_atividades[atividade]["titulo"]}")
                    else:
                        print("Não há nenhuma atividade ainda!")  

                    # ================================================================
                    # GESTÃO DE ATIVIDADES PARA PROFESSORES
                    # ================================================================
                    # Professores podem criar, editar e excluir atividades/conteúdos
                    if usuario_sistema["cargo"] == "professor":
                        if len(dados_atividades) > 0:
                            respost_prof_atv = input("\nDigite o ID da atividade para acessá-la ou + para adicionar uma atividade: ").upper()
                        else:
                            respost_prof_atv = input("\nAperte enter para voltar ou + para adicionar uma atividade: ").upper()

                        # ---- CRIAR NOVA ATIVIDADE/CONTEÚDO ----
                        if respost_prof_atv == "+":
                            print("\n--- ADICIONAR POSTAGEM ---")
                            
                            # Gera ID único para a nova atividade
                            while True:
                                id_atv = f"{''.join(random.choices(string.ascii_letters.upper(),k=3))}{''.join(random.choices("0123456789",k=4))}"
                                if id_atv not in dados_atividades.keys():
                                    break
                            
                            # Solicita tipo de postagem: C (Conteúdo) ou A (Atividade)
                            while True:
                                tipo_atv = input("Digite C para cadastrar um CONTEÚDO DE AULA e A para cadastrar uma ATIVIDADE: ").upper()
                                if tipo_atv == "C" or tipo_atv == "A":
                                    break
                                else:
                                    print("Digite um tipo de postagem!")
                            
                            # Coleta informações da postagem
                            titulo_atv = input("Digite o título da postagem: ")
                            conteudo_atv = input("Digite o conteúdo/explicação da postagem: ")
                            
                            # Se for ATIVIDADE (A), solicita prazo de entrega
                            if tipo_atv == "A":
                                while True:
                                    prazo_atv = input("Digite o prazo da atividade (dd/mm/aaaa): ")
                                    padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
                                    if re.match(padrao_data, prazo_atv):
                                        break
                                    else:
                                        print("Digite uma data válida!")
                            else:
                                # Conteúdos de aula não têm prazo
                                prazo_atv = None

                            # Cria o objeto atividade/conteúdo
                            atividade_cadastrar = {
                                "titulo": titulo_atv,
                                "conteudo": conteudo_atv,
                                "prazo": prazo_atv,
                                "tipo": tipo_atv,
                                "disciplina": resposta_disciplinas
                            }
                            
                            # Adiciona ao banco de dados
                            dados_atividades[id_atv] = atividade_cadastrar
                            with open(caminho_atividades, "w", encoding='utf-8') as arquivo_escrita:
                                json.dump(dados_atividades, arquivo_escrita, ensure_ascii=False)

                            print("Atividade cadastrada com sucesso!")

                            
                        elif respost_prof_atv in dados_atividades:
                            # Mostra os detalhes da atividade/conteúdo
                            show_atividade(respost_prof_atv)
                            resposta_atv_edit = input("\nAperte enter para continuar, + para editar a atividade e - para excluí-la. ")

                            # ---- EXCLUIR ATIVIDADE ----
                            if resposta_atv_edit == "-":
                                # Pede confirmação do usuário para excluir a atividade
                                resposta_atv_exc = input("Tem certeza que deseja excluir essa atividade? (s/n) ").lower()
                                if resposta_atv_exc == "s" or resposta_atv_exc == "sim":
                                    del dados_atividades[respost_prof_atv]
                                    # Salva a alteração no banco de dados
                                    with open(caminho_atividades, "w", encoding='utf-8') as arquivo_escrita:
                                        json.dump(dados_atividades, arquivo_escrita, ensure_ascii=False)
                                    print("Atividade excluída!")
                                else:
                                    continue

                            # ---- EDITAR ATIVIDADE ----
                            if resposta_atv_edit == "+":
                                # Solicita o novo título da atividade
                                novo_titulo_atv = input("Digite o novo título da atividade: ")
                                # Solicita o novo conteúdo da atividade
                                novo_conteudo_atv = input("Digite o novo conteúdo da atividade: ")
                                # Verifica se a atividade é uma atividade (tipo "A")
                                if dados_atividades[respost_prof_atv]["prazo"] == "A":
                                    # Solicita o novo prazo da atividade
                                    while True:
                                        novo_prazo_atv = input("Digite o prazo da atividade (dd/mm/aaaa): ")
                                        novo_padrao_data = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
                                        # Verifica se o prazo está no formato correto
                                        if re.match(novo_padrao_data, novo_prazo_atv):
                                            break
                                        else:
                                            print("Digite uma data válida!")
                                else:
                                    novo_prazo_atv = None
                                dados_atividades[respost_prof_atv]["titulo"] = novo_titulo_atv
                                dados_atividades[respost_prof_atv]["conteudo"] = novo_conteudo_atv
                                dados_atividades[respost_prof_atv]["prazo"] = novo_prazo_atv
                                # Salva a alteração no banco de dados
                                with open(caminho_atividades, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_atividades, arquivo_escrita, ensure_ascii=False)
                                print("Dados da atividade atualizados!")
                                
                            
                        else:
                            print("Digite uma atividade válida!")

                    # ================================================================
                    # ENTREGA DE ATIVIDADES PARA ALUNOS
                    # ================================================================
                    # Alunos podem visualizar e entregar atividades
                    # Conteúdos de aula (tipo "C") apenas são visualizados, não podem ser entregues
                    if usuario_sistema["cargo"] == "aluno" and len(dados_atividades) > 0:
                        respost_aluno_atv = input("Digite o ID da atividade para acessá-la: ").upper()
                        
                        if respost_aluno_atv in dados_atividades:
                            # Exibe os detalhes da atividade/conteúdo
                            show_atividade(respost_aluno_atv)
                            
                            # ---- ENTREGA DE ATIVIDADE ----
                            # Apenas atividades (tipo "A") podem ser entregues
                            if dados_atividades[respost_aluno_atv]["tipo"] == "A":
                                aluno_atv_resp = input("Deseja fazer a entrega desta atividade? (s/n) ").lower()
                                
                                if aluno_atv_resp == "s":
                                    # Coleta a resposta do aluno
                                    aluno_atividade_entrega = input("Escreva a sua resposta para a atividade acima: ")
                                    
                                    # Prepara os dados para enviar ao programa externo
                                    # IMPORTANTE: A ordem dos dados é crucial para o programa atividade_aluno.exe
                                    aluno_atv_array = []
                                    aluno_atv_array.append(respost_aluno_atv)  # ID da atividade
                                    aluno_atv_array.append(dados_atividades[respost_aluno_atv]["titulo"])  # Título
                                    aluno_atv_array.append(dados_atividades[respost_aluno_atv]["conteudo"])  # Conteúdo/enunciado
                                    aluno_atv_array.append(usuario_sistema["nome"])  # Nome do aluno
                                    aluno_atv_array.append(usuario_sistema["matricula"])  # Matrícula
                                    aluno_atv_array.append(aluno_atividade_entrega)  # Resposta do aluno
                                    aluno_atv_array.append(dados_disciplinas[resposta_disciplinas]["nome"].title())  # Disciplina
                                    
                                    # Chama o programa externo atividade_aluno.exe (escrito em C)
                                    # Este programa cria um arquivo .txt com a resposta do aluno
                                    # Arquivo será salvo em: atividades_alunos/<id_atividade>_<matricula>.txt
                                    subprocess.run(["output/atividade_aluno.exe"] + aluno_atv_array)
                                    
                        else:
                            print("Digite uma atividade válida!")

                else:
                    print("Digite uma disciplina válida!") 


            elif resposta_login == 5 and usuario_sistema["admin"] != True:
                print("\nSem problemas! Parando a execução...")
                break




            # ================================================================
            # OPÇÃO 5 (ADMIN): LISTA DE APROVAÇÃO DE NOVOS CADASTROS
            # ================================================================
            # Funcionalidade exclusiva para administradores
            # Permite aprovar ou reprovar cadastros pendentes (aprovado = None)
            # 
            # FLUXO:
            # 1. Exibe lista de usuários com cadastro pendente
            # 2. Admin seleciona um usuário para avaliar
            # 3. Sistema mostra todos os dados do usuário
            # 4. Admin decide: 1 = Aprovar, 2 = Reprovar
            # 5. Status é atualizado no banco de dados
            # 
            # IMPORTANTE: Apenas usuários aprovados (aprovado = True) podem fazer login
            elif resposta_login == 5 and usuario_sistema["admin"] == True:
                os.system("cls")
                
                while True:
                    print("----- LISTA DE APROVAÇÕES -----")
                    
                    # Lista todos os usuários com aprovação pendente (None)
                    for usuario in dados_users:
                        if dados_users[usuario]["aprovado"] == None:
                            print(f"ID {usuario}: {dados_users[usuario]["nome"]}")
                    print("< Sair")
                    resposta_aprovacao = input("\nEscolha qual usuário você seja avaliar (digite o ID): ").upper()

                    if resposta_aprovacao == "<":
                        break  # Sai da lista de aprovação       


                    os.system('cls')
                    for usuario_aprovar in dados_users:
                        if usuario_aprovar == resposta_aprovacao:
                            while True:
                                # Mostra os detalhes do usuário para analisar
                                cpf_user = dados_users[usuario_aprovar]["cpf"]
                                print(f"----- USUÁRIO: {dados_users[usuario_aprovar]["nome"]} -----")
                                print(f"Email: {dados_users[usuario_aprovar]["email"]}")
                                print(f"Matrícula: {dados_users[usuario_aprovar]["matricula"]}")
                                print(f"Cargo: {dados_users[usuario_aprovar]["cargo"]}")
                                print(f"Data de nascimento: {dados_users[usuario_aprovar]["data_nascimento"]}")
                                print(f"CPF: {cpf_user[0:3]}.{cpf_user[3:6]}.{cpf_user[6:9]}-{cpf_user[9:11]}")
                                if dados_users[usuario_aprovar]["cargo"] == "aluno":
                                    turma_user_show = dados_users[usuario_aprovar]["turma"]
                                    print(f"Turma: {dados_users[usuario_aprovar]["turma"]}")
                                    try:
                                        print(f"Curso: {dados_turmas[turma_user_show]["curso"]}")
                                    except:
                                        print(f"Curso: Turma ainda não cadastrada no sistema")
                                print(f"----------------------------------------")
                                resposta_user_aprovacao = int(input("\nDigite 1 para aprovar e 2 para reprovar: "))

                                if resposta_user_aprovacao == 1:
                                    # Aprova o usuário
                                    dados_users[usuario_aprovar]["aprovado"] = True
                                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                                        os.system("cls")
                                        print("Usuário aprovado!\n")
                                        break

                                elif resposta_user_aprovacao == 2:
                                    # Reprova o usuário
                                    dados_users[usuario_aprovar]["aprovado"] = False
                                    with open(caminho_users, "w", encoding='utf-8') as arquivo_escrita:
                                        json.dump(dados_users, arquivo_escrita, ensure_ascii=False)
                                        os.system("cls")
                                        print("Usuário reprovado!\n")
                                        break
                                    
                                else:
                                    os.system("cls")
                                    print("ERRO: digite uma resposta válida!\n")
                                    continue
                            break

                        elif usuario_aprovar == list(dados_users)[-1]:
                            print("ERRO: digite uma resposta válida!\n")
                            continue

            # ================================================================
            # OPÇÃO 6 (ADMIN): ADMINISTRAR TURMAS
            # ================================================================
            # Funcionalidade exclusiva para administradores
            # CRUD completo de turmas: Create, Read, Update, Delete
            # 
            # ESTRUTURA DE TURMA:
            # - Código: 6 caracteres (exemplo: SI1A23)
            # - Curso: Nome do curso
            # - Semestre: Número do semestre atual da turma

            elif resposta_login == 6 and usuario_sistema["admin"] == True:
                os.system("cls")
                print("--- CONSULTA DE TURMAS ---")
                print("1. Visualizar turmas")
                print("2. Cadastrar turmas")
                print("3. Atualizar turmas")
                print("4. Excluir turmas")
                print("5. Voltar")
                resposta_turmas = int(input("Digite a opção desejada: "))

                # ---- VISUALIZAR TURMAS ----
                if resposta_turmas == 1:
                    os.system("cls")
                    if len(dados_turmas) > 0:
                        print("\nTurmas já cadastradas:")
                        for turma_cadastrada in dados_turmas:
                            print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].title()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                    else:
                        print("Não há nenhuma turma cadastrada!")
                    
                # ---- CADASTRAR TURMA ----
                if resposta_turmas == 2:
                    os.system("cls")
                    print("\n--- CADASTRAR NOVA TURMA ---")

                    while True:
                        nome_turma_cadastro = input("Digite o nome da turma no sistema: ").upper()
                        # Verifica se a turma já existe
                        if nome_turma_cadastro in dados_turmas:
                            print("Essa turma já existe! Digite uma turma nova.")
                        # Verifica se o nome da turma está no formato correto
                        elif nome_turma_cadastro[0:2].isalpha() and nome_turma_cadastro[2].isdigit() and nome_turma_cadastro[3].isalpha() and nome_turma_cadastro[4:6].isdigit():
                            break
                        else:
                            print("Digite uma turma válida!")

                    # Solicita o curso da turma
                    curso_turma_cadastro = input(f"Digite o curso respectivo da turma {nome_turma_cadastro}: ").lower()
                    # Solicita o semestre da turma
                    semestre_turma_cadastro = int(input(f"Digite o número do respectivo semestre da turma {nome_turma_cadastro}: "))

                    turma_cadastrar = {
                        "curso": curso_turma_cadastro,
                        "semestre": semestre_turma_cadastro
                    }
                    # Adiciona a turma ao banco de dados
                    dados_turmas[nome_turma_cadastro] = turma_cadastrar
                    # Salva a alteração no banco de dados
                    with open(caminho_turmas, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_turmas, arquivo_escrita, ensure_ascii=False)

                    print("Turma cadastrada com sucesso!")

                # ---- ATUALIZAR TURMA ----
                if resposta_turmas == 3:
                    os.system("cls")
                    print("\n--- ATUALIZAR TURMA ---")
                    # Verifica se há turmas cadastradas
                    if len(dados_turmas) > 0:
                        print("\nTurmas cadastradas:")
                        for turma_cadastrada in dados_turmas:
                            # Mostra as turmas cadastradas
                            print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].title()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                        print("< Voltar")
                        turma_update = input("\nDigite o nome da turma a ser atualizada: ").upper()

                        if turma_update == "<":
                            continue

                        elif turma_update in dados_turmas:
                            print(f"\nTurma {turma_update}: {dados_turmas[turma_update]["curso"].title()}, {dados_turmas[turma_update]["semestre"]}º semestre.")
                            # Solicita o novo semestre da turma
                            turma_update_semestre = int(input("Digite o número do novo semestre da turma: "))
                            # Atualiza o semestre da turma
                            dados_turmas[turma_update]["semestre"] = turma_update_semestre
                            # Salva a alteração no banco de dados
                            with open(caminho_turmas, "w", encoding='utf-8') as arquivo_escrita:
                                json.dump(dados_turmas, arquivo_escrita, ensure_ascii=False)
                            print("Dados atualizados!")
                                
                        else:
                            print("Digite uma turma válida!")
                    else:
                        print("Não há nenhuma turma cadastrada!")

                # ---- EXCLUIR TURMA ----
                if resposta_turmas == 4:
                    os.system("cls")
                    print("\n--- EXCLUIR TURMA ---")
                    # Verifica se há turmas cadastradas
                    if len(dados_turmas) > 0:
                        print("\nTurmas cadastradas:")
                        # Mostra as turmas cadastradas
                        for turma_cadastrada in dados_turmas:
                            print(f"Turma {turma_cadastrada}: {dados_turmas[turma_cadastrada]["curso"].title()}, {dados_turmas[turma_cadastrada]["semestre"]}º semestre.")
                        print("< Voltar")
                        # Solicita o nome da turma a ser excluída
                        turma_excluir = input("\nDigite o nome da turma a ser excluída: ").upper()

                        if turma_excluir == "<":
                            continue

                        elif turma_excluir in dados_turmas:
                            print(f"\nTurma {turma_excluir}: {dados_turmas[turma_excluir]["curso"].title()}, {dados_turmas[turma_excluir]["semestre"]}º semestre.")
                            # Solicita confirmação do usuário para excluir a turma
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


            # ================================================================
            # OPÇÃO 7 (ADMIN): ADMINISTRAR DISCIPLINAS
            # ================================================================
            # Funcionalidade exclusiva para administradores
            # CRUD completo de disciplinas: Create, Read, Update, Delete
            # 
            # ESTRUTURA DE DISCIPLINA:
            # - ID: Gerado automaticamente (ABC1234)
            # - Nome: Nome da disciplina
            # - Curso: Curso ao qual a disciplina pertence
            # - Semestre: Semestre em que deve ser cursada
            # - Professor: ID do professor responsável (pode ser None)
            # 
            # FUNÇÕES PRINCIPAIS:
            # - Criar novas disciplinas
            # - Atribuir professores às disciplinas
            # - Alterar informações (nome, curso, semestre, professor)
            # - Excluir disciplinas
            elif resposta_login == 7 and usuario_sistema["admin"] == True:

                os.system("cls")
                print("\n--- CONSULTA DE DISCIPLINAS ---")
                print("1. Visualizar disciplinas")
                print("2. Cadastrar disciplinas")
                print("3. Atualizar disciplinas")
                print("4. Excluir disciplinas")
                print("5. Voltar")
                resposta_disciplinas_admin = int(input("Digite a opção desejada: "))

                # ---- VISUALIZAR DISCIPLINAS ----
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

                    # Solicita o nome da nova disciplina
                    nome_disc_cadastro = input("Digite o nome da nova disciplina: ").lower()
                    # Solicita o curso da nova disciplina
                    curso_disc_cadastro = input("Digite o nome do curso que a disciplina faz parte: ").lower()
                    # Solicita o semestre da nova disciplina
                    sem_disc_cadastro = int(input("Digite o número do semestre que a disciplina deve ser cursada: "))

                    # Mostra os professores disponíveis
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
                    # Salva a alteração no banco de dados
                    with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                        json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)

                    print("Disciplina cadastrada com sucesso!")

                # ---- ATUALIZAR DISCIPLINA ----
                elif resposta_disciplinas_admin == 3:
                    os.system("cls")
                    print("\n--- ATUALIZAR DISCIPLINA ---")

                    # Verifica se há disciplinas cadastradas
                    if len(dados_disciplinas) > 0:
                        # Mostra as disciplinas cadastradas
                        print("\nDisciplinas já cadastradas:")
                        for disciplina_cadastrada in dados_disciplinas:
                            show_professor_disc(disciplina_cadastrada)
                        print("< Voltar")
                        disc_update = input("\nDigite o ID da disciplina a ser atualizada: ").upper()

                        if disc_update == "<":
                            continue

                        elif disc_update in dados_disciplinas:
                            # Mostra os detalhes da disciplina para analisar
                            show_professor_disc(disc_update)
                            # Solicita a opção de alteração
                            print("1. Alterar nome")
                            print("2. Alterar curso")
                            print("3. Alterar professor")
                            print("4. Alterar semestre")
                            print("< Voltar")
                            disc_update_input = int(input("\nO que você gostaria de alterar? "))

                            if disc_update_input == "<":
                                continue

                            elif disc_update_input == 1:
                                # Solicita o novo nome da disciplina
                                nome_novo_disc = input("\nDigite o novo nome da disciplina: ").lower()
                                dados_disciplinas[disc_update]["nome"] = nome_novo_disc
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")

                            elif disc_update_input == 2:
                                # Solicita o novo curso da disciplina
                                curso_novo_disc = input("\nDigite o novo curso da disciplina: ").lower()
                                dados_disciplinas[disc_update]["curso"] = curso_novo_disc
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")

                            elif disc_update_input == 3:
                                # Mostra os professores disponíveis
                                print("\nProfessores disponíveis:")
                                for usuario_disc in dados_users:
                                    if dados_users[usuario_disc]["cargo"] == "professor":
                                        print(f"{dados_users[usuario_disc]["matricula"]}: Prof. {dados_users[usuario_disc]["nome"]}")
                                # Solicita a matrícula do novo professor responsável
                                prof_disc_novo = input("\nSe já houver cadastro, digite a matrícula do novo professor responsável: ").upper()
                                # Verifica se o professor existe
                                if prof_disc_novo not in dados_users.values():
                                    prof_disc_novo = None
                                dados_disciplinas[disc_update]["professor"] = prof_disc_novo
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")

                            elif disc_update_input == 4:
                                # Solicita o novo semestre da disciplina
                                sem_novo_disc = int(input("\nDigite o novo semestre da disciplina: "))
                                dados_disciplinas[disc_update]["semestre"] = sem_novo_disc
                                with open(caminho_disciplinas, "w", encoding='utf-8') as arquivo_escrita:
                                    json.dump(dados_disciplinas, arquivo_escrita, ensure_ascii=False)
                                print("Dados atualizados!")
                                
                        else:
                            print("Digite uma disciplina válida!")
                    else:
                        print("Não há nenhuma disciplina cadastrada!")

                # ---- EXCLUIR DISCIPLINA ----
                elif resposta_disciplinas_admin == 4:
                    os.system("cls")
                    print("\n--- EXCLUIR DISCIPLINA ---")
                    # Verifica se há disciplinas cadastradas
                    if len(dados_disciplinas) > 0:
                        # Mostra as disciplinas cadastradas
                        for disciplina_cadastrada in dados_disciplinas:
                            show_professor_disc(disciplina_cadastrada)
                        print("< Voltar")
                        disc_delete = input("\nDigite o ID da disciplina a ser excluída: ").upper()

                        if disc_delete == "<":
                            continue

                        elif disc_delete in dados_disciplinas:
                            show_professor_disc(disciplina_cadastrada)
                            # Solicita confirmação do usuário para excluir a disciplina
                            disc_excluir_confirmar = input("Tem certeza que deseja excluir essa disciplina? (s/n) ").upper()
                            if disc_excluir_confirmar == "S":
                                del dados_disciplinas[disc_delete]
                                # Salva a alteração no banco de dados
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

    # ================================================================
    # OPÇÃO 3: SAIR DO SISTEMA
    # ================================================================
    else:
        print("\nSem problemas! Parando a execução...")
        sys.exit()

# ================================================================================
# TRATAMENTO DE ERROS GERAIS
# ================================================================================
except ValueError:
    # Captura erros de conversão de tipo (ex: digitar texto onde esperava número)
    print("Erro: digite uma resposta válida.")

#except:
    # Se algo der errado durante o cadastro ou log-in
    #print("Erro de processamento, tente novamente mais tarde.")

# ================================================================================
# FIM DO SISTEMA UNITECH
# ================================================================================