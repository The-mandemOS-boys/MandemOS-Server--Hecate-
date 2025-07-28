import os
import importlib.util
import urllib.parse
import sys

def load_hecate():
    if 'openai' not in sys.modules:
        sys.modules['openai'] = type('openai', (), {'api_key': None, 'ChatCompletion': None})
    spec = importlib.util.spec_from_file_location("hecate", os.path.join("OK workspaces", "hecate.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Hecate

Hecate = load_hecate()


def test_remember_and_recall(tmp_path):
    h = Hecate()
    h.memory_file = tmp_path / "memory.txt"
    response = h._remember_fact("sky is blue")
    assert "remember" in response.lower()
    resp2 = h._recall_facts()
    assert "sky is blue" in resp2


def test_save_load_and_run(tmp_path):
    h = Hecate()
    h.memory_file = tmp_path / "memory.txt"
    h.last_code = "print('hi')"
    response = h._save_code("test.py")
    assert "saved" in response.lower()
    out = h._load_and_run("test.py")
    assert "hi" in out


def test_run_code_output():
    h = Hecate()
    result = h._run_code("print('hello')")
    assert "hello" in result


def test_search_web_encodes_query(monkeypatch):
    captured = {}
    def fake_get(url, headers=None, timeout=5):
        captured['url'] = url
        class FakeRes:
            text = '<html></html>'
        return FakeRes()
    monkeypatch.setattr('requests.get', fake_get)
    h = Hecate()
    h._search_web('c++ tutorial')
    assert urllib.parse.quote_plus('c++ tutorial') in captured['url']
