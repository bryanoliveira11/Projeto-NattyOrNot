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

def signin_email_template(username: str):
  return f"""
  <!DOCTYPE html>
  <html lang="pt-BR">
  <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body style="text-align: center;">
  <h1>👋</h1>
  <h1>Boas-Vindas !</h1>
  <h2>Seja bem vindo ao NattyOrNot, {username}.</h2>
  <h3>
  <pre>Aqui você pode criar e compartilhar seus exercícios e treinos,
  além de interagir com uma comunidade apaixonada por saúde e bem-estar.
  Vamos treinar juntos e alcançar nossos objetivos! 💪🏋️‍♀️
  </pre></h3>
  <p>&copy; 2024 NattyOrNot.</p>
  </body>
  </html>
"""
