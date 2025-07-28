import sys
import io
import os
import requests
from bs4 import BeautifulSoup
import json
from json import JSONDecodeError

os.makedirs("scripts", exist_ok=True)

class Hecate:
    def __init__(self, name="Hecate", personality="bold and adaptive", coder=True):
        self.name = name
        self.personality = personality
        self.coder = coder
        self.memory_file = "memory.txt"
        self.knowledge_file = "knowledge.json"
        self.last_code = ""

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

        elif user_input.startswith("learn:"):
            pair = user_input.split("learn:", 1)[1].strip()
            return self._learn(pair)

        elif "code" in user_input.lower() and self.coder:
            return f"{self.name}: What kind of code would you like me to write for you?"

        knowledge = self._load_knowledge()
        if user_input in knowledge:
            return f"{self.name}: {knowledge[user_input]}"
        else:
            return f"{self.name}: (In a {self.personality} tone) You said: \"{user_input}\""

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

    def _load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, "r") as f:
                    return json.load(f)
            except (JSONDecodeError, OSError):
                # If the file is corrupted or unreadable, start fresh
                return {}
        return {}

    def _save_knowledge(self, data):
        with open(self.knowledge_file, "w") as f:
            json.dump(data, f)

    def _learn(self, pair):
        if "|" not in pair:
            return f"{self.name}: Please format learning as 'learn: question | answer'"
        question, answer = pair.split("|", 1)
        question = question.strip()
        answer = answer.strip()
        data = self._load_knowledge()
        data[question] = answer
        self._save_knowledge(data)
        return f"{self.name}: I've learned the answer to '{question}'."
