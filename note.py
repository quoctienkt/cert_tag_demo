
# Create tagged MSI files for testing.
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
for tag_name, tag_option in tags.items():
  unittest_support += env.OmahaCertificateTagForTesting(
     target = '$STAGING_DIR/unittest_support/tagged_msi/GUH-%s.msi' % tag_name,
     source = 'unittest_support/GoogleUpdateHelper.msi',
     magic_bytes = tag_option[0],
     tag = tag_option[1],
     tag_length = tag_option[2])
