import MT5Manager,zmq,json
import time
context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.bind("tcp://192.168.15.61:5561")
# https://support.metaquotes.net/en/docs/mt5/api/managerapi_python
# wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5admindebian.sh
# https://github.com/MTsocketAPI/MT5-API/blob/main/Python/Example%203%20-%20Stream%20actual%20EURUSD%20price%20from%20MT5.py
# https://support.metaquotes.net/en/articles/1589
# https://support.metaquotes.net/en/docs/mt5/api/managerapi


# https://stackoverflow.com/questions/19581059/misconf-redis-is-configured-to-save-rdb-snapshots
# https://www.linuxquestions.org/questions/linux-newbie-8/centos-disk-used-100-a-4175642630/

class TickSink:
    def OnTick(self, symbol, tick : MT5Manager.MTTickShort):
        
        msg={'scripcode':symbol,'ltp':(tick.bid+tick.ask)/2,'ltq':0.0,'bid':tick.bid,'bidqty':0.0,'ask':tick.ask,'askqty':0.0}
        
        # if 'GC.Q24' in str(symbol):
        #     print(msg)
        
        try:
            
            print(json.dumps(msg).encode('utf-8'))
            zmq_socket.send(json.dumps(msg).encode('utf-8'))
        except Exception as e :
            print(e)
            pass

    def OnTickStat(self, stat : MT5Manager.MTTickStat):
        pass

class Mt5_feeds:
    def __init__(self):

        with open('config.json') as f:
            config_data = json.load(f)

        manager = MT5Manager.ManagerAPI()
        sink = TickSink()

        if not manager.TickSubscribe(sink):
            print(f"Failed to subscribe: {MT5Manager.LastError()}")
        else:
            if manager.Connect(
                config_data.get('mts_login').get('server'), 
                config_data.get('mts_login').get('login'), 
                config_data.get('mts_login').get('password'), 
                MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS):
                print("Connected to server")
                for add_symbol in config_data.get('add_symbols'):
                    if not manager.SelectedAdd(add_symbol):
                        print(f"Failed to select symbol: {MT5Manager.LastError()}")
                while True:
                    pass
                # manager.Disconnect()
            else:
                print(f"Failed to connect to server: {MT5Manager.LastError()}")
            if not manager.TickUnsubscribe(sink):
                print(f"Failed to unsubscribe: {MT5Manager.LastError()}")

Mt5_feeds() 