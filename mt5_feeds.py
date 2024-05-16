import MT5Manager,zmq,json
import time
context = zmq.Context()
zmq_socket = context.socket(zmq.PUB)
zmq_socket.bind("tcp://192.168.15.61:5561")
# https://support.metaquotes.net/en/docs/mt5/api/managerapi_python
# wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt5/mt5admindebian.sh
# https://github.com/MTsocketAPI/MT5-API/blob/main/Python/Example%203%20-%20Stream%20actual%20EURUSD%20price%20from%20MT5.py
# https://support.metaquotes.net/en/articles/1589
class TickSink:
    def OnTick(self, symbol, tick : MT5Manager.MTTickShort):
        # print(symbol,tick.bid,tick.last,tick.datetime_msc)
        # print(symbol)
        # print("====================== ontick called ========================")
        msg={'scripcode':symbol,'ltp':(tick.bid+tick.ask)/2,'ltq':0.0,'bid':tick.bid,'bidqty':0.0,'ask':tick.ask,'askqty':0.0}
        # msg={'scripcode':symbol,'ltp':tick.last,'ltq':0.0,'bid':tick.bid,'bidqty':0.0,'ask':tick.ask,'askqty':0.0}
        # if symbol == 'XAUUSD':
        #     print(msg)
        # msg={'scripcode':symbol,'ltp':(tick.bid+tick.ask)/2,'ltq':tick.volume,'bid':tick.bid,'bidqty':0.0,'ask':tick.ask,'askqty':tick.ask_qty}
        # print(msg)
        # if str(symbol).startswith('IDX'):
        # if str(symbol).startswith('AUDCHF'):
        #     print(msg)
        # print(msg)
        # if str(symbol)=='AUDCHF':
        #     print(msg)
        #     time.sleep(1)
        # if str(symbol).startswith('DAX'):
        #     print(msg)
        #     time.sleep(1)
        # if str(symbol).startswith('XAUUSD'):
        #     print(msg)
        #     time.sleep(1)
        # if 'ZUI' in str(symbol):
        #     print(msg)
        #     time.sleep(1)
        try:
            zmq_socket.send(json.dumps(msg).encode('utf-8'))
            # print("============================ mssg has been send ============================")
        except Exception as e :
            print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
            print(e)
            print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")

            pass
        # print(f"tick: {symbol} \t {tick.bid:.5f} \t {tick.ask:.5f}")
    def OnTickStat(self, stat : MT5Manager.MTTickStat):
        pass
        # print(f"stat: {datetime.datetime.fromtimestamp(stat.datetime)} \t {stat.bid_high} \t {stat.bid_low} \t {stat.ask_high} \t {stat.ask_low}")

class Mt5_feeds:
    def __init__(self):
        manager = MT5Manager.ManagerAPI()
        sink = TickSink()
        if not manager.TickSubscribe(sink):
            print(f"Failed to subscribe: {MT5Manager.LastError()}")
        else:
            if manager.Connect("185.96.244.53:443", 8048, "Spectra@123", MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS):
                print("Connected to server")
                while True:
                    pass
                # manager.Disconnect()
            else:
                print(f"Failed to connect to server: {MT5Manager.LastError()}")
            if not manager.TickUnsubscribe(sink):
                print(f"Failed to unsubscribe: {MT5Manager.LastError()}")

Mt5_feeds() 