<?php

	echo $_GET["asd"];
	echo "<br>";
	echo $_GET["printer"];
	system("python3 sockSend.py ".$_GET["printer"]." < gcodes/".$_GET["asd"]." >> /var/www/html/3dPrintService/log.log & ");
?>
