<?php
    // get the process ID parameter from the URL
    $pid = $_REQUEST["PID"];

    $command = "ps " . $pid;

    // check if the PID is still running
    $output = shell_exec($command);
    $returnValue = "Alert!!! - Process ID " . $pid . " is no longer running. Raspberry-PI-Q has exited!";

    if ($output !== "") 
    {
        $len = strlen($output);
        if (stristr($output, substr("Raspberry-PI-Q.py", 0, $len))) 
        {
            $returnValue = "Process ID " . $pid . " is still executing.";
        }
    }

    echo $returnValue;
?>
<html>
<head>
	<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script>
	<script type="text/javascript">
		function ClearLogs()
		{
			// Erase/replace the current content of the text area with the following message
			$('#interactiveData').text("Log content has been erased!\n");
		}
	    var lastUpdate = new Date("2017-01-01");
		var auto_refresh = setInterval(
			function ()
			{
				$('#pidUpdate').load('processID.php?PID=<?php echo $pid ?>').fadeIn("slow");
				$.getJSON("https://dweet.io/get/dweets/for/Raspberry-PI-Q_log", function(data) {
					var arrayLength = data.with.length;
					// go through list of items from DWEEP in reverse order to match chronological events
					for (i = arrayLength - 1; i >= 0; i--)
					{
						var item = data.with[i];
						var itemDate = new Date(item.created);
						if (itemDate > lastUpdate)
						{
							$('#interactiveData').append(itemDate.toLocaleString() + " - " + item.content.log + "\n");
							lastUpdate = itemDate;
						}
                   	}
				});
			}, 10000); // refresh every 10 seconds. Number is in milliseconds
	</script>

	<title>Raspberry-PI-Q by michmike</title>
</head>
<body>	
	<h1>Raspberry-PI-Q by michmike</h1>
	<div id="shellOutput"><textarea id="interactiveData" rows="10" cols="160"><?php echo $shellexecOutput ?></textarea></div>
</body>
</html>