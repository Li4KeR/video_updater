import os

def check_ping(ip):
    response = os.system("ping -n 1 " + ip) # for linux ping -c 1
    # and then check the response...
    if response == 0:
        ping_print = "Network Active"
    else:
        ping_print = "Network Error"
    
    print(ping_print)

pingstatus = check_ping('10.3.110.245')

#Ans = ['1_video', '2_video', '3_video', '4_video']
#Word = ['1_video', '2_video', '3_video', '5_video']
#
#result=list(set(Ans) ^ set(Word))
#
#print(result)
