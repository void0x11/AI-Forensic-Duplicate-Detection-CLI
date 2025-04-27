from load_modules import modules

# This script tests the perceptual hash similarity between two images using the perceptual hash algorithm.
# It computes the perceptual hash for each image, calculates the Hamming distance between the hashes, and determines if the images are similar based on a specified threshold.
# The perceptual hash algorithm is designed to produce similar hashes for visually similar images, even if they are not identical.
# The Hamming distance is used to quantify the difference between the two hashes, and a similarity percentage is calculated based on this distance.
# The script prints the perceptual hashes, Hamming distance, similarity percentage, and whether the images are considered perceptually similar or different.
# -*- coding: utf-8 -*-


def test_perceptual_hash(image1_path, image2_path, similarity_threshold=98):

    """
    Tests perceptual hash similarity between two images.

    Args:
        image1_path (str): Path to the first image.
        image2_path (str): Path to the second image.
        similarity_threshold (float): Percentage threshold to consider images similar.
    """
    
    hash1 = modules.compute_phash(image1_path)
    hash2 = modules.compute_phash(image2_path)

    print(f"\npHash of {image1_path}: {hash1}")
    print(f"\npHash of {image2_path}: {hash2}")

    dist = modules.hamming_distance(hash1, hash2)
    total_bits = len(hash1)

    similarity = (1 - dist / total_bits) * 100
    print(f"Hamming Distance: {dist}")
    print(f"Similarity: {similarity:.2f}%")

    if similarity >= similarity_threshold:
        print(f"Result: Images are perceptually similar! [OK]")
    else:
        print(f"Result: Images are different. [X]")


if __name__ == "__main__":
    # Example images (update these paths as needed)
    img1 = r"C:\Users\ahmed\OneDrive - Higher Technological Institute\Github\AI-Forensic-Duplicate-Detection-CLI\src\ai_model\sample_cases\image5.jpg"
    img2 = r"C:\Users\ahmed\OneDrive - Higher Technological Institute\Github\AI-Forensic-Duplicate-Detection-CLI\src\ai_model\sample_cases\image6.jpg"
    test_perceptual_hash(img1, img2)