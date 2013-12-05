
***     dataGraph.py        ***

Simple script for graphing the pH recording data.Data from uD3 has several
columns for data including pH, mV, Force, and Time.  Changing the data.pH 
variable to one of these will allow graphing of other columns.

***     pH_data_read.py     ***

A script for parsing out small sections of the larger data set for analysis.

***     perfArray_2.0.py    ***

This script is used for analyzing the rate of data collection by uDaq.

***     uD3.py              ***

Script for recording data.  It has been localized to the OSx operating system.
It requires special drivers be installed for the USB serial function.  The 
precise values of the USB modem may also differ.  Entering /dev/tty.usbmodem*
will give a list of usb modem devices plugged into your machine.

