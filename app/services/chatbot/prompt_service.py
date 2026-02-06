def optimize_prompt(user_question: str) -> str:
    """
    Adds instructions to improve AI response.
    """
    return f"Answer the following clearly and concisely:\n{user_question}"

def build_chat_prompt(optimized_question: str, add_examples: bool = True) -> str:
    """
    Builds the final prompt with optional examples.
    """
    prompt = optimized_question
    if add_examples:
        prompt += "\nProvide examples if applicable."
    return prompt
