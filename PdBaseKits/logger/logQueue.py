from collections import deque
from os import getenv
from typing import Deque
from PdBaseKits.logger.logType import LogType
from PdBaseKits.tools.DataTools import dateTools


class Source:
    def __init__(self, c:str, l: str) -> None:
        self.content = c
        self.level = l #true:可用,false不可用


##用于维护执行资源池，不同于任务队列，资源池不需要pop，只需要使用时，将状态变更为使用:false，空闲时变更为true
class SourceQueue:
    def __init__(self, concur_size: int) -> None:
        self._queue_size = concur_size
        self._queue: Deque[ Source] = deque()


    def info(self, content):
        self.push(content, LogType.info)

    def error(self, content):
        self.push(content, LogType.error)

    def warnning(self, content):
        self.push(content, LogType.warnning)


    def push(self,content:str, level:str):

        log = "[" + dateTools.getCurrTime(4) + "]["+level+"]" + content
        print("push " + log)
        self._queue.append(Source(log, level))
        print("push succ")


    ## 释放已经执行完成的资源
    def pop(self) ->Source:
        if len(self._queue) <= 0:
            return None

        obj : Source = self._queue.pop()
        return obj

    def __printQueue(self):
        print("------------ source queue ["+str(len(self._queue))+"]--------------")
        for item in self._queue:
            print("channelId ["+item.channelId+"], state["+str(item.state)+"]")
        print("------------ end source queue--------------")


    def maxSize(self)->int:
        return self._queue_size

    def size(self)->int:
        return len(self._queue)

    def clear(self)->None:
        self._queue.clear()


logQueue = SourceQueue(
    int(getenv("CONCUR_SIZE") or 9999)
)
