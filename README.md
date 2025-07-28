# Hecate-v3

This simple project exposes a small voice assistant named **Hecate**. The
assistant can remember short facts, load and run code snippets and even modify
her own source file.

### Requirements

Install the required dependencies before running any of the scripts:

```bash
pip install flask flask-cors requests beautifulsoup4
```

### Running the server

To launch the assistant without sending an email, run:

```bash
python OK\ workspaces/main.py
```

### Self update

Send a message starting with `selfupdate:` followed by Python code and Hecate
will append that snippet to `hecate.py`.

### Starting with email notification

You can launch the server using `start_and_email.py`. If email credentials are
provided through environment variables, the script will send a notification when
Hecate starts so you can open the interface from your phone.

Set the following environment variables before running:

- `SMTP_SERVER` – address of your SMTP server (e.g. `smtp.gmail.com`)
- `SMTP_PORT` – server port (default `587`)
- `SMTP_USERNAME` – username/login for the SMTP server
- `SMTP_PASSWORD` – password for the SMTP server
- `TO_EMAIL` – destination email address
- `HECATE_LINK` – link included in the notification (defaults to
  `http://localhost:8080`)

Run the server with:

```bash
python start_and_email.py
```

When the email is sent successfully, open `http://<server-ip>:8080` in your
phone's browser to interact with Hecate.
