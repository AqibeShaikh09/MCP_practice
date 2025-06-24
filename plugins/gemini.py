import google.generativeai as genai
import os

# MCP metadata
DESCRIPTION = "Generate text using Google Gemini AI model"
SCHEMA = {
    "type": "object",
    "properties": {
        "prompt": {
            "type": "string",
            "description": "The text prompt to generate content for"
        },        "model": {
            "type": "string",
            "description": "Gemini model to use",
            "enum": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
            "default": "gemini-1.5-flash"
        },
        "max_tokens": {
            "type": "integer",
            "description": "Maximum tokens to generate",
            "default": 1000
        }
    },
    "required": ["prompt"]
}

def run(params):
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "tool": "gemini",
            "error": "GEMINI_API_KEY environment variable not set. Please set it with your API key."
        }
    
    # Configure API key
    genai.configure(api_key=api_key)
    
    prompt = params.get("prompt", "")
    if not prompt:
        return {
            "tool": "gemini",
            "error": "Missing 'prompt' parameter"
        }    # Get model name with fallback strategy
    model_name = params.get("model", "gemini-1.5-flash")  # Default to flash for lower quota usage
    fallback_models = ["gemini-1.5-flash", "gemini-pro", "gemini-1.5-pro"]
    
    # Remove the requested model from fallbacks if it's already there
    if model_name in fallback_models:
        fallback_models.remove(model_name)
    
    # Try the requested model first, then fallbacks
    models_to_try = [model_name] + fallback_models
    
    for current_model in models_to_try:
        try:
            # Initialize model
            model = genai.GenerativeModel(current_model)
            
            # Generate content with rate limiting considerations
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=min(params.get("max_tokens", 1000), 500),  # Reduce token usage
                    temperature=0.7
                )
            )
            
            return {
                "tool": "gemini",
                "model": current_model,
                "prompt": prompt,
                "result": response.text,
                "fallback_used": current_model != model_name,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else None,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else None
                }
            }
        
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a quota/rate limit error
            if "429" in error_str or "quota" in error_str.lower() or "rate limit" in error_str.lower():
                if current_model != models_to_try[-1]:  # Not the last model to try
                    continue  # Try next model
                else:
                    # All models failed due to quota
                    return {
                        "tool": "gemini",
                        "error": "All Gemini models have exceeded quota limits. Please try again later or upgrade your plan.",
                        "quota_exceeded": True,
                        "models_tried": models_to_try,
                        "suggestion": "Consider using gemini-1.5-flash model which has higher quotas, or try again in a few minutes.",
                        "rate_limit_info": "Free tier limits: 15 requests/minute, 1,500 requests/day per model"
                    }
            else:
                # Other error, try next model
                if current_model != models_to_try[-1]:
                    continue
                else:
                    # All models failed with non-quota errors
                    return {
                        "tool": "gemini",
                        "error": f"Gemini API error: {error_str}",
                        "model": current_model,
                        "models_tried": models_to_try
                    }
