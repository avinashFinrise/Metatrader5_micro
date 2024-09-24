import MT5Manager,zmq,json
import time


class Mt5_feeds:
    def __init__(self):

        # with open('config.json') as f:
        #     config_data = json.load(f)

        manager = MT5Manager.ManagerAPI()
        if manager.Connect(
            "159.100.13.166:443", 
            1015, 
            "lshqd6tu", 
            MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL):
            print("Connected to server")
            login = [70001, 80001]
            print("================ getting started =============")
            time.sleep(2)
            for i in login:
                # data = manager.UserAccountRequestArray
                data = manager.UserAccountGet(i)
                print(dir(data))
                print("Assets: ",data.Profit)
                print("Equity: ", data.Equity)
                print("Assets: ", data.Assets)
                print("Balance: ", data.Balance)
                print("BlockedCommission: ", data.BlockedCommission)
                print("BlockedProfit: ", data.BlockedProfit)
                print("Credit: ", data.Credit)
                print("CurrencyDigits: ", data.CurrencyDigits)
                print("EnSoActivation: ", data.EnSoActivation)
                print("Floating: ", data.Floating)
                print("Liabilities: ", data.Liabilities)
                print("Login: ", data.Login)
                print("Margin: ", data.Margin)
                print("MarginFree: ", data.MarginFree)
                print("MarginInitial: ", data.MarginInitial)
                print("MarginLevel: ", data.MarginLevel)
                print("MarginLeverage: ", data.MarginLeverage)
                print("MarginMaintenance: ", data.MarginMaintenance)
                print("ObsoleteValue: ", data.ObsoleteValue)
                print("Profit: ", data.Profit)
                print("SOActivation: ", data.SOActivation)
                print("SOEquity: ", data.SOEquity)
                print("SOLevel: ", data.SOLevel)
                print("SOMargin: ", data.SOMargin)
                print("SOTime: ", data.SOTime)
                print("Storage: ", data.Storage)
                print(f"================={i}=======================")
            # print("SOTime: ", data.SOTime)

            
            manager.Disconnect()
        else:
            print(f"Failed to connect to server: {MT5Manager.LastError()}")
            

Mt5_feeds() 