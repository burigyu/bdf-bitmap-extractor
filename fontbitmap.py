#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fontbitmap.py
#  usage python3 fontbitmap.py targetfont.bdf あ
#  
#  Copyright 2020 burigyu
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

def sjis2jis(c1, c2):
    # 定義に従ってあれこれする。
    # see http://www.tohoho-web.com/wwwkanji.htm 
    if c1 >= 0xe0:
        c1 = c1 - 0x40
    if c2 >= 0x80:
        c2 = c2 - 1
    if c2 >= 0x9e:
        c1 = (c1 - 0x70) * 2
        c2 = c2 - 0x7d
    else:
        c1 = ((c1 - 0x70) * 2) - 1
        c2 = c2 - 0x1f
    result = [c1, c2]
    return result

def main(args):
    c = args[2] # target character
    fn =args[1] # target bdf file
    
    sjisadr = c.encode('shift-jis-2004')
    jisadr = sjis2jis(*sjisadr)
    targetAdr = 'STARTCHAR ' + hex(jisadr[0])[2:] + hex(jisadr[1])[2:] + '\n'
    
    with open(fn,'r') as f:
        bdf = f.readlines()
        
    targetIndex = bdf.index(targetAdr) + 6
    bitmapBdf = bdf[targetIndex:targetIndex + 16]
    bitmap = []
    
    for i in range(len(bitmapBdf)):
        upperBit = '0x' + bitmapBdf[i][0:2]
        lowerBit = '0x' + bitmapBdf[i][2:4]    
        wholeBit = int(upperBit, 16) * 256 + int(lowerBit, 16)
        wholeBit = format(wholeBit, '#018b')
        bitmap.append(wholeBit)
        #print(wholeBit)
        #bitmap.append(hex(wholeBit))
    
    #print(bitmap)
    for i in range(len(bitmap)):
        if i == len(bitmap) - 1 :
            print(bitmap[i])
            print('}')
        
        elif i == 0:
            print('{')
            print(bitmap[i] + ',')
        else:
            print(bitmap[i] + ',')

    return 0

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        sys.exit(main(sys.argv))
    else:
        print('fontbitmap.py usage:python fontbitmap.py target.bdf kanji')
