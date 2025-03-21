from fastapi import FastAPI, HTTPException
import sqlite3
from fastapi.responses import JSONResponse

app = FastAPI()

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conexao = sqlite3.connect("filmes.db")
        conexao.row_factory = sqlite3.Row  # Para retornar dicionários
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")

# Endpoint para buscar todos os filmes
@app.get("/filmes")
async def buscar_filmes():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        # Buscar todos os filmes no banco de dados
        cursor.execute("SELECT * FROM filmes")
        filmes = cursor.fetchall()

        # Converter os resultados em uma lista de dicionários
        filmes_json = [dict(filme) for filme in filmes]

        return JSONResponse(content=filmes_json)
    except Exception as e:
        print(f"Erro ao buscar filmes: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar filmes.")
    finally:
        conexao.close()

# Endpoint para buscar um filme por ID
@app.get("/filmes/{id}")
async def buscar_filme_por_id(id: int):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        # Buscar o filme pelo ID
        cursor.execute("SELECT * FROM filmes WHERE id = ?", (id,))
        filme = cursor.fetchone()

        if filme:
            return JSONResponse(content=dict(filme))
        else:
            raise HTTPException(status_code=404, detail="Filme não encontrado.")
    except Exception as e:
        print(f"Erro ao buscar filme por ID: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar filme por ID.")
    finally:
        conexao.close()

# Endpoint de saúde
@app.get("/")
async def health_check():
    return {"status": "API está funcionando!"}
