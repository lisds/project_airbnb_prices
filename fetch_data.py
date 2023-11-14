""" Fetch and validate data
"""

from pathlib import Path
import requests
import hashlib

file_info = {
    # Dictionary with key values pairs, where keys are output filenames
    # and values are dictionaries with keys URL and SHA1 hash.
    'mosquito_beer.csv': {
        'url': 'https://raw.githubusercontent.com/lisds/textbook/4065a20/data/mosquito_beer.csv',
        'sha1': 'a49f198303d20f5f709b7b2ffad23726b0f537af'},
    'family_of_veterans.xlsx': {
        'url': 'https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/armedforcescommunity/datasets/spousesandchildrenorstepchildrenofukarmedforcesveteranshealthandunpaidcareenglandandwales/current/veteransspouseandchildrenhealthandunpaidcareenglandandwales.xlsx',
        'sha1': '9d1d93a6acac6ed207bcf3fce4e0694b511ed349'}
}

data_path = Path('data')

for fname, info in file_info.items():
    out_path = data_path / fname
    r = requests.get(info['url'])
    out_path.write_bytes(r.content)
    assert hashlib.sha1(out_path.read_bytes()).hexdigest() == info['sha1']

print('Fetch and validation passed')
