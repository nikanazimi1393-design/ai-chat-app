import os
import json
import requests
from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)

# ---------------------------------------------------------
# تنظیمات - این‌ها رو با متغیرهای محیطی (environment variables) ست کن
# مثلا تو ترموکس:
#   export OPENROUTER_API_KEY="sk-or-xxxxxxxx"
#   export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1/chat/completions"
#   export OPENROUTER_MODEL="openai/gpt-4o-mini"
# ---------------------------------------------------------
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")


@app.route("/")
def index():
    return render_template("index.html", model=MODEL)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages", [])

    if not API_KEY:
        return {"error": "OPENROUTER_API_KEY تنظیم نشده. اول اونو ست کن."}, 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # این دوتا اختیاریه ولی OpenRouter پیشنهاد میکنه بفرستیش
        "HTTP-Referer": "https://termux-ai-chat.local",
        "X-Title": "Termux AI Chat",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
    }

    def generate():
        try:
            with requests.post(BASE_URL, headers=headers, json=payload, stream=True, timeout=120) as r:
                r.encoding = "utf-8"
                if r.status_code != 200:
                    err_text = r.text
                    yield f"data: {json.dumps({'error': err_text})}\n\n"
                    return
                for raw_line in r.iter_lines(decode_unicode=False):
                    if not raw_line:
                        continue
                    line = raw_line.decode("utf-8", errors="replace")
                    if line.startswith("data: "):
                        chunk = line[len("data: "):]
                        if chunk.strip() == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        content_type="text/event-stream; charset=utf-8",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
