class Statistics:
    def __init__(self,area_num=0):
        self.area_num = area_num
        self.pushed_raffles = {}

        self.joined_raffles = {}
        self.raffle_results = {}

        self.raffle_ids = []

    def print_statistics(self):
        print("本次推送抽奖统计")
        for k,v in self.pushed_raffles.items():
            if isinstance(v,int):
                print(f'{v:^5} X {k}')
            else:
                print(f'{v:^5.2f} X {k}')
        print()

        self.print_one_stats()
    
    def print_one_stats(self):
        print('本次参与抽奖统计：')
        joined_of_id = self.joined_raffles.get()
        for k, v in joined_of_id.items():
            print(f'{v:^5} X {k}')
        print()
            
        print('本次抽奖结果统计：')
        results_of_id = self.raffle_results.get(id, {})
        for k, v in results_of_id.items():
            print(f'{v:^5} X {k}')
    
    def add2pushed_raffles(self,raffle_name,broadcast_type,num):
        origin_num = self.pushed_raffles.get(raffle_name,0)
        # broadcast_type 广播类型 0 全区广播 1 分区广播 2 本房间
        if broadcast_type == 0:
            self.pushed_raffles[raffle_name] = origin_num + num / self.area_num
        else:
            self.pushed_raffles[raffle_name] = origin_num + num

    def add2joined_raffles(self,raffle_name,num):
        raffles_of_id = self.joined_raffles[0]
        raffles_of_id[raffle_name] = raffles_of_id.get(raffle_name,0) + num

    def add2results(self,gift_name,num=1):
        results_of_id  = self.raffle_results[0]
        results_of_id[gift_name] = results_of_id.get(gift_name,0) + num

    def add2raffle_ids(self,raffle_id):
        self.raffle_ids.append(raffle_id)

        if len(self.raffle_ids) > 150:
            del self.raffle_ids[:75]
        
    def is_raffleid_duplicate(self,raffle_id):
        return (raffle_id in self.raffle_ids)

var = Statistics()

def add2pushed_raffles(raffle_name,broadcast_type=0,num=1):
    var.add2push_raffles(raffle_name,broadcast_type,int(num))

def add2joined_raffles(raffle_name,num=1):
    var.add2joined_raffles(raffle_name,int(num))

def add2results(gift_name,num=1):
    var.add2results(gift_name,int(num))

def add2raffle_ids(raffle_id):
    var.add2raffle_ids(int(raffle_id))

def is_raffleid_duplicate(raffle_id):
    return var.is_raffleid_duplicate(int(raffle_id))