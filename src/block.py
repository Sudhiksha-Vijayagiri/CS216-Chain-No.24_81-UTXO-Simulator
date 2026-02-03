def mine_block(miner, mempool, utxo_manager, max_txs=2):
    mempool.transactions.sort(key=lambda x: x["fee"], reverse=True)
    selected = mempool.transactions[:max_txs]

    total_fee = 0

    for tx in selected:
        for inp in tx["inputs"]:
            utxo_manager.remove_utxo(inp["prev_tx"], inp["index"])

        for idx, out in enumerate(tx["outputs"]):
            utxo_manager.add_utxo(tx["tx_id"], idx, out["amount"], out["address"])

        total_fee += tx["fee"]
        mempool.remove_transaction(tx)

        utxo_manager.add_utxo("COINBASE", 0, total_fee, miner)
        print("\nMining block...")
        
        print(f"Selected {len(selected)} transactions from mempool.")
        print(f"Total fees: {total_fee} BTC")
        print(f"Miner {miner} receives {total_fee} BTC")
        
        print("Block mined successfully!")
        print(f"Removed {len(selected)} transactions from mempool.")
