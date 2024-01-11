from os import environ

from utils.enviroment import parse_comma_sep_str_to_list

CORS_ALLOWED_ORIGINS = parse_comma_sep_str_to_list(
    environ.get('CORS_ALLOWED_ORIGINS')
)
