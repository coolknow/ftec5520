import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import random
import hashlib
import time

def mine_block(block_data, difficulty=4, max_nonce=1000000):
    """
    模拟矿工挖掘区块的过程。
    返回找到有效nonce的矿工ID和nonce值，如果未找到，则返回None。
    """
    miner_id, transactions, previous_hash, timestamp = block_data
    challenge = "0" * difficulty
    for nonce in range(max_nonce):
        # 模拟不同的矿工可能以不同的速度计算哈希值
        if random.random() < 0.1:  # 随机跳过某些计算以模拟现实情况
            continue
        block_string = "{}{}{}{}{}".format(miner_id, transactions, timestamp, previous_hash, nonce)
        hash_result = hashlib.sha256(block_string.encode()).hexdigest()
        if hash_result[:difficulty] == challenge:
            return (miner_id, nonce, hash_result)
    return (miner_id, None, None)

# 模拟的矿工数量
num_miners = 5

# 创建模拟的区块数据
block_data = [("Miner{}".format(i), "Block Transactions", "00005442d7a0fcc47293846284b0bf1d4743ec652772e9dd8103b88eeb6bd91a", time.time()) for i in range(num_miners)]

# # 使用进程池执行挖掘任务
# with ProcessPoolExecutor(max_workers=num_miners) as executor:
#     futures = [executor.submit(mine_block, data) for data in block_data]
#     results = []
#     for future in as_completed(futures):
#         results.append(future.result())

# print(results)
if __name__ == '__main__':
    # 创建进程池和其他多进程相关的代码
    with ProcessPoolExecutor(max_workers=num_miners) as executor:
        futures = [executor.submit(mine_block, data) for data in block_data]
        results = []
        for future in as_completed(futures):
            results.append(future.result())
    print(results)
