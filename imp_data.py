import pickle

enb_data = [
        ['1','enb161','','','135.242.110.45','lyz','',''],
        ['2','enb173','','','135.242.110.93','cjy','',''],
        ['3','enb176','','','135.242.110.105','wh','','']
        ]
'''
enb_data = []
'''

output = open('enb_data.txt','wb')
pickle.dump(enb_data,output)
output.close()
