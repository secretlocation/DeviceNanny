<html>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
<script type="text/JavaScript">
function timeRefresh(timeoutPeriod)
{
	setTimeout("location.reload(true);",timeoutPeriod);
}

function renew()
{
	if (document.getElementById("url").value!=""){
		var url="renew.php?userID="+document.getElementById("url").value;
	}
	else {
		var url="renew.php?userID="+document.getElementById("url2").value;
	}
	location.href=url;
	return false;
}

function users()
{
        var url = "/users.php"
        location.href=url;
}
</script>
<title>Device Nanny</title>
</head>
<body onload="JavaScript:timeRefresh(15000);">
<section>
<h1> Device Nanny </h1>
<form onSubmit="return renew();">
<input type="text" name="userid" placeholder="User ID" id="url" maxlength="3" size="6"><input type="submit" class="button" value="Renew Checkout(s)">
</form>
<form onSubmit="return users();">
<input type="button" class="button" value="I don't know my User ID" onclick="users();"/>
</form>

<p>
<?php

require_once('../mysqli_connect.php');

$query  = "SELECT DeviceName, Manufacturer, Model, Type, OS, CheckedOutBy, UserID, Location, CONCAT(FirstName, ' ', LastName) AS fullname FROM Devices, Users WHERE Devices.CheckedOutBy = Users.UserID ORDER BY CheckedOutBy, Type, OS DESC, Manufacturer, Model";

$response = @mysqli_query($dbc, $query);

if($response){
	echo '<div class="tbl-header">
    <table cellpadding="0" cellspacing="0" border="0">
	<thead>
	<tr>
	<th>Type</th>
	<th>Manufacturer</th>
	<th>Device Name</th>
	<th>Model</th>
	<th>OS</th>
	<th>Location</th>
	<th>Checked Out By</th>
	</tr>
	</thead>
	</table>
	</div>
	<div class="tbl-content">
	<table cellpadding="0" cellspacing="0" border="0">
    <tbody>';
	
	while($row = mysqli_fetch_array($response)){
		
		echo '<tr>';
		if($row['Type']=='Phone')
			echo "<td style='background-color: #ffffff;'>".$row['Type']."</td>";
		else
			echo "<td style='background-color: #f2f2f2;'>".$row['Type']."</td>";
		if($row['Manufacturer'] =='Apple')
			echo "<td style='background-color: #007cb5;'>".$row['Manufacturer']."</td>";
		else
			echo "<td align='left'; style='background-color: #4db9eb;'>".$row['Manufacturer']."</td>";
		if($row['CheckedOutBy']!='0')
			echo "<td style='background-color: #ff523d;'>".$row['DeviceName']."</td>";
		else
			echo "<td align='left'; style='background-color: #a9c94d;'>".$row['DeviceName']."</td>";
		echo '<td>' .
		$row['Model'] . '</td><td>' .
		$row['OS'] . '</td>';
		if($row['Location'] =='Omaha')
			echo "<td style='background-color: #007cb5;'>".$row['Location']."</td>";
		else
			echo "<td align='left'; style='background-color: transparent;'>".$row['Location']."</td>";
		if($row['fullname']!='- -')
			echo "<td>".$row['fullname']."</td>";
		else
			echo "<td>".$row['fullname']."</td>";
		echo '</tr>';

	}
	
	echo '</tbody></table></div>';
	
} else {
	
	echo "Couldn't issue database query";
	
	echo mysqli_error($dbc);
	
}

mysqli_close($dbc)

?>

</p>
<form onSubmit="return renew();">
<input type="text" name="userid" placeholder="User ID" id="url2" maxlength="3" size="6"><input type="submit" class="button" value="Renew Checkout(s)">
</form>
<form onSubmit="return users();">
<input type="button" class="button" value="I don't know my User ID" onclick="users();"/>
</form>
</section>
</body>
</html>
