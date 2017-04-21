<?php
/**
 * Created by PhpStorm.
 * User: marcolemmens
 * Date: 20-04-17
 * Time: 18:06
 */

$con = mysqli_connect("localhost","marc_com_ziggoTe","8EZsj9eLej6L","marcolemmens_com_ziggoTe");

// Check connection
if (mysqli_connect_errno())
{
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}


$playerName = "Eden Hazard";
$query = 'none';
$playerId = 1;

$playerArray = array('id' => 2, 'playerName' => 'Eden Hazard', 'currentTeam' => 'Chelsea', 'salary' => '6.5 million GPB', 'length' => '173');

if(isset($_GET['playerName'])){
    $playerName = $_GET['playerName'];

    // Search database for matching name
    $sql = "SELECT * FROM Players WHERE name like '".$playerName."'";
    $result = $con->query($sql);

    if ($result->num_rows > 0) {
        // output data of each row
        $row = $result->fetch_assoc();

        $playerArray = array('id' => $row['id'], 'playerName' => $row['name'], 'currentTeam' => $row['currentTeam'], 'salary' => $row['salary'], 'length' => $row['length']);

    } else {
    }


}
if(isset($_GET['playerId'])){

    if($_GET['playerId'] == "")
    {


        $playerId = $_GET['playerId'];

        // search database for matching ID
        $sql = "SELECT * FROM Players WHERE id = $playerId";
        $result = $con->query($sql);

        if ($result->num_rows > 0) {
            // output data of each row
            $row = $result->fetch_assoc();

            $playerArray = array('id' => $row['id'], 'playerName' => $row['name'], 'currentTeam' => $row['currentTeam'], 'salary' => $row['salary'], 'length' => $row['length']);

        }

    }

}

if(isset($_GET['query'])){
    $query = $_GET['query'];
}



switch ($query) {
    case 'playerSalary':
        contextPlayerSalaryResponse($playerArray);
        break;
    case 'playerLength':
        contextPlayerLengthResponse($playerArray);
        break;
    case 'specificPlayerInfo':
        specificPlayerInfoResponse($playerArray);
        break;
    default:
        contextPlayerResponse($playerArray);
}



function contextPlayerResponse($arr)
{
    $speech[0] = "That would be " . $arr['playerName'];
    $speech[1] = "That's ". $arr['playerName'] . " on the ball";
    $output = $speech[array_rand($speech)];

    echo json_encode(array ('output' => $output, "playerInfo" => $arr));

}

function contextPlayerSalaryResponse($arr)
{
    $speech[0] = $arr['playerName'] . "'s salary is " . $arr['salary'];
    $speech[1] = $arr['playerName'] . " makes " . $arr['salary'] . " a year";
    $output = $speech[array_rand($speech)];

    echo json_encode(array ('output' => $output, "playerInfo" => $arr));


}

function contextPlayerLengthResponse($arr)
{
    $speech[0] = $arr['playerName'] . " is " . $arr['length'] . "cm tall" ;
    $speech[1] = "He is " . $arr['length'] . "cm tall";
    $output = $speech[array_rand($speech)];

    echo json_encode(array ('output' => $output, "playerInfo" => $arr));

}

function specificPlayerInfoResponse($arr)
{
    $speech[0] = $arr['playerName'] . " is " . $arr['length'] . " SPECIFIEK" ;
    $speech[1] = "He is " . $arr['length'] . "SPECIFIEKSPECIFIEKSPECIFIEKSPECIFIEKSPECIFIEK";
    $output = $speech[array_rand($speech)];

    echo json_encode(array ('output' => $output, "playerInfo" => $arr));

}

$myfile = fopen("debug.txt", "w") or die("Unable to open file!");
$txt = $playerArray['playerName'] . "\n";
fwrite($myfile, $txt);
$txt = $query . "\n";
fwrite($myfile, $txt);
fclose($myfile);
