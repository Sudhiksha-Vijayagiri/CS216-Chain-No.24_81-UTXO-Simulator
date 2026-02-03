import time
import random


def generate_tx_id():
    return f"tx_{int(time.time())}_{random.randint(1000,9999)}"


def create_transaction(inputs, outputs):
    return {
        "tx_id": generate_tx_id(),
        "inputs": inputs,
        "outputs": outputs
    }
