from django.contrib.messages import constants

# tags que serão usadas no css para estilizar as mensagens ao usuário
MESSAGE_TAGS = {
    constants.DEBUG: 'message-debug',
    constants.ERROR: 'message-error',
    constants.SUCCESS: 'message-success',
    constants.INFO: 'message-info',
    constants.WARNING: 'message-warning',
}
