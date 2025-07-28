# Hecate-v3

This simple project exposes a small voice assistant named **Hecate**. The
assistant can remember short facts, load and run code snippets and even modify
her own source file.

### Learning

Teach Hecate simple question/answer pairs using the `learn:` command. Provide a
question and answer separated by `|`. Example:

```
learn: What is the capital of France? | Paris
```

Once learned, asking the same question will return the stored answer.

### Self update

Send a message starting with `selfupdate:` followed by Python code and Hecate
will append that snippet to `hecate.py`.
