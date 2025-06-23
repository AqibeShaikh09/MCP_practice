import google.generativeai as genai

# Configure API key (replace or use environment variable)
genai.configure(api_key="api-key")

def run(params):
    prompt = params.get("prompt", "")
    if not prompt:
        return {"error": "Missing 'prompt'"}

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")  # ✅ correct model name
        response = model.generate_content(prompt)
        return {
            "tool": "gemini",
            "model": "gemini-1.5-pro-latest",
            "result": response.text
        }
    except Exception as e:
        return {
            "tool": "gemini",
            "error": str(e)
        }
