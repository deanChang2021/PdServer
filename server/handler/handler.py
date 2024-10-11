import hashlib
import time
from functools import wraps
from typing import Union

from fastapi import status
from fastapi.responses import JSONResponse

from server.handler.exceptions import BannedPromptError
from server.handler.prompt import BANNED_PROMPT

PROMPT_PREFIX = "<#"
PROMPT_SUFFIX = "#>"


def check_banned(prompt: str):
    words = set(w.lower() for w in prompt.split())
    if len(words & BANNED_PROMPT) != 0:
        raise BannedPromptError(f"banned prompt: {prompt}")


def unique_id():
    """生成唯一的 10 位数字，作为任务 ID"""
    return int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10**10

def nonce_id():
    """生成唯一的 19 位数字"""
    int1 = int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 10 ** 10
    int2 = int(hashlib.sha256(str(time.time()).encode("utf-8")).hexdigest(), 16) % 9 ** 9

    nonceid = str(int1) + str(int2)
    return nonceid


def prompt_handler(prompt: str, picurl: Union[str, None] = None):
    """
    拼接 Prompt 形如: <#1234567890#>a cute cat
    """
    check_banned(prompt)

    trigger_id = str(unique_id())

    if not picurl and prompt.startswith(("http://", "https://")):
        picurl, _, prompt = prompt.partition(" ")

    # modify by zyy 20240508,删除了前后缀。
    return trigger_id, f"{picurl+' ' if picurl else ''}{prompt}"


def http_response(func):
    @wraps(func)
    async def router(*args, **kwargs):
        trigger_id, resp = await func(*args, **kwargs)
        if resp is not None:
            code, trigger_result = status.HTTP_200_OK, "success"
        else:
            code, trigger_result = status.HTTP_400_BAD_REQUEST, "fail"

        return JSONResponse(
            status_code=code,
            content={"trigger_id": trigger_id, "trigger_result": trigger_result}
        )

    return router
