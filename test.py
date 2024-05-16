import MT5Manager
# create the graphical interface
manager = MT5Manager.ManagerAPI()
# connect the server
# if manager.Connect("167.86.86.164:1950", 1000, "QaZ!@#456", 
#                     MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS, 120000):
if manager.Connect("185.96.244.53:443", 8048, "XsFd-7Pg", 
                    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS, 120000):
    # get the list of managers on the server
    managers = manager.UserGetByGroup("managers\\*")
    print(managers)
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