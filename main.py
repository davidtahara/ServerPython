import uvicorn
from fastapi import FastAPI

# Pega as variaveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# Váriaveis de ambiente
import os
porta = int(os.getenv("PORT"))

# Inicializa o FastAPI
app = FastAPI()

# Faz a importação de todos os modulos
# Pega todas as pastas dentro de modules
from os import listdir
from os.path import isfile, join
modules = listdir("Modules")
for module in modules:
    if isfile(join("Modules", module)):
        continue
    # Pega todos os arquivos dentro da pasta "Modules.{module}.routers"
    files = listdir(f"Modules/{module}/routers")
    for file in files:
        if file.endswith(".py"):
            # Importa o arquivo
            exec(f"from Modules.{module}.routers import {file[:-3]}")

            # Adiciona o router ao app
            exec(f"app.include_router({file[:-3]}.router)")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=porta)