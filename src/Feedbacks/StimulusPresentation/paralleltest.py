import parallel
import time
p=parallel.Parallel()


for i in range(1,100):
   p.setData(0)
   time.sleep(1)
   p.setData(int('{:07b}'.format(i)[::-1],2))
   print i
   print int('{:07b}'.format(i)[::-1],2)
   time.sleep(1)
   