import asyncio
import datetime
import time
from collections import deque
from os import getenv
from typing import ParamSpec, Callable, Any, Dict, List, Deque, Union
import logging

from PdBaseKits.logger.logQueue import logQueue
from PdBaseKits.logger.logType import LogType
from server.schema.schema import TriggerImagineIn
from server.handler.exceptions import QueueFullError, ConsurIdNotExistError
from server import TASK_TIMEOUT
from PdBaseKits.tools.DataTools import dateTools


P = ParamSpec("P")

class Task:
    def __init__(
        self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        print("init-----")
        print(self.args)

    async def __call__(self) -> None:
        print("call-----")
        print(self.args)

        await self.func(*self.args, **self.kwargs)

    def __repr__(self) -> str:
        return f"{self.func.__name__}({self.args}, {self.kwargs})"



## 执行列表对象
class ExeObj:
    def __init__(self, uId:str, cId:str, tId:str, type:str, time:datetime) -> None:
        self.userId :str = uId
        self.channelId : str = cId
        self.triggerId :str = tId
        self.type : str = type
        self.timestamp:datetime = time


class TaskQueue:
    def __init__(self, concur_size: int, wait_size: int) -> None:
        self._concur_size = concur_size
        self._wait_size = wait_size
        self._wait_queue: Deque[Dict[str, Task]] = deque() #userId, task
        self._concur_queue: List[ExeObj] = [] #channelId, exeobj

        self._cid2UserId = {}#空字典
        logging.info("taskqueue thread init")


        #thr2 = threading.Thread(target=self.clearTimeoutTask, daemon=True)
        #thr2.start()

    def clearTimeoutTask(self):
        # test
        #args[0] channelid, args[1] triggerId
        #self._concur_queue.append(ExeObj("11", "2222222", "207552908","generate", datetime.datetime.now()))
        # print("开始打印队列")
        # self.__printConsurQueue()
        # time.sleep(5)
        # for item in self._concur_queue:
        #     item.timestamp = datetime.datetime.now()
        # self.__printConsurQueue()
        # time.sleep(5)
        # self._concur_queue.append(ExeObj("11", "5555555", "666666", "upscale", datetime.datetime.now()))
        # self._concur_queue.append(ExeObj("11", "7777777", "888888", "describe", datetime.datetime.now()))
        # print("初始化了一个任务")
        #end test


        while True:
            logging.info("------执行超时清除任务----------")
            logQueue.push("------执行超时清除任务----------",LogType.info)
            self.__dealTimeOutTask()
            logging.info("------END 超时清除任务----------")
            logQueue.push("------END 超时清除任务----------",LogType.info)
            time.sleep(10)

    def __dealTimeOutTask(self):
        for item in self._concur_queue:

            if dateTools.timeDiff(item.timestamp, datetime.datetime.now()) >= int(TASK_TIMEOUT):
                channelId=item.channelId

                ## bot 清除执行队列任务
                try:
                    taskqueue.pop(channelId)
                except Exception as e:
                    logging.error("task queue pop error: "+str(e))




                logging.info("clearTimeoutTask succ channelId [" + item.channelId + "], userId[" + str(
                    item.userId) + "], triggerId[" + str(item.triggerId) + "], timestamp["+str(item.timestamp)+"]")


    def __printConsurQueue(self):
        logging.info("----------------Consur Queue--------------------")
        for item in self._concur_queue:
            logging.info("userId["+str(item.userId)+"],channelId["+str(item.channelId)+"],triggerId["+str(item.triggerId)+"],timestamp["+str(item.timestamp)+"]")
        logging.info("----------------END Consur Queue--------------------")


    ### 在等待列表中寻找当前任务
    def findWaitTask(self, userId:int)->bool:

        for i in range(0, len(self._wait_queue)):
            task : TriggerImagineIn = self._wait_queue[i]
            if task.userId == userId:
                return True;
        return False;


    def findConsurTask(self, userId:int)->bool:
        for i in range(0, len(self._concur_queue)):
            task : TriggerImagineIn = self._concur_queue[i]
            if task.userId == userId :
                return True;
        return False;


    def put(self,userId: str, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs) -> None:

        if len(self._wait_queue) >= self._wait_size:
            raise QueueFullError(f"Task queue is full: {self._wait_size}")


        self._wait_queue.append({
            userId: Task(func, *args, **kwargs)
        })

        logging.info("self._wait_queue,userId["+str(userId)+"] ,_wait_queue len[" + str(len(self._wait_queue)) + "] consur queue len[ " + str(len(self._concur_queue))+"]")
        logging.info("===>> self._concur_queue len:"+str(len(self._concur_queue)))


        ### 其在exec中，使用asyncio.get_running_loop来获取当前线程的事件循环，也就是另一个while，然后来执行。
        ### 三个while相当于有三个并行的协程。
        ### 如果第四个put到来时，while条件不满足则不会执行，这里之前的协和处理完成后，会继续执行这个exec，从待执行队列中取出任务。
        while self._wait_queue and len(self._concur_queue) <= self._concur_size:
            self._exec()



    def _exec(self):


        userId, task = self._wait_queue.popleft().popitem()
        print("task.args")
        print(task.args)
        #args[0] triggerId, args[2] type:
        self._concur_queue.append(ExeObj(userId, "",task.args[0], task.args[1], datetime.datetime.now()))

        print(">> _exec source channel id:" + task.args[0])

        logging.info("成功添加一个ID到执行队列 [" + str(userId) + "]")
        logging.info(f"===>> Task[{userId}] start execution: {task}")

        loop = asyncio.get_running_loop()
        tsk = loop.create_task(task())

        # tsk.add_done_callback(
        #     lambda t: print("===>> T.RESULT"+t.result())
        # )  # todo


    ## 任务执行完成后，需要将任务队列中的数据清除
    def pop(self, channelId: str):

        logging.info("queue pop id [" + channelId + "]")

        totalLen = len(self._concur_queue)
        find = False
        for idx in range(0, len(self._concur_queue)):
            if idx >= totalLen:
                break;
            item:ExeObj = self._concur_queue[idx]
            if item.channelId == channelId:
                find=True
                totalLen = totalLen -1
                self._concur_queue.pop(idx)
                logging.info("task queue pop id succ channelId [" + channelId + "], userId["+str(item.userId)+"], triggerId["+str(item.triggerId)+"]")

                if self._wait_queue:
                    self._exec()

        if find == False:
            logging.info("queue pop id ["+channelId+"] fail, 不存在")
            raise ConsurIdNotExistError(f"Consur id not exist :{channelId}")



    #用于查询channelId对应的任务的信息
    def getConsurTaskByCid(self, channelId:str)->Union[ExeObj,bool]:

        find = False
        for item in self._concur_queue:
            if item.channelId == channelId:
                item.timestamp = datetime.datetime.now() #更新时间，避免生成时间过长，超时。
                logging.info("item userId["+str(item.userId)+"],triggerId["+item.triggerId+"],channelId["+item.channelId+"],type["+item.type+"]")
                return item

        if not find:
            return False

    def currentWaitQueueLen(self):
        return len(self._wait_queue)

    def concur_size(self):
        return self._concur_size

    def wait_size(self):
        return self._wait_size

    def clear_wait(self):
        self._wait_queue.clear()

    def clear_concur(self):
        self._concur_queue.clear()




taskqueue = TaskQueue(
    int(getenv("CONCUR_SIZE") or 9999),
    int(getenv("WAIT_SIZE") or 9999),
)
