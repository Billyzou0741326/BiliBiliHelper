import sys
sys.path.append("Src")
import time
import asyncio
import Console
import threading
import Danmu_Monitor
from Raffle_Handler import RaffleHandler
import platform
if platform.system() == "Windows":
    from Windows_Log import Log
else:
    from Unix_Log import Log
from Auth import Auth
from Capsule import Capsule
from Coin2Silver import Coin2Silver
from DailyBag import DailyBag
from GiftSend import GiftSend
from Group import Group
from Heart import Heart
from Silver2Coin import Silver2Coin
from SilverBox import SilverBox
from Statistics import Statistics
from Task import Task
from Sentence import Sentence
from Timer import Timer
from config import config
from configcheck import ConfigCheck
from API import API

# 检查Config
ConfigCheck()

# 初始化所有class
API = API()
Auth = Auth()
Capsule = Capsule()
Coin2Silver = Coin2Silver()
DailyBag = DailyBag()
GiftSend = GiftSend()
Group = Group()
Heart = Heart()
Silver2Coin = Silver2Coin()
SilverBox = SilverBox()
Task = Task()
rafflehandler = RaffleHandler()

# 开启时清理日志
Log.clean_log(startup=True)

if config["Other"]["INFO_MESSAGE"] != "False":
    Log.info("BiliBiliHelper Python Beta v0.0.3")

Log.info("Powered By TheWanderingCoel")

if config["Other"]["SENTENCE"] != "False":
    Log.info(Sentence().get_sentence())

loop = asyncio.get_event_loop()

timer = Timer(loop)
console = Console.Console(loop)

area_ids = [1,2,3,4,5,6,]
Statistics(len(area_ids))
danmu_tasks = [Danmu_Monitor.run_Danmu_Raffle_Handler(i) for i in area_ids]
other_tasks = [
    rafflehandler.run()
]

api_thread = threading.Thread(target=API.work)
api_thread.start()

console_thread = threading.Thread(target=console.cmdloop)
console_thread.start()

# 先登陆一次,防止速度太快导致抽奖模块出错
Auth.work()

def daily_job():
    while (1):
        Auth.work()
        Capsule.work()
        Coin2Silver.work()
        DailyBag.work()
        GiftSend.work()
        Group.work()
        Heart.work()
        Silver2Coin.work()
        SilverBox.work()
        Task.work()
        # 休息0.5s,减少CPU占用
        time.sleep(0.5)

daily_job_thread = threading.Thread(target=daily_job)
daily_job_thread.start()

if config["Function"]["RAFFLE_HANDLER"] != "False":
    loop.run_until_complete(asyncio.wait(danmu_tasks+other_tasks))

api_thread.join()
console_thread.join()
daily_job_thread.join()

loop.close()
