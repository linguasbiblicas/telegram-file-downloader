import os
import re
import json
import time
import asyncio
import threading
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from getpass import getpass
from datetime import datetime
from tqdm import tqdm
import subprocess

CONFIG_FILE = 'config.json'
CACHE_FILE = 'file_cache.json'
skip_download = False
concurrent_downloads = 1

def monitorar_pular_download():
    global skip_download
    print("\n⏭️  Pressione 'p' e Enter a qualquer momento para pular o download atual.")
    while True:
        tecla = input()
        if tecla.strip().lower() == 'p':
            skip_download = True

def carregar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def salvar_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def entrada_config(campo, texto, obrigatorio=False, padrao=None):
    while True:
        valor = input(f"{texto} [{config.get(campo, padrao) or 'não definido'}]: ").strip()
        if valor:
            config[campo] = valor
            return valor
        elif config.get(campo):
            return config[campo]
        elif padrao is not None:
            config[campo] = padrao
            return padrao
        elif not obrigatorio:
            return ''
        else:
            print("❗ Campo obrigatório. Tente novamente.")

def combinar_nome(nome_arquivo, termos):
    if not termos:
        return True
    termos = termos.lower().split()
    return all(t in nome_arquivo.lower() for t in termos)

async def levantar_arquivos(client, group_username):
    arquivos = []
    count = 0
    inicio = datetime.now()
    try:
        async for msg in client.iter_messages(group_username):
            if msg.file and msg.file.name:
                arquivos.append({'id': msg.id, 'name': msg.file.name})
            count += 1
            if count % 100 == 0:
                duracao = datetime.now() - inicio
                print(f"🔄 Lidas {count} mensagens... Tempo: {str(duracao).split('.')[0]}")
    except KeyboardInterrupt:
        print("\n⛔ Busca interrompida pelo usuário.")
        return []
    print(f"\n📦 Total de arquivos listados: {len(arquivos)}")

    with open(CACHE_FILE, 'w') as f:
        json.dump(arquivos, f, indent=2)
        print(f"💾 Levantamento salvo em cache: {CACHE_FILE}")
    return arquivos

def aplicar_ocr(file_path, destino_textos):
    try:
        base = os.path.splitext(os.path.basename(file_path))[0]
        pdf_ocr_path = os.path.join(destino_textos, base + "_ocr.pdf")
        txt_path = os.path.join(destino_textos, base + ".txt")

        # OCR com ocrmypdf
        subprocess.run(["ocrmypdf", file_path, pdf_ocr_path], check=True)

        # Extração de texto com pdftotext
        subprocess.run(["pdftotext", pdf_ocr_path, txt_path], check=True)

        print(f"📑 OCR salvo em: {pdf_ocr_path}")
        print(f"📄 Texto extraído salvo em: {txt_path}")

    except Exception as e:
        print(f"❌ Erro ao aplicar OCR: {e}")

async def baixar_arquivo(client, arq, group_username, downloads_dir, destino_textos):
    global skip_download
    try:
        if skip_download:
            print(f"⏭️  {arq['name']} foi pulado.")
            skip_download = False
            return

        file_path = os.path.join(downloads_dir, arq['name'])

        if os.path.exists(file_path):
            print(f"✅ {arq['name']} já existe. Pulando download.")
            return

        msg = await client.get_messages(group_username, ids=arq['id'])
        print(f"⬇️  Baixando: {arq['name']}")

        with tqdm(total=msg.file.size or 0, unit='B', unit_scale=True, desc=arq['name'][:40]) as bar:
            def progresso(bytes_enviados, tamanho_total):
                bar.total = tamanho_total
                bar.update(bytes_enviados - bar.n)

            await msg.download_media(file_path, progress_callback=progresso)

        # Aplicar OCR se for PDF
        if file_path.lower().endswith(".pdf"):
            aplicar_ocr(file_path, destino_textos)

    except Exception as e:
        print(f"❌ Erro ao baixar {arq['name']}: {e}")

async def main():
    global config, concurrent_downloads
    config = carregar_config()

    print("🛠️  Cadastro do aplicativo no Telegram")
    pronto = input("Digite S (ou Enter) para sim ou N para sair: ").strip().lower()
    if pronto not in ['s', '']:
        print("❌ Você precisa concluir o cadastro antes de continuar.")
        return

    print("\n✅ Cadastro confirmado.")

    api_id = entrada_config("api_id", "Digite o API ID", obrigatorio=True)
    api_hash = entrada_config("api_hash", "Digite o API HASH", obrigatorio=True)
    phone = entrada_config("phone", "Digite seu telefone (com DDI)", obrigatorio=True)
    group_username = entrada_config("group_username", "Nome do grupo ou canal (sem @)", obrigatorio=True)

    downloads_dir = entrada_config(
        "downloads_dir",
        "Diretório de destino dos downloads",
        padrao=os.path.join(os.getcwd(), "downloads")
    )
    destino_textos = os.path.join(downloads_dir, "textospdf")
    os.makedirs(downloads_dir, exist_ok=True)
    os.makedirs(destino_textos, exist_ok=True)

    valor = input(f"Downloads simultâneos? (0 = ilimitado, Enter = {config.get('concurrent_downloads', 1)}): ").strip()
    if valor.isdigit():
        concurrent_downloads = int(valor)
        config['concurrent_downloads'] = concurrent_downloads
    elif valor == '':
        concurrent_downloads = int(config.get('concurrent_downloads', 1))
    salvar_config(config)

    print("🔐 Conectando ao Telegram...\n")
    client = TelegramClient('session_name', int(api_id), api_hash)
    await client.start(phone)

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input('Código recebido: ')
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            pw = getpass('Senha em duas etapas: ')
            await client.sign_in(password=pw)

    print(f"\n✅ Conectado. Acessando grupo/canal: {group_username}\n")

    usar_cache = input("📦 Usar levantamento anterior (S ou Enter), ou N para novo? ").strip().lower()
    if usar_cache in ['', 's'] and os.path.exists(CACHE_FILE):
        print("🗂️  Usando levantamento anterior.")
        with open(CACHE_FILE, 'r') as f:
            arquivos = json.load(f)
    else:
        print("🔄 Atualizando levantamento de arquivos...")
        arquivos = await levantar_arquivos(client, group_username)

    while True:
        termos = input("\n🔎 Digite termos para busca (ou Enter p/ tudo, ou 'sair'): ").strip()
        if termos.lower() == 'sair':
            print("👋 Encerrando busca.")
            break

        arquivos_filtrados = [a for a in arquivos if combinar_nome(a['name'], termos)]
        print(f"\n🔍 Arquivos encontrados com filtro: {len(arquivos_filtrados)}")

        try:
            if concurrent_downloads == 0:
                await asyncio.gather(*(baixar_arquivo(client, a, group_username, downloads_dir, destino_textos) for a in arquivos_filtrados))
            else:
                for i in range(0, len(arquivos_filtrados), concurrent_downloads):
                    tarefas = arquivos_filtrados[i:i+concurrent_downloads]
                    await asyncio.gather(*(baixar_arquivo(client, a, group_username, downloads_dir, destino_textos) for a in tarefas))
        except KeyboardInterrupt:
            print("\n⛔ Downloads interrompidos.")

    print("\n✅ Fim do programa.")

if __name__ == '__main__':
    try:
        thread_pular = threading.Thread(target=monitorar_pular_download, daemon=True)
        thread_pular.start()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⛔ Programa finalizado.")