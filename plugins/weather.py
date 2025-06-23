def run(params):
    city = params.get("city", "unknown")
    return {
        "tool": "weather",
        "result": f"The weather in {city} is sunny with 30°C."
    }
