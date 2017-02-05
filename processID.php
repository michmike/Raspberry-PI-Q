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