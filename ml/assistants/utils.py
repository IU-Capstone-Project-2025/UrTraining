def format_initial_user_prompt(user_prompt: str, user_form: str) -> str:
    final_prompt: str = (
        f"Client's form: {user_form}\n\nClient's first query: {user_prompt}"
    )
    return final_prompt
