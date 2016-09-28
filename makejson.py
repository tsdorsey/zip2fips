#!/usr/bin/env python

import json
import re
import os

statecodes = json.load(open('state2fips.json'))
patch = json.load(open('patch.json'))
zipmap = {}
cityFolder = 'zipctys/extracted'

for _, _, paths in os.walk(cityFolder):
    # Filter out system/hidden files.
    paths = [path for path in paths if path[0] != '.']

    print "Found {count} data files to process.".format(count=len(paths))
    for index, path in enumerate(paths):
        print "Processing {x:>2} of {y} - {name}".format(name=path, x=(index+1), y=(len(paths)))
        with open(os.path.join(cityFolder, path), 'r') as zfile:
            zfile.readline() # skip first line
            for l in zfile:
                l = l.strip() # Clean the whitespace off the front and back of the line.
                m = re.match(r"(?P<zip>.{5}).{18}(?P<state>..)(?P<fips>...)", l)
                if m:
                    r = m.groupdict()
                    zipmap.setdefault(r['zip'], set()).add(statecodes[r['state']] + r['fips'])
                else:
                    print 'Failed to parse: "{line}"'.format(line=l)

# Add patch values to the zip map. Provides a way to add missing codes.
print "Applying patch values"
for zip, fips in patch.iteritems():
    zipmap.setdefault(zip, set()).update(fips)

# Convert sets to lists so they can be serialized.
print ""
for key in zipmap.keys():
    zipmap[key] = sorted(zipmap[key])

with open('zip2fips.json', 'w') as out:
    out.write(json.dumps(zipmap))
