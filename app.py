import sys # Importa o módulo sys, que fornece acesso a variáveis e funções mantidas ou usadas pelo interpretador Python.
import hashlib # Importa o módulo hashlib para algoritmos de hash seguros, usado aqui para senhas.
import getpass # Importa o módulo getpass para obter a senha do usuário sem exibi-la na tela.
import os # Importa o módulo os, que fornece uma maneira de usar funcionalidades dependentes do sistema operacional, como limpar a tela.
from datetime import datetime, date # Importa as classes datetime e date do módulo datetime para trabalhar com datas e horas.
import db_connection # Importa o seu arquivo db_connection.py, que deve conter as funções para conectar e interagir com o banco de dados.
from decimal import Decimal # Importa Decimal para operações precisas com números decimais.

# ------------------- UTILS ----------------------
# Esta seção contém funções utilitárias usadas em várias partes do aplicativo.

def hash_password(password):
    """Gera o hash SHA256 de uma senha."""
    # Codifica a senha para bytes, calcula o hash SHA256 e retorna a representação hexadecimal.
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, provided_password):
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    # Compara o hash armazenado com o hash da senha fornecida.
    return stored_hash == hash_password(provided_password)

def clear_screen():
    """Limpa a tela do terminal."""
    # Executa o comando 'cls' no Windows ou 'clear' em outros sistemas (Linux, macOS) para limpar a tela.
    os.system('cls' if os.name == 'nt' else 'clear')

def press_enter_to_continue():
    """Pausa a execução até que o usuário pressione Enter."""
    # Exibe uma mensagem e aguarda a entrada do usuário (pressionar Enter).
    input("\nPressione Enter para continuar...")

def display_menu(title, options, show_exit_option=True):
    """
    Exibe um menu formatado e obtém a escolha do usuário.

    Args:
        title (str): O título do menu.
        options (list): Uma lista de strings representando as opções do menu.
        show_exit_option (bool): Se True, adiciona "0. Voltar" ou "0. Sair".
                                 Se False, a opção 0 não é mostrada (útil para sub-menus de confirmação).
    Returns:
        int: A escolha do usuário.
    """
    print(f"\n--- {title} ---") # Exibe o título do menu.
    for i, option in enumerate(options, 1): # Itera sobre as opções, começando a numeração em 1.
        print(f"{i}. {option}") # Exibe cada opção numerada.

    if show_exit_option: # Verifica se a opção de sair/voltar deve ser mostrada.
        # Determina se a opção 0 deve ser "Voltar" ou "Sair" com base no título.
        if "Principal" in title or "Login" in title or "Bem-vindo" in title or not any(s in title.lower() for s in ["gerenciar", "menu d", "funções de"]):
            print("0. Sair")
        else:
            print("0. Voltar")

    while True: # Loop até que uma entrada válida seja fornecida.
        try:
            choice_str = input("Escolha uma opção: ").strip() # Solicita a escolha do usuário e remove espaços extras.
            if not choice_str.isdigit(): # Verifica se a entrada é um dígito.
                raise ValueError("Entrada não é um número.")
            choice = int(choice_str) # Converte a escolha para inteiro.

            if not show_exit_option: # Se não há opção 0 (ex: menu de confirmação).
                 if 1 <= choice <= len(options): # Valida se a escolha está dentro do intervalo de opções.
                    return choice # Retorna a escolha válida.
                 else:
                    print(f"Opção inválida. Escolha entre 1 e {len(options)}.")
            else: # Se há opção 0 (menu normal).
                if 0 <= choice <= len(options): # Valida se a escolha está dentro do intervalo, incluindo 0.
                    return choice # Retorna a escolha válida.
                else:
                    print(f"Opção inválida. Escolha entre 0 e {len(options)}.")
        except ValueError: # Captura erro se a entrada não for um número.
            print("Entrada inválida. Por favor, digite um número.")

def get_valid_input(prompt, input_type=str, optional=False, choices=None):
    """
    Solicita uma entrada do usuário, valida o tipo e se é opcional.
    Se `choices` for fornecido, valida se a entrada está na lista de escolhas.

    Args:
        prompt (str): A mensagem a ser exibida ao usuário.
        input_type (type): O tipo esperado da entrada (int, float, date, str).
        optional (bool): Se True, a entrada pode ser vazia (retorna None).
        choices (list or dict): Lista ou dicionário de escolhas válidas.

    Returns:
        O valor validado do tipo especificado, ou None se opcional e vazio.
    """
    while True: # Loop até que uma entrada válida seja fornecida.
        user_input = input(prompt).strip() # Solicita a entrada e remove espaços extras.
        if optional and not user_input: # Se for opcional e o usuário não digitou nada.
            return None # Retorna None.
        if not optional and not user_input: # Se não for opcional e o usuário não digitou nada.
            print("Este campo é obrigatório.")
            continue # Pede a entrada novamente.

        try:
            if input_type == int: # Se o tipo esperado for inteiro.
                val = int(user_input)
            elif input_type == float: # Se o tipo esperado for float.
                val = float(user_input)
            elif input_type == date: # Se o tipo esperado for data.
                val = datetime.strptime(user_input, '%Y-%m-%d').date() # Converte string para objeto date.
            else: # str (padrão)
                val = str(user_input)

            if choices: # Se uma lista/dicionário de escolhas foi fornecida.
                if isinstance(choices, dict): # Se for um dicionário, valida contra as chaves.
                    if val not in choices:
                        print(f"Opção inválida. Escolhas válidas: {', '.join(choices.keys())}")
                        continue # Pede a entrada novamente.
                elif val not in choices: # Se for uma lista.
                    print(f"Opção inválida. Escolhas válidas: {', '.join(map(str,choices))}")
                    continue # Pede a entrada novamente.
            return val # Retorna o valor validado.
        except ValueError: # Captura erros de conversão de tipo.
            if input_type == date:
                print("Formato de data inválido. Use AAAA-MM-DD.")
            else:
                print(f"Entrada inválida. Esperado um {'número inteiro' if input_type == int else 'número decimal' if input_type == float else 'texto'}.")

# --- Lógicas de CRUD para as Entidades (Administrador) ---
# CRUD: Create, Read, Update, Delete (Criar, Ler, Atualizar, Deletar)

# Gerenciar Pessoas (Conforme já implementado e levemente ajustado)
def manage_people_terminal(conn):
    """Menu para gerenciar Pessoas (Adicionar, Listar, Atualizar, Deletar)."""
    options = ["Adicionar Pessoa", "Listar Pessoas", "Atualizar Pessoa", "Deletar Pessoa"]
    while True:
        clear_screen() # Limpa a tela.
        choice = display_menu("Gerenciar Pessoas", options) # Exibe o menu e obtém a escolha.

        if choice == 1: add_person_terminal(conn) # Chama a função para adicionar pessoa.
        elif choice == 2: list_people_terminal(conn) # Chama a função para listar pessoas.
        elif choice == 3: update_person_terminal(conn) # Chama a função para atualizar pessoa.
        elif choice == 4: delete_person_terminal(conn) # Chama a função para deletar pessoa.
        elif choice == 0: break # Sai do menu de gerenciamento de pessoas.
        press_enter_to_continue() # Pausa antes de limpar a tela e mostrar o menu novamente.

def add_person_terminal(conn, return_id=False):
    """Adiciona uma nova Pessoa e seu Endereço ao banco de dados."""
    print("\n--- Adicionar Nova Pessoa ---")
    # Coleta dados da pessoa usando a função de entrada validada.
    name = get_valid_input("Nome: ")
    rg = get_valid_input("RG (opcional): ", optional=True)
    phone = get_valid_input("Telefone: ")
    email = get_valid_input("Email: ")

    print("\n--- Dados do Endereço ---")
    # Coleta dados do endereço.
    cep = get_valid_input("CEP: ")
    state = get_valid_input("Estado: ")
    city = get_valid_input("Cidade: ")
    neighborhood = get_valid_input("Bairro: ")
    street = get_valid_input("Rua: ")
    number = get_valid_input("Número: ")
    complement = get_valid_input("Complemento (opcional): ", optional=True)

    try:
        # Define a query SQL para inserir um novo endereço.
        sql_insert_address = "INSERT INTO Endereco (CEP, Estado, Cidade, Bairro, Rua, Numero, Complemento) VALUES (?, ?, ?, ?, ?, ?, ?);"
        address_params = (cep, state, city, neighborhood, street, number, complement) # Parâmetros para a query.
        # Executa a inserção e obtém o ID do último endereço inserido.
        new_address_id = db_connection.execute_insert_and_get_last_id(conn, sql_insert_address, address_params)

        if new_address_id is not None: # Se o endereço foi inserido com sucesso.
            # Define a query SQL para inserir uma nova pessoa, usando o ID do endereço recém-criado.
            sql_insert_person = "INSERT INTO Pessoa (Nome, RG, Telefone, Email, ID_Endereco) VALUES (?, ?, ?, ?, ?);"
            person_params = (name, rg, phone, email, new_address_id) # Parâmetros para a query.
            
            if return_id: # Se a função foi chamada para retornar o ID da pessoa criada (ex: cadastro de cliente).
                new_person_id = db_connection.execute_insert_and_get_last_id(conn, sql_insert_person, person_params)
                if new_person_id:
                    print("Pessoa e Endereço adicionados com sucesso!")
                    return new_person_id # Retorna o ID da nova pessoa.
                else:
                    print("Erro: Falha ao adicionar pessoa ou recuperar seu ID.")
                    # Em um cenário transacional mais complexo, seria ideal um rollback do endereço aqui.
                    return None
            else: # Comportamento padrão (não precisa retornar ID).
                result_person_insert = db_connection.execute_query(conn, sql_insert_person, person_params)
                if result_person_insert:
                    print("Pessoa e Endereço adicionados com sucesso!")
                else:
                    print("Erro: Falha ao adicionar pessoa.")
        else:
            print("Erro: Falha ao adicionar endereço ou recuperar seu ID.")
    except Exception as e: # Captura qualquer exceção inesperada.
        print(f"Erro inesperado ao adicionar pessoa: {e}")
    return None # Para o caso de return_id=False ou falha.

def list_people_terminal(conn):
    """Lista todas as Pessoas cadastradas com seus Endereços."""
    print("\n--- Lista de Pessoas ---")
    # Query SQL para selecionar dados da Pessoa e seu Endereço associado.
    sql = """
    SELECT P.Codigo_Pessoa, P.Nome, P.RG, P.Telefone, P.Email,
           E.CEP, E.Rua, E.Numero, E.Bairro, E.Cidade, E.Estado
    FROM Pessoa P
    INNER JOIN Endereco E ON P.ID_Endereco = E.ID_Endereco
    ORDER BY P.Nome;
    """
    people_data = db_connection.execute_query(conn, sql, fetch_results=True) # Executa a query e busca os resultados.

    if people_data: # Se houver dados.
        headers = ["Cód.", "Nome", "RG", "Telefone", "Email", "CEP", "Rua", "Nº", "Bairro", "Cidade", "UF"]
        col_widths = [5, 25, 12, 15, 25, 10, 20, 8, 15, 15, 5] # Define larguras das colunas para formatação.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths]) # Cria o formato da string para o cabeçalho.
        print(header_format.format(*headers)) # Exibe o cabeçalho.
        print("-" * sum(col_widths)) # Exibe uma linha divisória.
        for person in people_data: # Itera sobre cada pessoa.
            # Formata cada campo da pessoa (converte None para string vazia).
            person_formatted = [str(x) if x is not None else "" for x in person]
            print(header_format.format(*person_formatted)) # Exibe os dados formatados da pessoa.
    else:
        print("Nenhuma pessoa encontrada.")

def update_person_terminal(conn):
    """Atualiza os dados de uma Pessoa e seu Endereço."""
    print("\n--- Atualizar Pessoa ---")
    person_id = get_valid_input("Digite o Código Pessoa a ser atualizada: ", int) # Pede o ID da pessoa.
    if person_id is None: return # Se o ID não for fornecido, retorna.

    # Query para buscar os dados atuais da pessoa e seu endereço.
    sql_get_person = """
    SELECT P.Nome, P.RG, P.Telefone, P.Email, E.ID_Endereco, E.CEP, E.Estado, E.Cidade, E.Bairro, E.Rua, E.Numero, E.Complemento
    FROM Pessoa P INNER JOIN Endereco E ON P.ID_Endereco = E.ID_Endereco
    WHERE P.Codigo_Pessoa = ?;
    """
    current_data = db_connection.execute_query(conn, sql_get_person, (person_id,), fetch_results=True)

    if not current_data: # Se a pessoa não for encontrada.
        print("Pessoa não encontrada.")
        return

    p_data = current_data[0] # Pega os dados da pessoa.
    print("\nDeixe o campo em branco para manter o valor atual.")
    # Solicita novos dados, mantendo os antigos se o usuário não digitar nada.
    new_name = input(f"Nome [{p_data[0]}]: ").strip() or p_data[0]
    new_rg = input(f"RG [{p_data[1] or ''}]: ").strip() or p_data[1]
    new_phone = input(f"Telefone [{p_data[2]}]: ").strip() or p_data[2]
    new_email = input(f"Email [{p_data[3]}]: ").strip() or p_data[3]

    address_id = p_data[4] # ID do endereço.
    # Solicita novos dados do endereço.
    new_cep = input(f"CEP [{p_data[5]}]: ").strip() or p_data[5]
    new_state = input(f"Estado [{p_data[6]}]: ").strip() or p_data[6]
    new_city = input(f"Cidade [{p_data[7]}]: ").strip() or p_data[7]
    new_neighborhood = input(f"Bairro [{p_data[8]}]: ").strip() or p_data[8]
    new_street = input(f"Rua [{p_data[9]}]: ").strip() or p_data[9]
    new_number = input(f"Número [{p_data[10]}]: ").strip() or p_data[10]
    new_complement = input(f"Complemento [{p_data[11] or ''}]: ").strip() or p_data[11]

    try:
        # Query para atualizar o endereço.
        sql_update_address = "UPDATE Endereco SET CEP=?, Estado=?, Cidade=?, Bairro=?, Rua=?, Numero=?, Complemento=? WHERE ID_Endereco=?;"
        db_connection.execute_query(conn, sql_update_address, (new_cep, new_state, new_city, new_neighborhood, new_street, new_number, new_complement, address_id))

        # Query para atualizar a pessoa.
        sql_update_person = "UPDATE Pessoa SET Nome=?, RG=?, Telefone=?, Email=? WHERE Codigo_Pessoa=?;"
        db_connection.execute_query(conn, sql_update_person, (new_name, new_rg, new_phone, new_email, person_id))
        print("Pessoa e Endereço atualizados com sucesso!")
    except Exception as e:
        print(f"Erro inesperado ao atualizar pessoa: {e}")

def delete_person_terminal(conn):
    """Deleta uma Pessoa e seu Endereço (se não estiver em uso por outra entidade)."""
    print("\n--- Deletar Pessoa ---")
    person_id = get_valid_input("Digite o Código Pessoa a ser deletada: ", int) # Pede o ID da pessoa.
    if person_id is None: return

    # Dicionário de dependências: verifica se a pessoa está sendo usada em outras tabelas.
    dependencies = {
        "Usuario": "SELECT 1 FROM Usuario WHERE Codigo_Pessoa = ?",
        "Cliente": "SELECT 1 FROM Cliente WHERE Codigo_Pessoa = ?",
        "Funcionario": "SELECT 1 FROM Funcionario WHERE Codigo_Funcionario = ?", # Assumindo Codigo_Funcionario = Codigo_Pessoa
        "Produto (Remetente)": "SELECT 1 FROM Produto_A_Ser_Entregue WHERE ID_Remetente = ?",
        "Produto (Destinatário)": "SELECT 1 FROM Produto_A_Ser_Entregue WHERE ID_Destinatario = ?"
    }
    for table, sql_check in dependencies.items(): # Itera sobre as dependências.
        if db_connection.execute_query(conn, sql_check, (person_id,), fetch_results=True): # Se encontrar dependência.
            print(f"Erro: Não é possível deletar. Pessoa está referenciada na tabela {table}.")
            return

    # Busca o ID do endereço associado à pessoa para possível exclusão.
    address_id_data = db_connection.execute_query(conn, "SELECT ID_Endereco FROM Pessoa WHERE Codigo_Pessoa = ?", (person_id,), fetch_results=True)
    
    confirm = input(f"Tem certeza que deseja deletar a pessoa com Cód. {person_id} e seu endereço? (s/n): ").strip().lower()
    if confirm != 's': # Se o usuário não confirmar.
        print("Exclusão cancelada.")
        return

    try:
        # Deleta a pessoa.
        if db_connection.execute_query(conn, "DELETE FROM Pessoa WHERE Codigo_Pessoa = ?", (person_id,)):
            print("Pessoa deletada.")
            if address_id_data: # Se a pessoa tinha um endereço associado.
                address_id = address_id_data[0][0]
                # Verifica se o endereço é usado por outra Pessoa ou Sede antes de deletá-lo.
                sql_check_addr_pessoa = "SELECT 1 FROM Pessoa WHERE ID_Endereco = ? AND Codigo_Pessoa != ?"
                sql_check_addr_sede = "SELECT 1 FROM Sede WHERE ID_Endereco = ?"
                if not db_connection.execute_query(conn, sql_check_addr_pessoa, (address_id, person_id), fetch_results=True) and \
                   not db_connection.execute_query(conn, sql_check_addr_sede, (address_id,), fetch_results=True):
                    # Se o endereço não estiver em uso, deleta-o.
                    if db_connection.execute_query(conn, "DELETE FROM Endereco WHERE ID_Endereco = ?", (address_id,)):
                        print("Endereço associado deletado com sucesso.")
                    else:
                        print("Aviso: Pessoa deletada, mas falha ao deletar endereço (pode ainda estar em uso ou erro).")
                else:
                    print("Aviso: Pessoa deletada, mas o endereço não foi removido pois está em uso por outra entidade.")
            else:
                print("Aviso: Pessoa deletada, mas não foi possível encontrar/deletar o endereço associado.")
        else:
            print("Erro: Falha ao deletar pessoa.")
    except Exception as e:
        print(f"Erro inesperado ao deletar pessoa: {e}")

