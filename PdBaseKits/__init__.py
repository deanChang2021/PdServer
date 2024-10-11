from PdBaseKits.tools.ini.Initial import getIni
from server.handler.exceptions import MissRequiredVariableError

THIRD_API_TOKEN = getIni("thirdApi","token")

if not all([THIRD_API_TOKEN]):
    raise MissRequiredVariableError("Missing required environment variable: [THIRD_API_TOKEN]")
