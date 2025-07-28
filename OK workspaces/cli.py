from hecate import Hecate
import argparse
import speech_recognition as sr


def voice_chat(bot):
    """Continuous microphone input loop."""
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("Speak into the microphone. Press Ctrl+C to exit.")
    while True:
        try:
            with mic as source:
                audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
            except Exception as e:
                print(f"[error] {e}")
                continue
            print(f'You: {text}')
            reply = bot.respond(text)
            print(reply)
        except KeyboardInterrupt:
            print()
            break


def text_chat(bot):
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
    parser = argparse.ArgumentParser(description="Hecate CLI")
    parser.add_argument("--voice", action="store_true", help="Use microphone input")
    args = parser.parse_args()

    bot = Hecate()
    if args.voice:
        voice_chat(bot)
    else:
        text_chat(bot)
