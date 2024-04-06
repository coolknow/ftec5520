import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import random
import hashlib
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

class BlockPoW:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0  # 初始化nonce值
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.transactions, self.timestamp, self.previous_hash, self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()
    

class BlockchainPoW:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        
    def create_genesis_block(self):
        genesis_block = BlockPoW(0, "Genesis Block", time.time(), "0")
        self.mine(genesis_block)
        self.chain.append(genesis_block)
        
    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = BlockPoW(len(self.chain), transactions, time.time(), previous_block.hash)
        self.mine(new_block)
        self.chain.append(new_block)
        
    def mine(self, block, difficulty=5):
        challenge = "0" * difficulty
        while block.hash[:difficulty] != challenge:
            block.nonce += 1
            block.hash = block.calculate_hash()
        
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True
    
bc = BlockchainPoW()

@app.route('/addBlock', methods=['POST'])
def addBlock():
    data = request.json
    bc.add_block("add")
    return jsonify(username=data['username'], password=data['password'])

@app.route('/check', methods=['GET'])
def getBCInfo():
    return str([(block.index, block.transactions, block.timestamp, block.previous_hash, block.nonce, block.hash) for block in bc.chain])

if __name__ == '__main__':
    app.run(debug=True)