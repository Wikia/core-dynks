<html>
<head>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" />
	<title>Coding task - Fandom</title>
</head>
<body>
	<nav class="nav navbar bg-light">
		<div class="container">
			<a class="navbar-brand" href="/">Coding task</a>
		</div>
	</nav>

    <section class="jumbotron text-center">
        <div class="container">
            <h1 class="jumbotron-heading">Coding task</h1>
            <p class="lead text-muted">Please refer to <tt>README.md</tt> for instructions. Good luck!</p>
        </div>
    </section>

	<div class="container" style="margin: 8em auto">
		<form>
            <div class="form-group row">
                <label for="message" class="col-4 col-form-label">Your message</label>
                <div class="col-6">
                    <input type="text" id="message" class="form-control">
                </div>
                <div class="col-2">
                    <button id="send" class="form-control btn btn-primary">Send</button>
                </div>
            </div>

            <div class="form-group row">
                <label for="read" class="col-4 col-form-label">Message from the service</label>
                <div class="col-6">
                    <input type="text" id="read" class="form-control" readonly>
                </div>
                <div class="col-2">
                    <button id="read" class="form-control btn btn-secondary">Read</button>
                </div>
            </div>
		</form>
	</div>

	<footer class="bg-light jumbotron">
		<div class="container">Running using service v<?= $version ?></div>
	</footer>

<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script>
	// ...
</script>
</body>
</html>