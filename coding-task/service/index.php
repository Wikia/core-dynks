<?php

require 'vendor/limonade.php';

define('VERSION', '0.1');
define('TOKEN', '0d5f153fb24410ec8c83092b976ac8205cd4a302');
define('MESSAGE_FILE', '/tmp/.message');

function assert_token_is_valid() {
	$token = $_SERVER['HTTP_X_TOKEN'];

	if ($token !== TOKEN) {
		halt( HTTP_UNAUTHORIZED, "Provided X-Token request header is not valid." );
	}
}

// error handling
error(E_LIM_HTTP, function ($errno, $errstr, $errfile, $errline) {
    status($errno);
    return json([
    	'error' => $errno,
	    'message' => $errstr,
	]);
});

dispatch('/', function ()  {
	return json([
		'php_version' => phpversion(),
		'service_version' => VERSION,
		'message_path' => MESSAGE_FILE
	]);
});

// gets a message
dispatch_get('/message', function() {
	assert_token_is_valid();

	$message = trim(file_get_contents(MESSAGE_FILE));

	if ($message === false) {
		halt( HTTP_NOT_FOUND);
	}

	return json([
		'message' => $message
	]);
});

// updates a message
dispatch_post('/message', function() {
	assert_token_is_valid();

	$message = $_POST['message'];
	$res = file_put_contents(MESSAGE_FILE, $message);

	if (!$res) {
		halt(SERVER_ERROR, 'Storing the message failed');
	}

	status(HTTP_ACCEPTED);
});

run();
