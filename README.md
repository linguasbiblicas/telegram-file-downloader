# 📥 Telegram File Downloader

Automatize o download de arquivos enviados em canais e grupos do Telegram com filtros avançados, controle de simultaneidade, OCR automático para PDFs e uma interface de terminal interativa.

> ✅ Ideal para pesquisadores, arquivistas, estudiosos e qualquer pessoa que precise organizar grandes volumes de arquivos compartilhados no Telegram.

---

## ⚙️ Funcionalidades

- 🔐 Conexão segura via API e número de telefone
- 🔄 Reutilização de configurações anteriores via `config.json`
- 📥 Download completo de arquivos com:
  - Filtro por nome com lógica booleana (`AND`, `OR`, aspas para frase exata)
  - Cache persistente de arquivos (`file_cache.json`)
  - Controle de downloads simultâneos
  - Detecção e pulo automático de arquivos já baixados
- ⏭️ Pulador de download (pressione `p` + Enter durante o processo)
- ⌨️ `CTRL+C` não interrompe o programa: retorna à busca
- 📑 Aplicação automática de OCR em PDFs (usando `ocrmypdf` + `pdftotext`)
- 🧠 Busca interativa com múltiplas sessões no terminal
- 📂 Organização de textos extraídos em subpasta dedicada (`textospdf`)

---

## 🧪 Pré-requisitos

- Python 3.7 ou superior
- Telegram API ID e HASH ([crie aqui](https://my.telegram.org))
- Pacotes Python:
  - `telethon`
  - `tqdm`
- Ferramentas do sistema:
  - [`ocrmypdf`](https://ocrmypdf.readthedocs.io)
  - `pdftotext` (via `poppler-utils`)

### Instalação no macOS / Linux:

```bash
brew install ocrmypdf poppler
pip install -r requirements.txt
```

### Instalação no Windows (via Chocolatey):

```bash
choco install ocrmypdf
choco install poppler
pip install -r requirements.txt
```

---

## 🚀 Como usar

```bash
git clone https://github.com/linguasbiblicas/telegram-file-downloader
cd telegram-file-downloader
python filesdownload.py
```

Durante a execução:

- Serão solicitados:
  - API ID e HASH
  - Número de telefone com DDI
  - Nome do grupo ou canal (sem o `@`)
- Se já tiver usado o script antes, basta pressionar Enter para manter o valor anterior salvo
- Escolha o número de downloads simultâneos (0 = ilimitado)
- A busca de arquivos usará lógica booleana:
  - `torah AND fragment` → arquivos contendo **ambos**
  - `scroll OR isaiah` → arquivos contendo **um ou outro**
  - `"dead sea"` → busca pela **frase exata**

---

## ⌨️ Comandos úteis durante o uso

| Comando        | Ação                                                                 |
|----------------|----------------------------------------------------------------------|
| `p` + Enter    | Pula o download atual                                                |
| `CTRL+C`       | Interrompe a operação atual e retorna ao prompt de busca             |
| `Enter` vazio  | Mantém o conteúdo da sessão anterior (para configurações ou busca)   |
| `sair`         | Encerra o programa                                                   |

---

## 🧾 Exemplo de fluxo

```bash
🔎 Digite termos para busca (ou Enter p/ tudo, ou 'sair'):
scroll AND isaiah
⬇️  Baixando: isaiah_scroll_part1.pdf
📄 Texto extraído salvo em: downloads/textospdf/isaiah_scroll_part1.txt
⏭️  Pressione 'p' e Enter a qualquer momento para pular o download atual.
```

---

## 📁 Estrutura dos arquivos

```
telegram-file-downloader/
├── config.json            # Configurações persistentes
├── file_cache.json        # Lista de arquivos do canal (cache)
├── downloads/             # Arquivos baixados
│   └── textospdf/         # Arquivos de texto extraídos via OCR
├── filesdownload.py       # Script principal
└── requirements.txt       # Dependências Python
```

---

## 📜 Licença

MIT License. © 2025 [@linguasbiblicas](https://github.com/linguasbiblicas)

---

## 🤖 Uso de Inteligência Artificial

Este projeto foi inicialmente estruturado com o auxílio da IA da OpenAI (ChatGPT), com adaptações manuais posteriores para ajustes e refinamento.

---

## ✉️ Contato

Desenvolvido por [Erike Lourenço](http://lattes.cnpq.br/8214982422267735) | [@linguasbiblicas](https://www.instagram.com/linguasbiblicas)
