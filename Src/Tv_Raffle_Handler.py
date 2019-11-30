import json
import random
import asyncio
import time
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Utils import Utils
from Timer import Timer
from Statistics import Statistics
from AsyncioCurl import AsyncioCurl
from BasicRequest import BasicRequest

class TvRaffleHandler:

    @staticmethod
    async def check(real_roomid,raffle_name):
        if not await Utils.is_normal_room(real_roomid):
            return
        data = await BasicRequest.tv_req_check(real_roomid)
        checklen = data["data"]["list"]
        list_available_raffleid = []
        for j in checklen:
            raffle_id = j["raffleId"]
            raffle_type = j["type"]
            time_wanted = j["time_wait"] + int(time.time())

            if not Statistics.is_raffleid_duplicate(raffle_id):
                Log.info("本次获取到 %s 的抽奖id为: %s"%(raffle_name,raffle_id))
                list_available_raffleid.append((raffle_id,raffle_type,time_wanted))
                Statistics.add2raffle_ids(raffle_id)
        # 暂时没啥用    
        #num_aviable = len(list_available_raffleid)
        for raffle_id,raffle_type,time_wanted in list_available_raffleid:
            Timer.add2list_jobs(TvRaffleHandler.join,time_wanted,(real_roomid,raffle_id,raffle_type,raffle_name))

    @staticmethod
    async def join(real_roomid,raffle_id,raffle_type,raffle_name):
        await BasicRequest.enter_room(real_roomid)
        data2 = await BasicRequest.tv_req_join(real_roomid,raffle_id,raffle_type)
        Log.info("参与了房间 %s 的 %s 抽奖"%(real_roomid,raffle_name))
        Log.info("%s 抽奖状态: %s"%(raffle_name,"OK" if data2["code"] == 0 else data2["msg"]))
        Statistics.add2joined_raffles("小电视类(合计)")

        code = data2["code"]
        # tasklist = []
        if not code:
            # await asyncio.sleep(random.randint(170,190))
            # task = asyncio.ensure_future(TvRaffleHandler.notice(raffle_id,real_roomid,raffle_name))
            # tasklist.append(task)
            # await asyncio.wait(tasklist, return_when=asyncio.FIRST_COMPLETED)
            Log.critical("房间 %s %s 抽奖结果: %s X %s"%(real_roomid,raffle_name,data2["data"]["award_name"],data2["data"]["award_num"]))
            Statistics.add2results(data2["data"]["award_name"],int(data2["data"]["award_num"]))
        elif code == -500:
            Log.error("-500繁忙,稍后重试")
            return False
        elif code == 400:
            Log.error("当前账号正在小黑屋中")
            return False

    @staticmethod
    async def notice(raffleid,real_roomid,raffle_name):
        data = await BasicRequest.tv_req_notice(real_roomid,raffleid)
        if not data["code"]:
            if data["data"]["gift_id"] == "-1":
                return
            elif data["data"]["gift_id"] != "-1":
                data = data["data"]
                Log.critical("房间 %s %s 抽奖结果: %s X %s"%(real_roomid,raffle_name,data["gift_name"],data["gift_num"]))
                Statistics.add2results(data["gift_name"],int(data["gift_num"]))