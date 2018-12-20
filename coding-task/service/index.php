<?php

require 'vendor/limonade.php';

define('VERSION', '0.1');
define('TOKEN', '0d5f153fb24410ec8c83092b976ac8205cd4a302');
define('MESSAGE_FILE', '/tmp/.message');

/**
 * Validates provided X-Token request header
 */
function assert_token_is_valid() {
	$token = $_SERVER['HTTP_X_TOKEN'];

	if ($token !== TOKEN) {
		halt( HTTP_UNAUTHORIZED, "Provided X-Token request header is not valid." );
	}
}

/**
 * We want this service to be a bit unreliable.
 * Let's inject a failure (i.e. HTTP 502 response) for ~40% of responses
 */
function inject_failure() {
	if ( mt_rand() % 100 < 40 ) {
		halt(HTTP_SERVICE_UNAVAILABLE, 'We\'re having some technical issues. Please try again.');
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
	inject_failure();

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
	inject_failure();

	$message = $_POST['message'];
	$res = file_put_contents(MESSAGE_FILE, $message);

	if (!$res) {
		halt(SERVER_ERROR, 'Storing the message failed');
	}

	status(HTTP_ACCEPTED);
});

run();
