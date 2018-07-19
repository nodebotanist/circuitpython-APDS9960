flash:
	rm -f /Volumes/CIRCUITPY/main.py
	cp example.py /Volumes/CIRCUITPY/main.py
	rm -f /Volumes/CIRCUITPY/APDS9960_circuitpython.py
	cp APDS9960_circuitpython.py /Volumes/CIRCUITPY/APDS9960_circuitpython.py

clean: 
	rm -f /Volumes/CIRCUITPY/main.py
	rm -f /Volumes/CIRCUITPY/APDS9960_circuitpython.py
