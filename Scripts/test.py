# Custom test command

def do_command(dolwin, args):
    for i in args:
        if i != "":
            dolwin.Execute("echo " + i)
