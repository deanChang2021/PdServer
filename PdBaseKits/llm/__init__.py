from PdBaseKits.tools.ini.Initial import getIni
from server.handler.exceptions import MissRequiredVariableError

CHAT_MODEL = getIni("ai","chatModel")
MATH_MODEL = getIni("ai","mathModel")


if not all([CHAT_MODEL,MATH_MODEL]):
    raise MissRequiredVariableError("Missing required environment variable: [WAIT_SIZE][CONSUR_SIZE]")
