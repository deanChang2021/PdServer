from PdBaseKits.tools.ini.Initial import getIni
from server.handler.exceptions import MissRequiredVariableError

SERVER_PORT = getIni("server","port")

if not all([SERVER_PORT]):
    raise MissRequiredVariableError("Missing required environment variable: [SERVER_PORT]")
