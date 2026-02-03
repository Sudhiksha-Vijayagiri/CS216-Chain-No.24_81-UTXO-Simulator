import sys
import os
sys.path.append(os.path.abspath("../tests"))

from test_scenarios import run_all_tests
from utxo_manager import UTXOManager
from mempool import Mempool
from block import mine_block
from transaction import create_transaction


utxo = UTXOManager()
mempool = Mempool()

utxo.add_utxo("GENESIS", 0, 50, "Alice")
utxo.add_utxo("GENESIS", 1, 30, "Bob")
utxo.add_utxo("GENESIS", 2, 20, "Charlie")
utxo.add_utxo("GENESIS", 3, 10, "David")
utxo.add_utxo("GENESIS", 4, 5, "Eve")

def check_balance_ui():
    name = input("Enter user name: ")
    bal = utxo.get_balance(name)
    print(f"{name}'s balance: {bal} BTC")

def create_tx_ui():

    sender = input("Sender: ")

    outputs = []
    total_send = 0

    n = int(input("How many receivers? "))

    for i in range(n):
        receiver = input(f"Receiver {i+1}: ")
        amt = float(input(f"Amount to {receiver}: "))

        if amt <= 0:
            print("Invalid amount")
            return

        outputs.append({
            "amount": amt,
            "address": receiver
        })

        total_send += amt

    utxos = utxo.get_utxos_for_owner(sender)

    if not utxos:
        print("No funds available")
        return

    print("\nAvailable UTXOs:")

    for i, (k, v) in enumerate(utxos):
        print(f"{i}: {k} -> {v['amount']} BTC")

    choices = input(
        "Enter UTXO numbers (comma separated, e.g. 0,2,3): "
    )

    try:
        indices = [int(x.strip()) for x in choices.split(",")]
    except:
        print("Invalid input")
        return

    selected = []
    total = 0

    for i in indices:
        if i < 0 or i >= len(utxos):
            print("Wrong UTXO selected")
            return

        key, data = utxos[i]
        selected.append((key, data))
        total += data["amount"]

    FEE = 0
    needed = total_send

    if total < needed:
        print("Insufficient funds")
        return

    inp = []

    for key, data in selected:
        inp.append({
            "prev_tx": key[0],
            "index": key[1],
            "owner": sender
        })

    FEE = 0.001
    
    change = total - total_send - FEE
    change = round(change, 3)

    change = round(change, 3)

    if change > 0:
        outputs.append({
            "amount": change,
            "address": sender
        })

    tx = create_transaction(inp, outputs)

    ok, msg = mempool.add_transaction(tx, utxo)
    
    if ok:
        print("\nCreating transaction...")
        print(f"Transaction valid! Fee: {tx['fee']} BTC")
        print(f"Transaction ID: {tx['tx_id']}")
        print("Transaction added to mempool.")
        print(f"Mempool now has {len(mempool.transactions)} transactions.")
    else:
        print(msg)


def add_user_ui():

    name = input("Enter new user name: ")
    amount = float(input("Enter initial balance: "))

    if amount <= 0:
        print("Amount must be > 0")
        return

    tx_id = "GENESIS_" + name
    index = len(utxo.utxos)

    utxo.add_utxo(tx_id, index, amount, name)

    print(f"User {name} added with {amount} BTC")



while True:
    print("\n1.Create TX  2.View UTXO  3.View Mempool  4.Mine  5.Run Tests  6.Exit  7.Check Balance")


    ch = input("> ")

    if ch == "1":
        create_tx_ui()

    elif ch == "2":

        print("\n--- UTXO SET ---")

        if not utxo.utxos:
            print("No UTXOs available")

        else:
            for (tx_id, index), data in utxo.utxos.items():

                print(f"TX: {tx_id}")
                print(f"  Index : {index}")
                print(f"  Owner : {data['owner']}")
                print(f"  Amount: {data['amount']} BTC")
                print("-" * 30)

    elif ch == "3":

        print("\n--- MEMPOOL ---")

        if not mempool.transactions:
            print("Mempool is empty")

        else:
            for i, tx in enumerate(mempool.transactions, 1):

                print(f"Transaction {i}")
                print(f"  TX ID : {tx['tx_id']}")
                print(f"  Fee   : {tx['fee']} BTC")

                print("  Inputs:")
                for inp in tx["inputs"]:
                    print(f"    {inp['prev_tx']} : {inp['index']}")

                print("  Outputs:")
                for out in tx["outputs"]:
                    print(f"    {out['address']} -> {out['amount']} BTC")

                print("-" * 30)

    elif ch == "4":

        mine_block("Miner1", mempool, utxo)
        print("Block mined")

    elif ch == "7":

        check_balance_ui()
    elif ch == "5":
        run_all_tests()

    elif ch == "6":

        break

    else:
        print("Invalid option")
