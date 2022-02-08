<html>
	<form method="GET" action="sender/zxc.php">
	<select name="asd">
	<?php
		$dir  = '/var/www/html/3dPrintService/sender/gcodes/';
		$files = scandir($dir);
		foreach ($files as $file){
			if($file == "." or $file == "..") continue;

			echo '<option value="'.$file.'">'.$file.'</option>';
		}
	?>


	</select>
	<br>
	<br>
	<select name="printer">
        <?php
                $dir  = '/var/www/html/3dPrintService/sender/sockets';
                $files = scandir($dir);
                foreach ($files as $file){
                        if($file == "." or $file == "..") continue;

                        echo '<option value="sockets/'.$file.'">sockets/'.$file.'</option>';
                }          
        ?>


        </select>
	<input type="submit" value="zxc clown">
	</form>
</html>
