import os
import json
import requests
from flask import Flask, render_template, request, Response, stream_with_context, jsonify

app = Flask(__name__)

# ---------------------------------------------------------
# تنظیمات - این‌ها رو با متغیرهای محیطی (environment variables) ست کن
# مثلا تو ترموکس:
#   export OPENROUTER_API_KEY="sk-or-xxxxxxxx"
#   export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1/chat/completions"
#   export OPENROUTER_MODEL="openai/gpt-4o-mini"
#   export OPENROUTER_IMAGE_MODEL="google/gemini-2.5-flash-image-preview:free"
# ---------------------------------------------------------
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
BASE_URL = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
IMAGE_MODEL = os.environ.get("OPENROUTER_IMAGE_MODEL", "google/gemini-2.5-flash-image")


def _headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://termux-ai-chat.local",
        "X-Title": "Termux AI Chat",
    }


@app.route("/")
def index():
    return render_template("index.html", model=MODEL)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages", [])

    if not API_KEY:
        return {"error": "OPENROUTER_API_KEY تنظیم نشده. اول اونو ست کن."}, 400

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
    }

    def generate():
        try:
            with requests.post(BASE_URL, headers=_headers(), json=payload, stream=True, timeout=120) as r:
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


@app.route("/api/generate-image", methods=["POST"])
def generate_image():
    """یک پرامپت متنی میگیره و از مدل تصویرساز رایگان Gemini عکس تولید میکنه."""
    data = request.get_json(force=True)
    prompt = (data.get("prompt") or "").strip()

    if not API_KEY:
        return jsonify({"error": "OPENROUTER_API_KEY تنظیم نشده."}), 400
    if not prompt:
        return jsonify({"error": "متن توصیف عکس خالیه."}), 400

    payload = {
        "model": IMAGE_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }

    try:
        r = requests.post(BASE_URL, headers=_headers(), json=payload, timeout=120)
        r.encoding = "utf-8"
        if r.status_code != 200:
            return jsonify({"error": r.text}), 400

        result = r.json()
        message = result.get("choices", [{}])[0].get("message", {})
        images = message.get("images", [])

        if not images:
            text_fallback = message.get("content", "")
            return jsonify({"error": "مدل عکسی برنگردوند. پاسخ متنی: " + (text_fallback or "خالی")}), 400

        image_url = images[0].get("image_url", {}).get("url", "")
        return jsonify({"image_url": image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
