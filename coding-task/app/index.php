<?php

require 'vendor/autoload.php';

dispatch('/', function ()  {
	return json('hello');
});

run();
