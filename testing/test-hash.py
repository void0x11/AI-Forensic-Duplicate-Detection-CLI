from load_modules import modules

def test_single_file_hash(file_path):
    """
    Tests hash computation for a single file.
    """
    print(f"Computing hashes for: {file_path}")
    md5 = modules.compute_md5(file_path)
    sha1 = modules.compute_sha1(file_path)
    sha256 = modules.compute_sha256(file_path)

    print(f"MD5:    {md5}")
    print(f"SHA-1:  {sha1}")
    print(f"SHA-256:{sha256}")


def test_directory_hash(directory_path):
    """
    Tests hash computation for all files in a directory.
    """
    print(f"Scanning directory: {directory_path}")
    hashes = modules.scan_directory(directory_path)

    for file_path, hash_dict in hashes.items():
        print(f"\nFile: {file_path}")
        for alg, h in hash_dict.items():
            print(f"  {alg.upper()}: {h}")


if __name__ == "__main__":
    # Example usage
    file_to_test = r"C:\Users\ahmed\OneDrive - Higher Technological Institute\Github\AI-Forensic-Duplicate-Detection-CLI\src\ai_model\sample_cases\image1.jpg"
    directory_to_test = r"C:\Users\ahmed\OneDrive - Higher Technological Institute\Github\AI-Forensic-Duplicate-Detection-CLI\src\ai_model\sample_cases"

    # Test single file
    test_single_file_hash(file_to_test)

    print("\n" + "="*50 + "\n")

    # Test entire directory
    test_directory_hash(directory_to_test)