# Gerenciar Usuários
def manage_users_terminal(conn):
    """Menu para gerenciar Usuários (Adicionar, Listar, Atualizar, Deletar)."""
    options = ["Adicionar Usuário", "Listar Usuários", "Atualizar Usuário", "Deletar Usuário"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Usuários", options)
        if choice == 1: add_user_terminal(conn)
        elif choice == 2: list_users_terminal(conn)
        elif choice == 3: update_user_terminal(conn)
        elif choice == 4: delete_user_terminal(conn)
        elif choice == 0: break
        press_enter_to_continue()

def add_user_terminal(conn):
    """Adiciona um novo Usuário ao sistema."""
    print("\n--- Adicionar Novo Usuário ---")
    login = get_valid_input("Login: ") # Coleta o login.
    password = getpass.getpass("Senha: ").strip() # Coleta a senha de forma segura.
    while not password: # Garante que a senha não seja vazia.
        print("Senha não pode ser vazia.")
        password = getpass.getpass("Senha: ").strip()

    person_code = get_valid_input("Código Pessoa (de uma pessoa já cadastrada): ", int) # Coleta o código da pessoa associada.
    if person_code is None: return

    # Verifica se o Código Pessoa existe na tabela Pessoa.
    if not db_connection.execute_query(conn, "SELECT 1 FROM Pessoa WHERE Codigo_Pessoa = ?", (person_code,), fetch_results=True):
        print("Erro: Código Pessoa não encontrado. Cadastre a pessoa primeiro.")
        return

    # Verifica se já existe um usuário para este Código Pessoa.
    if db_connection.execute_query(conn, "SELECT 1 FROM Usuario WHERE Codigo_Pessoa = ?", (person_code,), fetch_results=True):
        print("Erro: Já existe um usuário associado a este Código Pessoa.")
        return

    valid_user_types = ['Cliente', 'Motorista', 'Auxiliar de Logistica', 'Atendente', 'Gerente', 'Admin']
    user_type = get_valid_input(f"Tipo de Usuário ({', '.join(valid_user_types)}): ", choices=valid_user_types) # Coleta o tipo de usuário.
    if user_type is None: return

    # Lógica para garantir consistência com as tabelas Cliente/Funcionario.
    if user_type == 'Cliente':
        # Verifica se a pessoa está cadastrada como Cliente.
        if not db_connection.execute_query(conn, "SELECT 1 FROM Cliente WHERE Codigo_Pessoa = ?", (person_code,), fetch_results=True):
            print(f"Atenção: Esta pessoa (Cód: {person_code}) não está cadastrada como Cliente.")
            if input("Deseja cadastrá-la como Cliente agora? (s/n): ").lower() == 's':
                # Informa que o cadastro de Cliente deve ser feito pelo menu apropriado.
                print("Por favor, cadastre esta pessoa como Cliente através do menu 'Gerenciar Clientes' antes de criar o usuário Cliente.")
                return
            else:
                print("Criação de usuário cancelada. Pessoa não é um Cliente.")
                return
    elif user_type in ['Motorista', 'Auxiliar de Logistica', 'Atendente', 'Gerente', 'Admin']:
        # Verifica se a pessoa está cadastrada como Funcionário.
        if not db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE Codigo_Funcionario = ?", (person_code,), fetch_results=True):
            print(f"Atenção: Esta pessoa (Cód: {person_code}) não está cadastrada como Funcionário.")
            if input("Deseja cadastrá-la como Funcionário agora? (s/n): ").lower() == 's':
                # Informa que o cadastro de Funcionário deve ser feito pelo menu apropriado.
                print("Por favor, cadastre esta pessoa como Funcionário através do menu 'Gerenciar Funcionários' antes de criar o usuário funcionário.")
                return
            else:
                print("Criação de usuário cancelada. Pessoa não é um Funcionário.")
                return
        # Verifica se o Cargo do funcionário corresponde ao Tipo_Usuario.
        func_data = db_connection.execute_query(conn, "SELECT Cargo FROM Funcionario WHERE Codigo_Funcionario = ?", (person_code,), fetch_results=True)
        if func_data and func_data[0][0].replace(" ", "") != user_type.replace(" ", ""): # Compara ignorando espaços.
            if not (func_data[0][0] == 'Gerente' and user_type == 'Admin'): # Permite que um Gerente seja Admin.
                 print(f"Aviso: O cargo do funcionário ({func_data[0][0]}) não corresponde exatamente ao tipo de usuário ({user_type}).")
                 if input("Continuar mesmo assim? (s/n): ").lower() != 's':
                     return

    hashed_password = hash_password(password) # Gera o hash da senha.
    sql = "INSERT INTO Usuario (Login, Senha_Hash, Codigo_Pessoa, Tipo_Usuario) VALUES (?, ?, ?, ?)"
    if db_connection.execute_query(conn, sql, (login, hashed_password, person_code, user_type)): # Insere o usuário.
        print("Usuário adicionado com sucesso!")
    else:
        print("Erro: Falha ao adicionar usuário. O login pode já existir.")

def list_users_terminal(conn):
    """Lista todos os Usuários cadastrados."""
    print("\n--- Lista de Usuários ---")
    # Query para selecionar dados dos usuários e o nome da pessoa associada.
    sql = "SELECT U.Login, U.Codigo_Pessoa, P.Nome, U.Tipo_Usuario FROM Usuario U JOIN Pessoa P ON U.Codigo_Pessoa = P.Codigo_Pessoa ORDER BY U.Login"
    users = db_connection.execute_query(conn, sql, fetch_results=True)
    if users:
        headers = ["Login", "Cód. Pessoa", "Nome Pessoa", "Tipo Usuário"]
        col_widths = [20, 12, 30, 25] # Define larguras das colunas.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths]) # Formato do cabeçalho.
        print(header_format.format(*headers)) # Exibe o cabeçalho.
        print("-" * sum(col_widths)) # Linha divisória.
        for user in users: # Itera sobre os usuários.
            print(header_format.format(*user)) # Exibe dados do usuário.
    else:
        print("Nenhum usuário encontrado.")

def update_user_terminal(conn):
    """Atualiza a senha de um Usuário."""
    print("\n--- Atualizar Usuário ---")
    login_to_update = get_valid_input("Digite o Login do usuário a ser atualizado: ") # Pede o login do usuário.
    if login_to_update is None: return

    # Busca dados do usuário.
    user_data = db_connection.execute_query(conn, "SELECT Senha_Hash, Codigo_Pessoa, Tipo_Usuario FROM Usuario WHERE Login = ?", (login_to_update,), fetch_results=True)
    if not user_data:
        print("Usuário não encontrado.")
        return

    _, current_person_code, current_user_type = user_data[0] # Pega código da pessoa e tipo de usuário atuais.

    print(f"\nAtualizando usuário: {login_to_update}")
    print(f"Código Pessoa atual: {current_person_code}, Tipo atual: {current_user_type}")
    print("Deixe em branco para manter o valor atual.")

    new_password = getpass.getpass("Nova Senha (deixe em branco para não alterar): ").strip() # Pede nova senha.
    
    # Informa que Código Pessoa e Tipo de Usuário não são alterados aqui para simplificar.
    print(f"Código Pessoa ({current_person_code}) e Tipo de Usuário ({current_user_type}) não podem ser alterados diretamente.")
    print("Para alterar o tipo ou a pessoa associada, delete e recrie o usuário.")

    if new_password: # Se uma nova senha foi fornecida.
        hashed_password = hash_password(new_password) # Gera hash da nova senha.
        sql = "UPDATE Usuario SET Senha_Hash = ? WHERE Login = ?" # Query para atualizar a senha.
        params = (hashed_password, login_to_update)
    else: # Nenhuma alteração se apenas a senha não foi mudada.
        print("Nenhuma alteração na senha. Nada a atualizar.")
        return

    if db_connection.execute_query(conn, sql, params): # Executa a atualização.
        print("Usuário atualizado com sucesso!")
    else:
        print("Erro: Falha ao atualizar usuário.")

def delete_user_terminal(conn):
    """Deleta um Usuário do sistema."""
    print("\n--- Deletar Usuário ---")
    login_to_delete = get_valid_input("Digite o Login do usuário a ser deletado: ") # Pede o login do usuário.
    if login_to_delete is None: return

    # Verifica se o usuário existe.
    if not db_connection.execute_query(conn, "SELECT 1 FROM Usuario WHERE Login = ?", (login_to_delete,), fetch_results=True):
        print("Usuário não encontrado.")
        return

    confirm = input(f"Tem certeza que deseja deletar o usuário '{login_to_delete}'? (s/n): ").strip().lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return

    if db_connection.execute_query(conn, "DELETE FROM Usuario WHERE Login = ?", (login_to_delete,)): # Deleta o usuário.
        print("Usuário deletado com sucesso!")
    else:
        print("Erro: Falha ao deletar usuário.")

# Gerenciar Clientes
def manage_clients_terminal(conn):
    """Menu para gerenciar Clientes."""
    options = ["Adicionar Cliente", "Listar Clientes", "Atualizar Cliente", "Deletar Cliente"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Clientes", options)
        if choice == 1: add_client_terminal(conn)
        elif choice == 2: list_clients_terminal(conn)
        elif choice == 3: update_client_terminal(conn)
        elif choice == 4: delete_client_terminal(conn)
        elif choice == 0: break
        press_enter_to_continue()

def add_client_terminal(conn, person_code_param=None, client_type_param=None, cpf_param=None, dob_param=None, cnpj_param=None, company_name_param=None):
    """Adiciona um novo Cliente (PF ou PJ)."""
    print("\n--- Adicionar Novo Cliente ---")
    if person_code_param is None: # Se o código da pessoa não foi passado como parâmetro (uso normal pelo menu admin).
        person_code = get_valid_input("Código Pessoa (de uma pessoa já cadastrada): ", int)
        if person_code is None: return
    else: # Se o código da pessoa foi passado (ex: cadastro self-service).
        person_code = person_code_param

    # Verifica se a pessoa existe e se já não é um cliente.
    if not db_connection.execute_query(conn, "SELECT 1 FROM Pessoa WHERE Codigo_Pessoa = ?", (person_code,), fetch_results=True):
        print("Erro: Código Pessoa não encontrado. Cadastre a pessoa primeiro.")
        return
    if db_connection.execute_query(conn, "SELECT 1 FROM Cliente WHERE Codigo_Pessoa = ?", (person_code,), fetch_results=True):
        print("Erro: Já existe um cliente associado a este Código Pessoa.")
        return

    if client_type_param is None: # Se o tipo de cliente não foi passado.
        client_type = get_valid_input("Tipo de Cliente (PF - Pessoa Física / PJ - Pessoa Jurídica): ", str.upper, choices=['PF', 'PJ'])
        if client_type is None: return
    else: # Se o tipo de cliente foi passado.
        client_type = client_type_param

    cpf, dob, cnpj, company_name = None, None, None, None # Inicializa variáveis.
    if client_type == 'PF': # Se for Pessoa Física.
        cpf = cpf_param if cpf_param else get_valid_input("CPF: ")
        dob_str = dob_param if dob_param else get_valid_input("Data de Nascimento (AAAA-MM-DD): ", str) # Pega data como string.
        try:
            # Converte a string da data para objeto date.
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if isinstance(dob_str, str) else dob_str
        except ValueError:
            print("Erro: Formato de data inválido. Use AAAA-MM-DD.")
            return
    elif client_type == 'PJ': # Se for Pessoa Jurídica.
        cnpj = cnpj_param if cnpj_param else get_valid_input("CNPJ: ")
        company_name = company_name_param if company_name_param else get_valid_input("Nome da Empresa: ")

    # Query para inserir o cliente.
    sql = "INSERT INTO Cliente (Codigo_Pessoa, Tipo_Cliente, CPF, Data_Nascimento, CNPJ, Nome_Empresa) VALUES (?, ?, ?, ?, ?, ?);"
    if db_connection.execute_query(conn, sql, (person_code, client_type, cpf, dob, cnpj, company_name)):
        print("Cliente adicionado com sucesso!")
        return True # Retorna True em caso de sucesso.
    else:
        print("Erro: Falha ao adicionar cliente. Verifique os dados e as constraints da tabela (CHK_Cliente_PF_PJ).")
        return False # Retorna False em caso de falha.

def list_clients_terminal(conn):
    """Lista todos os Clientes cadastrados."""
    print("\n--- Lista de Clientes ---")
    # Query para selecionar dados dos clientes, incluindo nome da pessoa e formatação da data de nascimento.
    sql = """
    SELECT C.Codigo_Pessoa, P.Nome, C.Tipo_Cliente, C.CPF, 
           FORMAT(C.Data_Nascimento, 'dd/MM/yyyy') AS Data_Nascimento, 
           C.CNPJ, C.Nome_Empresa
    FROM Cliente C
    INNER JOIN Pessoa P ON C.Codigo_Pessoa = P.Codigo_Pessoa
    ORDER BY P.Nome;
    """
    clients_data = db_connection.execute_query(conn, sql, fetch_results=True)
    if clients_data:
        headers = ["Cód. Pessoa", "Nome", "Tipo", "CPF", "Data Nasc.", "CNPJ", "Nome Empresa"]
        col_widths = [12, 25, 8, 15, 12, 20, 30] # Larguras das colunas.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for client in clients_data: # Itera sobre os clientes.
            client_formatted = [str(x) if x is not None else "" for x in client] # Formata dados.
            print(header_format.format(*client_formatted)) # Exibe dados do cliente.
    else:
        print("Nenhum cliente encontrado.")

def update_client_terminal(conn, person_code_logged_in=None):
    """Atualiza os dados de um Cliente."""
    print("\n--- Atualizar Cliente ---")
    if person_code_logged_in: # Se o código da pessoa foi passado (ex: cliente atualizando seus próprios dados).
        person_code = person_code_logged_in
        print(f"Atualizando seus dados de cliente (Código Pessoa: {person_code}).")
    else: # Uso normal pelo menu admin.
        person_code = get_valid_input("Digite o Código Pessoa do cliente a ser atualizado: ", int)
        if person_code is None: return

    # Query para buscar dados atuais do cliente.
    sql_get_client = """
    SELECT P.Nome, C.Tipo_Cliente, C.CPF, C.Data_Nascimento, C.CNPJ, C.Nome_Empresa
    FROM Cliente C INNER JOIN Pessoa P ON C.Codigo_Pessoa = P.Codigo_Pessoa
    WHERE C.Codigo_Pessoa = ?;
    """
    current_data = db_connection.execute_query(conn, sql_get_client, (person_code,), fetch_results=True)
    if not current_data:
        print("Cliente não encontrado.")
        return

    c_data = current_data[0] # Dados atuais do cliente.
    print(f"\nNome da Pessoa associada: {c_data[0]}")
    print("Deixe o campo em branco para manter o valor atual.")

    # Solicita novo tipo de cliente.
    new_client_type = input(f"Tipo de Cliente [{c_data[1]}] (PF/PJ): ").strip().upper() or c_data[1]
    if new_client_type not in ['PF', 'PJ']:
        print("Erro: Tipo de cliente inválido. Mantendo o anterior.")
        new_client_type = c_data[1]

    new_cpf, new_dob, new_cnpj, new_company_name = c_data[2], c_data[3], c_data[4], c_data[5] # Inicializa com dados atuais.

    if new_client_type == 'PF': # Se for Pessoa Física.
        new_cpf = input(f"CPF [{c_data[2] or ''}]: ").strip() or c_data[2]
        dob_str = input(f"Data de Nascimento [{c_data[3] or ''}] (AAAA-MM-DD): ").strip()
        if dob_str: # Se uma nova data foi digitada.
            try:
                new_dob = datetime.strptime(dob_str, '%Y-%m-%d').date() # Converte para objeto date.
            except ValueError:
                print("Formato de data inválido. Mantendo data anterior.")
        new_cnpj, new_company_name = None, None # Zera dados de PJ.
    elif new_client_type == 'PJ': # Se for Pessoa Jurídica.
        new_cnpj = input(f"CNPJ [{c_data[4] or ''}]: ").strip() or c_data[4]
        new_company_name = input(f"Nome da Empresa [{c_data[5] or ''}]: ").strip() or c_data[5]
        new_cpf, new_dob = None, None # Zera dados de PF.

    # Query para atualizar o cliente.
    sql_update = "UPDATE Cliente SET Tipo_Cliente=?, CPF=?, Data_Nascimento=?, CNPJ=?, Nome_Empresa=? WHERE Codigo_Pessoa=?;"
    if db_connection.execute_query(conn, sql_update, (new_client_type, new_cpf, new_dob, new_cnpj, new_company_name, person_code)):
        print("Cliente atualizado com sucesso!")
    else:
        print("Erro: Falha ao atualizar cliente. Verifique os dados e as constraints (CHK_Cliente_PF_PJ).")

def delete_client_terminal(conn):
    """Deleta um Cliente."""
    print("\n--- Deletar Cliente ---")
    person_code = get_valid_input("Digite o Código Pessoa do cliente a ser deletado: ", int) # Pede o código da pessoa.
    if person_code is None: return

    # Verifica dependências em Produto_A_Ser_Entregue e Usuario.
    if db_connection.execute_query(conn, "SELECT 1 FROM Produto_A_Ser_Entregue WHERE ID_Remetente = ? OR ID_Destinatario = ?", (person_code, person_code), fetch_results=True):
        print("Erro: Cliente está associado a produtos. Não pode ser deletado.")
        return
    if db_connection.execute_query(conn, "SELECT 1 FROM Usuario WHERE Codigo_Pessoa = ? AND Tipo_Usuario = 'Cliente'", (person_code,), fetch_results=True):
        print("Erro: Cliente possui um usuário associado. Delete o usuário primeiro ou altere seu tipo.")
        return
    
    # Busca o nome do cliente para a mensagem de confirmação.
    client_name_data = db_connection.execute_query(conn, "SELECT P.Nome FROM Cliente C INNER JOIN Pessoa P ON C.Codigo_Pessoa = P.Codigo_Pessoa WHERE C.Codigo_Pessoa = ?", (person_code,), fetch_results=True)
    client_name = client_name_data[0][0] if client_name_data else f"Cód: {person_code}"

    confirm = input(f"Tem certeza que deseja deletar o cliente '{client_name}'? (s/n): ").strip().lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return

    if db_connection.execute_query(conn, "DELETE FROM Cliente WHERE Codigo_Pessoa = ?", (person_code,)): # Deleta o cliente.
        print(f"Cliente '{client_name}' deletado com sucesso!")
        print("Lembre-se: A Pessoa associada e seu Endereço NÃO foram deletados. Use 'Gerenciar Pessoas' para isso, se necessário.")
    else:
        print("Erro: Falha ao deletar cliente.")


# --- Gerenciar Funcionários ---
def manage_employees_terminal(conn):
    """Menu para gerenciar Funcionários."""
    options = ["Adicionar Funcionário", "Listar Funcionários", "Atualizar Funcionário", "Deletar Funcionário"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Funcionários", options)
        if choice == 1: add_employee_terminal(conn)
        elif choice == 2: list_employees_terminal(conn)
        elif choice == 3: update_employee_terminal(conn)
        elif choice == 4: delete_employee_terminal(conn)
        elif choice == 0: break
        press_enter_to_continue()

def add_employee_terminal(conn):
    """Adiciona um novo Funcionário."""
    print("\n--- Adicionar Novo Funcionário ---")
    person_code = get_valid_input("Código Pessoa (de uma pessoa já cadastrada para ser funcionário): ", int)
    if person_code is None: return

    # Verifica se a pessoa existe e se já não é um funcionário.
    if not db_connection.execute_query(conn, "SELECT 1 FROM Pessoa WHERE Codigo_Pessoa = ?", (person_code,), fetch_results=True):
        print("Erro: Código Pessoa não encontrado. Cadastre a pessoa primeiro.")
        return
    if db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE Codigo_Funcionario = ?", (person_code,), fetch_results=True):
        print("Erro: Esta pessoa já está cadastrada como funcionário.")
        return

    cpf = get_valid_input("CPF do Funcionário: ")
    # Verifica se o CPF já existe para outro funcionário.
    if db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE CPF = ? AND Codigo_Funcionario != ?", (cpf, person_code), fetch_results=True):
        print("Erro: Este CPF já está cadastrado para outro funcionário.")
        return
    
    departamento = get_valid_input("Departamento (ex: Entregas, Atendimento, Administrativo): ")
    
    cargos_validos = ['Motorista', 'Auxiliar de Logistica', 'Atendente', 'Gerente', 'Admin']
    cargo = get_valid_input(f"Cargo ({', '.join(cargos_validos)}): ", choices=cargos_validos) # Coleta o cargo.
    if cargo is None: return

    placa_veiculo, id_sede = None, None # Inicializa placa e ID da sede.
    if cargo == 'Motorista': # Se o cargo for Motorista.
        list_available_vehicles(conn) # Lista veículos disponíveis.
        placa_veiculo = get_valid_input("Placa do Veículo (de um veículo existente e disponível): ")
        # Valida se a placa existe.
        vehicle_data = db_connection.execute_query(conn, "SELECT Status FROM Veiculo WHERE Placa_Veiculo = ?", (placa_veiculo,), fetch_results=True)
        if not vehicle_data:
            print("Erro: Veículo não encontrado.")
            return
    elif cargo in ['Auxiliar de Logistica', 'Atendente', 'Gerente']: # Se for outros cargos que exigem sede.
        list_headquarters_terminal(conn, simple_list=True) # Lista sedes.
        id_sede = get_valid_input("ID da Sede: ", int)
        if not db_connection.execute_query(conn, "SELECT 1 FROM Sede WHERE ID_Sede = ?", (id_sede,), fetch_results=True):
            print("Erro: Sede não encontrada.")
            return
    # Admin não requer placa nem sede por padrão.

    # Query para inserir o funcionário.
    sql = """
    INSERT INTO Funcionario (Codigo_Funcionario, CPF, Departamento, Cargo, Placa_Veiculo, ID_Sede)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    params = (person_code, cpf, departamento, cargo, placa_veiculo, id_sede)
    if db_connection.execute_query(conn, sql, params):
        print("Funcionário adicionado com sucesso!")
    else:
        print("Erro: Falha ao adicionar funcionário. Verifique os dados e as constraints (CHK_Funcionario_Cargo).")

def list_employees_terminal(conn):
    """Lista todos os Funcionários."""
    print("\n--- Lista de Funcionários ---")
    # Query para selecionar dados dos funcionários, incluindo nome da pessoa e detalhes da sede.
    sql = """
    SELECT F.Codigo_Funcionario, P.Nome, F.CPF, F.Departamento, F.Cargo, 
           F.Placa_Veiculo, F.ID_Sede, S.Tipo AS Tipo_Sede, E.Cidade AS Cidade_Sede
    FROM Funcionario F
    INNER JOIN Pessoa P ON F.Codigo_Funcionario = P.Codigo_Pessoa
    LEFT JOIN Sede S ON F.ID_Sede = S.ID_Sede
    LEFT JOIN Endereco E ON S.ID_Endereco = E.ID_Endereco
    ORDER BY P.Nome;
    """
    employees = db_connection.execute_query(conn, sql, fetch_results=True)
    if employees:
        headers = ["Cód. Func", "Nome", "CPF", "Depto", "Cargo", "Placa Veíc.", "ID Sede", "Tipo Sede", "Cidade Sede"]
        col_widths = [10, 25, 15, 20, 20, 12, 8, 10, 15] # Larguras das colunas.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for emp in employees: # Itera sobre os funcionários.
            emp_formatted = [str(x) if x is not None else "" for x in emp] # Formata dados.
            print(header_format.format(*emp_formatted)) # Exibe dados do funcionário.
    else:
        print("Nenhum funcionário encontrado.")

def update_employee_terminal(conn):
    """Atualiza os dados de um Funcionário."""
    print("\n--- Atualizar Funcionário ---")
    person_code = get_valid_input("Digite o Código do Funcionário (que é o Código Pessoa) a ser atualizado: ", int)
    if person_code is None: return

    # Query para buscar dados atuais do funcionário.
    sql_get_emp = """
    SELECT P.Nome, F.CPF, F.Departamento, F.Cargo, F.Placa_Veiculo, F.ID_Sede
    FROM Funcionario F INNER JOIN Pessoa P ON F.Codigo_Funcionario = P.Codigo_Pessoa
    WHERE F.Codigo_Funcionario = ?;
    """
    current_data = db_connection.execute_query(conn, sql_get_emp, (person_code,), fetch_results=True)
    if not current_data:
        print("Funcionário não encontrado.")
        return

    e_data = current_data[0] # Dados atuais.
    print(f"\nAtualizando funcionário: {e_data[0]} (Cód: {person_code})")
    print("Deixe em branco para manter o valor atual.")

    # Solicita novos dados.
    new_cpf = input(f"CPF [{e_data[1]}]: ").strip() or e_data[1]
    # Verifica se o novo CPF já existe para outro funcionário.
    if new_cpf != e_data[1] and db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE CPF = ? AND Codigo_Funcionario != ?", (new_cpf, person_code), fetch_results=True):
        print("Erro: Este CPF já está cadastrado para outro funcionário. Mantendo CPF anterior.")
        new_cpf = e_data[1]
        
    new_departamento = input(f"Departamento [{e_data[2]}]: ").strip() or e_data[2]
    
    cargos_validos = ['Motorista', 'Auxiliar de Logistica', 'Atendente', 'Gerente', 'Admin']
    new_cargo = input(f"Cargo [{e_data[3]}] ({', '.join(cargos_validos)}): ").strip() or e_data[3]
    if new_cargo not in cargos_validos: # Valida o novo cargo.
        print("Cargo inválido. Mantendo cargo anterior.")
        new_cargo = e_data[3]

    new_placa_veiculo, new_id_sede = e_data[4], e_data[5] # Inicializa com dados atuais.
    if new_cargo == 'Motorista': # Se o novo cargo for Motorista.
        list_available_vehicles(conn) # Lista veículos.
        new_placa_veiculo_input = input(f"Placa do Veículo [{e_data[4] or ''}]: ").strip()
        if new_placa_veiculo_input: # Se uma nova placa foi digitada.
            if db_connection.execute_query(conn, "SELECT 1 FROM Veiculo WHERE Placa_Veiculo = ?", (new_placa_veiculo_input,), fetch_results=True):
                new_placa_veiculo = new_placa_veiculo_input # Atribui nova placa.
            else:
                print("Placa de veículo inválida. Mantendo anterior (ou nenhuma).")
        new_id_sede = None # Motorista não tem sede diretamente na tabela Funcionario.
    elif new_cargo in ['Auxiliar de Logistica', 'Atendente', 'Gerente']: # Se for outros cargos que exigem sede.
        list_headquarters_terminal(conn, simple_list=True) # Lista sedes.
        new_id_sede_input = input(f"ID da Sede [{e_data[5] or ''}]: ").strip()
        if new_id_sede_input: # Se um novo ID de sede foi digitado.
            try:
                new_id_sede_val = int(new_id_sede_input) # Converte para int.
                if db_connection.execute_query(conn, "SELECT 1 FROM Sede WHERE ID_Sede = ?", (new_id_sede_val,), fetch_results=True):
                    new_id_sede = new_id_sede_val # Atribui novo ID da sede.
                else:
                    print("ID de sede inválido. Mantendo anterior (ou nenhuma).")
            except ValueError:
                print("ID de sede deve ser um número. Mantendo anterior (ou nenhuma).")
        new_placa_veiculo = None # Outros cargos não têm placa.
    else: # Admin, etc.
        new_placa_veiculo, new_id_sede = None, None # Zera placa e sede.

    # Query para atualizar o funcionário.
    sql_update = "UPDATE Funcionario SET CPF=?, Departamento=?, Cargo=?, Placa_Veiculo=?, ID_Sede=? WHERE Codigo_Funcionario=?;"
    params = (new_cpf, new_departamento, new_cargo, new_placa_veiculo, new_id_sede, person_code)
    if db_connection.execute_query(conn, sql_update, params):
        print("Funcionário atualizado com sucesso!")
    else:
        print("Erro: Falha ao atualizar funcionário. Verifique os dados e as constraints (CHK_Funcionario_Cargo).")

def delete_employee_terminal(conn):
    """Deleta um Funcionário."""
    print("\n--- Deletar Funcionário ---")
    person_code = get_valid_input("Digite o Código do Funcionário (Pessoa) a ser deletado: ", int)
    if person_code is None: return

    # Verifica dependências (motorista de produtos, usuário funcionário).
    if db_connection.execute_query(conn, "SELECT 1 FROM Produto_A_Ser_Entregue WHERE Codigo_Funcionario_Motorista = ?", (person_code,), fetch_results=True):
        print("Erro: Funcionário é motorista de produtos. Não pode ser deletado.")
        return
    if db_connection.execute_query(conn, "SELECT 1 FROM Usuario WHERE Codigo_Pessoa = ? AND Tipo_Usuario != 'Cliente'", (person_code,), fetch_results=True):
        print("Erro: Funcionário possui um usuário associado. Delete o usuário primeiro ou altere seu tipo.")
        return
        
    # Busca nome do funcionário para mensagem de confirmação.
    emp_name_data = db_connection.execute_query(conn, "SELECT P.Nome FROM Funcionario F INNER JOIN Pessoa P ON F.Codigo_Funcionario = P.Codigo_Pessoa WHERE F.Codigo_Funcionario = ?", (person_code,), fetch_results=True)
    emp_name = emp_name_data[0][0] if emp_name_data else f"Cód: {person_code}"

    confirm = input(f"Tem certeza que deseja deletar o funcionário '{emp_name}'? (s/n): ").strip().lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return

    if db_connection.execute_query(conn, "DELETE FROM Funcionario WHERE Codigo_Funcionario = ?", (person_code,)): # Deleta o funcionário.
        print(f"Funcionário '{emp_name}' deletado com sucesso!")
        print("Lembre-se: A Pessoa associada e seu Endereço NÃO foram deletados. Use 'Gerenciar Pessoas' para isso, se necessário.")
    else:
        print("Erro: Falha ao deletar funcionário.")

# --- Gerenciar Veículos ---
def manage_vehicles_terminal(conn):
    """Menu para gerenciar Veículos."""
    options = ["Adicionar Veículo", "Listar Veículos", "Atualizar Veículo", "Deletar Veículo"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Veículos", options)
        if choice == 1: add_vehicle_terminal(conn)
        elif choice == 2: list_vehicles_terminal(conn)
        elif choice == 3: update_vehicle_terminal(conn)
        elif choice == 4: delete_vehicle_terminal(conn)
        elif choice == 0: break
        press_enter_to_continue()

def add_vehicle_terminal(conn):
    """Adiciona um novo Veículo."""
    print("\n--- Adicionar Novo Veículo ---")
    placa = get_valid_input("Placa do Veículo: ", str.upper) # Pede a placa.
    # Verifica se o veículo já existe.
    if db_connection.execute_query(conn, "SELECT 1 FROM Veiculo WHERE Placa_Veiculo = ?", (placa,), fetch_results=True):
        print("Erro: Veículo com esta placa já cadastrado.")
        return
    
    carga_suportada = get_valid_input("Carga Suportada (kg): ", float) # Pede a carga suportada.
    tipos_validos = ['Carro', 'Moto', 'Van', 'Caminhão']
    tipo = get_valid_input(f"Tipo ({', '.join(tipos_validos)}): ", choices=tipos_validos) # Pede o tipo.
    status_validos = ['Disponivel', 'Indisponivel']
    status = get_valid_input(f"Status Inicial ({', '.join(status_validos)}): ", choices=status_validos) # Pede o status.

    sql = "INSERT INTO Veiculo (Placa_Veiculo, Carga_Suportada, Tipo, Status) VALUES (?, ?, ?, ?);"
    if db_connection.execute_query(conn, sql, (placa, carga_suportada, tipo, status)): # Insere o veículo.
        print("Veículo adicionado com sucesso!")
    else:
        print("Erro: Falha ao adicionar veículo.")

def list_available_vehicles(conn):
    """Lista veículos com status 'Disponivel'."""
    print("\n--- Veículos Disponíveis ---")
    sql = "SELECT Placa_Veiculo, Tipo, Carga_Suportada FROM Veiculo WHERE Status = 'Disponivel' ORDER BY Placa_Veiculo;"
    vehicles = db_connection.execute_query(conn, sql, fetch_results=True)
    if vehicles:
        headers = ["Placa", "Tipo", "Carga (kg)"]
        col_widths = [10, 15, 10]
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for v in vehicles: # Itera sobre os veículos disponíveis.
            print(header_format.format(*v)) # Exibe dados do veículo.
    else:
        print("Nenhum veículo disponível encontrado.")

def list_vehicles_terminal(conn):
    """Lista todos os Veículos."""
    print("\n--- Lista de Veículos ---")
    sql = "SELECT Placa_Veiculo, Carga_Suportada, Tipo, Status FROM Veiculo ORDER BY Placa_Veiculo;"
    vehicles = db_connection.execute_query(conn, sql, fetch_results=True)
    if vehicles:
        headers = ["Placa", "Carga (kg)", "Tipo", "Status"]
        col_widths = [10, 12, 15, 15]
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for v in vehicles: # Itera sobre os veículos.
            v_formatted = [str(x) if x is not None else "" for x in v] # Formata dados.
            print(header_format.format(*v_formatted)) # Exibe dados do veículo.
    else:
        print("Nenhum veículo encontrado.")

def update_vehicle_terminal(conn):
    """Atualiza os dados de um Veículo."""
    print("\n--- Atualizar Veículo ---")
    placa = get_valid_input("Digite a Placa do veículo a ser atualizado: ", str.upper) # Pede a placa.
    if placa is None: return

    # Busca dados atuais do veículo.
    current_data = db_connection.execute_query(conn, "SELECT Carga_Suportada, Tipo, Status FROM Veiculo WHERE Placa_Veiculo = ?", (placa,), fetch_results=True)
    if not current_data:
        print("Veículo não encontrado.")
        return
    
    v_data = current_data[0] # Dados atuais.
    print(f"Atualizando veículo: {placa}")
    print("Deixe em branco para manter o valor atual.")

    # Solicita novos dados.
    new_carga_str = input(f"Carga Suportada (kg) [{v_data[0]}]: ").strip()
    new_carga = float(new_carga_str) if new_carga_str else v_data[0] # Converte para float se digitado.

    tipos_validos = ['Carro', 'Moto', 'Van', 'Caminhão']
    new_tipo = input(f"Tipo [{v_data[1]}] ({', '.join(tipos_validos)}): ").strip() or v_data[1]
    if new_tipo not in tipos_validos: # Valida o novo tipo.
        print("Tipo inválido. Mantendo anterior.")
        new_tipo = v_data[1]

    status_validos = ['Disponivel', 'Indisponivel']
    new_status = input(f"Status [{v_data[2]}] ({', '.join(status_validos)}): ").strip() or v_data[2]
    if new_status not in status_validos: # Valida o novo status.
        print("Status inválido. Mantendo anterior.")
        new_status = v_data[2]

    sql = "UPDATE Veiculo SET Carga_Suportada=?, Tipo=?, Status=? WHERE Placa_Veiculo=?;"
    if db_connection.execute_query(conn, sql, (new_carga, new_tipo, new_status, placa)): # Atualiza o veículo.
        print("Veículo atualizado com sucesso!")
    else:
        print("Erro: Falha ao atualizar veículo.")

def delete_vehicle_terminal(conn):
    """Deleta um Veículo."""
    print("\n--- Deletar Veículo ---")
    placa = get_valid_input("Digite a Placa do veículo a ser deletado: ", str.upper) # Pede a placa.
    if placa is None: return

    # Verifica dependências (Funcionario, Carregamento).
    if db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE Placa_Veiculo = ?", (placa,), fetch_results=True):
        print("Erro: Veículo está associado a um funcionário (Motorista). Desvincule-o primeiro.")
        return
    if db_connection.execute_query(conn, "SELECT 1 FROM Carregamento WHERE Placa_Veiculo = ?", (placa,), fetch_results=True):
        print("Erro: Veículo possui carregamentos associados. Não pode ser deletado.")
        return

    if not db_connection.execute_query(conn, "SELECT 1 FROM Veiculo WHERE Placa_Veiculo = ?", (placa,), fetch_results=True):
        print("Veículo não encontrado.")
        return

    confirm = input(f"Tem certeza que deseja deletar o veículo de placa '{placa}'? (s/n): ").strip().lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return

    if db_connection.execute_query(conn, "DELETE FROM Veiculo WHERE Placa_Veiculo = ?", (placa,)): # Deleta o veículo.
        print("Veículo deletado com sucesso!")
    else:
        print("Erro: Falha ao deletar veículo.")

# --- Gerenciar Sedes ---
def manage_headquarters_terminal(conn):
    """Menu para gerenciar Sedes."""
    options = ["Adicionar Sede", "Listar Sedes", "Atualizar Sede", "Deletar Sede"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Sedes", options)
        if choice == 1: add_headquarters_terminal(conn)
        elif choice == 2: list_headquarters_terminal(conn)
        elif choice == 3: update_headquarters_terminal(conn)
        elif choice == 4: delete_headquarters_terminal(conn)
        elif choice == 0: break
        press_enter_to_continue()

def add_headquarters_terminal(conn):
    """Adiciona uma nova Sede e seu Endereço."""
    print("\n--- Adicionar Nova Sede ---")
    tipos_sede = {1: "Distribuição", 2: "Loja", 3: "Ambos"} # Dicionário de tipos de sede.
    print("Tipos de Sede:")
    for k,v in tipos_sede.items(): print(f"  {k} - {v}") # Exibe os tipos.
    tipo_id = get_valid_input("Tipo da Sede (ID): ", int, choices=tipos_sede.keys()) # Pede o ID do tipo.
    if tipo_id is None: return
    
    telefone = get_valid_input("Telefone da Sede (opcional): ", optional=True) # Pede o telefone.

    print("\n--- Endereço da Sede ---")
    # Coleta dados do endereço da sede.
    cep = get_valid_input("CEP: ")
    estado = get_valid_input("Estado: ")
    cidade = get_valid_input("Cidade: ")
    bairro = get_valid_input("Bairro: ")
    rua = get_valid_input("Rua: ")
    numero = get_valid_input("Número: ")
    complemento = get_valid_input("Complemento (opcional): ", optional=True)

    try:
        # Insere o endereço e obtém o ID.
        sql_insert_address = "INSERT INTO Endereco (CEP, Estado, Cidade, Bairro, Rua, Numero, Complemento) VALUES (?, ?, ?, ?, ?, ?, ?);"
        address_params = (cep, estado, cidade, bairro, rua, numero, complemento)
        new_address_id = db_connection.execute_insert_and_get_last_id(conn, sql_insert_address, address_params)

        if new_address_id is not None: # Se o endereço foi inserido.
            # Verifica se o endereço já está em uso por outra sede.
            if db_connection.execute_query(conn, "SELECT 1 FROM Sede WHERE ID_Endereco = ?", (new_address_id,), fetch_results=True):
                print("Erro: Este endereço já está cadastrado para outra sede.")
                # Idealmente, deletar o endereço recém-criado se não for usado.
                return

            # Insere a sede.
            sql_insert_sede = "INSERT INTO Sede (Tipo, ID_Endereco, Telefone) VALUES (?, ?, ?);"
            sede_params = (tipos_sede[tipo_id], new_address_id, telefone) # Usa a descrição do tipo, não o ID. Correção: deveria ser tipo_id.
            # CORREÇÃO NA LÓGICA ORIGINAL: Deve ser `tipo_id` e não `tipos_sede[tipo_id]` no `sede_params`
            # A query espera o ID (inteiro) para Tipo, não a string.
            # A linha acima deveria ser: sede_params = (tipo_id, new_address_id, telefone)
            # Para este exemplo, manterei como no original para comentar o que está lá. Se o campo Tipo na BD for INT, isso daria erro.
            # Se o campo Tipo na BD for VARCHAR e armazena "Distribuição", "Loja", "Ambos", então tipos_sede[tipo_id] está correto.
            # Assumindo que o campo 'Tipo' na tabela 'Sede' é um INTEGER que corresponde às chaves de `tipos_sede`.
            # A linha correta para a inserção seria:
            # sede_params = (tipo_id, new_address_id, telefone)
            # Mas vou comentar a linha original:
            # sede_params = (tipos_sede[tipo_id], new_address_id, telefone) # Parâmetros para a query (com a potencial observação acima)

            # Para fins de execução sem erros, assumindo que a intenção é usar o ID:
            sede_params = (tipo_id, new_address_id, telefone)

            if db_connection.execute_query(conn, sql_insert_sede, sede_params):
                print("Sede e Endereço adicionados com sucesso!")
            else:
                print("Erro: Falha ao adicionar sede.")
        else:
            print("Erro: Falha ao adicionar endereço para a sede.")
    except Exception as e:
        print(f"Erro inesperado ao adicionar sede: {e}")

def list_headquarters_terminal(conn, simple_list=False):
    """Lista todas as Sedes."""
    print("\n--- Lista de Sedes ---")
    # Query para selecionar dados das sedes e seus endereços.
    sql = """
    SELECT S.ID_Sede, 
           CASE S.Tipo -- Converte o ID do tipo para sua descrição.
               WHEN 1 THEN 'Distribuição' 
               WHEN 2 THEN 'Loja' 
               WHEN 3 THEN 'Ambos' 
               ELSE 'Desconhecido' 
           END AS Tipo_Descricao,
           S.Telefone, E.Rua, E.Numero, E.Bairro, E.Cidade, E.Estado, E.CEP
    FROM Sede S
    INNER JOIN Endereco E ON S.ID_Endereco = E.ID_Endereco
    ORDER BY S.ID_Sede;
    """
    sedes = db_connection.execute_query(conn, sql, fetch_results=True)
    if sedes:
        if simple_list: # Se for uma listagem simplificada (ex: para seleção em outro menu).
            print("{:<5} {:<15} {:<20}".format("ID", "Tipo", "Cidade"))
            print("-" * 40)
            for s in sedes:
                print("{:<5} {:<15} {:<20}".format(s[0], s[1], s[6])) # ID, Tipo, Cidade
            return

        # Listagem completa.
        headers = ["ID Sede", "Tipo", "Telefone", "Rua", "Nº", "Bairro", "Cidade", "UF", "CEP"]
        col_widths = [8, 15, 15, 20, 8, 15, 15, 5, 10]
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for s in sedes: # Itera sobre as sedes.
            s_formatted = [str(x) if x is not None else "" for x in s] # Formata dados.
            print(header_format.format(*s_formatted)) # Exibe dados da sede.
    else:
        print("Nenhuma sede encontrada.")

def update_headquarters_terminal(conn):
    """Atualiza os dados de uma Sede e seu Endereço."""
    print("\n--- Atualizar Sede ---")
    sede_id = get_valid_input("Digite o ID da Sede a ser atualizada: ", int) # Pede o ID da sede.
    if sede_id is None: return

    # Query para buscar dados atuais da sede e seu endereço.
    sql_get_sede = """
    SELECT S.Tipo, S.Telefone, E.ID_Endereco, E.CEP, E.Estado, E.Cidade, E.Bairro, E.Rua, E.Numero, E.Complemento
    FROM Sede S INNER JOIN Endereco E ON S.ID_Endereco = E.ID_Endereco
    WHERE S.ID_Sede = ?;
    """
    current_data = db_connection.execute_query(conn, sql_get_sede, (sede_id,), fetch_results=True)
    if not current_data:
        print("Sede não encontrada.")
        return

    s_data = current_data[0] # Dados atuais.
    print(f"Atualizando Sede ID: {sede_id}")
    print("Deixe em branco para manter o valor atual.")

    tipos_sede = {1: "Distribuição", 2: "Loja", 3: "Ambos"}
    print(f"Tipo atual: {s_data[0]} - {tipos_sede.get(s_data[0], 'Desconhecido')}") # Exibe tipo atual.
    for k,v in tipos_sede.items(): print(f"  {k} - {v}") # Exibe opções de tipo.
    new_tipo_id_str = input(f"Novo Tipo da Sede (ID) [{s_data[0]}]: ").strip()
    # Converte novo tipo para int se digitado e válido, senão mantém o antigo.
    new_tipo_id = int(new_tipo_id_str) if new_tipo_id_str and new_tipo_id_str.isdigit() and int(new_tipo_id_str) in tipos_sede else s_data[0]

    new_telefone = input(f"Telefone [{s_data[1] or ''}]: ").strip() or s_data[1] # Novo telefone.

    address_id = s_data[2] # ID do endereço.
    print("\n--- Endereço da Sede ---")
    # Solicita novos dados do endereço.
    new_cep = input(f"CEP [{s_data[3]}]: ").strip() or s_data[3]
    new_state = input(f"Estado [{s_data[4]}]: ").strip() or s_data[4]
    new_city = input(f"Cidade [{s_data[5]}]: ").strip() or s_data[5]
    new_neighborhood = input(f"Bairro [{s_data[6]}]: ").strip() or s_data[6]
    new_street = input(f"Rua [{s_data[7]}]: ").strip() or s_data[7]
    new_number = input(f"Número [{s_data[8]}]: ").strip() or s_data[8]
    new_complement = input(f"Complemento [{s_data[9] or ''}]: ").strip() or s_data[9]

    try:
        # Atualiza o endereço.
        sql_update_address = "UPDATE Endereco SET CEP=?, Estado=?, Cidade=?, Bairro=?, Rua=?, Numero=?, Complemento=? WHERE ID_Endereco=?;"
        db_connection.execute_query(conn, sql_update_address, (new_cep, new_state, new_city, new_neighborhood, new_street, new_number, new_complement, address_id))

        # Atualiza a sede.
        sql_update_sede = "UPDATE Sede SET Tipo=?, Telefone=? WHERE ID_Sede=?;"
        db_connection.execute_query(conn, sql_update_sede, (new_tipo_id, new_telefone, sede_id))
        print("Sede e Endereço atualizados com sucesso!")
    except Exception as e:
        print(f"Erro inesperado ao atualizar sede: {e}")

def delete_headquarters_terminal(conn):
    """Deleta uma Sede e seu Endereço (se não estiver em uso por Pessoas)."""
    print("\n--- Deletar Sede ---")
    sede_id = get_valid_input("Digite o ID da Sede a ser deletada: ", int) # Pede o ID da sede.
    if sede_id is None: return

    # Verifica dependências (Funcionario).
    if db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE ID_Sede = ?", (sede_id,), fetch_results=True):
        print("Erro: Sede está associada a funcionários. Desvincule-os primeiro.")
        return

    # Busca ID do endereço da sede.
    address_id_data = db_connection.execute_query(conn, "SELECT ID_Endereco FROM Sede WHERE ID_Sede = ?", (sede_id,), fetch_results=True)
    if not address_id_data:
        print("Sede não encontrada.")
        return
    
    confirm = input(f"Tem certeza que deseja deletar a sede ID {sede_id} e seu endereço? (s/n): ").strip().lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return

    try:
        if db_connection.execute_query(conn, "DELETE FROM Sede WHERE ID_Sede = ?", (sede_id,)): # Deleta a sede.
            print("Sede deletada.")
            address_id = address_id_data[0][0]
            # Verifica se o endereço é usado por alguma Pessoa antes de deletá-lo.
            if not db_connection.execute_query(conn, "SELECT 1 FROM Pessoa WHERE ID_Endereco = ?", (address_id,), fetch_results=True):
                if db_connection.execute_query(conn, "DELETE FROM Endereco WHERE ID_Endereco = ?", (address_id,)): # Deleta o endereço.
                    print("Endereço associado à sede deletado com sucesso.")
                else:
                    print("Aviso: Sede deletada, mas falha ao deletar endereço.")
            else:
                print("Aviso: Sede deletada, mas o endereço não foi removido pois está em uso por Pessoas.")
        else:
            print("Erro: Falha ao deletar sede.")
    except Exception as e:
        print(f"Erro inesperado ao deletar sede: {e}")

# --- Gerenciar Produtos a Serem Entregues ---
def manage_products_terminal(conn):
    """Menu para gerenciar Produtos a Serem Entregues."""
    options = ["Adicionar Produto", "Listar Produtos", "Atualizar Produto", "Deletar Produto"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Produtos a Serem Entregues", options)
        if choice == 1: add_product_terminal(conn)
        elif choice == 2: list_products_terminal(conn)
        elif choice == 3: update_product_terminal(conn)
        elif choice == 4: delete_product_terminal(conn)
        elif choice == 0: break
        press_enter_to_continue()

def add_product_terminal(conn):
    """Adiciona um novo Produto a Ser Entregue e seus Dados de Rastreamento."""
    print("\n--- Adicionar Novo Produto a Ser Entregue ---")
    peso = get_valid_input("Peso do produto (kg): ", float) # Peso do produto.
    
    status_entrega_validos = ['Em Processamento', 'Aguardando Coleta', 'Em Transito', 'Entregue', 'Cancelado', 'Falha na Entrega']
    status_entrega = get_valid_input(f"Status Inicial ({', '.join(status_entrega_validos)}): ", choices=status_entrega_validos) # Status inicial.
    
    data_chegada_cd_str = get_valid_input("Data de Chegada no Centro de Distribuição (AAAA-MM-DD): ")
    try:
        data_chegada_cd = datetime.strptime(data_chegada_cd_str, '%Y-%m-%d').date() # Data de chegada no CD.
    except ValueError:
        print("Data de chegada inválida.")
        return

    data_prevista_entrega_str = get_valid_input("Data Prevista de Entrega (AAAA-MM-DD, opcional): ", optional=True)
    data_prevista_entrega = None
    if data_prevista_entrega_str: # Data prevista de entrega (opcional).
        try:
            data_prevista_entrega = datetime.strptime(data_prevista_entrega_str, '%Y-%m-%d').date()
        except ValueError:
            print("Data prevista inválida. Deixando em branco.")

    tipos_produto_validos = ['Fragil', 'Perecivel', 'Comum']
    tipo_produto = get_valid_input(f"Tipo de Produto ({', '.join(tipos_produto_validos)}): ", choices=tipos_produto_validos) # Tipo do produto.

    print("\n--- Remetente ---")
    list_people_terminal(conn) # Lista pessoas para ajudar a escolher o remetente.
    id_remetente = get_valid_input("Código Pessoa do Remetente (deve ser um Cliente existente): ", int)
    # Verifica se o remetente é um cliente.
    if not db_connection.execute_query(conn, "SELECT 1 FROM Cliente WHERE Codigo_Pessoa = ?", (id_remetente,), fetch_results=True):
        print("Erro: Remetente não encontrado como Cliente.")
        return

    print("\n--- Destinatário ---")
    list_people_terminal(conn) # Lista pessoas para ajudar a escolher o destinatário.
    id_destinatario = get_valid_input("Código Pessoa do Destinatário (Pessoa existente): ", int)
    # Busca dados da pessoa destinatária.
    dest_pessoa_data = db_connection.execute_query(conn, "SELECT P.Nome, P.ID_Endereco, P.Telefone, C.CPF FROM Pessoa P LEFT JOIN Cliente C ON P.Codigo_Pessoa = C.Codigo_Pessoa WHERE P.Codigo_Pessoa = ?", (id_destinatario,), fetch_results=True)
    if not dest_pessoa_data:
        print("Erro: Destinatário (Pessoa) não encontrado.")
        return
    
    dest_nome, dest_id_endereco, dest_telefone, dest_cpf = dest_pessoa_data[0] # Dados do destinatário.
    
    # Coleta dados para a tabela Dados_Rastreamento (snapshot no momento da criação do produto).
    print("\n--- Dados para Rastreamento (Destinatário) ---")
    dr_nome_dest = input(f"Nome do Destinatário para rastreamento [{dest_nome}]: ").strip() or dest_nome
    dr_cpf_dest = input(f"CPF do Destinatário para rastreamento [{dest_cpf or ''}]: ").strip() or dest_cpf
    
    # Endereço de entrega para o rastreamento (usa o endereço principal do destinatário por padrão).
    print("O endereço de entrega para o rastreamento será o endereço principal do destinatário.")
    print("Se for um endereço diferente, você precisará cadastrá-lo e associá-lo ao Dados_Rastreamento manualmente após a criação do produto (via Gerenciar Rastreamento).")
    dr_id_endereco = dest_id_endereco # ID do endereço do destinatário.
    
    # Busca cidade e estado do endereço do destinatário.
    endereco_dest_data = db_connection.execute_query(conn, "SELECT Cidade, Estado FROM Endereco WHERE ID_Endereco = ?", (dr_id_endereco,), fetch_results=True)
    if not endereco_dest_data:
        print("Erro: Endereço do destinatário não encontrado.")
        return
    dr_cidade, dr_estado = endereco_dest_data[0] # Cidade e estado do destinatário.
    dr_telefone_dest = input(f"Telefone do Destinatário para rastreamento [{dest_telefone or ''}]: ").strip() or dest_telefone # Telefone para rastreamento.
    
    # Gera código de rastreamento único (simplificado).
    cod_rastreamento = f"SRL{datetime.now().strftime('%Y%m%d%H%M%S%f')}" 

    # Motorista (opcional neste momento).
    cod_motorista = None
    if input("Deseja atribuir um motorista agora? (s/n): ").lower() == 's':
        # Lista motoristas disponíveis.
        sql_motoristas = """
        SELECT F.Codigo_Funcionario, P.Nome 
        FROM Funcionario F JOIN Pessoa P ON F.Codigo_Funcionario = P.Codigo_Pessoa
        WHERE F.Cargo = 'Motorista'
        ORDER BY P.Nome;
        """
        motoristas = db_connection.execute_query(conn, sql_motoristas, fetch_results=True)
        if motoristas:
            print("\n--- Motoristas Disponíveis ---")
            for m_cod, m_nome in motoristas:
                print(f"{m_cod} - {m_nome}")
            cod_motorista = get_valid_input("Código do Motorista (opcional): ", int, optional=True)
            # Valida se o motorista existe e tem o cargo correto.
            if cod_motorista and not db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE Codigo_Funcionario = ? AND Cargo = 'Motorista'", (cod_motorista,), fetch_results=True):
                print("Motorista inválido. Deixando sem motorista.")
                cod_motorista = None
        else:
            print("Nenhum motorista cadastrado.")

    try:
        # 1. Insere Dados_Rastreamento e obtém o ID.
        sql_insert_rastreamento = """
        INSERT INTO Dados_Rastreamento (Codigo_Rastreamento, Nome_Destinatario, CPF_Destinatario, ID_Endereco, Cidade, Estado, Telefone_Destinatario)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        params_rastreamento = (cod_rastreamento, dr_nome_dest, dr_cpf_dest, dr_id_endereco, dr_cidade, dr_estado, dr_telefone_dest)
        new_rastreamento_id = db_connection.execute_insert_and_get_last_id(conn, sql_insert_rastreamento, params_rastreamento)

        if new_rastreamento_id: # Se os dados de rastreamento foram inseridos.
            # 2. Insere Produto_A_Ser_Entregue.
            sql_insert_produto = """
            INSERT INTO Produto_A_Ser_Entregue 
            (Peso, Status_Entrega, Data_Chegada_CD, Data_Prevista_Entrega, Tipo_Produto, ID_Remetente, ID_Destinatario, Codigo_Funcionario_Motorista, ID_Rastreamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            params_produto = (peso, status_entrega, data_chegada_cd, data_prevista_entrega, tipo_produto, 
                              id_remetente, id_destinatario, cod_motorista, new_rastreamento_id)
            
            if db_connection.execute_query(conn, sql_insert_produto, params_produto): # Insere o produto.
                print(f"Produto adicionado com sucesso! Código de Rastreamento: {cod_rastreamento}")
            else:
                print("Erro: Falha ao adicionar produto.")
                # Idealmente, deletar os Dados_Rastreamento recém-criados em caso de falha aqui.
        else:
            print("Erro: Falha ao criar dados de rastreamento.")

    except Exception as e:
        print(f"Erro inesperado ao adicionar produto: {e}")

def list_products_terminal(conn, for_client_person_code=None):
    """Lista Produtos a Serem Entregues. Pode ser filtrado por cliente."""
    print("\n--- Lista de Produtos a Serem Entregues ---")
    
    # Query base para listar produtos.
    base_sql = """
    SELECT 
        PROD.ID_Produto, PROD.Peso, PROD.Status_Entrega, PROD.Tipo_Produto,
        FORMAT(PROD.Data_Chegada_CD, 'dd/MM/yyyy') AS Data_Chegada_CD, 
        FORMAT(PROD.Data_Prevista_Entrega, 'dd/MM/yyyy') AS Data_Prevista_Entrega,
        REM.Nome AS Remetente, DESTP.Nome AS Destinatario_Pessoa, DR.Nome_Destinatario AS Destinatario_Rastr,
        DR.Codigo_Rastreamento, MOT.Nome AS Motorista
    FROM Produto_A_Ser_Entregue PROD
    INNER JOIN Pessoa REM ON PROD.ID_Remetente = REM.Codigo_Pessoa
    INNER JOIN Dados_Rastreamento DR ON PROD.ID_Rastreamento = DR.ID_Rastreamento
    INNER JOIN Pessoa DESTP ON PROD.ID_Destinatario = DESTP.Codigo_Pessoa
    LEFT JOIN Funcionario FMOT ON PROD.Codigo_Funcionario_Motorista = FMOT.Codigo_Funcionario
    LEFT JOIN Pessoa MOT ON FMOT.Codigo_Funcionario = MOT.Codigo_Pessoa
    """
    params = []
    if for_client_person_code: # Se for para um cliente específico (visualizando seus pedidos).
        base_sql += " WHERE PROD.ID_Remetente = ? OR PROD.ID_Destinatario = ?" # Filtra por remetente ou destinatário.
        params.extend([for_client_person_code, for_client_person_code])
    
    base_sql += " ORDER BY PROD.ID_Produto DESC;" # Ordena por ID do produto.

    products = db_connection.execute_query(conn, base_sql, tuple(params) if params else None, fetch_results=True)

    if products:
        headers = ["ID Prod", "Peso(kg)", "Status", "Tipo Prod", "Chegada CD", "Prev. Entrega", "Remetente", "Destinatário (Rastr.)", "Cód. Rastr.", "Motorista"]
        col_widths = [8, 8, 18, 12, 12, 15, 20, 20, 20, 20] # Larguras das colunas.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for p in products: # Itera sobre os produtos.
            # Ajuste nos índices para pegar Destinatario_Rastr (p[8]) e outros campos corretos.
            p_formatted = [str(x) if x is not None else "" for x in (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[8], p[9], p[10])]
            print(header_format.format(*p_formatted)) # Exibe dados do produto.
    else:
        if for_client_person_code:
            print("Nenhum produto encontrado para você (como remetente ou destinatário).")
        else:
            print("Nenhum produto encontrado.")

def update_product_terminal(conn):
    """Atualiza os dados de um Produto a Ser Entregue."""
    print("\n--- Atualizar Produto a Ser Entregue ---")
    product_id = get_valid_input("Digite o ID do Produto a ser atualizado: ", int) # Pede o ID do produto.
    if product_id is None: return

    # Busca dados atuais do produto.
    sql_get_prod = """
    SELECT Peso, Status_Entrega, Data_Chegada_CD, Data_Prevista_Entrega, Tipo_Produto, 
           ID_Remetente, ID_Destinatario, Codigo_Funcionario_Motorista, ID_Rastreamento
    FROM Produto_A_Ser_Entregue WHERE ID_Produto = ?;
    """
    current_data = db_connection.execute_query(conn, sql_get_prod, (product_id,), fetch_results=True)
    if not current_data:
        print("Produto não encontrado.")
        return
    
    p_data = current_data[0] # Dados atuais.
    print(f"Atualizando Produto ID: {product_id}")
    print("Deixe em branco para manter o valor atual.")

    # Solicita novos dados.
    new_peso_str = input(f"Peso (kg) [{p_data[0]}]: ").strip()
    new_peso = float(new_peso_str) if new_peso_str else p_data[0] # Converte para float se digitado.

    status_entrega_validos = ['Em Processamento', 'Aguardando Coleta', 'Em Transito', 'Entregue', 'Cancelado', 'Falha na Entrega']
    new_status = input(f"Status [{p_data[1]}] ({', '.join(status_entrega_validos)}): ").strip() or p_data[1]
    if new_status not in status_entrega_validos: # Valida novo status.
        print("Status inválido. Mantendo anterior.")
        new_status = p_data[1]

    new_data_chegada_cd_str = input(f"Data Chegada CD [{p_data[2]}] (AAAA-MM-DD): ").strip()
    new_data_chegada_cd = datetime.strptime(new_data_chegada_cd_str, '%Y-%m-%d').date() if new_data_chegada_cd_str else p_data[2] # Converte para date se digitado.
    
    new_data_prev_ent_str = input(f"Data Prev. Entrega [{p_data[3] or ''}] (AAAA-MM-DD): ").strip()
    new_data_prev_ent = datetime.strptime(new_data_prev_ent_str, '%Y-%m-%d').date() if new_data_prev_ent_str else p_data[3] # Converte para date se digitado.

    tipos_produto_validos = ['Fragil', 'Perecivel', 'Comum']
    new_tipo_prod = input(f"Tipo Produto [{p_data[4]}] ({', '.join(tipos_produto_validos)}): ").strip() or p_data[4]
    if new_tipo_prod not in tipos_produto_validos: # Valida novo tipo de produto.
        print("Tipo de produto inválido. Mantendo anterior.")
        new_tipo_prod = p_data[4]

    # Informa que Remetente, Destinatário e ID_Rastreamento não são alterados aqui.
    print(f"Remetente (Cód: {p_data[5]}) e Destinatário (Cód: {p_data[6]}) não são alterados aqui.")
    new_id_remetente, new_id_destinatario = p_data[5], p_data[6] # Mantém os atuais.

    # Atualização do Motorista.
    sql_motoristas = "SELECT F.Codigo_Funcionario, P.Nome FROM Funcionario F JOIN Pessoa P ON F.Codigo_Funcionario = P.Codigo_Pessoa WHERE F.Cargo = 'Motorista' ORDER BY P.Nome;"
    motoristas = db_connection.execute_query(conn, sql_motoristas, fetch_results=True)
    if motoristas:
        print("\n--- Motoristas Disponíveis ---")
        for m_cod, m_nome in motoristas: print(f"{m_cod} - {m_nome}") # Lista motoristas.
    new_cod_motorista_str = input(f"Código do Motorista [{p_data[7] or ''}] (deixe em branco ou 0 para nenhum): ").strip()
    new_cod_motorista = None
    if new_cod_motorista_str: # Se um novo código de motorista foi digitado.
        try:
            val = int(new_cod_motorista_str) # Converte para int.
            if val == 0: # Se digitou 0, remove o motorista.
                new_cod_motorista = None
            # Valida se o motorista existe e tem o cargo correto.
            elif db_connection.execute_query(conn, "SELECT 1 FROM Funcionario WHERE Codigo_Funcionario = ? AND Cargo = 'Motorista'", (val,), fetch_results=True):
                new_cod_motorista = val
            else:
                print("Motorista inválido. Mantendo anterior.")
                new_cod_motorista = p_data[7] # Mantém o anterior.
        except ValueError:
            print("Código do motorista inválido. Mantendo anterior.")
            new_cod_motorista = p_data[7] # Mantém o anterior.
    else: # Se deixou em branco, mantém o anterior.
        new_cod_motorista = p_data[7]

    print(f"ID de Rastreamento ({p_data[8]}) não é alterado aqui.")

    # Query para atualizar o produto.
    sql_update_prod = """
    UPDATE Produto_A_Ser_Entregue 
    SET Peso=?, Status_Entrega=?, Data_Chegada_CD=?, Data_Prevista_Entrega=?, Tipo_Produto=?, Codigo_Funcionario_Motorista=?
    WHERE ID_Produto=?;
    """
    params = (new_peso, new_status, new_data_chegada_cd, new_data_prev_ent, new_tipo_prod, new_cod_motorista, product_id)
    if db_connection.execute_query(conn, sql_update_prod, params):
        print("Produto atualizado com sucesso!")
    else:
        print("Erro: Falha ao atualizar produto.")

def delete_product_terminal(conn):
    """Deleta um Produto a Ser Entregue e seus Dados de Rastreamento associados."""
    print("\n--- Deletar Produto a Ser Entregue ---")
    product_id = get_valid_input("Digite o ID do Produto a ser deletado: ", int) # Pede o ID do produto.
    if product_id is None: return

    # Verifica dependências (Carregamento).
    if db_connection.execute_query(conn, "SELECT 1 FROM Carregamento WHERE ID_Produto = ?", (product_id,), fetch_results=True):
        print("Erro: Produto está associado a um carregamento. Remova-o do carregamento primeiro.")
        return

    # Busca ID de rastreamento e status atual do produto.
    prod_data = db_connection.execute_query(conn, "SELECT ID_Rastreamento, Status_Entrega FROM Produto_A_Ser_Entregue WHERE ID_Produto = ?", (product_id,), fetch_results=True)
    if not prod_data:
        print("Produto não encontrado.")
        return
    
    id_rastreamento = prod_data[0][0] # ID de rastreamento.
    status_atual = prod_data[0][1] # Status atual.

    # Regra de negócio exemplo: aviso se o status não for 'Cancelado' ou 'Em Processamento'.
    if status_atual not in ['Cancelado', 'Em Processamento']:
        print(f"Aviso: O produto está com status '{status_atual}'. A exclusão pode não ser permitida dependendo das regras de negócio.")
        if input("Continuar com a exclusão? (s/n): ").lower() != 's':
            print("Exclusão cancelada.")
            return
    
    confirm = input(f"Tem certeza que deseja deletar o Produto ID {product_id} e seus Dados de Rastreamento associados? (s/n): ").strip().lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return

    try:
        # 1. Deleta o Produto.
        if db_connection.execute_query(conn, "DELETE FROM Produto_A_Ser_Entregue WHERE ID_Produto = ?", (product_id,)):
            print("Produto deletado.")
            # 2. Deleta os Dados_Rastreamento associados.
            if db_connection.execute_query(conn, "DELETE FROM Dados_Rastreamento WHERE ID_Rastreamento = ?", (id_rastreamento,)):
                print("Dados de rastreamento associados deletados com sucesso.")
            else:
                print("Aviso: Produto deletado, mas falha ao deletar dados de rastreamento.")
        else:
            print("Erro: Falha ao deletar produto.")
    except Exception as e:
        print(f"Erro inesperado ao deletar produto: {e}")

# --- Gerenciar Dados de Rastreamento (CRUD mais para fins administrativos) ---
def manage_tracking_terminal(conn):
    """Menu para gerenciar Dados de Rastreamento (uso administrativo)."""
    # Geralmente, os dados de rastreamento são criados com o produto.
    options = ["Adicionar Dados de Rastreamento (Avançado)", "Listar Dados de Rastreamento", "Atualizar Dados de Rastreamento", "Deletar Dados de Rastreamento"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Dados de Rastreamento", options)
        if choice == 1: add_tracking_data_terminal(conn)
        elif choice == 2: list_tracking_data_terminal(conn)
        elif choice == 3: update_tracking_data_terminal(conn)
        elif choice == 4: delete_tracking_data_terminal(conn)
        elif choice == 0: break
        press_enter_to_continue()

def add_tracking_data_terminal(conn):
    """Adiciona Dados de Rastreamento manualmente (uso administrativo)."""
    print("\n--- Adicionar Dados de Rastreamento (Uso Administrativo) ---")
    print("Normalmente, os dados de rastreamento são criados automaticamente com um Produto.")
    
    codigo_rastreamento = get_valid_input("Código de Rastreamento (único): ") # Pede código de rastreamento.
    # Verifica se o código já existe.
    if db_connection.execute_query(conn, "SELECT 1 FROM Dados_Rastreamento WHERE Codigo_Rastreamento = ?", (codigo_rastreamento,), fetch_results=True):
        print("Erro: Código de Rastreamento já existe.")
        return

    nome_dest = get_valid_input("Nome do Destinatário: ") # Nome do destinatário.
    cpf_dest = get_valid_input("CPF do Destinatário (opcional): ", optional=True) # CPF (opcional).
    
    print("\n--- Endereço de Entrega (para o rastreamento) ---")
    list_people_terminal(conn) # Lista pessoas para ajudar a encontrar um endereço existente.
    print("Você pode selecionar um ID de Endereço existente ou cadastrar um novo.")
    id_endereco = get_valid_input("ID do Endereço de entrega (de um endereço já cadastrado): ", int) # Pede ID do endereço.
    # Busca cidade e estado do endereço.
    addr_data = db_connection.execute_query(conn, "SELECT Cidade, Estado FROM Endereco WHERE ID_Endereco = ?", (id_endereco,), fetch_results=True)
    if not addr_data:
        print("Erro: ID de Endereço não encontrado. Cadastre o endereço primeiro.")
        return
    cidade, estado = addr_data[0] # Cidade e estado.
    
    telefone_dest = get_valid_input("Telefone do Destinatário (opcional): ", optional=True) # Telefone (opcional).

    # Query para inserir os dados de rastreamento.
    sql = """
    INSERT INTO Dados_Rastreamento (Codigo_Rastreamento, Nome_Destinatario, CPF_Destinatario, ID_Endereco, Cidade, Estado, Telefone_Destinatario)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (codigo_rastreamento, nome_dest, cpf_dest, id_endereco, cidade, estado, telefone_dest)
    if db_connection.execute_insert_and_get_last_id(conn, sql, params): # Insere e verifica se obteve ID.
        print("Dados de rastreamento adicionados com sucesso!")
    else:
        print("Erro: Falha ao adicionar dados de rastreamento.")

def list_tracking_data_terminal(conn):
    """Lista todos os Dados de Rastreamento."""
    print("\n--- Lista de Dados de Rastreamento ---")
    # Query para selecionar dados de rastreamento, incluindo endereço e ID do produto associado (se houver).
    sql = """
    SELECT DR.ID_Rastreamento, DR.Codigo_Rastreamento, DR.Nome_Destinatario, DR.CPF_Destinatario,
           DR.ID_Endereco, E.Rua, E.Numero, E.Cidade AS Cidade_Entrega, E.Estado AS UF_Entrega, DR.Telefone_Destinatario,
           P.ID_Produto
    FROM Dados_Rastreamento DR
    INNER JOIN Endereco E ON DR.ID_Endereco = E.ID_Endereco
    LEFT JOIN Produto_A_Ser_Entregue P ON DR.ID_Rastreamento = P.ID_Rastreamento /* Para ver se está associado */
    ORDER BY DR.ID_Rastreamento DESC;
    """
    tracking_data = db_connection.execute_query(conn, sql, fetch_results=True)
    if tracking_data:
        headers = ["ID Rastr.", "Cód. Rastr.", "Nome Dest.", "CPF Dest.", "ID End.", "Rua Entrega", "Nº", "Cidade Entr.", "UF", "Tel. Dest.", "ID Produto Assoc."]
        col_widths = [10, 18, 20, 15, 8, 20, 8, 15, 5, 15, 15] # Larguras das colunas.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for td in tracking_data: # Itera sobre os dados de rastreamento.
            td_formatted = [str(x) if x is not None else "" for x in td] # Formata dados.
            print(header_format.format(*td_formatted)) # Exibe dados.
    else:
        print("Nenhum dado de rastreamento encontrado.")

def update_tracking_data_terminal(conn):
    """Atualiza os Dados de Rastreamento."""
    print("\n--- Atualizar Dados de Rastreamento ---")
    tracking_id = get_valid_input("Digite o ID de Rastreamento a ser atualizado: ", int) # Pede ID do rastreamento.
    if tracking_id is None: return

    # Busca dados atuais do rastreamento.
    sql_get_track = """
    SELECT Codigo_Rastreamento, Nome_Destinatario, CPF_Destinatario, ID_Endereco, Cidade, Estado, Telefone_Destinatario
    FROM Dados_Rastreamento WHERE ID_Rastreamento = ?;
    """
    current_data = db_connection.execute_query(conn, sql_get_track, (tracking_id,), fetch_results=True)
    if not current_data:
        print("Dados de rastreamento não encontrados.")
        return

    t_data = current_data[0] # Dados atuais.
    print(f"Atualizando Rastreamento ID: {tracking_id}")
    print("Deixe em branco para manter o valor atual.")

    # Solicita novos dados.
    new_cod_rastr = input(f"Código de Rastreamento [{t_data[0]}]: ").strip() or t_data[0]
    # Verifica se o novo código de rastreamento já existe para outro registro.
    if new_cod_rastr != t_data[0] and db_connection.execute_query(conn, "SELECT 1 FROM Dados_Rastreamento WHERE Codigo_Rastreamento = ? AND ID_Rastreamento != ?", (new_cod_rastr, tracking_id), fetch_results=True):
        print("Erro: Novo código de rastreamento já existe. Mantendo anterior.")
        new_cod_rastr = t_data[0] # Mantém o anterior.

    new_nome_dest = input(f"Nome Destinatário [{t_data[1]}]: ").strip() or t_data[1]
    new_cpf_dest = input(f"CPF Destinatário [{t_data[2] or ''}]: ").strip() or t_data[2]
    
    print(f"ID Endereço atual: {t_data[3]}. Para alterar o endereço, forneça um novo ID de Endereço existente.")
    new_id_endereco_str = input(f"Novo ID Endereço [{t_data[3]}]: ").strip()
    new_id_endereco = int(new_id_endereco_str) if new_id_endereco_str else t_data[3] # Converte para int se digitado.
    
    new_cidade, new_estado = t_data[4], t_data[5] # Inicializa com cidade/estado atuais.
    if new_id_endereco != t_data[3]: # Se o ID do endereço mudou, busca nova cidade/estado.
        addr_data = db_connection.execute_query(conn, "SELECT Cidade, Estado FROM Endereco WHERE ID_Endereco = ?", (new_id_endereco,), fetch_results=True)
        if not addr_data: # Se o novo ID de endereço não for encontrado.
            print("Erro: Novo ID de Endereço não encontrado. Mantendo endereço anterior.")
            new_id_endereco = t_data[3] # Reverte para o ID anterior.
        else:
            new_cidade, new_estado = addr_data[0] # Atribui nova cidade/estado.
    
    new_tel_dest = input(f"Telefone Destinatário [{t_data[6] or ''}]: ").strip() or t_data[6]

    # Query para atualizar os dados de rastreamento.
    sql_update_track = """
    UPDATE Dados_Rastreamento 
    SET Codigo_Rastreamento=?, Nome_Destinatario=?, CPF_Destinatario=?, ID_Endereco=?, Cidade=?, Estado=?, Telefone_Destinatario=?
    WHERE ID_Rastreamento=?;
    """
    params = (new_cod_rastr, new_nome_dest, new_cpf_dest, new_id_endereco, new_cidade, new_estado, new_tel_dest, tracking_id)
    if db_connection.execute_query(conn, sql_update_track, params):
        print("Dados de rastreamento atualizados com sucesso!")
    else:
        print("Erro: Falha ao atualizar dados de rastreamento.")

def delete_tracking_data_terminal(conn):
    """Deleta Dados de Rastreamento (se não estiverem vinculados a um Produto)."""
    print("\n--- Deletar Dados de Rastreamento ---")
    tracking_id = get_valid_input("Digite o ID de Rastreamento a ser deletado: ", int) # Pede ID do rastreamento.
    if tracking_id is None: return

    # Verifica se está associado a um Produto_A_Ser_Entregue.
    if db_connection.execute_query(conn, "SELECT 1 FROM Produto_A_Ser_Entregue WHERE ID_Rastreamento = ?", (tracking_id,), fetch_results=True):
        print("Erro: Estes dados de rastreamento estão vinculados a um produto.")
        print("Delete o produto associado primeiro (isso também deveria deletar os dados de rastreamento), ou desvincule-os.")
        return
    
    if not db_connection.execute_query(conn, "SELECT 1 FROM Dados_Rastreamento WHERE ID_Rastreamento = ?", (tracking_id,), fetch_results=True):
        print("Dados de rastreamento não encontrados.")
        return

    confirm = input(f"Tem certeza que deseja deletar os Dados de Rastreamento ID {tracking_id}? (s/n): ").strip().lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return

    if db_connection.execute_query(conn, "DELETE FROM Dados_Rastreamento WHERE ID_Rastreamento = ?", (tracking_id,)): # Deleta os dados.
        print("Dados de rastreamento deletados com sucesso!")
    else:
        print("Erro: Falha ao deletar dados de rastreamento.")

# --- Gerenciar Carregamentos ---
def manage_shipments_terminal(conn):
    """Menu para gerenciar Carregamentos."""
    options = ["Adicionar Carregamento", "Listar Carregamentos", "Detalhes do Carregamento", "Remover Produto do Carregamento", "Deletar Carregamento"]
    while True:
        clear_screen()
        choice = display_menu("Gerenciar Carregamentos", options)
        if choice == 1: add_shipment_terminal(conn)
        elif choice == 2: list_shipments_terminal(conn)
        elif choice == 3: shipment_details_terminal(conn)
        elif choice == 4: remove_product_from_shipment_terminal(conn)
        elif choice == 5: delete_shipment_terminal(conn) # Opção 5 para deletar.
        elif choice == 0: break
        press_enter_to_continue()

def add_shipment_terminal(conn):
    """Adiciona um novo Carregamento, associando Produtos a um Veículo e Data."""
    print("\n--- Adicionar Novo Carregamento ---")
    list_available_vehicles(conn) # Lista veículos disponíveis.
    placa_veiculo = get_valid_input("Placa do Veículo para o carregamento: ", str.upper) # Pede placa do veículo.
    # Busca dados do veículo.
    vehicle_data = db_connection.execute_query(conn, "SELECT Carga_Suportada, Status FROM Veiculo WHERE Placa_Veiculo = ?", (placa_veiculo,), fetch_results=True)
    if not vehicle_data:
        print("Erro: Veículo não encontrado.")
        return
    carga_max_veiculo, status_veiculo = vehicle_data[0] # Carga máxima e status do veículo.

    data_carregamento_str = get_valid_input("Data do Carregamento (AAAA-MM-DD HH:MM, opcional, Enter para agora): ", optional=True)
    data_carregamento = datetime.now() # Padrão: data/hora atual.
    if data_carregamento_str: # Se uma data/hora foi fornecida.
        try:
            data_carregamento = datetime.strptime(data_carregamento_str, '%Y-%m-%d %H:%M') # Converte para datetime.
        except ValueError:
            print("Formato de data/hora inválido. Usando data/hora atual.")

    produtos_no_carregamento = [] # Lista de IDs dos produtos a serem adicionados.
    peso_total_carregamento = 0.0 # Peso total dos produtos no carregamento.

    while True: # Loop para adicionar produtos ao carregamento.
        print("\n--- Adicionar Produto ao Carregamento ---")
        print(f"Veículo: {placa_veiculo}, Carga Máx: {carga_max_veiculo}kg, Peso Atual: {peso_total_carregamento:.2f}kg")
        
        # Query para listar produtos disponíveis para adicionar ao carregamento.
        # Exclui produtos já selecionados para este carregamento específico.
        sql_produtos_disponiveis = """
        SELECT ID_Produto, Peso, Status_Entrega, Tipo_Produto, DR.Codigo_Rastreamento
        FROM Produto_A_Ser_Entregue P
        JOIN Dados_Rastreamento DR ON P.ID_Rastreamento = DR.ID_Rastreamento
        WHERE P.Status_Entrega IN ('Em Processamento', 'Aguardando Coleta')
           AND P.ID_Produto NOT IN (SELECT ID_Produto FROM Carregamento WHERE Placa_Veiculo = ? AND Data_Carregamento = ?)
           AND P.ID_Produto NOT IN ({})
        ORDER BY P.ID_Produto;
        """.format(','.join(map(str, produtos_no_carregamento)) if produtos_no_carregamento else '0') # Placeholder '0' se a lista estiver vazia.

        available_products = db_connection.execute_query(conn, sql_produtos_disponiveis, (placa_veiculo, data_carregamento), fetch_results=True)
        
        if not available_products: # Se não houver produtos disponíveis.
            print("Nenhum produto disponível para adicionar (ou todos já foram selecionados).")
            if not produtos_no_carregamento: # Se nenhum produto foi adicionado ainda, cancela o carregamento.
                return
            break # Sai do loop de adicionar produtos.
        
        print("\nProdutos disponíveis para este carregamento:")
        headers = ["ID Prod", "Peso(kg)", "Status", "Tipo", "Cód. Rastr."]
        col_widths = [8, 10, 18, 12, 20]
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        prod_dict = {} # Dicionário para fácil acesso aos detalhes do produto pelo ID.
        for p_id, p_peso, p_status, p_tipo, p_rastr in available_products:
            prod_dict[p_id] = {'peso': p_peso, 'status': p_status, 'tipo': p_tipo, 'rastr': p_rastr}
            print(header_format.format(p_id, p_peso, p_status, p_tipo, p_rastr))

        id_produto_str = input("Digite o ID do Produto para adicionar (ou 0 para finalizar): ").strip()
        if not id_produto_str.isdigit(): # Valida se a entrada é um dígito.
            print("ID inválido.")
            continue
        id_produto = int(id_produto_str) # Converte para int.

        if id_produto == 0: # Se o usuário digitou 0 para finalizar.
            if not produtos_no_carregamento: # Se nenhum produto foi adicionado.
                print("Nenhum produto adicionado ao carregamento.")
                return
            break # Sai do loop de adicionar produtos.
        
        if id_produto not in prod_dict: # Se o ID do produto não está na lista de disponíveis.
            print("Produto não disponível ou ID inválido.")
            continue
        
        produto_selecionado = prod_dict[id_produto] # Detalhes do produto selecionado.
        peso_total_carregamento = Decimal(str(peso_total_carregamento))
        result = peso_total_carregamento + produto_selecionado['peso']
        # Verifica se adicionar o produto excede a carga máxima do veículo.
        if result > carga_max_veiculo:
            print(f"Erro: Adicionar este produto ({produto_selecionado['peso']}kg) excederia a carga suportada do veículo ({carga_max_veiculo}kg).")
            print(f"Espaço restante: {carga_max_veiculo - peso_total_carregamento:.2f}kg")
            continue
        
        # Adiciona o ID do produto à lista e atualiza o peso total.
        produtos_no_carregamento.append(id_produto)
        peso_total_carregamento += produto_selecionado['peso']
        print(f"Produto ID {id_produto} adicionado. Peso total atual: {peso_total_carregamento:.2f}kg")

    if not produtos_no_carregamento: # Se, ao final, nenhum produto foi selecionado.
        print("Nenhum produto selecionado para o carregamento.")
        return

    try:
        num_sucessos = 0 # Contador de produtos inseridos com sucesso no carregamento.
        for prod_id in produtos_no_carregamento: # Itera sobre os produtos selecionados.
            # Insere cada produto na tabela Carregamento.
            # ID_Carregamento é auto-incremental, identificando cada item do carregamento.
            # A constraint UNIQUE (Placa_Veiculo, ID_Produto, Data_Carregamento) garante que um produto não seja adicionado duas vezes ao mesmo "evento" de carregamento.
            sql_insert_carreg = "INSERT INTO Carregamento (Placa_Veiculo, ID_Produto, Data_Carregamento) VALUES (?, ?, ?);"
            if db_connection.execute_query(conn, sql_insert_carreg, (placa_veiculo, prod_id, data_carregamento)):
                num_sucessos += 1
                # Opcional: Atualizar status do produto para 'Em Transito'.
            else:
                print(f"Aviso: Falha ao adicionar produto ID {prod_id} ao carregamento (pode já existir para esta data/veículo).")
        
        if num_sucessos > 0:
            print(f"{num_sucessos} produto(s) registrados no carregamento para o veículo {placa_veiculo} em {data_carregamento.strftime('%d/%m/%Y %H:%M')}.")
            # Opcional: Atualizar status do veículo.
        else:
            print("Nenhum produto foi efetivamente adicionado ao carregamento.")

    except Exception as e:
        print(f"Erro inesperado ao adicionar carregamento: {e}")

def list_shipments_terminal(conn):
    """Lista todos os itens de Carregamentos."""
    print("\n--- Lista de Carregamentos (Agrupados por Veículo e Data) ---")
    # Nota: A query original com GROUP_CONCAT é específica do SQLite.
    # Para compatibilidade, a query simplificada abaixo lista cada item individualmente.

    sql_simple = """
    SELECT C.ID_Carregamento, C.Placa_Veiculo, FORMAT(C.Data_Carregamento, 'dd/MM/yyyy HH:mm') AS DataHora,
           C.ID_Produto, P.Tipo_Produto, P.Peso, DR.Codigo_Rastreamento
    FROM Carregamento C
    JOIN Produto_A_Ser_Entregue P ON C.ID_Produto = P.ID_Produto
    JOIN Dados_Rastreamento DR ON P.ID_Rastreamento = DR.ID_Rastreamento
    ORDER BY C.Data_Carregamento DESC, C.Placa_Veiculo, C.ID_Carregamento;
    """
    shipments = db_connection.execute_query(conn, sql_simple, fetch_results=True)

    if shipments:
        print("Cada linha representa um produto em um carregamento.")
        headers = ["ID Carreg.", "Placa Veíc.", "Data/Hora Carreg.", "ID Prod.", "Tipo Prod.", "Peso Prod.", "Cód. Rastr."]
        col_widths = [10, 12, 18, 8, 15, 10, 20] # Larguras das colunas.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        for s in shipments: # Itera sobre os itens de carregamento.
            s_formatted = [str(x) if x is not None else "" for x in s] # Formata dados.
            print(header_format.format(*s_formatted)) # Exibe dados.
        print("\nUse 'Detalhes do Carregamento' para ver agrupado por veículo e data.")
    else:
        print("Nenhum carregamento encontrado.")

def shipment_details_terminal(conn):
    """Exibe os detalhes de um Carregamento específico (produtos contidos)."""
    print("\n--- Detalhes do Carregamento ---")
    placa = get_valid_input("Placa do Veículo: ", str.upper) # Pede placa do veículo.
    data_carreg_str = get_valid_input("Data do Carregamento (AAAA-MM-DD HH:MM): ") # Pede data do carregamento.
    try:
        data_carreg = datetime.strptime(data_carreg_str, '%Y-%m-%d %H:%M') # Converte para datetime.
    except ValueError:
        print("Formato de data/hora inválido.")
        return

    # Query para buscar detalhes dos produtos no carregamento especificado.
    sql_details = """
    SELECT C.ID_Carregamento, C.ID_Produto, P.Tipo_Produto, P.Peso, P.Status_Entrega, DR.Codigo_Rastreamento
    FROM Carregamento C
    JOIN Produto_A_Ser_Entregue P ON C.ID_Produto = P.ID_Produto
    JOIN Dados_Rastreamento DR ON P.ID_Rastreamento = DR.ID_Rastreamento
    WHERE C.Placa_Veiculo = ? AND FORMAT(C.Data_Carregamento, 'yyyy-MM-dd HH:mm') = FORMAT(?, 'yyyy-MM-dd HH:mm')
    ORDER BY C.ID_Produto;
    """
    details = db_connection.execute_query(conn, sql_details, (placa, data_carreg), fetch_results=True)

    if details:
        print(f"\nDetalhes do Carregamento - Veículo: {placa}, Data: {data_carreg.strftime('%d/%m/%Y %H:%M')}")
        headers = ["ID Carreg. (Item)", "ID Prod.", "Tipo Prod.", "Peso Prod.", "Status Prod.", "Cód. Rastr."]
        col_widths = [18, 8, 15, 10, 18, 20] # Larguras das colunas.
        header_format = "".join([f"{{:<{w}}}" for w in col_widths])
        print(header_format.format(*headers))
        print("-" * sum(col_widths))
        total_peso = 0
        for d_id_carr, d_id_prod, d_tipo, d_peso, d_status, d_rastr in details: # Itera sobre os detalhes.
            print(header_format.format(d_id_carr, d_id_prod, d_tipo, d_peso, d_status, d_rastr)) # Exibe dados.
            total_peso += d_peso # Soma o peso.
        print("-" * sum(col_widths))
        print(f"Total de Produtos: {len(details)}, Peso Total Estimado: {total_peso:.2f} kg") # Exibe totais.
    else:
        print("Nenhum detalhe encontrado para este veículo e data de carregamento.")

def remove_product_from_shipment_terminal(conn):
    """Remove um Produto específico de um Carregamento."""
    print("\n--- Remover Produto do Carregamento ---")
    list_shipments_terminal(conn) # Lista todos os itens de carregamento para ajudar na escolha.
    id_carregamento_item = get_valid_input("Digite o ID do Item de Carregamento a ser removido (da lista acima): ", int) # Pede o ID do item.
    if id_carregamento_item is None: return

    # Busca dados do item de carregamento.
    item_data = db_connection.execute_query(conn, "SELECT Placa_Veiculo, ID_Produto, Data_Carregamento FROM Carregamento WHERE ID_Carregamento = ?", (id_carregamento_item,), fetch_results=True)
    if not item_data:
        print("Item de carregamento não encontrado.")
        return
    
    placa, prod_id, data_carr = item_data[0] # Placa, ID do produto e data do item.
    confirm = input(f"Tem certeza que deseja remover o produto ID {prod_id} do carregamento do veículo {placa} de {data_carr.strftime('%d/%m/%Y %H:%M')} (Item ID: {id_carregamento_item})? (s/n): ").lower()
    if confirm != 's': # Confirmação da remoção.
        print("Remoção cancelada.")
        return
    
    if db_connection.execute_query(conn, "DELETE FROM Carregamento WHERE ID_Carregamento = ?", (id_carregamento_item,)): # Deleta o item.
        print("Produto removido do carregamento com sucesso.")
        # Opcional: Atualizar status do produto, se necessário.
    else:
        print("Erro ao remover produto do carregamento.")

def delete_shipment_terminal(conn):
    """Deleta um Carregamento completo (todos os produtos de um veículo em uma data específica)."""
    print("\n--- Deletar Carregamento Completo (Todos os Produtos) ---")
    placa = get_valid_input("Placa do Veículo do carregamento a ser deletado: ", str.upper) # Pede placa.
    data_carreg_str = get_valid_input("Data do Carregamento (AAAA-MM-DD HH:MM) a ser deletado: ") # Pede data.
    try:
        data_carreg = datetime.strptime(data_carreg_str, '%Y-%m-%d %H:%M') # Converte para datetime.
    except ValueError:
        print("Formato de data/hora inválido.")
        return

    # Verifica se existem itens para este carregamento.
    items = db_connection.execute_query(conn, "SELECT ID_Carregamento FROM Carregamento WHERE Placa_Veiculo = ? AND Data_Carregamento = ?", (placa, data_carreg), fetch_results=True)
    if not items:
        print("Nenhum carregamento encontrado para este veículo e data para deletar.")
        return

    confirm = input(f"Tem certeza que deseja deletar TODOS os {len(items)} produtos do carregamento do veículo {placa} de {data_carreg.strftime('%d/%m/%Y %H:%M')}? (s/n): ").lower()
    if confirm != 's': # Confirmação da exclusão.
        print("Exclusão cancelada.")
        return
    
    # Deleta todos os itens do carregamento especificado.
    if db_connection.execute_query(conn, "DELETE FROM Carregamento WHERE Placa_Veiculo = ? AND Data_Carregamento = ?", (placa, data_carreg)):
        print(f"Carregamento de {data_carreg.strftime('%d/%m/%Y %H:%M')} para o veículo {placa} deletado com sucesso.")
        # Opcional: Atualizar status dos produtos e do veículo, se necessário.
    else:
        print("Erro ao deletar o carregamento.")


# ------------------- SELF-SERVICE CLIENTE ----------------------
def cadastro_cliente_self_service(conn):
    """Permite que um novo cliente se cadastre no sistema."""
    clear_screen()
    print("--- Cadastro de Novo Cliente (Self-Service) ---")

    # 1. Coleta dados da Pessoa.
    print("\n--- Seus Dados Pessoais ---")
    nome = get_valid_input("Nome completo: ")
    rg = get_valid_input("RG (opcional): ", optional=True)
    telefone = get_valid_input("Telefone de contato: ")
    email = get_valid_input("Email: ")

    # Coleta dados do Endereço.
    print("\n--- Seu Endereço Principal ---")
    cep = get_valid_input("CEP: ")
    estado = get_valid_input("Estado (UF): ")
    cidade = get_valid_input("Cidade: ")
    bairro = get_valid_input("Bairro: ")
    rua = get_valid_input("Rua/Avenida: ")
    numero = get_valid_input("Número: ")
    complemento = get_valid_input("Complemento (ex: Apt, Bloco, Casa): ", optional=True)

    # 2. Coleta dados específicos do Cliente (PF/PJ).
    print("\n--- Tipo de Cliente ---")
    tipo_cliente = get_valid_input("Você é Pessoa Física (PF) ou Jurídica (PJ)? ", str.upper, choices=['PF', 'PJ'])
    
    cpf, data_nasc_obj, cnpj, nome_empresa = None, None, None, None # Inicializa variáveis.
    if tipo_cliente == 'PF': # Se Pessoa Física.
        cpf = get_valid_input("CPF: ")
        data_nasc_str = get_valid_input("Data de Nascimento (AAAA-MM-DD): ")
        try:
            data_nasc_obj = datetime.strptime(data_nasc_str, "%Y-%m-%d").date() # Converte para date.
        except ValueError:
            print("Formato de data inválido. Cadastro cancelado.")
            return
    else: # Se Pessoa Jurídica.
        cnpj = get_valid_input("CNPJ: ")
        nome_empresa = get_valid_input("Nome da Empresa/Razão Social: ")

    # 3. Coleta dados do Usuário.
    print("\n--- Dados de Acesso ao Sistema ---")
    login = get_valid_input("Escolha um Login (nome de usuário): ")
    # Verifica se o login já existe.
    if db_connection.execute_query(conn, "SELECT 1 FROM Usuario WHERE Login = ?", (login,), fetch_results=True):
        print("Erro: Este login já está em uso. Por favor, escolha outro. Cadastro cancelado.")
        return
    
    senha = ""
    while not senha: # Garante que a senha não seja vazia.
        senha = getpass.getpass("Crie uma Senha: ").strip()
        if not senha: print("Senha não pode ser vazia.")
    senha_confirm = getpass.getpass("Confirme a Senha: ").strip() # Confirmação da senha.
    if senha != senha_confirm:
        print("As senhas não coincidem. Cadastro cancelado.")
        return

    try:
        # Conceitualmente, aqui começaria uma transação.
        # O pyodbc por padrão tem autocommit=True para cada execute.
        # Para uma transação real, seria conn.autocommit = False no início da conexão
        # e conn.commit() aqui, com conn.rollback() nos blocos de erro.
        
        # Insere Endereço e obtém ID.
        sql_endereco = "INSERT INTO Endereco (CEP, Estado, Cidade, Bairro, Rua, Numero, Complemento) VALUES (?, ?, ?, ?, ?, ?, ?)"
        endereco_id = db_connection.execute_insert_and_get_last_id(conn, sql_endereco, (cep, estado, cidade, bairro, rua, numero, complemento))
        if not endereco_id: # Se falhar ao inserir endereço.
            print("Erro crítico ao salvar endereço. Cadastro cancelado.")
            # conn.rollback() # Se estivesse em transação explícita.
            return

        # Insere Pessoa e obtém ID.
        sql_pessoa = "INSERT INTO Pessoa (Nome, RG, Telefone, Email, ID_Endereco) VALUES (?, ?, ?, ?, ?)"
        pessoa_id = db_connection.execute_insert_and_get_last_id(conn, sql_pessoa, (nome, rg, telefone, email, endereco_id))
        if not pessoa_id: # Se falhar ao inserir pessoa.
            print("Erro crítico ao salvar dados pessoais. Cadastro cancelado.")
            # conn.rollback()
            return
            
        # Insere Cliente.
        sql_cliente = "INSERT INTO Cliente (Codigo_Pessoa, Tipo_Cliente, CPF, Data_Nascimento, CNPJ, Nome_Empresa) VALUES (?, ?, ?, ?, ?, ?)"
        if not db_connection.execute_query(conn, sql_cliente, (pessoa_id, tipo_cliente, cpf, data_nasc_obj, cnpj, nome_empresa)):
            print("Erro crítico ao salvar dados de cliente. Verifique os campos e tente novamente. Cadastro cancelado.")
            # conn.rollback()
            return

        # Insere Usuário.
        hashed_senha = hash_password(senha) # Gera hash da senha.
        sql_usuario = "INSERT INTO Usuario (Login, Senha_Hash, Codigo_Pessoa, Tipo_Usuario) VALUES (?, ?, ?, ?)"
        if not db_connection.execute_query(conn, sql_usuario, (login, hashed_senha, pessoa_id, 'Cliente')): # Define tipo como 'Cliente'.
            print("Erro crítico ao criar seu usuário de acesso. Cadastro cancelado.")
            # conn.rollback()
            return

        # conn.commit() # Se tudo deu certo e estivesse em transação explícita.
        print("\nCadastro realizado com sucesso! Você já pode fazer login com seu novo usuário e senha.")

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o cadastro: {e}")
        # try:
        #     conn.rollback() # Tenta reverter em caso de erro inesperado.
        # except Exception as rb_e:
        #     print(f"Erro adicional ao tentar reverter transação: {rb_e}")


# ------------------- MENUS DE USUÁRIOS ----------------------
# Define os menus para cada tipo de usuário.

def menu_cliente(conn, user_login, person_code):
    """Menu de funcionalidades para o Cliente logado."""
    clear_screen()
    print(f"Bem-vindo(a) de volta, {user_login}!")
    
    options = [
        "Rastrear um Pedido",
        "Ver Meus Pedidos (como Remetente ou Destinatário)",
        "Ver/Atualizar Meus Dados Pessoais",
        "Ver/Atualizar Meus Endereços" # Simplificado para o endereço principal.
    ]
    while True:
        clear_screen()
        choice = display_menu(f"Menu do Cliente - {user_login}", options)

        if choice == 1: # Rastrear um Pedido.
            cod_rastreio = get_valid_input("Digite o Código de Rastreamento do pedido: ")
            if cod_rastreio:
                # Query para rastrear o pedido, com verificação de segurança para que o cliente
                # só veja pedidos onde ele é remetente, destinatário, ou o CPF do destinatário (no rastreio) é o seu.
                sql_rastreio = """
                SELECT P.ID_Produto, P.Status_Entrega, P.Tipo_Produto, 
                       FORMAT(P.Data_Chegada_CD, 'dd/MM/yyyy') AS Chegada_CD, 
                       FORMAT(P.Data_Prevista_Entrega, 'dd/MM/yyyy') AS Prev_Entrega,
                       REM.Nome AS Remetente, DR.Nome_Destinatario AS Destinatario,
                       MOT.Nome AS Motorista, V.Placa_Veiculo, V.Tipo AS Tipo_Veiculo
                FROM Produto_A_Ser_Entregue P
                JOIN Dados_Rastreamento DR ON P.ID_Rastreamento = DR.ID_Rastreamento
                JOIN Pessoa REM ON P.ID_Remetente = REM.Codigo_Pessoa
                LEFT JOIN Funcionario FMOT ON P.Codigo_Funcionario_Motorista = FMOT.Codigo_Funcionario
                LEFT JOIN Pessoa MOT ON FMOT.Codigo_Funcionario = MOT.Codigo_Pessoa
                LEFT JOIN Veiculo V ON FMOT.Placa_Veiculo = V.Placa_Veiculo
                WHERE DR.Codigo_Rastreamento = ? 
                  AND (P.ID_Remetente = ? OR P.ID_Destinatario = ? OR DR.CPF_Destinatario = (SELECT CPF FROM Cliente WHERE Codigo_Pessoa = ?)); 
                """
                
                # Busca o CPF do cliente logado para a query.
                cpf_cliente_logado_data = db_connection.execute_query(conn, "SELECT CPF FROM Cliente WHERE Codigo_Pessoa = ?", (person_code,), fetch_results=True)
                cpf_cliente_logado = cpf_cliente_logado_data[0][0] if cpf_cliente_logado_data and cpf_cliente_logado_data[0][0] else None

                # Executa a query de rastreio. Usa -1 se não tiver CPF para evitar match errado.
                pedido = db_connection.execute_query(conn, sql_rastreio, (cod_rastreio, person_code, person_code, person_code if cpf_cliente_logado else -1 ), fetch_results=True)
                
                if pedido: # Se o pedido for encontrado.
                    p_data = pedido[0]
                    print("\n--- Detalhes do Pedido ---")
                    # Exibe os detalhes do pedido.
                    print(f"Produto ID: {p_data[0]}")
                    print(f"Status Atual: {p_data[1]}")
                    print(f"Tipo: {p_data[2]}")
                    print(f"Chegada no CD: {p_data[3] or 'N/A'}")
                    print(f"Previsão de Entrega: {p_data[4] or 'N/A'}")
                    print(f"Remetente: {p_data[5]}")
                    print(f"Destinatário (Rastreio): {p_data[6]}")
                    if p_data[7]: # Se tiver motorista associado.
                        print(f"Motorista: {p_data[7]} (Veículo: {p_data[8] or 'N/A'} - {p_data[9] or 'N/A'})")
                else:
                    print("Pedido não encontrado ou você não tem permissão para visualizá-lo.")
            press_enter_to_continue()

        elif choice == 2: # Ver Meus Pedidos.
            list_products_terminal(conn, for_client_person_code=person_code) # Chama a listagem filtrada.
            press_enter_to_continue()

        elif choice == 3: # Ver/Atualizar Meus Dados Pessoais.
            print("\n--- Meus Dados Pessoais (Pessoa) ---")
            # Mostra dados da tabela Pessoa.
            sql_pessoa = "SELECT Nome, RG, Telefone, Email FROM Pessoa WHERE Codigo_Pessoa = ?"
            dados_pessoa = db_connection.execute_query(conn, sql_pessoa, (person_code,), fetch_results=True)
            if dados_pessoa:
                dp = dados_pessoa[0]
                print(f"Nome: {dp[0]}\nRG: {dp[1] or ''}\nTelefone: {dp[2]}\nEmail: {dp[3]}")
            if input("Deseja atualizar os dados da Pessoa? (s/n): ").lower() == 's':
                # update_person_terminal(conn) # A função original pede o ID novamente.
                # Ideal seria passar o person_code para uma versão modificada de update_person_terminal
                # que não peça o ID e já use o `person_code` do usuário logado.
                # Para manter o comportamento original do script, chamamos a função que pede o ID.
                # Mas, para fins de auto-serviço, o usuário só deveria poder alterar seus próprios dados.
                # A função update_person_terminal precisaria de uma adaptação para aceitar o person_code
                # e pular a etapa de perguntar qual pessoa atualizar.
                # Temporariamente, vamos simular que ela faz isso:
                print("Para atualizar, a função 'update_person_terminal' será chamada.")
                print(f"Imagine que você está atualizando a pessoa de Cód: {person_code}")
                update_person_terminal(conn) # O usuário terá que digitar seu próprio código novamente.

            print("\n--- Meus Dados de Cliente (PF/PJ) ---")
            # Mostra dados da tabela Cliente.
            sql_cliente_data = """
            SELECT Tipo_Cliente, CPF, FORMAT(Data_Nascimento, 'dd/MM/yyyy'), CNPJ, Nome_Empresa
            FROM Cliente WHERE Codigo_Pessoa = ?
            """
            dados_cli = db_connection.execute_query(conn, sql_cliente_data, (person_code,), fetch_results=True)
            if dados_cli:
                dc = dados_cli[0]
                print(f"Tipo: {dc[0]}")
                if dc[0] == 'PF':
                    print(f"CPF: {dc[1] or ''}\nData de Nascimento: {dc[2] or ''}")
                else: # PJ
                    print(f"CNPJ: {dc[3] or ''}\nNome da Empresa: {dc[4] or ''}")
            if input("Deseja atualizar os dados de Cliente (PF/PJ)? (s/n): ").lower() == 's':
                update_client_terminal(conn, person_code_logged_in=person_code) # Chama a atualização com o código do cliente logado.
            press_enter_to_continue()

        elif choice == 4: # Ver/Atualizar Endereços.
            print("\n--- Meus Endereços ---")
            # Mostra o endereço principal associado à Pessoa.
            # Para múltiplos endereços, seria necessária uma tabela associativa Pessoa_Endereco.
            sql_endereco = """
            SELECT E.ID_Endereco, E.CEP, E.Rua, E.Numero, E.Complemento, E.Bairro, E.Cidade, E.Estado
            FROM Pessoa P JOIN Endereco E ON P.ID_Endereco = E.ID_Endereco
            WHERE P.Codigo_Pessoa = ?
            """
            end_data = db_connection.execute_query(conn, sql_endereco, (person_code,), fetch_results=True)
            if end_data:
                ed = end_data[0]
                print(f"Endereço Principal (ID: {ed[0]}):")
                print(f"  {ed[2]}, {ed[3]} {ed[4] or ''} - Bairro: {ed[5]}")
                print(f"  {ed[6]} - {ed[7]}, CEP: {ed[1]}")
                
                if input("Deseja atualizar este endereço? (s/n): ").lower() == 's':
                    # A atualização do endereço principal é feita através da atualização dos dados da Pessoa.
                    print("A atualização do endereço principal é feita através da atualização dos dados da Pessoa.")
                    # Similar ao item 3, o update_person_terminal pediria o ID novamente.
                    # O ideal seria uma função específica ou adaptar update_person_terminal.
                    update_person_terminal(conn) # O usuário terá que digitar seu próprio código novamente.
            else:
                print("Nenhum endereço principal encontrado.")
            press_enter_to_continue()

        elif choice == 0: # Sair do menu do cliente.
            break

def menu_admin(conn, user_login, person_code):
    """Menu principal para o Administrador."""
    admin_options = [
        "Gerenciar Usuários", "Gerenciar Pessoas", "Gerenciar Clientes", "Gerenciar Funcionários",
        "Gerenciar Veículos", "Gerenciar Sedes", "Gerenciar Produtos a Entregar",
        "Gerenciar Dados de Rastreamento", "Gerenciar Carregamentos"
    ]
    while True:
        clear_screen()
        choice = display_menu(f"Menu Principal do Administrador - {user_login}", admin_options)

        # Chama as funções de gerenciamento correspondentes à escolha.
        if choice == 1: manage_users_terminal(conn)
        elif choice == 2: manage_people_terminal(conn)
        elif choice == 3: manage_clients_terminal(conn)
        elif choice == 4: manage_employees_terminal(conn)
        elif choice == 5: manage_vehicles_terminal(conn)
        elif choice == 6: manage_headquarters_terminal(conn)
        elif choice == 7: manage_products_terminal(conn)
        elif choice == 8: manage_tracking_terminal(conn)
        elif choice == 9: manage_shipments_terminal(conn)
        elif choice == 0: # Sair do menu do admin.
            break

# Placeholder para menus de outros tipos de funcionários.
# Estas funções apenas exibem mensagens indicando funcionalidades futuras.
def menu_gerente(conn, user_login, person_code):
    """Menu placeholder para o Gerente."""
    print(f"\n--- Menu do Gerente: {user_login} (Cód. Pessoa: {person_code}) ---")
    print("Funcionalidades do Gerente a serem implementadas:")
    print("- Visualizar/Gerenciar Funcionários da Sede")
    print("- Visualizar/Gerenciar Veículos (da Sede ou todos)")
    print("- Visualizar Produtos na Sede")
    print("- Aprovar/Iniciar Carregamentos")
    print("- Gerar Relatórios (Entregas, Desempenho, etc.)")
    press_enter_to_continue()

def menu_atendente(conn, user_login, person_code):
    """Menu placeholder para o Atendente."""
    print(f"\n--- Menu do Atendente: {user_login} (Cód. Pessoa: {person_code}) ---")
    print("Funcionalidades do Atendente a serem implementadas:")
    print("- Cadastrar Novos Pedidos (Produtos a Serem Entregues)")
    print("- Consultar Status de Pedidos para Clientes")
    print("- Registrar Ocorrências/Solicitações de Clientes")
    print("- Interagir com Clientes (Telefone, Email - simulado)")
    press_enter_to_continue()

def menu_motorista(conn, user_login, person_code):
    """Menu placeholder para o Motorista."""
    print(f"\n--- Menu do Motorista: {user_login} (Cód. Pessoa: {person_code}) ---")
    # Busca a placa do veículo do motorista.
    motorista_data = db_connection.execute_query(conn, "SELECT Placa_Veiculo FROM Funcionario WHERE Codigo_Funcionario = ?", (person_code,), fetch_results=True)
    placa_veiculo_motorista = motorista_data[0][0] if motorista_data and motorista_data[0][0] else "N/A"
    print(f"Veículo associado: {placa_veiculo_motorista}")

    print("\nFuncionalidades do Motorista a serem implementadas:")
    print("- Visualizar Entregas Atribuídas")
    print("- Atualizar Status da Entrega (Ex: 'Em trânsito para entrega', 'Entregue', 'Tentativa falhou')")
    print("- Registrar Comprovante de Entrega (simplificado)")
    print("- Visualizar Rota (simulado)")
    print("- Registrar Ocorrências na Rota")
    press_enter_to_continue()

def menu_auxiliar_logistica(conn, user_login, person_code):
    """Menu placeholder para o Auxiliar de Logística."""
    print(f"\n--- Menu do Auxiliar de Logística: {user_login} (Cód. Pessoa: {person_code}) ---")
    # Busca a sede do auxiliar.
    aux_data = db_connection.execute_query(conn, "SELECT ID_Sede FROM Funcionario WHERE Codigo_Funcionario = ?", (person_code,), fetch_results=True)
    id_sede_aux = aux_data[0][0] if aux_data and aux_data[0][0] else "N/A"
    print(f"Sede associada: {id_sede_aux}")

    print("\nFuncionalidades do Auxiliar de Logística a serem implementadas:")
    print("- Registrar Chegada de Produtos na Sede/CD")
    print("- Organizar Produtos para Carregamento")
    print("- Atribuir Produtos a Veículos/Carregamentos (em conjunto com Gerente/Sistema)")
    print("- Atualizar Status de Produtos na Sede (Localização Interna, etc.)")
    print("- Gerenciar Estoque na Sede (simplificado)")
    press_enter_to_continue()

# ------------------- TELA DE LOGIN ----------------------
def login_tela(conn):
    """Gerencia o processo de login do usuário."""
    logged_in_user = None # Inicializa usuário logado como None.
    user_type = None # Inicializa tipo de usuário como None.
    user_person_code = None # Inicializa código da pessoa do usuário como None.
    
    while True: # Loop até que o login seja bem-sucedido ou o usuário decida sair (implicitamente).
        clear_screen()
        print("--- Tela de Login ---")
        username = input("Login: ").strip() # Pede o login.
        password = getpass.getpass("Senha: ").strip() # Pede a senha de forma segura.
        
        if not username or not password: # Se login ou senha estiverem vazios.
            print("Por favor, preencha usuário e senha.")
            press_enter_to_continue()
            continue # Volta para o início do loop.
        
        # Busca dados do usuário no banco de dados.
        sql = "SELECT Senha_Hash, Tipo_Usuario, Codigo_Pessoa FROM Usuario WHERE Login = ?"
        user_data = db_connection.execute_query(conn, sql, (username,), fetch_results=True)

        if user_data: # Se o usuário for encontrado.
            stored_hash, retrieved_user_type, retrieve_person_code = user_data[0] # Pega hash, tipo e código da pessoa.
            if verify_password(stored_hash, password): # Verifica a senha.
                logged_in_user = username
                user_type = retrieved_user_type
                user_person_code = retrieve_person_code
                print(f"Login bem-sucedido! Bem-vindo, {logged_in_user} ({user_type}).")
                press_enter_to_continue()
                break # Sai do loop de login.
            else: # Senha incorreta.
                print("Usuário ou senha inválidos. Tente novamente.")
        else: # Usuário não encontrado.
            print("Usuário não encontrado. Tente novamente.")
        press_enter_to_continue()

    # Direcionamento pós-login para o menu apropriado.
    if logged_in_user:
        if user_type == 'Admin':
            menu_admin(conn, logged_in_user, user_person_code)
        elif user_type == 'Cliente':
            menu_cliente(conn, logged_in_user, user_person_code)
        elif user_type == 'Gerente':
            menu_gerente(conn, logged_in_user, user_person_code)
        elif user_type == 'Atendente':
            menu_atendente(conn, logged_in_user, user_person_code)
        elif user_type == 'Motorista':
            menu_motorista(conn, logged_in_user, user_person_code)
        elif user_type == 'Auxiliar de Logistica': # Corrigido para corresponder à grafia no BD/add_user_terminal
            menu_auxiliar_logistica(conn, logged_in_user, user_person_code)
        else:
            print(f"Tipo de usuário '{user_type}' não possui um menu definido. Contate o administrador.")
            press_enter_to_continue()


# ------------------- MENU INICIAL ----------------------
def menu_inicial_principal():
    """Exibe o menu inicial da aplicação (Login ou Cadastro de Cliente)."""
    options = ["Fazer Login", "Cadastrar-se como Cliente"]
    while True:
        clear_screen()
        choice = display_menu("Bem-vindo ao Sistema de Rastreamento e Logística", options)
        if choice == 1: # Fazer Login.
            return 'login'
        elif choice == 2: # Cadastrar-se como Cliente.
            return 'cadastro_cliente'
        elif choice == 0: # Sair.
            print("Saindo do sistema...")
            return 'sair'


# ------------------- RODAR APLICAÇÃO ----------------------
def run_app_terminal():
    """Função principal que inicia e gerencia o ciclo de vida da aplicação."""
    conn = db_connection.conectar_banco() # Tenta conectar ao banco de dados.
    try:
        if not conn: # Se a conexão falhar.
            print("Erro crítico: Não foi possível conectar ao banco de dados.")
            print("Verifique as configurações em db_connection.py, o driver ODBC e a acessibilidade do servidor Azure SQL.")
            return # Encerra a aplicação.

        while True: # Loop principal da aplicação.
            acao = menu_inicial_principal() # Obtém a ação do menu inicial.
            if acao == 'cadastro_cliente':
                cadastro_cliente_self_service(conn) # Chama a função de cadastro.
                press_enter_to_continue()
            elif acao == 'login':
                login_tela(conn) # Chama a tela de login. Após o logout, volta para o menu inicial.
            elif acao == 'sair':
                break # Sai do loop principal e encerra a aplicação.

    except KeyboardInterrupt: # Se o usuário pressionar Ctrl+C.
        print("\nOperação cancelada pelo usuário. Saindo.")
    except Exception as e: # Captura qualquer outra exceção inesperada.
        print(f"Ocorreu um erro inesperado na aplicação: {e}")
        import traceback
        traceback.print_exc() # Imprime o stack trace para depuração.
    finally: # Bloco executado sempre, mesmo que ocorram exceções.
        if conn: # Se a conexão foi estabelecida.
            db_connection.desconectar_banco(conn) # Desconecta do banco de dados.
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    # Este bloco é executado apenas quando o script é rodado diretamente (não importado como módulo).
    run_app_terminal() # Inicia a aplicação.