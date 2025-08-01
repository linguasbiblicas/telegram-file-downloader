# 📁 Telegram File Downloader

Este é um utilitário simples e seguro em Python para baixar automaticamente arquivos de **canais ou grupos do Telegram** diretamente para o seu computador.

Ideal para professores, pesquisadores ou estudantes que precisam organizar arquivos compartilhados em grupos de estudo.

---

## 1. Funcionalidades

- 🔍 Busca automática por arquivos em grupos e canais do Telegram  
- 📊 Barra de progresso amigável com porcentagem  
- 🔁 Evita downloads duplicados  
- ⏭️ Permite pular arquivos em tempo real  
- ⚡ Armazena cache local para maior velocidade  
- ✅ Totalmente gratuito e de código aberto  

---

## 2. Requisitos

- Python 3.7 ou superior  
- Conta no Telegram  
- Chaves de autenticação da API (`api_id` e `api_hash`)

---

## 3. Instalação (Windows, Mac ou Linux)

### 3.1 Baixe o Python

- [Windows](https://www.python.org/downloads/windows/)
- [Mac](https://www.python.org/downloads/macos/)
- **Linux (Ubuntu):**

```bash
sudo apt update
sudo apt install python3 python3-pip
```

> Dica: verifique se o Python está instalado com:

```bash
python --version
```

ou

```bash
python3 --version
```

---

### 3.2 Baixe este projeto

#### Se tiver o Git instalado:

```bash
git clone https://github.com/linguasbiblicas/telegram-file-downloader.git
cd telegram-file-downloader
```

#### Ou baixe como ZIP:

[📦 Download ZIP](https://github.com/linguasbiblicas/telegram-file-downloader/archive/refs/heads/main.zip)

Depois de extrair o arquivo, abra o terminal na pasta extraída.

---

### 3.3 Instale os pacotes necessários
Acione este comando:
```bash
pip install -r requirements.txt
```
Ou este:
```bash
python3 -m pip install -r requirements.txt
```
---

## 4. Como obter seu API ID e API HASH

1. Acesse: [https://my.telegram.org](https://my.telegram.org)
2. Faça login com seu número de telefone
3. Clique em **API Development Tools**
4. Crie um novo app
5. Copie seu `api_id` e `api_hash`

---

## 5. Como usar

Dentro da pasta do projeto, execute o script:

```bash
python main.py
```

Depois disso, siga os passos no terminal:

- Digite seu número de telefone
- Insira o código de verificação que receber
- Escolha o grupo ou canal
- Busque e baixe os arquivos desejados

---

## 6. Privacidade

✅ Nenhum dado pessoal é armazenado fora do seu computador.  
✅ As configurações e cache são locais e acessíveis apenas por você.

---

## 7. Autor

Desenvolvido por Erike Lourenço [contato@linguasbiblicas.com.br](mailto:contato@linguasbiblicas.com.br)  
📚 Escola de Línguas Bíblicas: [www.linguasbiblicas.com.br](https://linguasbiblicas.com.br)   
📬 Contato: [wa.me/linguasbiblicas](https://wa.me/linguasbiblicas)

---

## 8. Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

> Este repositório faz parte do ambiente de projetos da **Escola de Línguas Bíblicas**, voltado à automação, organização de acervos e ensino crítico dos idiomas originais da Bíblia.
