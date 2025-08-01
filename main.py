# [...] todas as importações, funções e variáveis continuam as mesmas até aqui

async def main():
    global config, concurrent_downloads
    config = carregar_config()

    print("🛠️  Cadastro do aplicativo no Telegram")
    print("Antes de prosseguir, você já preencheu o formulário de app em https://my.telegram.org/apps?")
    pronto = input("Digite S (ou Enter) para sim ou N para sair: ").strip().lower()
    if pronto != 's' and pronto != '':
        print("❌ Você precisa concluir o cadastro antes de continuar.")
        return

    print("\n✅ Cadastro confirmado. Vamos coletar os dados necessários:")

    api_id = entrada_config("api_id", "Digite o API ID", obrigatorio=True)
    api_hash = entrada_config("api_hash", "Digite o API HASH", obrigatorio=True)
    phone = entrada_config("phone", "Digite seu telefone (com DDI)", obrigatorio=True)
    group_username = entrada_config("group_username", "Nome do grupo ou canal (sem @)", obrigatorio=True)

    downloads_dir = entrada_config(
        "downloads_dir",
        "Diretório de destino dos downloads",
        padrao=os.path.join(os.getcwd(), "downloads")
    )

    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        print(f"📁 Diretório '{downloads_dir}' criado.")

    # Quantidade de downloads simultâneos
    valor = input(f"Quantos downloads simultâneos por vez? (0 = ilimitado, Enter para manter {config.get('concurrent_downloads', 1)}) [1]: ").strip()
    if valor.isdigit():
        concurrent_downloads = int(valor)
        config['concurrent_downloads'] = concurrent_downloads
    elif valor == '':
        concurrent_downloads = int(config.get('concurrent_downloads', 1))
    else:
        concurrent_downloads = 1

    salvar_config(config)

    print("\n🔐 Conectando ao Telegram...\n")
    client = TelegramClient('session_name', int(api_id), api_hash)
    await client.start(phone)

    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            code = input('Digite o código que você recebeu: ')
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            pw = getpass('Senha em duas etapas: ')
            await client.sign_in(password=pw)

    print(f"\n✅ Conectado. Acessando grupo/canal: {group_username}\n")

    usar_cache = input("📦 Usar o levantamento anterior de arquivos (Enter ou S), ou não, isto é, atualizar a listagem de arquivos (N): ").strip().lower()
    if usar_cache in ['', 's'] and os.path.exists(CACHE_FILE):
        print("🗂️  Usando levantamento anterior.")
        with open(CACHE_FILE, 'r') as f:
            arquivos = json.load(f)
    else:
        print("🔄 Atualizando levantamento de arquivos...")
        arquivos = await levantar_arquivos(client, group_username)

    # 🔁 Loop de busca contínua
    while True:
        termos = input("\n🔎 Digite termos para busca (AND, OR, *, Enter p/ tudo, Q p/ sair): ").strip()
        if termos.lower() == 'q':
            print("👋 Encerrando busca.")
            break

        arquivos_filtrados = [a for a in arquivos if combinar_nome(a['name'], termos)]
        print(f"\n🔍 Arquivos encontrados com filtro: {len(arquivos_filtrados)}")

        try:
            if concurrent_downloads == 0:
                await asyncio.gather(*(baixar_arquivo(client, a, group_username, downloads_dir) for a in arquivos_filtrados))
            else:
                for i in range(0, len(arquivos_filtrados), concurrent_downloads):
                    tarefas = arquivos_filtrados[i:i+concurrent_downloads]
                    await asyncio.gather(*(baixar_arquivo(client, a, group_username, downloads_dir) for a in tarefas))
        except KeyboardInterrupt:
            print("\n⛔ Downloads interrompidos pelo usuário.")

        print("\n🔁 Busca concluída. Você pode realizar uma nova busca ou digitar 'Q' para sair.")

    print("\n✅ Todas as buscas e downloads foram concluídos.")

if __name__ == '__main__':
    try:
        thread_pular = threading.Thread(target=monitorar_pular_download, daemon=True)
        thread_pular.start()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⛔ Programa finalizado pelo usuário com CTRL+C.")