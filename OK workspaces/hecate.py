import sys
import io
import os
import requests
from bs4 import BeautifulSoup
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
import openai


def _load_openai_key():
    """Fetch the OpenAI API key from env or local file."""
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key

    # Try to read from openai_key.txt at repository root
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    key_path = os.path.join(root_dir, "openai_key.txt")
    if os.path.exists(key_path):
        with open(key_path, "r") as f:
            return f.read().strip()
    return None


openai.api_key = _load_openai_key()

os.makedirs("scripts", exist_ok=True)

class Hecate:
    def __init__(self, name="Hecate", personality="bold and adaptive", coder=True):
        self.name = name
        self.personality = personality
        self.coder = coder
        self.memory_file = "memory.txt"
        self.last_code = ""
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_pass = os.getenv("GMAIL_PASS")
        self.current_location = None
        self.distress_phrases = [
            "help",
            "help me",
            "i'm scared",
            "i’m scared",
            "i'll call my dad",
            "i’ll call my dad",
            "stop it now",
            "leave me alone",
        ]

    def respond(self, user_input):
        if user_input.startswith("remember:"):
            fact = user_input.split("remember:", 1)[1].strip()
            return self._remember_fact(fact)

        elif user_input == "recall":
            return self._recall_facts()

        elif user_input == "summarize":
            return self._summarize_memory()

        elif user_input.startswith("run:"):
            code = user_input.split("run:", 1)[1].strip()
            self.last_code = code
            return self._run_code(code)

        elif user_input.startswith("save:"):
            filename = user_input.split("save:", 1)[1].strip()
            return self._save_code(filename)

        elif user_input.startswith("load:"):
            filename = user_input.split("load:", 1)[1].strip()
            return self._load_and_run(filename)

        elif user_input.startswith("retrieve:"):
            try:
                url, filename = user_input.split("retrieve:", 1)[1].split("|", 1)
                return self._retrieve_file(url.strip(), filename.strip())
            except ValueError:
                return f"{self.name}: Use 'retrieve:url|filename'"

        elif user_input.startswith("create:"):
            try:
                parts = user_input.split("create:", 1)[1].split("|", 1)
                filename = parts[0].strip()
                content = parts[1] if len(parts) > 1 else ""
                return self._create_file(filename, content)
            except Exception:
                return f"{self.name}: Use 'create:filename|content'"

        elif user_input.startswith("move:"):
            try:
                src, dest = user_input.split("move:", 1)[1].split("|", 1)
                return self._move_file(src.strip(), dest.strip())
            except ValueError:
                return f"{self.name}: Use 'move:src|dest'"

        elif user_input.strip() == "list":
            return self._list_files()

        elif user_input.startswith("read:"):
            filename = user_input.split("read:", 1)[1].strip()
            return self._read_file(filename)

        elif user_input.startswith("delete:"):
            filename = user_input.split("delete:", 1)[1].strip()
            return self._delete_file(filename)

        elif user_input.startswith("search:"):
            query = user_input.split("search:", 1)[1].strip()
            return self._search_web(query)

        elif user_input.startswith("selfupdate:"):
            code_snippet = user_input.split("selfupdate:", 1)[1].strip()
            return self._self_update(code_snippet)

        elif user_input.startswith("email:"):
            try:
                to, subject, body = user_input.split("email:", 1)[1].split("|", 2)
                return self._send_email(to.strip(), subject.strip(), body.strip())
            except ValueError:
                return f"{self.name}: Use 'email:recipient|subject|body'"

        elif user_input.startswith("location:"):
            try:
                parts = user_input.split("location:", 1)[1].split("|")
                lat = parts[0].strip()
                lon = parts[1].strip()
                self.current_location = (lat, lon)
                if len(parts) > 2:
                    to = parts[2].strip()
                    subject = "Location Data"
                    body = f"Latitude: {lat}\nLongitude: {lon}"
                    return self._send_email(to, subject, body)
                return f"{self.name}: Location tagged at {lat}, {lon}."
            except Exception:
                return f"{self.name}: Use 'location:lat|lon|email'"

        elif any(p in user_input.lower() for p in self.distress_phrases) or "alika in distress" in user_input.lower():
            to = os.getenv("DISTRESS_EMAIL")
            if not self.current_location:
                return f"{self.name}: No location available."
            if not to:
                return f"{self.name}: No emergency contact configured."
            lat, lon = self.current_location
            subject = "Distress Location"
            body = f"Latitude: {lat}\nLongitude: {lon}"
            return self._send_email(to, subject, body)

        elif user_input.startswith("inbox"):
            try:
                count = int(user_input.split(":", 1)[1]) if ":" in user_input else 5
            except ValueError:
                count = 5
            return self._fetch_emails(count)

        elif "code" in user_input.lower() and self.coder:
            return f"{self.name}: What kind of code would you like me to write for you?"

        else:
            return self._chatgpt_response(user_input)

    def _remember_fact(self, fact):
        with open(self.memory_file, "a") as f:
            f.write(fact + "\n")
        return f"{self.name}: Got it. I’ll remember that."

    def _recall_facts(self):
        if not os.path.exists(self.memory_file):
            return f"{self.name}: I don’t have any memories yet."
        with open(self.memory_file, "r") as f:
            facts = f.read().strip()
        return f"{self.name}: Here's what I remember:\n{facts if facts else '(empty)'}"

    def _summarize_memory(self):
        """Return a short summary of remembered facts using ChatGPT."""
        if not os.path.exists(self.memory_file):
            return f"{self.name}: I don’t have any memories yet."
        with open(self.memory_file, "r") as f:
            facts = f.read().strip()
        if not facts:
            return f"{self.name}: Memory file is empty."
        try:
            prompt = (
                "Summarize the following notes in a concise paragraph:"\
                f"\n{facts}"
            )
            resp = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            summary = resp.choices[0].message["content"].strip()
            return f"{self.name}: {summary}"
        except Exception as e:
            return f"{self.name}: Failed to summarize memory:\n{e}"

    def _save_code(self, filename):
        if not self.last_code:
            return f"{self.name}: There's no code to save yet."
        path = os.path.join("scripts", filename)
        with open(path, "w") as f:
            f.write(self.last_code)
        return f"{self.name}: Code saved as {filename}."

    def _load_and_run(self, filename):
        path = os.path.join("scripts", filename)
        if not os.path.exists(path):
            return f"{self.name}: I couldn’t find a file named {filename}."
        with open(path, "r") as f:
            code = f.read()
        self.last_code = code
        return self._run_code(code)

    def _retrieve_file(self, url, filename):
        path = os.path.join("scripts", filename)
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            with open(path, "wb") as f:
                f.write(res.content)
            return f"{self.name}: File saved as {filename}."
        except Exception as e:
            return f"{self.name}: Failed to retrieve file:\n{e}"

    def _create_file(self, filename, content=""):
        path = os.path.join("scripts", filename)
        try:
            with open(path, "w") as f:
                f.write(content)
            return f"{self.name}: Created file {filename}."
        except Exception as e:
            return f"{self.name}: Failed to create file:\n{e}"

    def _move_file(self, src, dest):
        src_path = os.path.join("scripts", src)
        dest_path = os.path.join("scripts", dest)
        try:
            if not os.path.exists(src_path):
                return f"{self.name}: Source file {src} not found."
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            os.rename(src_path, dest_path)
            return f"{self.name}: Moved {src} to {dest}."
        except Exception as e:
            return f"{self.name}: Failed to move file:\n{e}"

    def _list_files(self):
        path = "scripts"
        try:
            files = os.listdir(path)
            if not files:
                return f"{self.name}: No files found."
            return "\n".join(files)
        except Exception as e:
            return f"{self.name}: Failed to list files:\n{e}"

    def _read_file(self, filename):
        path = os.path.join("scripts", filename)
        try:
            if not os.path.exists(path):
                return f"{self.name}: {filename} not found."
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            return f"{self.name}: Failed to read file:\n{e}"

    def _delete_file(self, filename):
        path = os.path.join("scripts", filename)
        try:
            if not os.path.exists(path):
                return f"{self.name}: {filename} not found."
            os.remove(path)
            return f"{self.name}: Deleted {filename}."
        except Exception as e:
            return f"{self.name}: Failed to delete file:\n{e}"

    def _run_code(self, code):
        buffer = io.StringIO()
        try:
            sys.stdout = buffer
            exec(code, {})
            sys.stdout = sys.__stdout__
            return f"{self.name}: Output from your code:\n{buffer.getvalue()}"
        except Exception as e:
            sys.stdout = sys.__stdout__
            return f"{self.name}: Error while running code:\n{e}"

    def _search_web(self, query):
        try:
            url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            results = soup.find_all('a', class_='result__a', limit=3)
            if not results:
                return f"{self.name}: I searched, but found no clear results."
            response = f"{self.name}: Here's what I found:\n"
            for i, r in enumerate(results, 1):
                response += f"{i}. {r.text.strip()}\n   Link: {r['href']}\n"
            return response
        except Exception as e:
            return f"{self.name}: I ran into an issue while searching:\n{e}"

    def _self_update(self, code_snippet):
        """Append a code snippet to my own source file."""
        try:
            my_path = os.path.abspath(__file__)
            with open(my_path, "a") as f:
                f.write("\n" + code_snippet + "\n")
            return f"{self.name}: I've added the provided code to my source file."
        except Exception as e:
            return f"{self.name}: Failed to update myself:\n{e}"

    def _send_email(self, to_addr, subject, body):
        if not (self.gmail_user and self.gmail_pass):
            return f"{self.name}: Gmail credentials not configured."
        try:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = self.gmail_user
            msg["To"] = to_addr
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(self.gmail_user, self.gmail_pass)
                server.sendmail(self.gmail_user, [to_addr], msg.as_string())
            return f"{self.name}: Email sent to {to_addr}."
        except Exception as e:
            return f"{self.name}: Failed to send email:\n{e}"

    def _fetch_emails(self, count=5):
        if not (self.gmail_user and self.gmail_pass):
            return f"{self.name}: Gmail credentials not configured."
        try:
            with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
                imap.login(self.gmail_user, self.gmail_pass)
                imap.select("inbox")
                typ, data = imap.search(None, "ALL")
                if typ != 'OK':
                    return f"{self.name}: Unable to fetch emails."
                ids = data[0].split()
                latest_ids = ids[-count:]
                messages = []
                for i in reversed(latest_ids):
                    typ, msg_data = imap.fetch(i, "(RFC822)")
                    if typ != 'OK':
                        continue
                    msg = email.message_from_bytes(msg_data[0][1])
                    subj = msg.get("Subject", "(no subject)")
                    frm = msg.get("From", "(unknown)")
                    messages.append(f"From: {frm}\nSubject: {subj}")
                imap.close()
            return "\n\n".join(messages) if messages else f"{self.name}: No emails found."
        except Exception as e:
            return f"{self.name}: Failed to fetch emails:\n{e}"

    def _chatgpt_response(self, text):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": text}]
            )
            answer = resp.choices[0].message["content"].strip()
            return f"{self.name}: {answer}"
        except Exception as e:
            return f"{self.name}: Error contacting ChatGPT:\n{e}"
