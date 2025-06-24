import random

# MCP metadata
DESCRIPTION = "Simple text generation when AI APIs are unavailable"
SCHEMA = {
    "type": "object",
    "properties": {
        "prompt": {
            "type": "string",
            "description": "The text prompt to generate content for"
        },
        "style": {
            "type": "string",
            "description": "Generation style",
            "enum": ["creative", "technical", "simple"],
            "default": "simple"
        }
    },
    "required": ["prompt"]
}

def run(params):
    prompt = params.get("prompt", "")
    if not prompt:
        return {
            "tool": "simple_text",
            "error": "Missing 'prompt' parameter"
        }
    
    style = params.get("style", "simple")
    
    # Simple template-based responses
    if "python" in prompt.lower() or "code" in prompt.lower():
        responses = [
            f"Here's a basic approach to {prompt}:\n\n```python\n# Your code here\npass\n```",
            f"For {prompt}, you might want to consider using standard Python libraries.",
            f"To implement {prompt}, start with defining your main function and work from there."
        ]
    elif "write" in prompt.lower() or "story" in prompt.lower():
        responses = [
            f"Based on your request '{prompt}', here's a creative response: Once upon a time...",
            f"This is an interesting topic: {prompt}. Let me elaborate on that...",
            f"Regarding '{prompt}', here are some thoughts to consider..."
        ]
    elif "explain" in prompt.lower() or "what" in prompt.lower():
        responses = [
            f"To explain {prompt}: This is a complex topic that involves multiple concepts.",
            f"Regarding {prompt}: This typically refers to processes or systems that...",
            f"The concept of {prompt} can be understood by breaking it down into components."
        ]
    else:
        responses = [
            f"Based on your prompt '{prompt}', here's a response generated using simple templates.",
            f"Regarding '{prompt}': This is an interesting topic that deserves further exploration.",
            f"Your request about '{prompt}' is noted. Here's a basic response to get you started."
        ]
    
    response = random.choice(responses)
    
    return {
        "tool": "simple_text",
        "prompt": prompt,
        "style": style,
        "result": response,
        "note": "This is a simple fallback generator. For better results, use the Gemini tool when quotas allow."
    }
