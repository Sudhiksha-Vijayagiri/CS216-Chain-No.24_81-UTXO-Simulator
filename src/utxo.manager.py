class UTXOManager:
    def __init__(self):
        self.utxos = {}  # (tx_id, index) -> {amount, owner}

    def add_utxo(self, tx_id, index, amount, owner):
        self.utxos[(tx_id, index)] = {
            "amount": amount,
            "owner": owner
        }

    def remove_utxo(self, tx_id, index):
        self.utxos.pop((tx_id, index), None)

    def exists(self, tx_id, index):
        return (tx_id, index) in self.utxos

    def get_balance(self, owner):
        return sum(
            utxo["amount"]
            for utxo in self.utxos.values()
            if utxo["owner"] == owner
        )

    def get_utxos_for_owner(self, owner):
        return [
            (k, v) for k, v in self.utxos.items()
            if v["owner"] == owner
        ]
