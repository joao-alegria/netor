import redis
import config
import json

redisClient=redis.Redis(host=config.REDIS_HOST,port=config.REDIS_PORT,password=config.REDIS_PASS, db=config.REDIS_DB)

def getEntireHash(mainkey):
    return redisClient.hgetall(mainkey)

def getHashKeys(mainkey):
    return redisClient.hkeys(mainkey)

def setKeyValue(mainkey,key,value):
    return redisClient.hset(mainkey,key, value)

def getHashValue(mainkey, key):
    return redisClient.hget(mainkey,key)

def deleteHash(mainKey, key):
    return redisClient.hdel(mainKey, key)

def deleteKey(mainKey):
    return redisClient.delete(mainKey)