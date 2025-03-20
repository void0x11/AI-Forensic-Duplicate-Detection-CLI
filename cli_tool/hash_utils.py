import hashlib
import os

def compute_hash(file_path, hash_algorithm):
    """Computes hash of a file using the specified algorithm."""
    hash_func = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def compute_md5(file_path):
    """Computes MD5 hash of a file."""
    return compute_hash(file_path, 'md5')

def compute_sha1(file_path):
    """Computes SHA-1 hash of a file."""
    return compute_hash(file_path, 'sha1')

def compute_sha256(file_path):
    """Computes SHA-256 hash of a file."""
    return compute_hash(file_path, 'sha256')

def scan_directory(directory, algorithms=['md5', 'sha1', 'sha256']):
    """Scans a directory and computes hashes for each file."""
    file_hashes = {}
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = {alg: compute_hash(file_path, alg) for alg in algorithms}
    
    return file_hashes