<?php
	$user = "root";
	$password = "haha, no.";
	$db = "my_super_db";
	$table = "users";

	$mysql = mysqli_connect("127.0.0.1", $user, $password);
	$mysql->select_db($db);

	if(isset($_POST["login"])) {
		$login = $_POST["login"];
		$password = $_POST["password"];
		defend($login);
		defend($password);

		$query = "СЛЫШ ЕСТЬ ЧО password В КАРМАНЕ $table ДА ЕЩЁ ЧТОБЫ С КАМЕРОЙ И (login БЫЛ '$login') И (password БЫЛ '$password') ВНАТУРЕ";
		#$query = "SELECT password from users WHERE (login='$login') AND (password='$password')";
		echo $query . "<hr />";
		$query = gop_stop_convert($query);
		echo $query . "<hr />";

		$res = $mysql->query($query) or die(mysqli_error($mysql));
		echo mysqli_error($mysql);
		$data = $res->fetch_all();
		if(count($data) > 0) {
			die("user $login is found with password <b>" . $data[0][0] . "</b>");
		}
	}

	function gop_stop_convert($query) {
		$query = str_replace("СЛЫШ ЕСТЬ ЧО", "SELECT", $query);
		$query = str_replace("В КАРМАНЕ", "FROM", $query);
		$query = str_replace("ДА ЕЩЁ ЧТОБЫ С КАМЕРОЙ И", "WHERE", $query);
		$query = str_replace("И ПОЯСНИ-КА ЗА ТО, ЧТО", "UNION SELECT", $query);
		$query = str_replace("БЫЛ", "=", $query);
		$query = str_replace("ВНАТУРЕ", ";", $query);
		$query = str_replace("ИЛИ", "OR", $query);
		$query = str_replace("И", "AND", $query);
		return $query;
	}

	function defend($string) {
		if(
			(strpos($string, "SELECT") !== false) ||
			(strpos($string, "UNION") !== false)||
			(strpos($string, "INSERT") !== false) ||
			(strpos($string, "CREATE") !== false) ||
			(strpos($string, "ALTER") !== false) ||
			(strpos($string, "DROP") !== false) ||
			(strpos($string, "AND") !== false) ||
			(strpos($string, "OR") !== false)
		) die("u da hacker? " . $string);
	}

?>

<html>
	<head>
		<meta charset="utf-8">
	</head>
	<body>
		<form method="post" action="">
			<input type="text" name="login" placeholder="alagunto">
			<input type="password" name="password" value="nice try">
			<input type="submit" value="log in" />
	</body>
</html>
