from chatterbot import ChatBot

def bot():
    chatbot = ChatBot(
        'Norman',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

    history = []
    history_dialogue = []
    exit_conditions = ("q","qui", "quit", "sair", "tchau", "xau", "bye")
    conversations_conditions = ("hello", "hi", "oi", "ola", "olá")

    print("\n\n I'm AI Bot and =======================")
    print("Opções no chat:")
    print(" ▶️  historico: para acessar o Histórico.")
    print(" ▶️  sair: para encerrar o chat.")
    print(" ▶️  ajuda: para pedir ajuda ao Bot.\n")
    while True:
        query = input(" You: ")
        history.append(query)
        history_dialogue.append(query)

        if query.lower() == 'historico':
            print("Histórico:")
            i = 0
            for ask in history:
                print(f" {i}. {ask}")
                i += 1
            continue
        
        elif query.lower() in exit_conditions:
            print("   🤖 Adeus 👋")
            break
        elif query.lower() in conversations_conditions:
            print("   🤖 Olá 👋")
        else:
            response = chatbot.get_response(query)
            history_dialogue.append(response)

            print(f"   🤖 {response}")
    
    with open("historico.txt", "+w", encoding='UTF-8') as file:
        for line in history_dialogue:
            file.write(str(f"{line}\n"))

if __name__ == "__main__":
    bot()