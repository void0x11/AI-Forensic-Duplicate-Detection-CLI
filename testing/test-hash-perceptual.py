from load_modules import modules

# This script tests the perceptual hash similarity between two images using the perceptual hash algorithm.
# It computes the perceptual hash for each image, calculates the Hamming distance between the hashes, and determines if the images are similar based on a specified threshold.
# The perceptual hash algorithm is designed to produce similar hashes for visually similar images, even if they are not identical.
# The Hamming distance is used to quantify the difference between the two hashes, and a similarity percentage is calculated based on this distance.
# The script prints the perceptual hashes, Hamming distance, similarity percentage, and whether the images are considered perceptually similar or different.
# -*- coding: utf-8 -*-


def test_perceptual_hash(image1_path, image2_path):
    """
    Tests perceptual hash similarity between two images and classifies based on similarity level.
    """
    hash1 = modules.compute_phash(image1_path)
    hash2 = modules.compute_phash(image2_path)

    print(f"pHash of {image1_path}: {hash1}")
    print(f"pHash of {image2_path}: {hash2}")

    # Now receiving 3 values
    flag, dist, similarity = modules.analyze_perceptual_hash_similarity(hash1, hash2)

    print(f"Hamming Distance: {dist}")
    print(f"Similarity: {similarity:.2f}%")

    if flag == 0:
        print("Decision: Images are IDENTICAL or nearly identical. [✓]")
    elif flag == 1:
        print("Decision: Images are HIGHLY similar with minor differences. [~]")
    elif flag == 2:
        print("Decision: Images have moderate similarity. RECOMMENDED for AI deep analysis. [!]")
    elif flag == 3:
        print("Decision: Images are DIFFERENT. [X]")
    else:
        print("Decision: Unknown similarity level. [?]")


if __name__ == "__main__":
    # Example images (update these paths as needed)
    img1 = r"C:\Users\ahmed\OneDrive - Higher Technological Institute\Github\AI-Forensic-Duplicate-Detection-CLI\src\ai_model\sample_cases\image5.jpg"
    img2 = r"C:\Users\ahmed\OneDrive - Higher Technological Institute\Github\AI-Forensic-Duplicate-Detection-CLI\src\ai_model\sample_cases\image6.jpg"
    test_perceptual_hash(img1, img2)