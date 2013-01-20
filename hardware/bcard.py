from xbee import ZigBee
import serial
import struct
import re
from time import sleep
from binascii import hexlify

ser = serial.Serial('/dev/tty.xbee', 57600)
xbee = ZigBee(ser, escaped=True)

destname  = ''
destaddr  = ''
destaddrS = ''

# find node
xbee.at(command='ND')
nodefound = 0;
while not nodefound:
	response = xbee.wait_read_frame()
	#print response
	if response['id'] == 'at_response':
		if response['command'] == 'ND':
			parameter = response['parameter']
			destaddrS = parameter[0:2]
			destaddr  = parameter[2:10]
			destname  = parameter[10:]
			index = destname.find('\x00')
			destname = destname[:index]
			print "received node reply for node %s short %s long %s" \
				% (destname, hexlify(destaddrS), hexlify(destaddr))
			nodefound = 1
		
sleep(1)

xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D0', parameter='\x05')
xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D1', parameter='\x05')
xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D2', parameter='\x05')
sleep(5)
xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D0', parameter='\x04')
xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D1', parameter='\x04')
xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D2', parameter='\x04')


while True:

	try:
		xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D0', parameter='\x05')
		sleep(1)
		xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D0', parameter='\x04')
		sleep(1)
		xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D1', parameter='\x05')
		sleep(1)
		xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D1', parameter='\x04')
		sleep(1)
		xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D2', parameter='\x05')
		sleep(1)
		xbee.send('remote_at', dest_addr_long=destaddr, dest_addr=destaddrS, command='D2', parameter='\x04')
		sleep(1)
	except KeyboardInterrupt:
		break


ser.close()