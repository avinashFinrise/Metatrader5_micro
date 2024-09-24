# include the library
import MT5Manager
 
# create manager interface
manager = MT5Manager.ManagerAPI()
# connect the server
if manager.Connect("159.100.13.166:443", 1014, "Galaxy#@7890", 
                    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS, 120000):
    # get the list of managers on the server
    managers = manager.UserGetByGroup("managers\\*")
    # check the obtained list
    if managers is not False:
        print(f"There are {len(managers)} managers on server")
    else:
        # failed to get the list
        print(f"Failed to get manager list: {MT5Manager.LastError()}")
    # disconnect from the server
    manager.Disconnect()
else:
    # failed to connect to the server
    print(f"Failed to connect to server: {MT5Manager.LastError()}")