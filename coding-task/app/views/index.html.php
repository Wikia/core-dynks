<html>
<head>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" />
	<title>Coding task - Fandom</title>
</head>
<body>
	<nav class="navbar bg-light">
		<div class="container">
			<a class="navbar-brand" href="/">Coding task</a>
		</div>
	</nav>
	<div class="container">
		<form>
			<label for="message">Your message</label>
			<input type="text" id="message">

			<button id="send">Send</button>

			<br>
			<br>

			<label for="message">Your message</label>
			<input type="text" id="read" readonly>

			<button id="read">Read</button>
		</form>
	</div>

	<footer class="bg-light">
		<div class="container">Running using service v<?= $version ?></div>
	</footer>

<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script>
	// ...
</script>
</body>
</html>