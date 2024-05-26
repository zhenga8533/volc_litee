def get_response(user_input: str) -> str:
    """
    Get a response based on the user's input.
    
    :param user_input: The user's input.
    :return: The response to the user's input.
    """

    if user_input == 'hi':
        return 'Hello!'
    elif user_input == 'bye':
        return 'Goodbye!'
    elif user_input == 'test':
        return 'Test successful!'
    