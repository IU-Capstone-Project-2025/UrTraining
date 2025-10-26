def format_initial_user_prompt(user_prompt: str, user_form: str) -> str:
    """
    Formats the initial user prompt by combining the client's form data and query.
    
    Args:
        user_prompt: The user's initial question/query
        user_form: The client's form data/information
        
    Returns:
        str: Combined prompt string in the format:
             "Client's form: [user_form]\n\nClient's first query: [user_prompt]"
    """
    final_prompt: str = (
        f"Client's form: {user_form}\n\nClient's first query: {user_prompt}"
    )
    return final_prompt
