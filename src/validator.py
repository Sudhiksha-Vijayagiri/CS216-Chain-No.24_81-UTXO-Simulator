FIXED_FEE = 0.001


def validate_transaction(tx, utxo_manager, mempool):
    seen_inputs = set()
    input_sum = 0
    output_sum = 0

    for inp in tx["inputs"]:
        key = (inp["prev_tx"], inp["index"])

        if key in seen_inputs:
            return False, "Duplicate input", 0
        seen_inputs.add(key)

        if not utxo_manager.exists(inp["prev_tx"], inp["index"]):
            return False, "Input UTXO does not exist", 0

        if key in mempool.spent_utxos:
            return False, "UTXO already spent in mempool", 0

        input_sum += utxo_manager.utxos[key]["amount"]

    for out in tx["outputs"]:
        if out["amount"] < 0:
            return False, "Negative output", 0
        output_sum += out["amount"]
       
    print(f"input_sum: {input_sum}, output_sum: {output_sum}")
    
    input_sum = round(input_sum, 3)
    output_sum = round(output_sum, 3)

    if input_sum < output_sum:
        return False, "Insufficient funds", 0
    
    elif input_sum == output_sum:
        return True, "Valid transaction", 0
    
    else:
        return True, "Valid transaction", FIXED_FEE
