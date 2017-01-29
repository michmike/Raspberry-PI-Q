<html>
<head>
	<title>Raspberry-PI-Q by michmike</title>
	<style>
		table {
		width:90%;
		border-top:1px solid #e5eff8;
		border-right:1px solid #e5eff8;
		margin:1em auto;
		border-collapse:collapse;
		}
		td {
		color:#678197;
		border-bottom:1px solid #e5eff8;
		border-left:1px solid #e5eff8;
		padding:.3em 1em;
		text-align:left;
		}
	</style>
</head>
<body>
	<h1>Raspberry-PI-Q by michmike</h1>
	<h2>Input Parameters</h2>
	<h3>Example invocation: sudo python3 /home/pi/Raspberry-PI-Q/Raspberry-PI-Q.py 180 225 125 email@address.com 5 30 Raspberry-PI-Q-Michael ff83612c-6814-466e-bd51-5d55039c184e &</h3>	
	<form method="get" action="index.php">
		<table>
			<tr><td>Grill Setup Temperature (in Fahrenheit)</td><td>For example 180 is the setup temperature of the grill. The fan will run continuously until this temperature is reached</td>
				<td><input name="grillSetupTemp" value="<?php if(isset($_GET['grillSetupTemp'])){echo $_GET['grillSetupTemp'];} else {echo '180';} ?>"></td></tr>
			<tr><td>Grill Desired Temperature (in Fahrenheit)</td><td>For example 225 is the desired temperature of the grill. The program will turn on/off the fan to maintain this temperature</td>
				<td><input name="desiredGrillTemp" value="<?php if(isset($_GET['desiredGrillTemp'])){echo $_GET['desiredGrillTemp'];} else {echo '225';} ?>"></td></tr>
			<tr><td>Meat Desired Temperature (in Fahrenheit)</td><td>For example 125 is the desired temperature of the meat. Insert the probe in the meat and we will predict the time when it will be ready</td>
				<td><input name="desiredMeatTemp" value="<?php if(isset($_GET['desiredMeatTemp'])){echo $_GET['desiredMeatTemp'];} else {echo '125';} ?>"></td></tr>
			<tr><td>Notification Email Address</td><td>This is the email address for notifications. You can use 10digitphonenumber@txt.att.net or 10digitphonenumber@tmomail.net for email-to-text</td>
				<td><input name="alertEmail" value="<?php if(isset($_GET['alertEmail'])){echo $_GET['alertEmail'];} else {echo '@tmomail.net @txt.att.net';} ?>"></td></tr>
			<tr><td>Update Interval (in Minutes)</td><td>This is the interval in minutes you want to receive regular updates and notifications. Alerts will come immediately</td>
				<td><input name="alertFrequency" value="<?php if(isset($_GET['alertFrequency'])){echo $_GET['alertFrequency'];} else {echo '5';} ?>"></td></tr>
			<tr><td>Loop Interval (in Seconds)</td><td>This is the interval in seconds that each loop will take. if set to 30 seconds, assume the fan will run X seconds every 30 seconds. You can adjust this for more or less fan time during your interval</td>
				<td><input name="loopInterval" value="<?php if(isset($_GET['loopInterval'])){echo $_GET['loopInterval'];} else {echo '30';} ?>"></td></tr>
			<tr><td>Device Unique Name</td><td>This is the unique name for your device that you want to use for tracking analytics on Dweet, Freeboard, and Grovestreams</td>
				<td><input name="uniqueName" value="<?php if(isset($_GET['uniqueName'])){echo $_GET['uniqueName'];} else {echo 'Raspberry-PI-Q-[name]';} ?>"></td></tr>
			<tr><td>Grill Setup Temperature</td><td>This is the unique application API ID you get from your grovestreams account</td>
			<td><input name="GROVE_API_KEY" value="<?php if(isset($_GET['GROVE_API_KEY'])){echo $_GET['GROVE_API_KEY'];} else {echo '[grove API guid]';} ?>"></td></tr>
		</table>
		<input type="submit" name="Run" value="Run"/>
		&nbsp; &nbsp;
		<input type="submit" name="Kill" value="Kill"/>
		&nbsp; &nbsp;
		<input type="submit" name="Shutdown" value="Shutdown"/>
		<input type="submit" name="test" value="test"/>
	</form>
	<?php
		if(isset($_GET['Run']))
		{
			$grillSetupTemp = $_GET['grillSetupTemp'];
			$desiredGrillTemp = $_GET['desiredGrillTemp'];
			$desiredMeatTemp = $_GET['desiredMeatTemp'];
			$alertEmail = $_GET['alertEmail'];
			$alertFrequency = $_GET['alertFrequency'];
			$loopInterval = $_GET['loopInterval'];
			$uniqueName = $_GET['uniqueName'];
			$GROVE_API_KEY = $_GET['GROVE_API_KEY'];

			$command = "sudo python3 /home/pi/Raspberry-PI-Q/Raspberry-PI-Q.py " . $grillSetupTemp . " " . $desiredGrillTemp . " " . $desiredMeatTemp . " " . $alertEmail . " " . $alertFrequency . " " . $loopInterval . " " . $uniqueName . " " . $GROVE_API_KEY . " &";
			exec($command);
		}
		else if (isset($_GET['Kill']))
		{
			echo exec("sudo pkill python3");
		}
		else if (isset($_GET['Shutdown']))
		{
			echo exec("sudo shutdown -h now");
		}
		else if (isset($_GET['test']))
		{
			$descriptorspec = array(
				0 => array("pipe", "r"),  // stdin
				1 => array("pipe", "w"),  // stdout
				2 => array("pipe", "w"),  // stderr
			);
			$process = proc_open('sudo pwd', $descriptorspec, $pipes, dirname(__FILE__), null);
			echo $process
			$stdout = stream_get_contents($pipes[1]);
			fclose($pipes[1]);

			$stderr = stream_get_contents($pipes[2]);
			fclose($pipes[2]);

			echo "stdout : \n";
			var_dump($stdout);

			echo "stderr :\n";
			var_dump($stderr);
			echo exec("sudo pwd");
		}

	?>

	<h2>Analytics</h2>
	<li><a target="new" href="https://dweet.io/follow/Raspberry-PI-Q-IPAddress">Get your IP Address - https://dweet.io/follow/Raspberry-PI-Q-IPAddress</a>
	<li><a target="new" href="https://freeboard.io/board/nrAnIB">Get the real-time analytics - https://freeboard.io/board/nrAnIB</a>
	<li><a target="new" href="https://www.grovestreams.com/observationStudio.html">View the historical analytics and alerts - https://www.grovestreams.com/observationStudio.html</a>		
</body>
</html>