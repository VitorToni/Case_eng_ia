import os
import yfinance as yf
import duckdb
import datetime
import logging

def conectar_ao_duckdb():
    """
    Conecta ao banco de dados DuckDB e retorna a conexão.

    Returns:
        duckdb.Connection: Conexão com o banco de dados DuckDB.
    """
        
    logger = logging.getLogger(__name__) 
    logging.basicConfig(level=logging.INFO)  
    db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'duckdb')
    # Verifica se o diretório existe, senão, cria o diretório
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        logger.info(f"Path Database criado: {db_dir}")

    db_path = os.path.join(db_dir, 'arquivo_cotacao.db')
    return duckdb.connect(database=db_path)


def ingest_dados(data_inicio, data_fim, tickers):
    """
    Realiza a ingestão de dados do Yahoo Finance para os tickers especificados e armazena no banco de dados DuckDB.

    Args:
        data_inicio (datetime.date): Data de início da coleta dos dados.
        data_fim (datetime.date): Data de fim da coleta dos dados.
        tickers (list): Lista de tickers a serem coletados.
    """

    logger = logging.getLogger(__name__)
    try:
        with conectar_ao_duckdb() as con:
            con.execute("DROP TABLE IF EXISTS Base_analitica")
            con.execute("""CREATE TABLE Base_analitica (Ticker TEXT,
                                                        Date TEXT, 
                                                        Open FLOAT, 
                                                        High FLOAT,  
                                                        Low FLOAT,  
                                                        Close FLOAT,  
                                                        Adj_Close FLOAT,  
                                                        Volume BIGINT)""")

            # Preparar os dados para inserção em massa
            dados_para_inserir = []
            for ticker in tickers:
                ticker = ticker.upper()
                data = yf.download(ticker, start=data_inicio, end=data_fim)
                data.reset_index(inplace=True)
                for _, row in data.iterrows():
                    date_without_time = row['Date'].date().strftime('%Y%m%d')
                    dados_para_inserir.append((ticker, 
                                            date_without_time, 
                                            row['Open'], 
                                            row['High'], 
                                            row['Low'], 
                                            row['Close'], 
                                            row['Adj Close'], 
                                            row['Volume']))

            con.executemany("INSERT INTO Base_analitica VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dados_para_inserir)
    except Exception as e:
        logger.error(f"Erro ao realizar a ingestão de dados: {e}")
        raise e
    logger.info("Dados foram inseridos com sucesso no DuckDB.")


def consultar_fechamentos(periodo):
    """
    Consulta e retorna os dados de fechamento dos ativos para o período especificado.

    Args:
        periodo (str): Período de consulta ("Diario", "Mensal" ou "Anual").

    Returns:
        DataFrame: DataFrame contendo os dados de fechamento.
    """

    logger = logging.getLogger(__name__)
    try:
        if periodo == "Diario":
            data_atual = datetime.datetime.now() - datetime.timedelta(days=180)
            data_formatada = int(data_atual.strftime('%Y%m%d'))
            with conectar_ao_duckdb() as con:
                result_set = con.execute(f"""
                                        SELECT DISTINCT
                                            ticker,
                                            Date,
                                            Open,
                                            High,
                                            Low,
                                            Close,
                                            Adj_Close,
                                            Volume
                                        FROM Base_analitica
                                        WHERE CAST(Date as INTEGER) >= {data_formatada}
                                        ORDER BY ticker, Date DESC
                                        """)
                return result_set.fetch_df()
        else:
            substr_length = 4 if periodo == "Anual" else 6
            with conectar_ao_duckdb() as con:
                result_set = con.execute(f"""
                                        SELECT DISTINCT
                                            ticker,
                                            SUBSTR(Date, 1, {substr_length}) AS Date,
                                            Open,
                                            High,
                                            Low,
                                            Close,
                                            Adj_Close,
                                            Volume
                                        FROM Base_analitica b1
                                        WHERE Date = (
                                            SELECT MAX(Date)
                                            FROM Base_analitica b2
                                            WHERE b1.ticker = b2.ticker
                                            AND SUBSTR(b1.Date, 1, {substr_length}) = SUBSTR(b2.Date, 1, {substr_length}))
                                        ORDER BY ticker, SUBSTR(Date, 1, {substr_length}) DESC
                                        """)
                return result_set.fetch_df()
    except Exception as e:
        logger.error(f"Erro ao consultar fechamentos: {e}")
        raise e
