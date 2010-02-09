import socket, StringIO  
   
''''' 
@author: ahuaxuan 
@date: 2008-10-22 
'''  
   
class mcstats(object):  
      
    def __init__(self, address, port):  
        self.address = address  
        self.port = port  
          
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.s.connect((self.address, self.port))  
      
    def __del__(self):  
        self.s.close()  
          
    def connect(self, command):  
           
        num = self.s.send(command)  
          
        totalData = ''  
        while True:  
           data = self.s.recv(1024)  
           if len(data) <= 0:  
               break  
              
           totalData = totalData + data  
           if totalData.find('END') >= 0:  
                break  
               
        return totalData  
                   
    def calcSlabsCount(self, data):  
         f = StringIO.StringIO(data)  
         tmp = None  
         for a in f:  
              
             if a.find('END') >= 0:  
                 break  
             else:  
                 tmp = a  
         f.close()  
         if tmp != None:  
             return int(tmp.split(":")[1])  
         else:  
             return 0  
           
    def showKVpairs(self, slabCounts, command):  
         for a in range(0, slabCounts):  
             tmpc = command + str(a + 1) + ' 0 \r\n'  
             data = self.connect(tmpc)  
             f = StringIO.StringIO(data)  
             for b in f:  
                 if b.find('ITEM') >= 0:
                     #print b
                     arr = b.split(' ')  
                     print 'key : ' + arr[1] + ' ------ value size : ' + arr[2][1:len(arr[2])]  
           
             f.close()  
               
if __name__ == "__main__":  
     mcs = mcstats("192.168.1.11", 11211)  
     mcs.showKVpairs(mcs.calcSlabsCount(mcs.connect('stats items \r\n')), 'stats cachedump ')
