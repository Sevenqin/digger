# import os
#
# if __name__ == '__main__':
#     bb = os.popen('hydra -L ./dict/rdp_u.dic -P ./dict/rdp_p.dic 172.27.3.81 rdp')
#     print bb.read()


# import commands
# if __name__ == '__main__':
#     aa = commands.getoutput('hydra -L ./dict/rdp_u.dic -P ./dict/rdp_p.dic 172.27.3.81 rdp')
#     print aa

import subprocess

if __name__ == '__main__':
    arr = ['hydra','-L','./dict/rdp_u.dic','-P','./dict/rdp_p.dic','172.27.3.81','rdp']
    handle = open('./logs/hydra.log','wt')
    child1 = subprocess.Popen(arr, stdout=subprocess.PIPE,stderr=handle)
    child1.wait()
    print "good"
    print child1.stdout.read()
