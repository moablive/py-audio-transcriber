# app/main.py
import os
import shutil
import secrets
from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from faster_whisper import WhisperModel
import uvicorn
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env (se ele existir localmente)
load_dotenv()

app = FastAPI(title="AudioTranscriber")
security = HTTPBasic()
templates = Jinja2Templates(directory="app/templates")

# --- CONFIGURAÇÕES DO .ENV ---
API_TOKEN = os.getenv("API_TOKEN", "token-padrao-inseguro")

# Credenciais Web
WEB_USER = os.getenv("WEB_USER", "admin")
WEB_PASSWORD = os.getenv("WEB_PASSWORD", "admin")

# Configurações do Whisper
MODEL_SIZE = os.getenv("WHISPER_MODEL", "tiny") 

# [ATUALIZADO] Hardware (Lê do .env ou usa padrão seguro)
DEVICE = os.getenv("WHISPER_DEVICE", "cpu") 
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8") 

# Carrega o modelo na memória ao iniciar
print(f"🌩️ AWLSRV: Carregando modelo Whisper ({MODEL_SIZE}) rodando em {DEVICE} ({COMPUTE_TYPE})...")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

# --- FUNÇÃO DE SEGURANÇA (LOGIN NO NAVEGADOR) ---
def verify_web_login(credentials: HTTPBasicCredentials = Depends(security)):
    """Verifica usuário e senha definidos no .env para acessar a interface visual"""
    is_user_ok = secrets.compare_digest(credentials.username, WEB_USER)
    is_pass_ok = secrets.compare_digest(credentials.password, WEB_PASSWORD)
    
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- ROTAS ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, username: str = Depends(verify_web_login)):
    """
    Interface Gráfica.
    PROTEGIDA: Exige login/senha do .env
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...), 
    x_api_token: str = Header(None, alias="x-api-token")
):
    """
    Endpoint da API (n8n).
    Protegida pelo Header 'x-api-token'.
    """
    # 1. Validação de Segurança
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token de acesso inválido")

    # 2. Salvar arquivo temporário
    # Usamos secrets.token_hex para evitar colisão de nomes se dois arquivos chegarem juntos
    temp_filename = f"temp_{secrets.token_hex(4)}_{file.filename}"
    
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Transcrição
        # beam_size=5 melhora a precisão, reduzindo alucinações da IA
        segments, info = model.transcribe(temp_filename, beam_size=5)
        
        full_text = ""
        for segment in segments:
            full_text += segment.text + " "

        return {
            "filename": file.filename,
            "language": info.language,
            "transcription": full_text.strip()
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    finally:
        # 4. Limpeza
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)