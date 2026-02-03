import sys
import os

sys.path.append(os.path.abspath("../src"))

from utxo_manager import UTXOManager
from mempool import Mempool
from block import mine_block
from transaction import create_transaction

def reset_state():
    utxo = UTXOManager()
    mempool = Mempool()

    # Genesis UTXOs
    utxo.add_utxo("GENESIS", 0, 50, "Alice")
    utxo.add_utxo("GENESIS", 1, 30, "Bob")
    utxo.add_utxo("GENESIS", 2, 20, "Charlie")

    return utxo, mempool


def print_utxos(utxo):
    print("\n--- UTXO SET ---")
    for k, v in utxo.utxos.items():
        print(k, v)


def print_mempool(mempool):
    print("\n--- MEMPOOL ---")

    if not mempool.transactions:
        print("Empty")
        return

    for i, tx in enumerate(mempool.transactions, 1):
        print(f"TX {i}:")
        print(" Inputs:", tx["inputs"])
        print(" Outputs:", tx["outputs"])
        print(" Fee:", tx["fee"])


def print_header(title):
    print(title)


def run_full_flow(title, utxo, mempool, tx):

    print_header(title)

    print_utxos(utxo)

    print("\nCreating TX...")
    print("Inputs:", tx["inputs"])
    print("Outputs:", tx["outputs"])

    result = mempool.add_transaction(tx, utxo)
    print("Result:", result)

    print_mempool(mempool)

    print("\nMining...")
    mine_block("Miner1", mempool, utxo)

    print_utxos(utxo)


def test1():

    utxo, mempool = reset_state()

    tx = create_transaction(
        [{"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}],
        [
            {"amount": 10, "address": "Bob"},
            {"amount": 39.999, "address": "Alice"}
        ]
    )

    run_full_flow("TEST 1: Basic Valid Transaction", utxo, mempool, tx)


def test2():

    utxo, mempool = reset_state()

    utxo.add_utxo("T1", 0, 20, "Alice")

    tx = create_transaction(
        [
            {"prev_tx": "GENESIS", "index": 0, "owner": "Alice"},
            {"prev_tx": "T1", "index": 0, "owner": "Alice"}
        ],
        [{"amount": 60, "address": "Bob"}]
    )

    run_full_flow("TEST 2: Multiple Inputs", utxo, mempool, tx)


def test3():

    utxo, mempool = reset_state()

    tx = create_transaction(
        [
            {"prev_tx": "GENESIS", "index": 0, "owner": "Alice"},
            {"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}
        ],
        [{"amount": 10, "address": "Bob"}]
    )

    run_full_flow("TEST 3: Double Spend (Same TX)", utxo, mempool, tx)


def test4():

    utxo, mempool = reset_state()

    print_header("TEST 4: Mempool Double Spend")

    print_utxos(utxo)

    tx1 = create_transaction(
        [{"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}],
        [{"amount": 10, "address": "Bob"}]
    )

    tx2 = create_transaction(
        [{"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}],
        [{"amount": 5, "address": "Charlie"}]
    )

    print("\nCreating TX1...")
    print("Result:", mempool.add_transaction(tx1, utxo))

    print("\nCreating TX2 (Double Spend)...")
    print("Result:", mempool.add_transaction(tx2, utxo))

    print_mempool(mempool)

    print("\nMining...")
    mine_block("Miner1", mempool, utxo)

    print_utxos(utxo)


def test5():

    utxo, mempool = reset_state()

    tx = create_transaction(
        [{"prev_tx": "GENESIS", "index": 1, "owner": "Bob"}],
        [{"amount": 40, "address": "Alice"}]
    )

    run_full_flow("TEST 5: Insufficient Funds", utxo, mempool, tx)


def test6():

    utxo, mempool = reset_state()

    tx = create_transaction(
        [{"prev_tx": "GENESIS", "index": 1, "owner": "Bob"}],
        [{"amount": -5, "address": "Alice"}]
    )

    run_full_flow("TEST 6: Negative Output", utxo, mempool, tx)


def test7():

    utxo, mempool = reset_state()

    tx = create_transaction(
        [{"prev_tx": "GENESIS", "index": 2, "owner": "Charlie"}],
        [{"amount": 20, "address": "Bob"}]
    )

    run_full_flow("TEST 7: Zero Fee Transaction", utxo, mempool, tx)


def test8():

    utxo, mempool = reset_state()

    print_header("TEST 8: Race Attack")

    print_utxos(utxo)

    low = create_transaction(
        [{"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}],
        [{"amount": 49.999, "address": "Bob"}]
    )

    high = create_transaction(
        [{"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}],
        [{"amount": 48, "address": "Charlie"}]
    )

    print("\nLow Fee TX:")
    print("Result:", mempool.add_transaction(low, utxo))

    print("\nHigh Fee TX:")
    print("Result:", mempool.add_transaction(high, utxo))

    print_mempool(mempool)

    print("\nMining...")
    mine_block("Miner1", mempool, utxo)

    print_utxos(utxo)



def test9():

    utxo, mempool = reset_state()

    print_header("TEST 9: Complete Mining Flow")

    print_utxos(utxo)

    tx1 = create_transaction(
        [{"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}],
        [{"amount": 10, "address": "Bob"}]
    )

    tx2 = create_transaction(
        [{"prev_tx": "GENESIS", "index": 1, "owner": "Bob"}],
        [{"amount": 5, "address": "Charlie"}]
    )

    mempool.add_transaction(tx1, utxo)
    mempool.add_transaction(tx2, utxo)

    print_mempool(mempool)

    print("\nMining...")
    mine_block("Miner1", mempool, utxo)

    print_utxos(utxo)


def test10():

    utxo, mempool = reset_state()

    print_header("TEST 10: Unconfirmed Chain")

    print_utxos(utxo)

    tx1 = create_transaction(
        [{"prev_tx": "GENESIS", "index": 0, "owner": "Alice"}],
        [{"amount": 10, "address": "Bob"}]
    )

    mempool.add_transaction(tx1, utxo)

    print("\nTX1 Added")
    print_mempool(mempool)

    tx2 = create_transaction(
        [{"prev_tx": tx1["tx_id"], "index": 0, "owner": "Bob"}],
        [{"amount": 5, "address": "Charlie"}]
    )

    print("\nBob tries to spend unconfirmed UTXO")
    print("Result:", mempool.add_transaction(tx2, utxo))

    print_mempool(mempool)

    print("\nMining...")
    mine_block("Miner1", mempool, utxo)

    print_utxos(utxo)


def run_all_tests():

    while True:

        print("""

1. Basic Transaction
2. Multiple Inputs
3. Double Spend (Same TX)
4. Mempool Double Spend
5. Insufficient Funds
6. Negative Output
7. Zero Fee
8. Race Attack
9. Mining Flow
10. Unconfirmed Chain

0. Back To Main Menu
""")

        ch = input("Choose test: ")

        if ch == "1":
            test1()
        elif ch == "2":
            test2()
        elif ch == "3":
            test3()
        elif ch == "4":
            test4()
        elif ch == "5":
            test5()
        elif ch == "6":
            test6()
        elif ch == "7":
            test7()
        elif ch == "8":
            test8()
        elif ch == "9":
            test9()
        elif ch == "10":
            test10()
        elif ch == "0":
            break
        else:
            print("Invalid choice")
