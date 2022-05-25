
import binascii
from copy import copy
from copy import deepcopy

import os.path
import struct
 
from subprocess import PIPE,Popen
 


def OmahaCertificateTag(env, target, source):
  """Adds a superfluous certificate with a magic signature to an EXE or MSI.

  The file must be signed with Authenticode in order for Certificate Tagging to
  succeed.

  Args:
    env: The environment.
    target: Name of the certificate-tagged file.
    source: Name of the file to be certificate-tagged.

  Returns:
    Output node list from env.Command().
  """

  certificate_tag = ('"' + env['ENV']['GOROOT'] + '/bin/go.exe' + '"' +
                     ' run ' +
                     '"$MAIN_DIR/certificate_tag.go"')
  magic_bytes = 'Gact2.0Omaha'
  padded_length = len(magic_bytes) + 2 + 8192
  certificate_tag_cmd = env.Command(
      target=target,
      source=source,
      action=certificate_tag + ' -set-superfluous-cert-tag=' + magic_bytes +
      ' -padded-length=' + str(padded_length) + ' -out $TARGET $SOURCE',
  )

  return certificate_tag_cmd


def OmahaCertificateTagForTesting(env,
                                  target,
                                  source,
                                  magic_bytes=None,
                                  tag='',
                                  tag_length=None):
  """Adds a superfluous certificate with a magic signature to an EXE or MSI.

  The file must be signed with Authenticode in order for Certificate Tagging to
  succeed.
  This function allows caller to overwrite some parts of the tag with invalid
  values for testing purpose.

  Args:
    env: The environment.
    target: Name of the certificate-tagged file.
    source: Name of the file to be certificate-tagged.
    magic_bytes: Optional customized magic bytes.
    tag: Optional tag value.
    tag_length: Optional tag length (only last two bytes are accountable).

  Returns:
    Output node list from env.Command().
  """

  certificate_tag = ('"' + env['ENV']['GOROOT'] + '/bin/go.exe' + '"' +
                     ' run ' +
                     '"$MAIN_DIR/certificate_tag.go"')
  if magic_bytes is None:
    magic_bytes = 'Gact2.0Omaha'
  if tag_length is None:
    tag_length = len(tag)
  if tag_length > 0xFFFF:
    raise ValueError('Input tag is too long')

  bin_tag = bytearray(binascii.hexlify(magic_bytes.encode()))
  bin_tag.extend(binascii.hexlify(struct.pack('>H', tag_length)))
  bin_tag.extend(binascii.hexlify(tag.encode()))
  full_tag_encoded = '0x' + bin_tag.decode()
  padded_length = len(bin_tag) + 8192
  certificate_tag_cmd = env.Command(
      target=target,
      source=source,
      action=certificate_tag + ' -set-superfluous-cert-tag=' +
      full_tag_encoded + ' -padded-length=' + str(padded_length) +
      ' -out $TARGET $SOURCE',
  )

  return certificate_tag_cmd


tags = {
  'brand-only': (None, 'brand=QAQA', None),
  'ampersand-ending': (None, 'brand=QAQA&', None),
  'multiple': (None,
               ('appguid={8A69D345-D564-463C-AFF1-A69D9E530F96}&'
                'iid={2D8C18E9-8D3A-4EFC-6D61-AE23E3530EA2}&'
                'lang=en&browser=4&usagestats=0&appname=Google%20Chrome&'
                'needsadmin=prefers&brand=CHMB&'
                'installdataindex=defaultbrowser'), None),
  'empty-key': (None, '=value&brand=QAQA', None),
  'empty-value': (None, 'brand=', None),
  'empty-tag': (None, '', None),
  'invalid-marker': ('Gact2.0Foo', 'brand=QAQA', None),
  'invalid-length': (None, 'brand=QAQA', 3000),
  'invalid-key': (None, 'br*nd=QAQA', None),
  'invalid-value': (None, 'brand=QA*A', None),
  'bad-format': (None, 'brand', None),
  'bad-format2': (None, '=======&=======&&&=&&&&0', None),
}

if __name__ == "__main__":
    # for tag_name, tag_option in tags.items():

    tag_name = "multiple"
    tag_option = tags[tag_name]

    unittest_support = OmahaCertificateTagForTesting(
        target = 'sw-%s.msi' % tag_name,
        source = 'sw.msi',
        magic_bytes = tag_option[0],
        tag = tag_option[1],
        tag_length = tag_option[2])

    print(unittest_support)
