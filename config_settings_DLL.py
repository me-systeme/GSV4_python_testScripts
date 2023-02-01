import ctypes
from ctypes import windll

if __name__ == '__main__':
	mydll = windll.LoadLibrary("MEGSV4x64.dll")

	Comnr = ctypes.c_int(13)  # COM port
	Baud = ctypes.c_int(115200)  # baud rate
	BufSize = ctypes.c_int(2048)  # buffer size

	ErrCode1 = mydll.GSV4actExt(Comnr, Baud, BufSize) # open COM port
	ErrCode3 = mydll.GSV4stopTX(Comnr)

	mydll.GSV4clearDLLbuffer(Comnr)

	# Rueckgabewert fuer DLL-Funktion GSV4DispGetNorm festlegen
	mydll.GSV4DispGetNorm.restype = ctypes.c_double

	# Anzeigenormierung schreiben
	for i in range(1, 5):
		new_Norm = ctypes.c_double(i * 1.0)
		print(f'GSV4DispSetNorm "{new_Norm}" - return: {mydll.GSV4DispSetNorm(Comnr, ctypes.c_int(i), new_Norm)}')

	# Anzeigenormierung lesen
	for i in range(1,5):
		Norm = mydll.GSV4DispGetNorm(Comnr, ctypes.c_int(i))
		print(f'Norm - Channel {i}: {Norm}')
		print(f'Gain - Channel {i}: {mydll.GSV4getGain(Comnr, ctypes.c_int(i))}')

	print('Freq', mydll.GSV4readFreq(Comnr))

	#ErrCode2 = mydll.GSV4startTX(Comnr)

	ErrCode4 = mydll.GSV4release(Comnr) # close COM port
