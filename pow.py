import hashlib
import time

# 重新定义BlockPoW和BlockchainPoW类以修复之前的问题

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

# 重新创建区块链并添加区块，同时实现挖矿
blockchain_pow_fixed = BlockchainPoW()
blockchain_pow_fixed.add_block("Block 1 Transactions")
blockchain_pow_fixed.add_block("Block 2 Transactions")

# 验证区块链是否有效并输出区块链信息
is_blockchain_valid_pow_fixed = blockchain_pow_fixed.is_valid()
is_blockchain_valid_pow_fixed, [(block.index, block.transactions, block.timestamp, block.previous_hash, block.nonce, block.hash) for block in blockchain_pow_fixed.chain]

print(is_blockchain_valid_pow_fixed)
print([(block.index, block.transactions, block.timestamp, block.previous_hash, block.nonce, block.hash) for block in blockchain_pow_fixed.chain])