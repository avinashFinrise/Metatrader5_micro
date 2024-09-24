import MT5Manager
import time
import json
import sys
from datetime import datetime
import os
import subprocess

with open('../galaxy_feeds/store/settings/settings.json') as f:
            settings_data = json.load(f)

path = settings_data.get("projectDir")
sys.path.append(path)
from utils.util import DatabaseConnection
from utils.ConnectToAPI_copy import ConnectToAPI

if settings_data:
    pg_connection = settings_data.get("pg_connection")     
    print(pg_connection)
    try:
        con = DatabaseConnection.pg_connection(pg_connection)
        data = settings_data.get('login')
        ConnectToAPI._login(data)
        websocket_connection = ConnectToAPI.connectWebSocket(data)
        print(websocket_connection)
        # self._login(data)
        # self.connectWebSocket()
        # print(self.websocket)
    except Exception as e:
        print(e)


def position_msg(position, event):
    # print(print(f"Position details: {dir(position)}"))
    print(print(f"Position details: {position.Print()}"))
    msg = {
            "event": event,
            "login_id": getattr(position, 'Login', 'Login attribute not found'),
            "symbol" : getattr(position, 'Symbol', 'Symbol attribute not found'),
            "action" : getattr(position, 'Action', 'Action attribute not found'),
            "contractSize" : getattr(position, 'ContractSize', 'ContractSize attribute not found'),
            "price_current" : getattr(position, 'PriceCurrent', 'PriceCurrent attribute not found'),
            "price_open" : getattr(position, 'PriceOpen', 'PriceOpen attribute not found'),
            "price_sl" : getattr(position, 'PriceSL', 'PriceSL attribute not found'),
            "price_tp" : getattr(position, 'PriceTP', 'PriceTP attribute not found'),
            "profit" : getattr(position, 'Profit', 'Profit attribute not found'),
            "rate_margin" : getattr(position, 'RateMargin', 'RateMargin attribute not found'),
            "rate_profit" : getattr(position, 'RateProfit', 'RateProfit attribute not found'),
            "time_create" : getattr(position, 'TimeCreate', 'TimeCreate attribute not found'),
            "time_update" : getattr(position, 'TimeUpdate', 'TimeUpdate attribute not found'),
            "Dealer" : getattr(position, 'Dealer', 'Dealer attribute not found'),
            "Digits" : getattr(position, 'Digits', 'Digits attribute not found'),
            "ExpertID" : getattr(position, 'ExpertID', 'ExpertID attribute not found'),
            "ExpertPositionID" : getattr(position, 'ExpertPositionID', 'ExpertPositionID attribute not found'),
            "ExternalID" : getattr(position, 'ExternalID', 'ExternalID attribute not found'),
            "ModificationFlags" : getattr(position, 'ModificationFlags', 'ModificationFlags attribute not found'),
            "ObsoleteValue" : getattr(position, 'ObsoleteValue', 'ObsoleteValue ModificationFlags not found'),
            "ActivationFlags" : getattr(position, 'ActivationFlags', 'ActivationFlags ModificationFlags not found'),
            "ActivationPrice" : getattr(position, 'ActivationPrice', 'ActivationPrice ModificationFlags not found'),
            "Comment" : getattr(position, 'Comment', 'Comment ModificationFlags not found'),
            "ContractSize" : getattr(position, 'ContractSize', 'ContractSize ModificationFlags not found'),
            "volume" : getattr(position, 'Volume', 'Volume attribute not found')
        }
    # print(msg)
    return msg

def make_pg_query(msg):
    query = f"""
                INSERT INTO public.mt5_trades_log(
                createddate, updateddate, event, userid, symbol, action, contract_size, price_current, price_sl, 
                price_tp, profit, rate_margin, rate_profit, price_open, time_create, time_update, dealer, digits, expert_id, expert_position_id, 
                external_id, modification_flags, obsolete_value, activation_flags, activation_price, comment, volume)
                VALUES ('{datetime.now()}', '{datetime.now()}', '{msg.get('event')}', {msg.get('login_id')}, '{msg.get('symbol')}', {msg.get('action')}, {msg.get('contractSize')}, 
                {msg.get('price_current')},{msg.get('price_sl')}, {msg.get('price_tp')},{msg.get('profit')}, {msg.get('rate_margin')}, {msg.get('rate_profit')},
                {msg.get('price_open')}, '2024-08-08', '2024-08-08', {msg.get('Dealer')}, {msg.get('Digits')}, {msg.get('ExpertID')}, {msg.get('ExpertPositionID')},
                '{msg.get('ExternalID')}',{msg.get('ModificationFlags')},{msg.get('ObsoleteValue')}, {msg.get('ActivationFlags')}, {msg.get('ActivationPrice')}, '{msg.get('Comment')}', 
                {msg.get('volume')});
                """
    return query

