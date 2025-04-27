import cv2
import numpy as np


def compute_phash(image_path):
    """
    Computes the basic perceptual hash (pHash) of an image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        str: A 64-character binary string representing the pHash.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Cannot load image at path: {image_path}")

    img = cv2.resize(img, (32, 32))
    dct = cv2.dct(np.float32(img))
    dct_low_freq = dct[:8, :8]
    median_val = np.median(dct_low_freq)
    phash_bits = dct_low_freq > median_val
    hash_str = ''.join('1' if bit else '0' for bit in phash_bits.flatten())

    return hash_str


def hamming_distance(hash1, hash2):
    """
    Computes the Hamming distance between two binary hash strings.

    Args:
        hash1 (str): First hash string.
        hash2 (str): Second hash string.

    Returns:
        int: Number of differing bits.
    """
    if len(hash1) != len(hash2):
        raise ValueError("Hashes must have the same length.")
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2))


def analyze_perceptual_hash_similarity(hash1, hash2):
    """
    Analyzes similarity between two perceptual hashes and returns a flag.

    Args:
        hash1 (str): First perceptual hash.
        hash2 (str): Second perceptual hash.

    Returns:
        int: Flag number indicating similarity category.
    """
    dist = hamming_distance(hash1, hash2)
    total_bits = len(hash1)
    similarity = (1 - dist / total_bits) * 100

    if similarity >= 98:
        return 0, dist, similarity   # IDENTICAL
    elif similarity >= 95:
        return 1, dist, similarity  # HIGHLY SIMILAR
    elif similarity >= 80:
        return 2, dist, similarity  # NEEDS DEEP ANALYSIS
    else:
        return 3, dist, similarity  # DIFFERENT