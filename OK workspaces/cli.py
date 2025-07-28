from hecate import Hecate


def main():
    bot = Hecate()
    print("Type your message. Enter 'quit' to exit.")
    while True:
        try:
            user_input = input('You: ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue
        if user_input.lower() in {'quit', 'exit'}:
            break
        reply = bot.respond(user_input)
        print(reply)


if __name__ == '__main__':
    main()
