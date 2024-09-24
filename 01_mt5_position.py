# include the library
import MT5Manager
# include module to use delays
import time
# create class to track positions
class PositionSink:
    # add position
    def OnPositionAdd(self, position):
        print(f"Position added: {position.Print()}")
    # update position
    def OnPositionUpdate(self, position):
        print(f"Position updated: {position.Print()}")
# create manager interface
manager = MT5Manager.ManagerAPI()
# create class to track positions
sink = PositionSink()
# subscribe to position changes
# OrderGet
if not manager.PositionSubscribe(sink):
    print(f"Failed to subscribe: {MT5Manager.LastError()}")
else:
    # connect the server
    if manager.Connect("185.96.244.53:443", 8057, "P-W7DgAy",
                       MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_POSITIONS,
                       300000):
        # connected to the server
        print("Connected to server")
        while True:
            position = manager.PositionRequestByLogins([90001,90003,123154, 123410, 123411, 123451, 123453, 123454, 123630])
            # position = manager.Posi
            print(position)
            # if position:
            #     for val in position:
            #         data = {
            #             "Login": val.Login,
            #             "Symbol": val.Symbol,
            #             "Volume": val.Volume/10000,
            #             "PriceOpen": val.PriceOpen,
            #             "PriceCurrent": val.PriceCurrent,
            #             "Profit": val.Profit,
            #             "Storage": val.Storage,
            #             "Action": val.Action,
            #             "ContractSize": val.ContractSize,
            #             "Dealer": val.Dealer,
            #             "Digits": val.Digits,
            #             "DigitsCurrency": val.DigitsCurrency,
            #             "ObsoleteValue": val.ObsoleteValue,
            #             "Position": val.Position,
            #             "PriceSL": val.PriceSL,
            #             "PriceTP": val.PriceTP,
            #             "RateMargin": val.RateMargin,
            #             "RateProfit": val.RateProfit,
            #         }
            #         print(data)
                
            #     print('data has been send')

        # watch position changes within 60 seconds
        # for s in range(6):
        #     time.sleep(10)
        #     print(".")
        # disconnect from the server
        manager.Disconnect()
    else:
        # failed to connect to the server
        print(f"Failed to connect to server: {MT5Manager.LastError()}")
    # unsubscribe from position changes
    if not manager.PositionUnsubscribe(sink):
        print(f"Failed to unsubscribe: {MT5Manager.LastError()}")