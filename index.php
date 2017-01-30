<html>
<head>
	<?php
		$shellexecOutput = "No content exists yet!"
		if (isset($_GET['Run']))
		{
			$grillSetupTemp = $_GET['grillSetupTemp'];
			$desiredGrillTemp = $_GET['desiredGrillTemp'];
			$desiredMeatTemp = $_GET['desiredMeatTemp'];
			$alertEmail = $_GET['alertEmail'];
			$alertFrequency = $_GET['alertFrequency'];
			$loopInterval = $_GET['loopInterval'];
			$uniqueName = $_GET['uniqueName'];
			$GROVE_API_KEY = $_GET['GROVE_API_KEY'];

			$command = "sudo python3 /home/pi/Raspberry-PI-Q/Raspberry-PI-Q.py " . $grillSetupTemp . " " . $desiredGrillTemp . " " . $desiredMeatTemp . " " . $alertEmail . " " . $alertFrequency . " " . $loopInterval . " " . $uniqueName . " " . $GROVE_API_KEY . " > /dev/null 2>&1 & echo $!";
			$output = shell_exec($command);
			$pid = trim(preg_replace('/\s+/', ' ', $output));			
		}
		else if (isset($_GET['KillPythonProcesses']))
		{
			echo shell_exec("sudo pkill python3");
		}
		else if (isset($_GET['ShutdownPI']))
		{
			echo shell_exec("sudo shutdown -h now");
		}
		else if (isset($_GET['TestThermocouple']))
		{
			$shellexecOutput = shell_exec("sudo python3 /home/pi/Raspberry-PI-Q/dual_read_temperature_fahrenheit.py 30");
		}
		else if (isset($_GET['TestRelay']))
		{
			$shellexecOutput = shell_exec("sudo python3 /home/pi/Raspberry-PI-Q/relay_tester.py 60");
		}		
	?>
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script>
	<script type="text/javascript">
	<?php
		// Only execute the self-updating jQuery if the PID is already set
		if (strlen($pid) > 0)
		{
	?>
		var auto_refresh = setInterval(
			function ()
			{
				$('#pidUpdate').load('processID.php?PID=<?=$pid?>').fadeIn("slow");
				$.getJSON("https://dweet.io/get/dweets/for/Raspberry-PI-Q-Michael_log", function(data) {            		
					data.with.forEach(function(item){
					    $('#interactiveData').append(item.content.log + "\n");						
                   	});										
				});
			}, 10000); // refresh every 10 seconds. Number is in milliseconds
	<?php
		}
	?>
	</script>

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
		button {
		border-top: 1px solid #96d1f8;
		background: #65a9d7;
		background: -webkit-gradient(linear, left top, left bottom, from(#3e779d), to(#65a9d7));
		background: -webkit-linear-gradient(top, #3e779d, #65a9d7);
		background: -moz-linear-gradient(top, #3e779d, #65a9d7);
		background: -ms-linear-gradient(top, #3e779d, #65a9d7);
		background: -o-linear-gradient(top, #3e779d, #65a9d7);
		padding: 5px 10px;
		-webkit-border-radius: 8px;
		-moz-border-radius: 8px;
		border-radius: 8px;
		-webkit-box-shadow: rgba(0,0,0,1) 0 1px 0;
		-moz-box-shadow: rgba(0,0,0,1) 0 1px 0;
		box-shadow: rgba(0,0,0,1) 0 1px 0;
		text-shadow: rgba(0,0,0,.4) 0 1px 0;
		color: white;
		font-size: 14px;
		font-family: Georgia, serif;
		text-decoration: none;
		vertical-align: middle;
		}
		button:hover {
		border-top-color: #28597a;
		background: #28597a;
		color: #ccc;
		}
		button:active {
		border-top-color: #1b435e;
		background: #1b435e;
		}
	</style>
</head>
<body>	
	<h1>Raspberry-PI-Q by michmike</h1>
	
	<div id="pidUpdate" style="color:#FF0000"></div>	
	<div id="shellOutput"><textarea id="interactiveData" rows="10" cols="100"><?php echo $shellexecOutput ?></textarea></div>

	<h2>Input Parameters</h2>
	<b>Example: sudo python3 /home/pi/Raspberry-PI-Q/Raspberry-PI-Q.py 180 225 125 email@address.com 5 30 Raspberry-PI-Q-Michael ff83612c-6814-466e-bd51-5d55039c184e</b>
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
		<ul style="list-style-type:circle">
			<li><b>Run</b> will execute the temperature manager script according to the parameters above. This page will self-refresh with output from the script every 10 seconds</li>
			<li><b>KillPythonProcesses</b> will terminate all python3 processes and anything you can launch from this page</li>
			<li><b>ShutdownPI</b> will shut down the operating system of the Raspberry PI. You can now unplug the power cord</li>
			<li><b>TestRelay</b> will execute the relay tests on/off for 60 seconds and output the results on this page once the test is complete</li>
			<li><b>TestThermocouple</b> will execute the temperature tests for each thermocouple for 30 seconds and output the results on this page once the test is complete</li>
		</ul>

		<input type="submit" name="Run" value="Run"/>
		&nbsp; &nbsp;
		<input type="submit" name="KillPythonProcesses" value="KillPythonProcesses"/>
		&nbsp; &nbsp;
		<input type="submit" name="ShutdownPI" value="ShutdownPI"/>
		&nbsp; &nbsp;
		<input type="submit" name="TestRelay" value="TestRelay"/>
		&nbsp; &nbsp;
		<input type="submit" name="TestThermocouple" value="TestThermocouple"/>		
	</form>

	<h2>Analytics</h2>
	<li><a target="new" href="https://dweet.io/follow/Raspberry-PI-Q-IPAddress">Get your IP Address - https://dweet.io/follow/Raspberry-PI-Q-IPAddress</a>
	<li><a target="new" href="https://freeboard.io/board/nrAnIB">Get the real-time analytics - https://freeboard.io/board/nrAnIB</a>
	<li><a target="new" href="https://www.grovestreams.com">View the historical analytics and alerts - https://www.grovestreams.com/observationStudio.html</a>		
</body>
</html>