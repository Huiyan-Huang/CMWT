# CMWT
Calculates Multi-Worm Tracker metrics
  The package, Calculator for Multiple Worm Tracker (CMWT), analyzes data from multiple worm tracker experiments.

   It reads the directory that contains the '.blobs','.summary','.set'and '.png' files and generate result.txt files that contains Total tracked time, average speed, total pausing time and number of pauses. These are followed by the duration of each pauses period.

   MWT.exe is the ONLY program you need to run. It should be used as "MWT <path> <time thershold>". The parameter: <time thershold>: if a worm stops for a duration less than it, the worm will not be consider as paused. The unit is Seconds.
   When <time thershold> is omitted, a default value of 10 seconds is assumed.

   For example, it can be run as (in Command Prompt):
	MWT c:\work 10
   DON'T write the previous command as:
	MWT c:\work\ 10
   The redundent "\" often will course problems!!!

   Just run MWT.exe without any parameters will display its help file.

   The other file you may need to change is the MWTconfig.txt file. It contains the parameter for the program Chore.jar. The defaults should work for most situation.

   If the .DAT files are not generated, which contains the movement of each worm, executing MWT.exe will generate them. If the .DAT files are already generated in the same directory, MWT.exe will detect them and skip the process of generating the .DAT files, which is computational demanding. 

   When MWT.exe need to generate the .DAT files, a Choregraphy JAVA window will show up. Only after the windows is closed will MWT.exe goes on to calculate and generating the result files. So, DO remember to close the Choregraphy JAVA window once it shows up.
   When MWT.exe doesn't need to generate the .DAT files, it will simply outputs the result files. The Choregraphy JAVA window will not show up.

   The result files are in plain text file format. You can use EXCEL to open them (Right click -> Open with -> Excel).
   
   The CMWT package must be put in C:\CMWT!
   
   CMWT is smart so you don't need to remove unrelevant files from the data directory.
   
   Also this package dependents on the following DLL's, but most windows installations should have them.
	WS2_32.dll - C:\WINDOWS\system32\WS2_32.dll
	SHELL32.dll - C:\WINDOWS\system32\SHELL32.dll
	USER32.dll - C:\WINDOWS\system32\USER32.dll
	ADVAPI32.dll - C:\WINDOWS\system32\ADVAPI32.dll
	KERNEL32.dll - C:\WINDOWS\system32\KERNEL32.dll


Written in Python 2.7.2. Creative commomes licenses: CC BY.
CT Zhu 2012/02/28

