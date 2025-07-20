import os
import pyodbc
import logging
from dotenv import load_dotenv

# Carrega as variáveis do arquivo config.env para o ambiente
load_dotenv('config.env')

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_DATABASE')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

def criar_string_conexao():
    """Cria a string de conexão para o banco de dados SQL Server."""
    driver = "{ODBC Driver 18 for SQL Server}" # Certifique-se de que este driver está instalado
    return f'DRIVER={driver};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

def conectar_banco():
    """Estabelece uma conexão com o banco de dados e retorna o objeto de conexão."""
    connection_string = criar_string_conexao()
    logging.info(f"Tentando conectar com: SERVER={SERVER}, DATABASE={DATABASE}, UID={USERNAME}")
    try:
        conn = pyodbc.connect(connection_string)
        logging.info("Conexão bem-sucedida!")
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        logging.error(f"Erro ao conectar ao banco de dados: {sqlstate}")
        logging.error(ex)
        if '08001' in str(sqlstate):
            logging.error("Verifique se o nome do servidor está correto e se o servidor SQL está acessível.")
        elif '28000' in str(sqlstate):
            logging.error("Verifique se o nome de usuário e a senha estão corretos.")
        elif 'IM002' in str(sqlstate):
            logging.error("Erro: Driver ODBC não encontrado. Verifique se 'ODBC Driver 18 for SQL Server' está instalado.")
            logging.error("Você pode precisar instalar o driver ODBC para SQL Server da Microsoft.")
        return None

def desconectar_banco(conexao):
    """Fecha a conexão com o banco de dados, se estiver ativa."""
    if conexao:
        try:
            conexao.close()
            logging.info("Conexão fechada com sucesso.")
        except pyodbc.Error as e:
            logging.error(f"Erro ao fechar a conexão: {e}")

def execute_query(conn, sql, params=None, fetch_results=False):
    """
    Executa uma consulta SQL (INSERT, UPDATE, DELETE) ou SELECT opcionalmente.

    Args:
        conn: Objeto de conexão pyodbc.
        sql (str): A string da consulta SQL.
        params (tuple, optional): Parâmetros para a consulta, para prevenir SQL Injection. Defaults to None.
        fetch_results (bool): Se True, retorna os resultados da consulta (para SELECT). Defaults to False.

    Returns:
        list or None: Lista de tuplas com os resultados se fetch_results for True, caso contrário None.
    """
    if not conn:
        logging.error("Conexão com o banco de dados não está ativa.")
        return None

    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        if fetch_results:
            results = cursor.fetchall()
            return results
        else:
            conn.commit() # Confirma as alterações para INSERT, UPDATE, DELETE
            logging.info(f"Consulta executada com sucesso: {sql[:100]}...")
            return True
    except pyodbc.Error as e:
        conn.rollback() # Reverte as alterações em caso de erro
        logging.error(f"Erro ao executar a consulta SQL: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

def execute_insert_and_get_last_id(conn, insert_sql, params=None):
    """
    Executa uma consulta INSERT e retorna o ID da última linha inserida
    usando @@IDENTITY na mesma transação/escopo.
    
    Args:
        conn: Objeto de conexão pyodbc.
        insert_sql (str): A string da consulta INSERT.
        params (tuple, optional): Parâmetros para a consulta. Defaults to None.

    Returns:
        int or None: O ID da última linha inserida se bem-sucedido, caso contrário None.
    """
    if not conn:
        logging.error("Conexão com o banco de dados não está ativa para inserir e obter ID.")
        return None

    try:
        cursor = conn.cursor()
        
        # 1. Executa o INSERT
        if params:
            cursor.execute(insert_sql, params)
        else:
            cursor.execute(insert_sql)
        
        # 2. Imediatamente após o INSERT, executa o SELECT @@IDENTITY
        # @@IDENTITY retorna o último valor de identidade gerado na sessão atual em qualquer tabela.
        cursor.execute("SELECT @@IDENTITY;")
        
        # 3. Pega o resultado
        result = cursor.fetchone() 
        
        new_id = None
        if result and result[0] is not None:
            new_id = int(result[0])
            conn.commit() # Comita a transação APENAS se o ID foi recuperado com sucesso
            logging.info(f"INSERT bem-sucedido e ID gerado (@@IDENTITY): {new_id}")
            return new_id
        else:
            conn.rollback() # Reverte se não conseguiu o ID (indicando problema no INSERT ou recuperação)
            logging.warning("INSERT bem-sucedido, mas @@IDENTITY retornou NULL ou não foi possível recuperar. Revertendo transação.")
            return None
    except pyodbc.Error as e:
        conn.rollback() # Reverte em caso de erro
        logging.error(f"Erro ao executar INSERT e obter ID: {e}")
        return None
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    conexao_db = None
    try:
        conexao_db = conectar_banco()
        if conexao_db:
            logging.info("Conexão de teste bem-sucedida. Desconectando...")
        else:
            logging.error("Falha na conexão de teste.")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado no programa principal: {e}")
    finally:
        if conexao_db:
            desconectar_banco(conexao_db)
    logging.info("Script de conexão finalizado.")
