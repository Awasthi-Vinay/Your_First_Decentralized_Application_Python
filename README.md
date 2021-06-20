# Your_First_Decentralized_Application_Python

This is an enhancement to integrate **Infineon's Security2Go Starterkit R1** Hardware wallet. 
This code is based on [adamyala's turtorial](https://github.com/adamyala/Your_First_Decentralized_Application_Python).

Please head over there to give a star on the repository.

## Overview

We will be building a decentralized voting application!

<a href="https://i.gyazo.com/02db73ac15a830c1ee0a1903dde91b2a.gif"><img src="https://i.gyazo.com/02db73ac15a830c1ee0a1903dde91b2a.gif"/></a>

The functionality of this repo is same to adamyala's but instead of using a Ganache CLI default account to sign the transaction, the transaction is signed using a key stored in **Infineon's Security2Go Starterkit R1** Hardware wallet.

## Setup

### Requirements

#### Software
* Python 3.6+
* Solidity 4.23+
* Node.js 9.8+

#### Hardware
* Smartcard Reader
* Security2Go Starterkit R1 Card. [High-level information about the Starterkit is available at [infineon.com/blockchain](https://www.infineon.com/blockchain)]
### Steps

1. Create and activate a virtual environment
1. Install dependencies with `pip install -r requirements.txt`
1. Install Blockchain Security 2Go starter kit Python Library [blocksec2go](https://pypi.org/project/blocksec2go/)
1. Install the [ganache-cli](https://github.com/trufflesuite/ganache-cli) command line tool with `npm install -g ganache-cli`
   1. **What does this cli do?** It runs an ethereum node locally. Normally we'd have to download a lot of blockchain transactions and run a test ethereum node locally. This tool lets us run a small local node for easy peasey development. This tool used to be called the `testrpc`.
   2. **Uh... This tool isn't python...** True, but I have found the JavaScript tooling for testrpc to be fantastic and easy to use. If you don't want to bother with `npm` or just want to try out a full python stack, try out [eth-testrpc](https://github.com/pipermerriam/eth-testrpc). It's pip installable but not as maintained as `ganache-cli`.

## Usage

Open up two tabs. In the first tab run `ganache-cli`. This will start a block chain network locally that we can play with.

In the second tab activate your virtual environment and run `Create_and_Fund_Account_on_StarterKit_R1.py`. 

This Script will read the public key from card at index 1, get the blockchain address from public key and will fund 3 test ethers to the blockchain address.


In the second tab run `main.py`. This will start our little flask app in debug mode, deploying our contract in the process.

After the python file runs you should see something like:
```
  Transaction: 0xd3d96eb1d0b8ca8b327d0eca60ff405d0000c5cd249d06712877effbcf73095f
  Contract created: 0x9e4fab9629b8768730d107ae909567974c4c8e35
  Gas usage: 352112
  Block Number: 1
  Block Time: Sat Dec 23 2017 22:31:13 GMT+0200 (SAST)
```
This is your contract being deployed to the chain on your local node!

`main.py` is where the bulk of our logic happens. It deploys our smart contract to our test ethereum node and starts serving our flask app. `main.py` and `voting.sol` are heavily commented so please give those a read to understand what each is doing.

Next open http://127.0.0.1:5000/ in your browser of choice. The web application will connect to our deployed contract and use it as the backend.

In Web-app, when user will click on **vote** button, the `main.py` will internally call the `handle_Transaction.py`.

`handle_Transaction.py` will check if Security2Go Starterkit R1 card is present on the connected reader [will show appropriate error if card not present].

If card is present then the Voting transaction will be signed with the private key stored on card at index 1 and sent to blockchain network.

Congrats! You setup your first decentralized application with python and using a  Security2Go Starterkit R1 Card for transaction signing!
