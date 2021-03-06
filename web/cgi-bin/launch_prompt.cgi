#!/usr/bin/perl
 
$conf_file = "/home/prompt_dir/prompt-test/config.txt";
$script_dir = "/usr/lib/prompt/";

system("$script_dir/launch_prompt.py $conf_file > /dev/null &");

print<<EOSTUFF; 
Content-type: text/html

<HTML>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Results</title>
        <link href='https://fonts.googleapis.com/css?family=Chivo:900' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" type="text/css" href="/prompt/stylesheets/stylesheet.css" media="screen">
        <link rel="stylesheet" type="text/css" href="/prompt/stylesheets/pygment_trac.css" media="screen">
        <link rel="stylesheet" type="text/css" href="/prompt/stylesheets/print.css" media="print">
    </head>
    <body>
      <div id="container">
        <div class="inner">

        <header>
          <center>
          <img src="/prompt/images/prompt-beta.png" alt="PROMpT logo">
          <h2>Navigation</h2>
          <h4><a href="/prompt/index.html">Home</a> | <a href="/prompt/processing.html">Processing</a> | <a href="/prompt/results.php">Results</a></h4>
        </header>
        <hr>
</BODY>
</HTML>
EOSTUFF
