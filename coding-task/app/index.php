<?php

require 'vendor/autoload.php';

define('SERVICE_URL', 'http://service:80');

/**
 * @return string
 */
function get_service_version() {
	$client = new GuzzleHttp\Client();

	$resp = $client->get(SERVICE_URL . '/');
	$json = json_decode( $resp->getBody(), true );

	return $json['service_version'];
}

/**
 * Render the main app page
 */
dispatch('/', function () {
	return html('index.html.php', null, array('version' => get_service_version() ));
});

/**
 * Fetch information from 3rd party service
 */
dispatch_get('/message', function() {

});

dispatch_post('/message', function() {

});

run();
