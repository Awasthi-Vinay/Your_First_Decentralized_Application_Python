from blocksec2go import select_app, verify_pin, generate_signature, get_key_info
from eth_account._utils.transactions import serializable_unsigned_transaction_from_dict, encode_transaction
from web3 import Web3, HTTPProvider


def get_signature_prefix( signature_rs, address, transaction_hash, chainId, web3 ):
    try:
        r, s = signature_rs
    except:
        print( "Invalid signature argument!" )
        raise SystemExit()

    v = chainId * 2 + 35
    if web3.eth.account._recover_hash( bytes( transaction_hash ), vrs=( v, r, s ) ) != address:
        v = chainId * 2 + 36
        if web3.eth.account._recover_hash( bytes( transaction_hash ), vrs=( v, r, s ) ) != address:
            print( "Could not verify the signature" )
            raise SystemExit()

    return v

def get_signature_components( der_encoded_signature ):
    # check signature lengthl
    if len( der_encoded_signature ) < 2:
        print( "Invalid signature!" )
        raise SystemExit
    # if does not start with signature DER TAG
    if not der_encoded_signature.startswith( b'\x30' ):
        print( "Invalid signature!" )
        raise SystemExit
    # get signature length
    sig_len = der_encoded_signature[1]
    if sig_len != len( der_encoded_signature[2:] ):
        print( "Signature length incorrect" )
        raise SystemExit

    pos = 2
    components = []
    while sig_len > 0:
        # if does not start with component DER TAG
        if der_encoded_signature[pos] != 0x02:
            print( "Expecting component DER TAG" )
            raise SystemExit
        pos += 1
        # get the component length
        component_len = der_encoded_signature[pos]
        pos += 1
        # get the component
        components.append( int.from_bytes( der_encoded_signature[pos:pos+component_len], byteorder='big' ) )
        pos += component_len
        sig_len = sig_len - component_len - 2

    return components

def sendTransaction(reader, contract_abi, contract_address, candidate_name):
    web3 =  Web3( Web3.HTTPProvider( "http://localhost:8545"))
    contract = web3.eth.contract( address=contract_address, abi=contract_abi)

    reader.connection.connect()
    select_app(reader)
    global_counter, counter, public_key_sec1 = get_key_info( reader, 1 )
    inf_card_addr = web3.toChecksumAddress( web3.keccak( public_key_sec1[1:] )[-20:].hex() )

    nonce = web3.eth.getTransactionCount(inf_card_addr )

    candidate_name_bytes = candidate_name.encode()

    # create the transaction dictionary for calling setCopyRightLyrics contract function
    transaction = contract.functions.voteForCandidate(candidate_name_bytes).buildTransaction( { 'nonce': nonce} )
    #del transaction['from']

    # serialize the transaction with the RLP encoding scheme
    unsigned_encoded_transaction = serializable_unsigned_transaction_from_dict( transaction )

    # sign the hash of the serialized transaction
    global_counter, counter, signature2 = generate_signature( reader, 1, bytes( unsigned_encoded_transaction.hash() ) )

    reader.connection.disconnect()

    #print("signature2: ",signature2)
    transaction_hash=unsigned_encoded_transaction.hash()



    r,s=get_signature_components(signature2)



    v = get_signature_prefix( ( r, s ), web3.toChecksumAddress(inf_card_addr), bytes( transaction_hash ), web3.eth.chainId, web3 )

    signed_encoded_transaction = encode_transaction( unsigned_encoded_transaction, vrs=( v, r, s ) )

    tx_hash=web3.eth.sendRawTransaction(signed_encoded_transaction)
    receipt  = web3.eth.waitForTransactionReceipt(tx_hash.hex())

    print("\nFrom Account Address: ", inf_card_addr)
    balance = web3.fromWei(web3.eth.getBalance(inf_card_addr),'ether')
    print("\nFrom Account Balance(Ethers): ", balance)

    return nonce, balance, receipt


