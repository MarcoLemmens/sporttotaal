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

$playerArray = array('id' => 999, 'playerName' => 'marco lemmens', 'currentTeam' => 'vv maarheeze', 'salary' => '10.5 euro', 'length' => '15cm');

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
    $playerId = $_GET['playerId'];

    // search database for matching ID
    $sql = "SELECT * FROM Players WHERE id = $playerId";
    $result = $con->query($sql);

    if ($result->num_rows > 0) {
        // output data of each row
        $row = $result->fetch_assoc();

        $playerArray = array('id' => $row['id'], 'playerName' => $row['name'], 'currentTeam' => $row['currentTeam'], 'salary' => $row['salary'], 'length' => $row['length']);

    }

    if(isset($_GET['query'])){
        $query = $_GET['query'];
    }


    echo json_encode($playerArray);
}



// switch ($query) {
//     case 'playerSalary':
//         contextPlayerSalaryResponse($arr);
//         break;
//     case 'playerLength':
//         contextPlayerLengthResponse($arr);
//         break;
//     default:
//         contextPlayerResponse($arr);
// }



// function contextPlayerResponse($arr)
// {
//     $speech[0] = "That would be " . $arr['playerName'];
//     $speech[1] = "That's ". $arr['playerName'] . "on the ball";
//     $output = $speech[array_rand($speech)];

//         echo json_encode(array ('output' => $output, 'playerName' => $arr['playerName']));

// }

// function contextPlayerSalaryResponse($arr)
// {
//     $speech[0] = $arr['playerName'] . "'s salary is " . $arr['salary'];
//     $speech[1] = $arr['playerName'] . " makes " . $arr['salary'] . " a year";
//     $output = $speech[array_rand($speech)];

//         echo json_encode(array ('output' => $output, "playerName" => $arr['playerName']));


// }

// function contextPlayerLengthResponse($arr)
// {
//     $speech[0] = $arr['playerName'] . " is " . $arr['length'] . "cm tall" ;
//     $speech[1] = "He is " . $arr['length'] . "cm tall";
//     $output = $speech[array_rand($speech)];

//         echo json_encode(array ('output' => $output, "playerName" => $arr['playerName']));


// }