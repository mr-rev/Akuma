from tar_put.dlc7A import As1d,Key
def on_press(key):
    try:
        print(key.char,end="",flush=True)
    except AttributeError:
        if(key==Key.enter):
            print("\n")
        elif(key==Key.space):
            print(" ",end="",flush=True)
        else:
            print(f" {key} ",end="",flush=True)

with As1d(on_press=on_press) as as1d:
    as1d.join()