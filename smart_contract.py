# smart_contract.py
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

contract_address = '0xd84b124758e180Db3264f1A93BD83c29C1c28860'

contract_abi =[
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "string",
				"name": "studentId",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "subject",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256[]",
				"name": "scores",
				"type": "uint256[]"
			},
			{
				"indexed": False,
				"internalType": "string[]",
				"name": "subjects",
				"type": "string[]"
			},
			{
				"indexed": False,
				"internalType": "string[]",
				"name": "reasons",
				"type": "string[]"
			},
			{
				"indexed": False,
				"internalType": "uint256[]",
				"name": "blockTimestamps",
				"type": "uint256[]"
			},
			{
				"indexed": False,
				"internalType": "string[]",
				"name": "teacherIds",
				"type": "string[]"
			}
		],
		"name": "ScoreUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "studentId",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "newScore",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "subject",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "reason",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "teacherId",
				"type": "string"
			}
		],
		"name": "updateScore",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "studentId",
				"type": "string"
			}
		],
		"name": "getScore",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			},
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			},
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			},
			{
				"internalType": "string[]",
				"name": "",
				"type": "string[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Account information
account_address = '0x38A90d57503Dd17cfc97b0960dC8Ff7a63d17f64'
account_private_key = '0x93aeb41bdf888aecdd0b886b89aab2d66d45d705ad99a4c8b829c7146e1131ec'


contract = w3.eth.contract(address=contract_address, abi=contract_abi)


async def getScore(student_id):
	result = contract.functions.getScore(student_id).call()
	return result


async def invokeUpdateScore(student_id: str, new_score: int, subject: str, reason: str, teacher_id: str) -> str:	
    account = w3.eth.account.from_key(account_private_key)

    # Build the transaction
    nonce = w3.eth.get_transaction_count(account_address)
    txn_dict = contract.functions.updateScore(student_id, new_score, subject, reason, teacher_id).build_transaction({
        'gas': 8000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=account.key)

    # Send the transaction
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    return txn_receipt
