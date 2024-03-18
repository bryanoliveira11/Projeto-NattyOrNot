def forgot_password_email_template(code: str):
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="text-align: center;">
    <h1>🔐</h1>
    <h1>Reset de Senha</h1>
    <h2>
    Recebemos seu pedido de reset de senha, seu código é <b>{code}<b>.
    </h2>
    <h3>Informe os 6 digitos no local correto para continuar.</h3>
    <p>&copy; 2024 NattyOrNot.</p>
    </body>
    </html>
  """
