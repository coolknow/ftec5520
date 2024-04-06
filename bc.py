import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_string = "{}{}{}{}".format(self.index, self.transactions, self.timestamp, self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
        
    def create_genesis_block(self):
        genesis_block = Block(0, "Genesis Block", time.time(), "0")
        self.chain.append(genesis_block)
        
    def add_block(self, transactions):
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), transactions, time.time(), previous_block.hash)
        self.chain.append(new_block)
        
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True

# 创建区块链并添加一些区块
blockchain = Blockchain()
blockchain.add_block("Block 1 Transactions")
blockchain.add_block("Block 2 Transactions")

# 验证区块链是否有效
is_blockchain_valid = blockchain.is_valid()

# 输出区块链的有效性和区块链的详细信息
is_blockchain_valid, [(block.index, block.transactions, block.timestamp, block.previous_hash, block.hash) for block in blockchain.chain]
# print(is_blockchain_valid)
# print([(block.index, block.transactions, block.timestamp, block.previous_hash, block.hash) for block in blockchain.chain])