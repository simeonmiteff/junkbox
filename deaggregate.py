#!/usr/bin/python
# deaggregate.py - deaggregate a network for a specific subnet, yielding the minimum number of subnets
# 	Add -exclude to only output the surrounding subnets. Subnet is read from stdin, all non matching subnets
# 	are output untouched. Use as a filter, rinse, repeat.
# 2009-10-12

from IPy import IP
import sys

def split(ip,sub,exclude):
    if ip==sub:
        if not exclude:
            print ip
    else:
        a = IP(str(ip.net())+'/'+str(ip.prefixlen()+1))
        b = IP(str(IP(ip.net().int()|2**(32-(ip.prefixlen()+1))))+'/'+str(ip.prefixlen()+1))
        if a.overlaps(sub):
            print b
            split(a,sub,exclude)
        elif b.overlaps(sub):
            print a
            split(b,sub,exclude)

if __name__=="__main__":
    if len(sys.argv)<2:
        sys.stderr.write("Usage: %s CIDR_prefix [-exclude]\n" % sys.argv[0]) 
        sys.exit(1)
    
    sub = IP(sys.argv[1])
    
    exclude = False
    if len(sys.argv)==3:
        if sys.argv[2]=='-exclude':
            exclude = True
    
    for line in sys.stdin:
        pre = IP(line.strip())
        if not pre.overlaps(sub):
            print line.strip()
        else:
            split(pre,sub,exclude)
