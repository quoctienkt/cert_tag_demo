import binascii
import struct


tag = "tenantname=portaluat"
tag_length = len(tag)
magic_bytes = 'Gact2.0Omaha'

bin_tag = bytearray(binascii.hexlify(magic_bytes.encode()))
bin_tag.extend(binascii.hexlify(struct.pack('>H', tag_length)))
bin_tag.extend(binascii.hexlify(tag.encode()))
full_tag_encoded = '0x' + bin_tag.decode()
padded_length = len(bin_tag) + 8192

print(padded_length)
print(bytes.fromhex(full_tag_encoded[2:]))

