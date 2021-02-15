#r/bin/env python3

import os, sys, re
                                      
def inputHandler(args):
    if len(args) == 0: #checks if there is an arguement
        return

    if "exit" in args:
        sys.exit(0)

    # Here we are changing the directory
    elif "cd" == args[0]:
        try:
            if len(args)==1: # This is here if cd is specified then reprompt the user
                return

            else:
                os.chdir(args[1])

        except: # It does not exist
            os.write(1, ("cd %s: No such file or directory\n" % args[1]).encode())

    else:
        rc = os.fork()
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        elif rc == 0:
            executeCommand(args)
            sys.exit(0)


def executeCommand(args): # Executes command
    for dir in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (dir, args[0])

        try:
            os.execve(program, args, os.environ) # checks if it can exec the program

        except FileNotFoundError:
            pass

    # The command was not found and prints an error message
    os.write(2, ("%s: command not found\n" % args[0]).encode())
    sys.exit(0)

def main():
    while True: 
        if 'PS1' in os.environ:
            os.write(1, (os.environ['PS1']).encode())
        else:
            os.write(1, ("$ ").encode())

        args = os.read(0, 1024) #amount of bytes

        if len(args) == 0: 
            break 

        args = args.decode().split("\n") #takes bytes to letters

        if not args: 
            continue #back to the while loop

        for arg in args:
            inputHandler(arg.split()) #reads each and every command inputted

if '__main__' == __name__:
    main() 
