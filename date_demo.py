from datetime import datetime

# Example timestamps
time_create = 1723114536
time_update = 1723114536

# Convert to datetime
create_datetime = datetime.utcfromtimestamp(time_create)
update_datetime = datetime.utcfromtimestamp(time_update)

print("Create datetime:", create_datetime)
print("Update datetime:", update_datetime)



msg = {
                        'event': 'add',
                        'userid': 11001,
                        'symbol': 'BANKNIFTY.Q24',
                        'action': 1,
                        'contractSize': 1.0,
                        'price_current': 50184.85,
                        'price_open': 50176.5,
                        'price_sl': 0.0,
                        'price_tp': 0.0,
                        'profit': -125.25,
                        'rate_margin': 1.0,
                        'rate_profit': 1.0,
                        'time_create': datetime.utcfromtimestamp(1723114536),
                        'time_update': datetime.utcfromtimestamp(1723114536),
                        'Dealer': 0,
                        'Digits': 2,
                        'ExpertID': 0,
                        'ExpertPositionID': 591,
                        'ExternalID': '',
                        'ModificationFlags': 0,
                        'ObsoleteValue': 0.0,
                        'ActivationFlags': 0,
                        'ActivationPrice': 0.0,
                        'Comment': '',
                        'ContractSize': 1.0,
                        'volume': 150000
                        }
pti