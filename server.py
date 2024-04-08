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

@app.route('/login', methods=['POST'])
def login():
    doctor_private_key = request.form.get('doctor_private_key')
    if doctor_private_key:
        return jsonify(doctor_private_key=doctor_private_key)
    else:
        # Handle the case where 'doctor_private_key' is not in the form data
        return "Missing doctor_private_key", 400

# 用于Register，Edit，Upload，
@app.route('/addBlock', methods=['POST'])
def addBlock():
    data = request.json
    bc.add_block("add")
    return jsonify(username=data['username'], password=data['password'])


@app.route('/upload_record', methods=['POST'])
def upload_record():
    doctor_key = request.form.get('doctor_private_key')
    patient_key = request.form.get('patient_key')
    diagnosis = request.form.get('diagnosis')
    bc.add_block(str(diagnosis))
    # 写入csv
    return jsonify(doctor_key=doctor_key)


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    private_key = request.form.get('private_key')
    public_key = request.form.get('public_key')
    bc.add_block("Edit profile")
    # 写入csv
    return jsonify(private_key=private_key, public_key=public_key)



# 用于Retrieve信息
@app.route('/access_record', methods=['GET'])
def get_records():
    # 这里，我们创建一个示例数据列表来模拟从数据库或其他源获取的记录。
    # 在实际应用中，你应该根据需要从数据库或其他数据源获取这些记录。
    example_records = [
        {'id': 1, 'record': 'Record 1'},
        {'id': 2, 'record': 'Record 2'},
        {'id': 3, 'record': 'Record 3'},
        # 更多记录...
    ]

    # 使用 jsonify 函数返回一个JSON格式的响应，
    # 其中包含一个名为 'records' 的键，值为上面定义的记录列表。
    return jsonify({'records': example_records})

@app.route('/check', methods=['GET'])
def getBCInfo():
    return str([(block.index, block.transactions, block.timestamp, block.previous_hash, block.nonce, block.hash) for block in bc.chain])

if __name__ == '__main__':
    app.run(debug=True)
