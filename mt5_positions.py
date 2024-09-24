# include the library
import MT5Manager
# include module to use delays
import time
# create class to track positions
class PositionSink:
    # add position
    def OnPositionAdd(self, position: MT5Manager.MTPosition):
        print(f"Position added: {position.Print()}")
        print(f"Login: {position.Login}")
        print(f"Symbol: {position.Symbol}")
        print(f"Volume: {position.Volume/10000}")
        print(f"PriceOpen: {position.PriceOpen}")
        print(f"PriceCurrent: {position.PriceCurrent}")
        print(f"Profit: {position.Profit}")
        print(f"Position: {position.Position}")
    
    def OnTradeProfit(self, position: MT5Manager.MTPosition):
        print(f"TradeProfit: {position.Print()}")
        print(f"Login: {position.Login}")
        print(f"PriceOpen: {position.PriceOpen}")
        print(f"PriceCurrent: {position.PriceCurrent}")
        print(f"Profit: {position.Profit}")
        print(f"Position: {position.Position}")
    # update position
    def OnPositionUpdate(self, position: MT5Manager.MTPosition):
        print(f"Position updated: {position.Print()}")
        print(f"Login: {position.Login}")
        print(f"PriceOpen: {position.PriceOpen}")
        print(f"PriceCurrent: {position.PriceCurrent}")
        print(f"Profit: {position.Profit}")
        print(f"Position: {position.Position}")
    def OnPositionUpdateBatch(self, position: MT5Manager.MTPosition):
        print(f"Position update batch: {position.Print()}")
        print(f"Login: {position.Login}")
        print(f"PriceOpen: {position.PriceOpen}")
        print(f"PriceCurrent: {position.PriceCurrent}")
        print(f"Profit: {position.Profit}")
        print(f"Position: {position.Position}")
# create manager interface
manager = MT5Manager.ManagerAPI()
# create class to track positions
sink = PositionSink()
print(sink)
# subscribe to position changes
if not manager.PositionSubscribe(sink):
    print(f"Failed to subscribe: {MT5Manager.LastError()}")
else:
    # connect the server
    mt5_server = "185.96.244.53:443"
    mt5_login = 8057  # Your manager account number
    mt5_password = "P-W7DgAy"
    if manager.Connect(mt5_server, mt5_login, mt5_password,
                       MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_POSITIONS,
                       300000):
        # connected to the server
        print("Connected to server")
        positions_list = []
        try:
            while True:
                user_list = (90001, 90003)
                positions = manager.PositionRequest(90001)
                print(positions)
                if positions:
                    # print(f"Login: {positions[0].Login} Position: {positions[0].Position} Profit: {positions[0].Profit}")
                    sumprofit = 0
                    for position in positions:
                        sumprofit += position.Profit
                        
                        # print(f"Login: {position.Login} Position: {position.Position} Profit: {position.Profit}")
                        # print(dir(position))
                        data = {
                            "Login": position.Login,
                            "Symbol": position.Symbol,
                            "Volume": position.Volume/10000,
                            "PriceOpen": position.PriceOpen,
                            "PriceCurrent": position.PriceCurrent,
                            "Profit": position.Profit,
                            "Storage": position.Storage,
                            "Action": position.Action,
                            "ContractSize": position.ContractSize,
                            "Dealer": position.Dealer,
                            "Digits": position.Digits,
                            "DigitsCurrency": position.DigitsCurrency,
                            "ObsoleteValue": position.ObsoleteValue,
                            "Position": position.Position,
                            "PriceSL": position.PriceSL,
                            "PriceTP": position.PriceTP,
                            "RateMargin": position.RateMargin,
                            "RateProfit": position.RateProfit,
                                        # "Comment": position.Comment
                        }
                        positions_list.append(data)
                    # print(f"Login: {position.Login} NetProfit: {sumprofit}")
                        print("data ======================> ", data)
                # watch position changes within 60 seconds
        
                # for i in positions_list:
                # print(f"Login: {positions_list[0]['Login']} Position: {position.Position} Profit: {positions_list[0]['Profit']}")
                time.sleep(2)
        #         # Keep the connection alive
        #         time.sleep(10)
        except KeyboardInterrupt:
            print("Stopping position polling")
            manager.Disconnect()
        # disconnect from the server
        
    else:
        # failed to connect to the server
        print(f"Failed to connect to server: {MT5Manager.LastError()}")
    # unsubscribe from position changes
    if not manager.PositionUnsubscribe(sink):
        print(f"Failed to unsubscribe: {MT5Manager.LastError()}")