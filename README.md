> [!IMPORTANT]
> **Este projeto mudou de lugar.** Desde 04/11/2026 ele mora em
> **[moablive/python-projects/py-audio-transcriber](https://github.com/moablive/python-projects/tree/main/py-audio-transcriber)**,
> junto com os outros projetos em Python (com o histórico de commits). Este repositório fica só como referência.

# 🌩️ AWLSRV - Audio Transcriber

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=docker,py,fastapi,cloudflare,bootstrap,linux&theme=dark" />
  </a>
</p>

<p align="center">
  <strong>API de Transcrição de Áudio (Whisper) Containerizada e Segura.</strong>
</p>

---

## 📖 Sobre o Projeto

O **Audio Transcriber** é uma solução leve e direta para converter áudio em texto usando o modelo **Faster-Whisper**. Ele foi desenhado para ser hospedado em Docker, exposto via **Cloudflare Tunnel** e integrado facilmente com automações (como **n8n**).

### ✨ Funcionalidades
- 🐳 **Docker Native:** Pronto para rodar em qualquer lugar.
- 🚀 **FastAPI:** Alta performance e processamento assíncrono.
- 🔒 **Segurança Dupla:**
  - **Interface Web:** Protegida por Login/Senha (HTTP Basic Auth).
  - **API:** Protegida por Token Fixo (Header `x-api-token`).
- ☁️ **Cloudflare Ready:** Configurado para rodar atrás de túneis Zero Trust.
- 🧠 **IA Offline:** Usa o modelo Whisper localmente (sem custos de API externa).

---

## 🛠️ Instalação

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/audio-transcriber.git](https://github.com/seu-usuario/audio-transcriber.git)
cd audio-transcriber