# include the library
import MT5Manager
# include module to use delays
import time
# include module for handling dates
import datetime
# create class to track quotes
class TickSink:
    # new quote
    def OnTick(self, symbol, tick : MT5Manager.MTTickShort):
        print(f"tick: {symbol} \t {tick.bid:.5f} \t {tick.ask:.5f}")
    # update statistical data on prices
    def OnTickStat(self, stat : MT5Manager.MTTickStat):
        print(f"stat: {datetime.datetime.fromtimestamp(stat.datetime)} \t "
              f"{stat.bid_high} \t {stat.bid_low} \t {stat.ask_high} \t {stat.ask_low}")
# create manager interface
manager = MT5Manager.ManagerAPI()
# create class to track quotes
sink = TickSink()
# subscribe to quote changes
if not manager.TickSubscribe(sink):
    print(f"Failed to subscribe: {MT5Manager.LastError()}")
else:
    # connect the server
    # enable pumping of symbols, this will allow to add EURUSD to the list of selected symbols
    # if manager.Connect("192.168.12.59:1950", 1001, "Spectra@401", MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS):
    if manager.Connect("185.96.244.53:443", 8048, "Spectra@123", MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS):
        # connected to the server
        print("Connected to server")
        # Add "EURUSD" to the list of selected symbols in order to receive the quotes
        if not manager.SelectedAdd("GC.Q24")or not manager.SelectedAdd("GBPUSD"):
            print(f"Failed to select symbol: {MT5Manager.LastError()}")
        # expect data within a minute
        time.sleep(60)
        # disconnect from the server
        manager.Disconnect()
    else:
        # failed to connect to the server
        print(f"Failed to connect to server: {MT5Manager.LastError()}")
    # unsubscribe from changes
    if not manager.TickUnsubscribe(sink):
        print(f"Failed to unsubscribe: {MT5Manager.LastError()}")