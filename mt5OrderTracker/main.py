import json
from MT5Manager import ManagerAPI

class OrderHandler:
    """Class to handle order events."""

    def OrderAdd(self, order):
        print(f"Order added: ID={order['ticket']}, Type={order['type']}, Volume={order['volume']}")

    def OrderCancel(self, order):
        print(f"Order cancelled: ID={order['ticket']}")

    def OrderDelete(self, order):
        print(f"Order deleted: ID={order['ticket']}")

    def OrderUpdate(self, order):
        print(f"Order updated: ID={order['ticket']}, New Volume={order['volume']}")


def main():
    # Load settings from JSON file
    with open('C:\\Users\\JAYESH\\Desktop\\mt5_python\\galaxy_feeds\\store\\settings\\settings.json') as f:
        settings_data = json.load(f)

    # Initialize the manager and connect
    manager = ManagerAPI()
    server = settings_data['mts_login']['server']
    login = settings_data['mts_login']['login']
    password = settings_data['mts_login']['password']

    if not manager.Connect(server, login, password, ManagerAPI.EnPumpModes.PUMP_MODE_ORDERS):
        print(f"Failed to connect: {manager.LastError()}")
        return

    print("Connected successfully to MT5 Manager")

    order_handler = OrderHandler()

    manager.OrderAdd(order_handler.OrderAdd)
    manager.OrderCancel(order_handler.OrderCancel)
    manager.OrderDelete(order_handler.OrderDelete)
    manager.OrderUpdate(order_handler.OrderUpdate)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping the trade updates listener")
    finally:
        manager.Disconnect()
        print("Disconnected from MT5 Manager")

if __name__ == "__main__":
    main()
