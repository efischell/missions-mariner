# python script to convert .def files (lamss) to .yaml
import re

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main(args):
    filename=args[0]
    
    print filename
    outname=filename[0:-3] + 'yaml'
    print outname
    k=open(outname,'w')
    # read each line in filename, print yaml version
    with open(filename) as f:
        for line in f:
            if line != '\n':
                #identify #define
                if '#define' in line:
                    # find varname
                    ll=line.replace("\t", " ")
                    ll=ll.replace("\n", " ")
                    sline=ll.split(' ');
                    
                    str_list = filter(None, sline) # fastest
                    if '//' not in str_list[0]:
                        # find the variable name
                        if str_list[0]=='#define':
                            print str_list
                            print len(str_list)
                            if len(str_list)==3:
                                var = str_list[1]
                                val=str_list[2]
                                print var
                                print val
                                if is_number(val):
                                    print >> k, var+ ': ' + str(float(val))
                                else:
                                    
                                    print >> k, var + ': \'' + val+'\'' 
        
    f.close()
    k.close()
                


import sys
main(sys.argv[1:])


