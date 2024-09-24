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
from utils.ConnectToAPI import ConnectToAPI

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
    try:
        print(print(f"Position details: {position.Print()}"))
        time_create = datetime.fromtimestamp(getattr(position, 'TimeCreate', 'TimeCreate attribute not found'))
        time_update = datetime.fromtimestamp(getattr(position, 'TimeUpdate', 'TimeUpdate attribute not found'))

        # Format the datetime object into a readable string
        time_create = time_create.strftime('%Y-%m-%d')
        time_update = time_update.strftime('%Y-%m-%d')
        msg = {
                "event": event,
                "userid": getattr(position, 'Login', 'Login attribute not found'),
                "symbol" : getattr(position, 'Symbol', 'Symbol attribute not found'),
                "action" : getattr(position, 'Action', 'Action attribute not found'),
                # "contractSize" : getattr(position, 'ContractSize', 'ContractSize attribute not found'),
                "price_current" : getattr(position, 'PriceCurrent', 'PriceCurrent attribute not found'),
                "price_open" : getattr(position, 'PriceOpen', 'PriceOpen attribute not found'),
                "price_sl" : getattr(position, 'PriceSL', 'PriceSL attribute not found'),
                "price_tp" : getattr(position, 'PriceTP', 'PriceTP attribute not found'),
                "profit" : getattr(position, 'Profit', 'Profit attribute not found'),
                "rate_margin" : getattr(position, 'RateMargin', 'RateMargin attribute not found'),
                "rate_profit" : getattr(position, 'RateProfit', 'RateProfit attribute not found'),
                "time_create" : str(time_create),
                "time_update" : str(time_update),
                "dealer" : getattr(position, 'Dealer', 'Dealer attribute not found'),
                "digits" : getattr(position, 'Digits', 'Digits attribute not found'),
                "expert_id" : getattr(position, 'ExpertID', 'ExpertID attribute not found'),
                "expert_position_id" : getattr(position, 'ExpertPositionID', 'ExpertPositionID attribute not found'),
                "external_id" : getattr(position, 'ExternalID', 'ExternalID attribute not found'),
                "modification_flags" : getattr(position, 'ModificationFlags', 'ModificationFlags attribute not found'),
                "obsolete_value" : getattr(position, 'ObsoleteValue', 'ObsoleteValue ModificationFlags not found'),
                "activation_flags" : getattr(position, 'ActivationFlags', 'ActivationFlags ModificationFlags not found'),
                "activation_price" : getattr(position, 'ActivationPrice', 'ActivationPrice ModificationFlags not found'),
                "comment" : getattr(position, 'Comment', 'Comment ModificationFlags not found'),
                "contract_size" : getattr(position, 'ContractSize', 'ContractSize ModificationFlags not found'),
                "volume" : getattr(position, 'Volume', 'Volume attribute not found')
            }
        # print(msg)
    except Exception as e:
        print("error on generating msg: ", e)
    print("================ position msg has been generated ====================")
    return msg

def make_pg_query(msg):
    print("================ start generation query ====================")
    query = f"""
                INSERT INTO public.mt5_trades_log(
                createddate, updateddate, event, userid, symbol, action, contract_size, price_current, price_sl, 
                price_tp, profit, rate_margin, rate_profit, price_open, time_create, time_update, dealer, digits, expert_id, expert_position_id, 
                external_id, modification_flags, obsolete_value, activation_flags, activation_price, comment, volume)
                VALUES ('{datetime.now()}', '{datetime.now()}', '{msg.get('event')}', {msg.get('userid')}, '{msg.get('symbol')}', {msg.get('action')}, {msg.get('contract_size')}, 
                {msg.get('price_current')},{msg.get('price_sl')}, {msg.get('price_tp')},{msg.get('profit')}, {msg.get('rate_margin')}, {msg.get('rate_profit')},
                {msg.get('price_open')}, '{msg.get('time_create')}', '{msg.get('time_update')}', {msg.get('dealer')}, {msg.get('digits')}, {msg.get('expert_id')}, {msg.get('expert_position_id')},
                '{msg.get('external_id')}',{msg.get('modification_flags')},{msg.get('obsolete_value')}, {msg.get('activation_flags')}, {msg.get('activation_price')}, '{msg.get('comment')}', 
                {msg.get('volume')});
                """
    print(query)
    print("================ query has been generated ====================")
    return query

class PositionSink():
    def OnPositionAdd(self, position):
        print("==================== position added =================")
        msg = position_msg(position, "add")
        pg_query = make_pg_query(msg)
        self.save_send_msg(msg, pg_query)
        # print(f"Position added: {position.Print()},")
        # print(f"Position details: {dir(position)}")

    def OnPositionUpdate(self, position):
        print("==================== position updated =================")
        msg = position_msg(position, "update")
        # websocket_connection.send(json.dumps({'event':'logs', 'data':msg}))
        pg_query = make_pg_query(msg)
        self.save_send_msg(msg, pg_query)
        # DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position updated: {position.Print()}")
        # print(f"Position details: {dir(position)}")

    def OnPositionDelete(self, position):
        print("==================== position deleted =================")
        msg = position_msg(position, "delete")
        # print("websocket_connection", websocket_connection)
        # websocket_connection.send(json.dumps({'event':'logs', 'data':msg}))
        pg_query = make_pg_query(msg)
        self.save_send_msg(msg, pg_query)
        # DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position delete: {position.Print()}")
        # print(f"Position details: {dir(position)}")
    
    def OnPositionClean(self, position):
        msg = position_msg(position, "clean")
        pg_query = make_pg_query(msg)
        # DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position clean: {position.Print()}")
        # print(f"Position details: {dir(position)}")
        print("==================== position cleaned =================")

    def OnPositionSync(self):
        # msg = position_msg(position, "sync")
        # pg_query = make_pg_query(msg)
        # DatabaseConnection.executeQueryPG(con, pg_query)
        # print(f"Position sync: {position.Print()}")
        # print(f"Position details: {dir(position)}")
        print("==================== position Sync =================")
    
    def reconnect_websocket(self):
        global websocket_connection
        data = settings_data.get('login')
        websocket_connection = ConnectToAPI.connectWebSocket(data)
    
    def save_send_msg(self, msg, pg_query):
        try:
            print(msg)
            filter_data = ["event", "userid", "symbol", "contractSize", "price_current", "profit", "price_open", "expert_position_id", "volume"]
            msg_to_send = {k:v for k, v in msg.items() if k in filter_data} 

            websocket_connection.send(json.dumps({'event':'logs', 'data':msg_to_send}))
            DatabaseConnection.executeQueryPG(con, pg_query)
        except Exception as e:
            self.reconnect_websocket()
            websocket_connection.send(json.dumps({'event':'logs', 'data':msg}))
            DatabaseConnection.executeQueryPG(con, pg_query)
            print("WebSocket connection could not be established.")
            print("Error on sending msg: ", e)



class MT5_TradeInfo(ConnectToAPI):
    def __init__(self):
        super().__init__()
        # cpu_affinity_mask = 0b00001101
        # pid = str(os.getpid())
        # subprocess.call(["taskset", "-p", hex(cpu_affinity_mask), pid])

       
        self.manager = MT5Manager.ManagerAPI()
        self.sink = PositionSink()
    
    def subscribeTrades(self):
        if not self.manager.PositionSubscribe(self.sink):
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

MT5_TradeInfo().subscribeTrades()
        


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