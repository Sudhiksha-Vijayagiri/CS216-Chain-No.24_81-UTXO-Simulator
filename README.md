# CS 216 – UTXO Blockchain Simulator

## Team Name
Chain-No.24_81

## Team Members
1. Prayuktha Lucky Reddy – Roll No: 240041025
2. Sigadapu Nitya – Roll No: 240005048
3. Vijayagiri Sudhiksha – Roll No: 240001079 
4. Madhavi K – Roll No: 240041021 

---

## Project Overview

This project is a simplified blockchain simulator using the **UTXO (Unspent Transaction Output)** model.

It allows users to:
- Create transactions
- Validate transactions
- Store pending transactions in a mempool
- Mine blocks
- Update balances
- Run test scenarios

All data is stored in memory.

---

## Folder Structure
project/
│
├── src/
│ ├── main.py
│ ├── utxo_manager.py
│ ├── mempool.py
│ ├── transaction.py
│ ├── block.py
│ └── validator.py
│
├── tests/
│ └── test_scenarios.py
│
└── README.md


---

## How to Run

### Step 1: Go to src folder


### Step 2: Run program


### Step 3: Use Menu
Choose options from the menu to:
- Create transaction
- View UTXOs
- View mempool
- Mine blocks
- Run tests

---

## File & Function Explanation

## (1️)main.py (Main Controller)

This file controls the whole program and menu.

### Important Functions

### create_tx_ui()
- Takes user input
- Selects UTXOs
- Creates transaction
- Sends it to mempool

### add_user_ui()
- Adds a new user
- Creates initial UTXO

### check_balance_ui()
- Shows balance of a user
- Uses UTXOManager

### Main Menu Loop
while True:
- Shows menu
- Calls correct function
- Keeps program running

---

## (2)utxo_manager.py (UTXO Storage)

Manages all confirmed coins.

### Important Functions

### add_utxo(tx_id, index, amount, owner)
- Adds new UTXO after mining

### remove_utxo(tx_id, index)
- Removes spent UTXO

### get_utxos_for_owner(name)
- Returns all UTXOs of a user

### get_balance(name)
- Calculates balance from UTXOs

### exists(tx_id, index)
- Checks if UTXO exists

This file acts as **wallet database**.

---

## (3)mempool.py (Pending Transactions)

Stores unconfirmed transactions.

### Important Functions

### add_transaction(tx, utxo_manager)
- Validates transaction
- Prevents double spend
- Adds TX to mempool

### transactions
- List of pending transactions

### spent_utxos
- Tracks reserved UTXOs

This prevents double spending.

---

## (4) transaction.py (Transaction Creation)

Creates transaction structure.

### Important Function

### create_transaction(inputs, outputs)
- Generates TX ID
- Calculates fee
- Returns transaction dictionary

Output format:
{
tx_id,
inputs,
outputs,
fee
}

---

## (5)validator.py (Transaction Validation)

Checks if transaction is valid.

### Important Function

### validate_transaction(tx, utxo, mempool)

Checks:

✔ Input UTXOs exist  
✔ No duplicate inputs  
✔ No mempool double spend  
✔ No negative outputs  
✔ Enough balance  

Fee Rules:
- input == output → fee = 0
- input > output → fee = input - output
- input < output → reject

Returns:

---
### (6)block.py (Mining Module)
Handles block mining.

Important Function
mine_block()
Steps:
Select transactions from mempool
Calculate total fees
Remove spent UTXOs
Create new UTXOs
Give reward to miner
Clear mempool
Simulates block confirmation.

---
### (7)test_scenarios.py (Test Module)
Contains all mandatory test cases.

Important Functions
reset_state()
Resets UTXO and mempool
run_full_flow()
Displays:

UTXOs before
Transaction details
Mempool
Mining
UTXOs after

test1() to test10()

Implements required test scenarios

run_all_tests()

Displays test menu
Used for validation and demonstration.


## Limitations

- No networking
- No persistence
- Single node simulation
- In-memory only

---
### Design Explanation
The project uses modular design:

UTXOManager → confirmed coins

Mempool → pending transactions

Validator → validation rules

Block → mining

Tests → verification

This follows a simplified Bitcoin workflow.

---

Dependencies / Installation

Python 3.8 or higher
No external libraries required
Check Python version:
python --version

---

## Purpose

This project demonstrates:
- UTXO model
- Transaction validation
- Mining flow
- Double spend prevention
- Fee calculation

For academic use only.

---

## Submitted For

CS 216 – Introduction to Blockchain  
Assignment 2 – UTXO Simulator


