#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import logging

"""
Redis数据格式
    (1) 字符串 | 存储形式: key - value:str
        - 存储二进制数据 : 可以存储任意类型的数据，包括文本、数字、二进制数据等
        - 键值对存储 : 每个字符串有键（key）和对应的值（value）
        - 支持设置过期时间 : 可设置过期时间，到期后自动删除

    (2) 哈希 | 存储形式: key - { field:value, field:value ...}
        - 键值对存储 : 存储多个键值对，每个键对应一个值
        - 不可重复 : 每个key的field字段唯一，不可重复
        - 高效查找 : 通过键可以快速查找对应的值，时间复杂度为O(1)
        - 支持添加、删除、修改键值对，以及获取指定键的值

    (3) 列表 | 存储形式: key - [value , value ...]
        - 可重复 : 同一个元素可以出现多次
        - 元素有序 : 列表中的元素按照插入顺序排列，保持有序性
        - 支持在列表两端进行元素的插入、删除操作

    (4) 集合 | 存储形式: key - [member , member ...]
        - 不可重复 : 成员唯一，不能重复
        - 元素无序：没有固定的顺序，每次获取的元素顺序可能不同

    (5) 有序集合 | 存储形式: key - [member:score , member:score ...]
        - 不可重复 : 成员唯一，不能重复
        - 成员按照分数的大小顺序排列，相同分数的成员按照字典序排列
"""


