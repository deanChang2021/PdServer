from PdBaseKits.tools.ini.Initial import getIni
from server.handler.exceptions import MissRequiredVariableError

DB_HOST = getIni("db","host")
DB_NAME =getIni("db","name")
DB_USER =getIni("db","user")
DB_PWD=getIni("db","pwd")

if not all([DB_HOST,DB_NAME,DB_USER,DB_PWD]):
    raise MissRequiredVariableError("Missing required environment variable: [DB_HOST][DB_NAME][DB_USER][DB_PWD]")
