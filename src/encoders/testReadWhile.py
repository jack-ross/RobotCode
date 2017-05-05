import time
from readRotary import Encoder
import logging
import threading

from multiprocessing import Queue, Process, Value, Array


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

leftEncoder = Encoder(1, 2, "leftEncoder")
 
reset= False

mutex = threading.Lock()
bs = threading.Lock()

def test(q, count):
	logging.debug('Starting Left Encoder Thread')

	while True:
		while q.empty():	
			logging.debug('incrementing')
			leftEncoder.testWhile(count)
		q.get()
		count.value = 0
		logging.debug('val reset')

		# mutex.acquire()
  #       try:
  #           logging.debug('Acquired a mutex')
  #           bs.acquire()
  #           reset = False
  #           #bs.release()
  #       finally:
  #           bs.release()
  #           logging.debug('Released a mutex')
  #           mutex.release()
	logging.debug('Ending Thread')

# countD = {'leftEncoder': 0}
# encoderThreadLeft = threading.Thread(name='leftEncodersThread', target=test, args=(countD,))
# encoderThreadLeft.start()

count = Value('i', 0)
q = Queue()

p = Process(target=test, args=(q,count,))
p.start()
    

while True:
	print count
	time.sleep(5)
	q.put(True)
	# mutex.acquire()
 #   	try:
	# 	logging.debug('Acquired a mutex')
	# 	bs.acquire()
	# 	reset = True
	# 	# bs.release()
	# finally:
	# 	bs.release()
	# 	logging.debug('Released a mutex')
	# 	mutex.release()
	print "reset sent"
	print count
	time.sleep(3)

q.close()
p.join()
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()

