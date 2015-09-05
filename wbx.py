#!/usr/bin/python
# wbx.py - dump MikroTik winbox addresses.wbx file format
# Mon Oct 13 10:03:26 SAST 2008

import sys

def munge_pair(pair):
    """ Convert integer values to integers """
    name, value, offset = pair
    if name in ['secure-mode', 'keep-pwd']:
        value = ord(value)
    return (name, value, offset)

def get_pair(offset,data):
    """ Extract a name/value pair from the data at offset. """
    if ord(data[offset])==0:
        # End of record
        # Return (None, None, offset of next record)
        return (None, None, offset+2)
    rlen = ord(data[offset])-1 # Record length
    nlen = ord(data[offset+2]) # Name length
    vlen = rlen-nlen # Value length
    offset = offset+3 # Skip to the name
    name = data[offset:offset+nlen]
    offset = offset+nlen # Skip to the value
    value = data[offset:offset+vlen]
    # Return (name, value, offset of next pair)
    return (name, value, offset+vlen)

if __name__ == "__main__":
    # Check arguments
    if len(sys.argv)<2:
        sys.stderr.write("Usage: %s [addresses.wbx]\n" % sys.argv[0])
        sys.exit(1)
    
    # Open file
    try:
        wbxfile = open(sys.argv[1])
    except IOError, e:
        sys.stderr.write("Failed to open file '%s': %s\n" % (sys.argv[1], str(e)))
        sys.exit(1)
    
    data = wbxfile.read() # Slurp the wbx file into a string
    headings = ['host','login','note','secure-mode','keep-pwd','pwd']
    offset = 4 # Skip the 4-byte file header
    
    for head in headings: # Print headings
        sys.stdout.write(head.ljust(16))
    print
    for head in headings: # Underline them
        sys.stdout.write(('-'*len(head)).ljust(16))
    print
    
    # Dump data
    try:
        while True:
            n, v, offset = munge_pair(get_pair(offset,data))
            if n == "type": continue
            if not n:
                print
                continue
            sys.stdout.write(str(v).ljust(16))
    except IndexError:
            pass
