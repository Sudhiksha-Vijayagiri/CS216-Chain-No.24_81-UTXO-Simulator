from validator import validate_transaction
MAX_MEMPOOL_SIZE = 10   # You can change 10 to any limit

class Mempool:
    def __init__(self):
        self.transactions = []
        self.spent_utxos = set()

    def add_transaction(self, tx, utxo_manager):
    
        # If mempool is full, remove lowest-fee transaction
        if len(self.transactions) >= MAX_MEMPOOL_SIZE:
    
            # Sort by fee (lowest first)
            self.transactions.sort(key=lambda x: x["fee"])
    
            removed = self.transactions.pop(0)
    
            # Free its UTXOs
            for inp in removed["inputs"]:
                self.spent_utxos.discard((inp["prev_tx"], inp["index"]))
    
            print("Mempool full: Removed low-fee transaction")
    
        is_valid, msg, fee = validate_transaction(tx, utxo_manager, self)
    
        if not is_valid:
            return False, msg
    
        for inp in tx["inputs"]:
            self.spent_utxos.add((inp["prev_tx"], inp["index"]))
    
        tx["fee"] = fee
        self.transactions.append(tx)
    
        return True, "Transaction added"


    def remove_transaction(self, tx):
        self.transactions.remove(tx)
        for inp in tx["inputs"]:
            self.spent_utxos.discard((inp["prev_tx"], inp["index"]))
