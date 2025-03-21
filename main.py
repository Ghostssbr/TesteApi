from fastapi import FastAPI, HTTPException
import sqlite3
from fastapi.responses import JSONResponse

app = FastAPI()

# Carregar dados do banco de dados em memória
def carregar_dados():
    try:
        conexao = sqlite3.connect("filmes.db")
        conexao.row_factory = sqlite3.Row  # Para retornar dicionários
        cursor = conexao.cursor()

        # Buscar todos os filmes
        cursor.execute("SELECT * FROM filmes")
        filmes = cursor.fetchall()

        # Converter os resultados em uma lista de dicionários
        filmes_json = [dict(filme) for filme in filmes]

        conexao.close()
        return filmes_json
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao carregar dados.")

# Carregar os dados ao iniciar a API
filmes = carregar_dados()

# Endpoint para buscar todos os filmes
@app.get("/filmes")
async def buscar_filmes():
    return JSONResponse(content=filmes)

# Endpoint para buscar um filme por ID
@app.get("/filmes/{id}")
async def buscar_filme_por_id(id: int):
    filme = next((f for f in filmes if f["id"] == id), None)
    if filme:
        return JSONResponse(content=filme)
    else:
        raise HTTPException(status_code=404, detail="Filme não encontrado.")

# Endpoint de saúde
@app.get("/")
async def health_check():
    return {"status": "API está funcionando!"}
