#!/usr/bin/python
# bindnorm.py - "normalise" a bind zone file by expanding relative names.
# Tue Sep 23 10:03:35 SAST 2008

import dns.zone
import sys

if len(sys.argv)<2:
	sys.stderr.write("Usage: %s [zone fqdn]\n" % sys.argv[0])
	sys.stderr.write("Example: %s example.com < db.example.com > norm.db.example.com\n" % sys.argv[0])
	sys.exit(1)

zone = dns.zone.from_text(sys.stdin.read(), sys.argv[1], relativize=False, check_origin=False)
zone.to_file(sys.stdout, relativize=False)
