from pathlib import Path
import hashlib

#File info: Name and Hash
file_info = {
    'clean_df.csv': 'e39bf160068d6f578937be2cfb57a6b6b321461e',
}

#Path to data directory
data_path = Path('data')

#Set file name and file location
fname = list(file_info.keys())[0]
file_path = data_path / fname

#Calculate hash and test that it is the same as expected
calculated_hash = hashlib.sha1(file_path.read_bytes()).hexdigest()

#Test hash for the file is as expected
assert calculated_hash == file_info[fname]

#Print statement so that user knows it has completed successfully
print('Fetch and validation passed')