class RedisUtils:
    def __init__(self, host='localhost', port=6379, db=0, password='', maxConn=99):
        """
            初始化Redis连接池
        :param host: 主机名
        :param port: 端口
        :param db: 数据库
        :param password: 密码
        """
        pool = redis.ConnectionPool(host=host, port=port, db=db, password=password, max_connections=maxConn)
        self.rdb = redis.Redis(connection_pool=pool, port=port, decode_responses=True)

        self.ListLeft = 0
        self.ListRight = 1

    def __del__(self):
        """ 程序结束后，自动关闭连接，释放资源 """
        self.rdb.connection_pool.disconnect()

    def iniIncr(self, key, val):
        """一般来说，在启动初始时，从关系库或本地文件中初始化"""
        self.rdb.set(key, val)

    def incrKey(self, key):
        self.rdb.incr(key)

    def flushAllData(self):
        """
            清除数据库所有数据
        :return: 是否清除成功
        """
        result = self.rdb.flushdb()
        self.logger.debug("[Redis] Database cleared successfully") \
            if result else self.logger.error("[Redis] Failed to clear the database")
        return result

    def printAllData(self):
        """ 遍历数据库所有键值对 """
        for key in self.rdb.scan_iter(match='*'):
            key_type = self.rdb.type(key).decode('utf-8')

            if key_type == 'string':
                value = self.rdb.get(key).decode('utf-8')
            elif key_type == 'hash':
                value = self.rdb.hgetall(key)
            elif key_type == 'list':
                value = self.rdb.lrange(key, 0, -1)
            elif key_type == 'set':
                value = self.rdb.smembers(key)
            elif key_type == 'zset':
                value = self.rdb.zrange(key, 0, -1, withscores=True)
            else:
                value = "Unsupported type"

            print(f'{key_type} -> {key.decode("utf-8")} : {value}')

    def getKeyType(self, key):
        """
            获取指定key的类型
        :param key: 键
        :return: 类型（字符串格式）
        """
        return self.rdb.type(key)

    def isExistsKey(self, key):
        """
            判断是否存在指定key
        :param key: 键
        :return: 布尔值
        """
        return False if self.rdb.exists(key) == 0 else True

    def deleteKey(self, key):
        """
            删除指定key的成员
        :param key: 键
        :return: 成功删除的个数
        """
        return self.rdb.delete(key)

    def renameKey(self, old, new):
        """
            重命名指定key
        :param old: 旧key值
        :param new: 新key值
        :return:
        """
        if self.isExists_key(old):
            return self.rdb.rename(old, new)

    def setExpireBySecond(self, key, second=60 * 60 * 24 * 7):
        """
            以秒为单位设置过期时间
        :param key: 键
        :param second: 默认7天
        :return:
        """
        return self.rdb.expire(key, time=second)

    def removeExpire(self, key):
        """
            移除key的过期时间，持久保持
        :param key: 键
        :return:
        """
        return self.rdb.persist(key)

    def getExpireBySecond(self, key):
        """
            以秒为单位返回key的剩余过期时间
        :param key: 键
        :return:
        """
        return self.rdb.ttl(key)

    def addStr(self, key: str, value: str):
        """
            添加字符串类型键值对 <key:value(str)>
        :param key: 键
        :param value: 字符串值
        :return: 是否添加成功
        """
        result = self.rdb.set(key, value)
        (logging.info(f"[Redis] Successfully added <{key}:{value}>")) \
            if result else logging.error(f"[Redis] Failed added <{key}:{value}>")
        return result

    def getStr(self, key):
        """
            获取指定key的value，若不存在key，返回 None
        :param key: 键
        :return: 值
        """
        return self.rdb.get(key)

    def appendStr(self, key, append_str: str):
        """
            追加指定key的value,若不存在key，新建键值对 <key:append_str(str)>
        :param key: 键
        :param append_str: 追加字符串值
        :return: 追加后值的长度
        """
        return self.rdb.append(key, append_str)

    def addList(self, key, *value, direction=0):
        """
            列表添加数据
        :param key: 键
        :param value: 列表值
        :param direction: 添加方向（左边ListLeft /右边ListRight）
        :return:
        """
        if direction == self.ListLeft:
            self.rdb.lpush(key, *value)
        elif direction == self.ListRight:
            self.rdb.rpush(key, *value)
        else:
            self.logger.error("[Redis] Unrecognized type of direction")

    def getListByRange(self, key, start=0, end=-1):
        """
            获取列表指定索引范围的列表值
        :param key: 键
        :param start: 起始索引位置
        :param end: 结束索引位置
        :return: 索引范围内的列表值
        """
        return self.rdb.lrange(key, start, end)

    def getlistByIndex(self, key, index):
        """
            获取列表指定下标的列表值
        :param key: 键
        :param index: 指定索引
        :return: 索引对应列表值
        """
        return self.rdb.lindex(key, index)

    def popListByDirection(self, key, direction=0):
        """
            根据删除方向删除列表数据
        :param key: 键
        :param direction: 删除方向（左边ListLeft /右边ListRight）
        :return:
        """
        if direction == self.ListLeft:
            self.rdb.lpop(key)
        elif direction == self.ListRight:
            self.rdb.rpop(key)
        else:
            self.logger.error("[Redis] Unrecognized type of direction")

    def popListByValue(self, key, value, count=1):
        """
            根据指定列表值删除列表数据
        :param key: 键
        :param value:指定列表值
        :param count:若存在多个，删除指定个数
        :return: 成功删除的个数
        """
        result = self.rdb.lrem(key, count, value)
        self.logger.debug(f"[Redis] List delete {result} values:{value}")
        return result

    def addHash(self, key, field, value):
        """
            哈希添加数据
        :param key: 键
        :param field: filed域
        :param value: value域
        :return: 成功添加数据的条数
        """
        _value = self.rdb.hget(key, field)
        msg = f"[Redis] Hash add {key} = {{{field} : {value}}}" \
            if _value is None else f"[Redis] Set replace {key} = {{{field} : {_value} -> {value}}}"
        self.logger.debug(msg)
        return self.rdb.hset(key, field, value)

    def getHashByField(self, key, field):
        """
            获取哈希指定key、field的value值
        :param key: 键
        :param field: filed值
        :return: value值
        """
        return self.rdb.hget(key, field)

    def getHashAllFiled(self, key):
        """
            获取所有的field值
        :param key: 键
        :return: 列表 [field,field ...]
        """
        return self.rdb.hkeys(key)

    def getHashAllValue(self, key):
        """
            获取所有的value值
        :param key: 键
        :return: 列表 [value,value ...]
        """
        return self.rdb.hvals(key)

    def getHashAllKeyValue(self, key):
        """
            获取所有的键值对 <field:value>
        :param key: 键
        :return: 字典 {field:value,field:value ...}
        """
        return self.rdb.hgetall(key)

    def addSet(self, key, *values):
        """
            集合添加数据
        :param key: 键
        :param values: 值（可以多个）
        :return: 添加到集合中的新成员的数量
        """
        return self.rdb.sadd(key, *values)

    def getSet(self, key):
        """
            获取集合指定key的value列表
        :param key: 键
        :return: 列表 [value,value ...]
        """
        return self.rdb.smembers(key)

    def deleteSetRandom(self, key):
        """
            移除指定key的随机value值
        :param key: 键
        :return: 删除的值
        """
        return self.rdb.spop(key)

    def deleteSetAssign(self, key, *values):
        """
            移除指定key的指定value值
        :param key: 键
        :param values: 指定value值
        :return: 删除成功的个数
        """
        return self.rdb.srem(key, *values)

    def addSortSet(self, key, mapping):
        """
            有序集合添加数据，若已存在member，则更新分数score
        :param key: 键
        :param mapping: 值 {member:score , member:score ...}
        :return: 成功添加到有序集合中的新成员的数量
        """
        return self.rdb.zadd(key, mapping)

    def getSortSetByIndexRange(self, key, start=0, end=-1, with_score=True):
        """
            获取指定下标index范围内(start,end)的成员及分数
        :param key: 键
        :param start: 起始索引值
        :param end: 结束索引值
        :param with_score: 返回结果是否包含分数scores
        :return: 列表 [(member, scores), (member, scores) ...] 或 [member, member ...]
        """
        return self.rdb.zrange(key, start, end, withscores=with_score)

    def getSortSetByScoreRange(self, key, min, max):
        """
            获取指定分数score范围内(min,max)的成员及分数
        :param key: 键
        :param min: 最小分数值
        :param max: 最大分数值
        :return: 列表 [member, member ...]
        """
        return self.rdb.zrangebyscore(key, min, max)

    def deleteSortSetByMember(self, key, *members):
        """
            删除指定member的成员
        :param key: 键
        :param members: 指定member值
        :return: 成功移除的成员数量
        """
        return self.rdb.zrem(key, *members)

    def deleteSortSetByIndexRange(self, key, start=0, end=-1):
        """
            删除指定下标index范围内(start,end)的成员及分数
        :param key: 键
        :param start: 起始索引值
        :param end: 结束索引值
        :return: 成功移除的成员数量
        """
        return self.rdb.zremrangebyrank(key, start, end)

    def deleteSortSetByScoreRange(self, key, min, max):
        """
            删除指定分数score范围内(min,max)的成员及分数
        :param key: 键
        :param min: 最小分数值
        :param max: 最大分数值
        :return: 成功移除的成员数量
        """
        return self.rdb.zremrangebyscore(key, min, max)

#实例化
redisUtil = RedisUtils()