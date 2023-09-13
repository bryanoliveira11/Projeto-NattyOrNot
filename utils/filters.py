def username_limit_length(username: str) -> str:
    if len(username) < 10:
        return 'Olá, ' + username
    return 'Bem-Vindo(a)'
