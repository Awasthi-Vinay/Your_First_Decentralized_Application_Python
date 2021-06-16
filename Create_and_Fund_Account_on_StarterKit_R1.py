# web3
from web3 import Web3, HTTPProvider

import hashlib
from blocksec2go import open_pyscard, CardError
from blocksec2go import select_app, verify_pin, generate_signature
from blocksec2go.util import bytes_from_hex
from blocksec2go import select_app, get_key_info

def transfer_ether(account_to):
    # open a connection to the local ethereum node
    http_provider = HTTPProvider('http://localhost:8545')

    w3 = Web3(http_provider)

    if(w3.isConnected() == True):
        print("Blockchain Connection Established Successfully")
    else:
        print("Blockchain Connection Failed")
        return 1
    account_from = w3.eth.accounts[0]
    print("\nFunding Account Address: ", account_from)

    print("\nFunding Account Balance(Ethers): ", w3.fromWei(w3.eth.getBalance(account_from),'ether'))
    print("\nBeneficiary Account Address: ", account_to)
    print("\nBeneficiary Account Balance(Ethers): ", w3.fromWei(w3.eth.getBalance(account_to),'ether'))
    print("\n################################################################################################")
    print("Funding 3 Ethers to Beneficiary Account from Funding Account")
    print("################################################################################################\n")
    try:
        txn_hash = w3.eth.sendTransaction({'from': account_from, 'to': account_to, 'value': w3.toWei(3,"ether")})

        print("\nTransaction Hash: ", txn_hash.hex())

        txn_details = w3.eth.waitForTransactionReceipt(txn_hash)
        print("\nTransaction Details:", txn_details)

        print("\n################################################################################################")
        print("Funding 3 Ethers Successful")
        print("################################################################################################\n")
        print("\nBeneficiary Account Address: ", account_to)
        print("\nBeneficiary Account Balance(Ethers): ", w3.fromWei(w3.eth.getBalance(account_to),'ether'))
        print("################################################################################################\n")
    except Exception as err:
        print("\nTransaction Failed with Error: ", err)

if __name__ == '__main__':
    #  only once but reloading is disabled

    reader = open_pyscard(None)
    select_app(reader)
    global_counter, counter, public_key_sec1 = get_key_info( reader, 1 )
    beneficiary_account = Web3.toChecksumAddress( Web3.keccak( public_key_sec1[1:] )[-20:].hex() )
    #beneficiary_account = "0xfa6eABdD950B671E30C10D689Cb126f642B51091"
    transfer_ether(beneficiary_account)
