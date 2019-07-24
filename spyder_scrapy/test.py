import sys
import os
print(sys.argv)
if 'scrapy.conf' in sys.modules:
	print(sys.modules['scrapy.conf'])
else:
	print(os.environ.keys())