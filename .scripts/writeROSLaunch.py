# writeROSLaunch.py
# Erin Fischell
# March 2018
# efischell@whoi.edu
#
# Takes in yaml file, meta file
# creates a ros.launch file in current folder with all parameters

import yaml
import os

def getyamldict(filename):
     with open(filename, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print 'ERROR: this may not be a yaml file'
            return 0

def checkrplug(rdict,rfile):
    # confirm that the dictionary contains: node dict, param dict
    try:
        node = rdict['node']
    except ValueError:
        raise Exception('There must be a node dict represented in the file' + rfile)
     # confirm that node contains fields name, pkg, type
    if 'name' not in node:
        raise Exception('There must be a name defined in node dict represented in the file- this is what you want it to be called' + rfile)
    
    if 'pkg' not in node:
        raise Exception('There must be a pkg defined in node dict represented in the file- this is the ros package' + rfile)
    if 'type' not in node:
        raise Exception('There must be a type defined in node dict represented in the file- this is the .py or executable file' + rfile)
    if viewmode == 'auto':
        if 'viewmode' in node:
            if node['viewmode'] != 'xterm' and node['viewmode'] != 'quiet':
                print 'ERROR: viewmode must be xterm or quiet.  Defaulting to xterm...'
                node['viewmode']='xterm'
        else:
            print 'using default viewmode...' + viewmode
            node['viewmode']='xterm'
    else:
        node['viewmode']=viewmode 
    
    #get any params
    try:
        params = rdict['param']
    except ValueError:
        print "No parameters for file " + rflie  
    else:
        # identify and $(VARNAME) and plug:
        for key,val in params.items():
            if '$(' in val:
                if val[2:-1] in config:
                    params[key]=config[val[2:-1]]
                else:

                    raise Exception('Parameter error: plugged variable ' + val + ' not found in config files.')
    return [node,params]

def writeToLaunchFile(node,params,f):
    # write node, params to launch file:
    if node['viewmode']=='xterm':
        print >> f,'<node name=\"' + node['name'] +'\" pkg=\"' + node['pkg'] +'\" type="' + node['type'] + '\" output="screen" launch-prefix="xterm -e">'
    elif node['viewmode']=='quiet':
        print >> f,'<node name=\"' + node['name'] +'\" pkg=\"' + node['pkg'] +'\" type="' + node['type'] + '\" >'
    
    for key in params:
        print >> f, '<param name=\"' + key +'\" value=\"' + params[key] + '\"/>'
    print >> f,'</node>'
    # TODO: Add in respawn, required options for ros nodes!

def readrplug_writefile(rplug,f):
    # read in the .rplug:
    rinit=getyamldict(rplug)
    print rinit

    # check that there are no issues with the dictionary:
    [node,params]=checkrplug(rinit,rplug)    

    #format strings and write to launch file:
    writeToLaunchFile(node,params,f)

def main(args):
    global config_yaml
    config_yaml=args[0] # will usually be allconfig.yaml
    ros_meta=args[1] # will usually by ros.meta
    global viewmode
    viewmode='auto'
    if len(args)>2:
        viewmode = args[2]
        
    
    # load config vars in config_yaml:
    global config
    config=getyamldict(config_yaml)
    
    # read in ros.meta file.  
    out=getyamldict(ros_meta)

    # open launch file, prepare to write:
    filename=os.getcwd() + '/../.tmp/roslaunch.launch'
    
    
    if 'filelist' in out:
        f=open(filename,'w')
        print >> f, '<launch>'
        for rplug in out['filelist']:
            rplug = os.getcwd() + '/../' + rplug
            readrplug_writefile(rplug,f)
        print >>f,'</launch>'
        f.close()
            
    else:
        print "Something is wrong with your ros filelist!  Example format:"
        print "filelist:"
        print "  - cruise/current/mariner_missionmanage.rplug"
        print "  - sensors/splitbeam/splitbeam_parser.rplug"
        
        raise Exception('ERROR: ros.meta must be in yaml format with a variable filelist')
    
    

import sys
main(sys.argv[1:])