class PositionSink():
    def OnPositionAdd(self, position):
        msg = position_msg(position, "add")
        pg_query = make_pg_query(msg)
        print(websocket_connection)
        websocket_connection.send(json.dumps({'event':'logs', 'data':msg}))
        DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position added: {position.Print()},")
        # print(f"Position details: {dir(position)}")
        print("==================== position added =================")

    def OnPositionUpdate(self, position):
        msg = position_msg(position, "update")
        print(websocket_connection)
        websocket_connection.send(json.dumps({'event':'logs', 'data':msg}))
        pg_query = make_pg_query(msg)
        DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position updated: {position.Print()}")
        # print(f"Position details: {dir(position)}")
        print("==================== position updated =================")

    def OnPositionDelete(self, position):
        msg = position_msg(position, "delete")
        print(websocket_connection)
        websocket_connection.send(json.dumps({'event':'logs', 'data':msg}))
        pg_query = make_pg_query(msg)
        DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position delete: {position.Print()}")
        # print(f"Position details: {dir(position)}")
        print("==================== position deleted =================")
    
    def OnPositionClean(self, position):
        msg = position_msg(position, "clean")
        pg_query = make_pg_query(msg)
        # DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position clean: {position.Print()}")
        # print(f"Position details: {dir(position)}")
        print("==================== position cleaned =================")

    def OnPositionSync(self, position):
        msg = position_msg(position, "sync")
        pg_query = make_pg_query(msg)
        # DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position sync: {position.Print()}")
        # print(f"Position details: {dir(position)}")
        print("==================== position Sync =================")


class MT5_TradeInfo(ConnectToAPI):
    def __init__(self):
        super().__init__()
        subscriptionMSG = {
            "event":"subscribe",
            "stream":"logs",
            "data":{
                
            }
        }
        self.recieveWebsocket(subscriptionMSG)
        # cpu_affinity_mask = 0b00001101
        # pid = str(os.getpid())
        # subprocess.call(["taskset", "-p", hex(cpu_affinity_mask), pid])

       
        self.manager = MT5Manager.ManagerAPI()
        self.sink = PositionSink()
    
    def recieveWebsocket(self,msg):
        print("=============== subscribe =====================", msg)
        websocket_connection.send(json.dumps(msg))
        print(websocket_connection.recv())
        while 1>0:
            try:
                data = json.loads(websocket_connection.recv())
                if data.get('event')=='logs' :
                    print(data)
            except:
                pass
    
    def subscribeTrades(self):
        if not self.manager.DealSubscribe(self.sink):
            print(f"Failed to subscribe: {MT5Manager.LastError()}")
        else:
            if self.manager.Connect("159.100.13.166:443", 1014, "Galaxy#@7890",
                            MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_POSITIONS,
                            300000):
                print("Connected to server")
                
                while True:
                    pass
                self.manager.Disconnect()
            else:
                print(f"Failed to connect to server: {MT5Manager.LastError()}")
            if not self.manager.PositionUnsubscribe(self.sink):
                print(f"Failed to unsubscribe: {MT5Manager.LastError()}")

MT5_TradeInfo()
        


# manager = MT5Manager.ManagerAPI()
# sink = PositionSink()
# if not manager.PositionSubscribe(sink):
#     print(f"Failed to subscribe: {MT5Manager.LastError()}")
# else:
#     if manager.Connect("159.100.13.166:443", 1014, "Galaxy#@7890",
#                        MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_POSITIONS,
#                        300000):
#         print("Connected to server")
        
#         while True:
#             pass
#         manager.Disconnect()
#     else:
#         print(f"Failed to connect to server: {MT5Manager.LastError()}")
#     if not manager.PositionUnsubscribe(sink):
#         print(f"Failed to unsubscribe: {MT5Manager.LastError()}")