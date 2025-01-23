import os
import hmac
import hashlib

class RandomGenerator:
    @staticmethod
    def generate_random_bytes(length):
        return os.urandom(length)

    @staticmethod
    def generate_random_int(max_value):
        return int.from_bytes(os.urandom(4), 'big') % max_value

    @staticmethod
    def compute_hmac(key, message):
        hmac_obj = hmac.new(key, message.encode('utf-8'), hashlib.sha3_256)
        return hmac_obj.hexdigest()
