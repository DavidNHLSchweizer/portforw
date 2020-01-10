import re
import sys
import os

def parseLine(line):
    pattern = re.compile(r'port=(?P<port>\d+)',re.IGNORECASE)
    match = pattern.match(line)
    if match:
        return match.group('port')

def readConfigurationFile(filename):        
    results = []
    with(open(filename, "r")) as fileHandler:
        for line in fileHandler:
            parsedLine = parseLine(line)
            if parsedLine:
                results.append(parsedLine)
    return results

print(readConfigurationFile(os.path.join(sys.path[0], 'config.txt')))

            
