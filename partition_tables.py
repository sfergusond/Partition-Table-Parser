# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 22:05:19 2019

@author: sferg
"""

import struct
import uuid
import argparse


def parse_mbr(mbr_bytes):
    mbr = []
    j = 0
    
    entries = mbr_bytes[446:]
    
    for i in range(4):
        if '{}'.format(entries[j + 4]) != '0':
            mbr.append({"number": i})
            j += 4

            mbr[-1].update({"type": '0x{:01x}'.format(entries[j])})
            j += 4
            
            mbr[-1].update({"start": struct.unpack('<L', entries[j:j+4])[0]})
            j += 4
           
            mbr[-1].update({"end": struct.unpack('<L', entries[j:j+4])[0] + mbr[-1].get("start") - 1})
            j += 4
        else:
            j += 16
    
    return mbr

def parse_gpt(gpt_file, sector_size=512):
    gpt = []
    gpt_header = gpt_file.read(sector_size * 2)[sector_size:]
    num_entries = struct.unpack('<L', gpt_header[80:84])[0]
    
    for i in range(num_entries):
        entry = gpt_file.read(128)

        if entry[0:16] != bytes([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
            gpt.append({"number": i})
            # type
            gpt[-1].update({"type":uuid.UUID(bytes_le = entry[0:16])})
        
            # start
            gpt[-1].update({"start":struct.unpack("<Q", entry[32:40])[0]})
        
            # end
            gpt[-1].update({"end":struct.unpack("<Q", entry[40:48])[0]})
        
            # name
            str = ''
            name = entry[56:]
            for i in range(0, len(name), 2):
                if chr(name[i]) == chr(0):
                    break
                str += chr(name[i])
            gpt[-1].update({"name":str})
    
    
    return gpt
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('mbr_type')
    parser.add_argument('sector', default = 512)
    
    args = parser.parse_args()

    with open(args.filename, 'rb') as f:
        if args.mbr_type == "gpt":
            _dict = parse_gpt(f, int(args.sector, 10))
        elif args.mbr_type == "mbr":
            data = f.read(512)
            _dict = parse_mbr(data)
        else:
            pass
    
    print(_dict)
        
if __name__ == '__main__':
    main()
    