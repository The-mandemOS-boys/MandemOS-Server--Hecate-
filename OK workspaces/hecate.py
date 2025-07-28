import sys
import io
import os
import requests
from bs4 import BeautifulSoup
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from urllib.parse import quote
from twilio.rest import Client
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

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
        self.twilio_sid = os.getenv("TWILIO_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from = os.getenv("TWILIO_FROM")
        self.twilio_to = os.getenv("TWILIO_TO")

    def respond(self, user_input):
        if user_input.startswith("remember:"):
            fact = user_input.split("remember:", 1)[1].strip()
            return self._remember_fact(fact)

        elif user_input == "recall":
            return self._recall_facts()

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

        elif user_input.startswith("inbox"):
            try:
                count = int(user_input.split(":", 1)[1]) if ":" in user_input else 5
            except ValueError:
                count = 5
            return self._fetch_emails(count)

        elif user_input.startswith("sms:"):
            message = user_input.split("sms:", 1)[1].strip()
            return self._send_sms(message)

        elif user_input.startswith("call:"):
            message = user_input.split("call:", 1)[1].strip()
            return self._call_phone(message)

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

    def _send_sms(self, body, to=None):
        to = to or self.twilio_to
        if not all([self.twilio_sid, self.twilio_token, self.twilio_from, to]):
            return f"{self.name}: Twilio credentials not configured."
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            client.messages.create(body=body, from_=self.twilio_from, to=to)
            return f"{self.name}: SMS sent to {to}."
        except Exception as e:
            return f"{self.name}: Failed to send SMS:\n{e}"

    def _call_phone(self, message, to=None):
        to = to or self.twilio_to
        if not all([self.twilio_sid, self.twilio_token, self.twilio_from, to]):
            return f"{self.name}: Twilio credentials not configured."
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            url = f"http://twimlets.com/message?Message%5B0%5D={quote(message)}"
            client.calls.create(to=to, from_=self.twilio_from, url=url)
            return f"{self.name}: Placing call to {to}."
        except Exception as e:
            return f"{self.name}: Failed to place call:\n{e}"

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
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": text}]
            )
            answer = resp.choices[0].message["content"].strip()
            return f"{self.name}: {answer}"
        except Exception as e:
            return f"{self.name}: Error contacting ChatGPT:\n{e}"
