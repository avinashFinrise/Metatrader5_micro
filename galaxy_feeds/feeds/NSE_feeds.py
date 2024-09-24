import MT5Manager,zmq,json
import time
import pandas as pd

# context = zmq.Context()
# zmq_socket = context.socket(zmq.PUB)
# zmq_socket.bind("tcp://192.168.15.61:5561")
# https://support.metaquotes.net/en/docs/mt5/api/managerapi_python
# wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5admindebian.sh
# https://github.com/MTsocketAPI/MT5-API/blob/main/Python/Example%203%20-%20Stream%20actual%20EURUSD%20price%20from%20MT5.py
# https://support.metaquotes.net/en/articles/1589
# https://support.metaquotes.net/en/docs/mt5/api/managerapi


# https://stackoverflow.com/questions/19581059/misconf-redis-is-configured-to-save-rdb-snapshots
# https://www.linuxquestions.org/questions/linux-newbie-8/centos-disk-used-100-a-4175642630/


with open('../store/settings/settings.json') as f:
            settings_data = json.load(f)

context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.bind(settings_data.get("zmq_connection").get("nse_connection"))

class TickSink:
    def OnTick(self, symbol, tick : MT5Manager.MTTickShort):
        
        if '.' in str(symbol):
            msg={'scripcode':symbol,'ltp':(tick.bid+tick.ask)/2,'ltq':0.0,'bid':tick.bid,'bidqty':0.0,'ask':tick.ask,'askqty':0.0}
            
            # if 'GC.Q24' in str(symbol):
            #     print(msg)
            
            try:
                zmq_socket.send(json.dumps(msg).encode('utf-8'))
                print(json.dumps(msg).encode('utf-8'))
            except Exception as e :
                print(e)
                pass

    def OnTickStat(self, stat : MT5Manager.MTTickStat):
        pass

class NSE_feeds:
    def __init__(self):

        if settings_data:
            print(settings_data.get("zmq_connection").get("nse_connection"))
            manager = MT5Manager.ManagerAPI()
            sink = TickSink()

            NSE_symbol_list = self.read_contract_file(settings_data.get('nse_contract_file_path'))

            


            if not manager.TickSubscribe(sink):
                print(f"Failed to subscribe: {MT5Manager.LastError()}")
            else:
                print(settings_data.get('nse_login').get('server'), 
                    settings_data.get('nse_login').get('login'), 
                    settings_data.get('nse_login').get('password'))
                if manager.Connect(
                    settings_data.get('nse_login').get('server'), 
                    settings_data.get('nse_login').get('login'), 
                    settings_data.get('nse_login').get('password'), 
                    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS):
                    print("Connected to server")
                    # NSE_symbol_list = ["SIEMENS.Q24", "POLYCAB.Q24", "VEDL.Q24"]
                    for symbol in NSE_symbol_list:
                        print(symbol)
                        if not manager.SelectedAdd(symbol):
                            print(f"Failed to select symbol: {MT5Manager.LastError()}")
                        else:
                            print("SYMBOL ADDED")
                    
                    # if not manager.SelectedAdd('PNB.Q24'):
                    #     print(f"Failed to select symbol: {MT5Manager.LastError()}")
                    # else:
                    #     print("SYMBOL ADDED")
                    while True:
                        pass
                    manager.Disconnect()
                else:
                    print(f"Failed to connect to server: {MT5Manager.LastError()}")
                if not manager.TickUnsubscribe(sink):
                    print(f"Failed to unsubscribe: {MT5Manager.LastError()}")
                print("==============================================================")
    def read_contract_file(self, path):
        print("========= reading contract file  =================")
        NSE_contract_df = pd.read_csv(path)
        NSE_contract_df = NSE_contract_df[['Exchange', 'Symbol', 'Security ID']].rename(
            columns={'Exchange':"exchange", 'Symbol':"symbol", 'Security ID':"security_id"}).reset_index(drop=True)
        return set(NSE_contract_df['security_id'])

NSE_feeds() 