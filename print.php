<?php	
//	$command = escapeshellcmd('python3 /home/pi/ubuntu/gcode/try.py -f /home/pi/ubuntu/gcode/home.gcode -p /dev/ttyUSB0 >> log.log 2>&1');
//   	$output = shell_exec($command);
//    	echo $output;


	echo "well lets start";
	echo system("python3 gcode/try.py -f /home/pi/ubuntu/gcode/home.gcode -p /dev/ttyUSB0 >> log.log 2>&1");
?>
