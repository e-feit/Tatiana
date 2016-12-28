<?php
function writeLog($pinNum)
{

   $fg = file_get_contents(STATUSES.$pinNum);
   $stfile = fopen(LOGFILE,"a");
   $moment = date('d.m.Y H:i:s');
   
   switch($fg)
   {
//pin - имя статус файла он же номер пина
//filedata - содержимое статус-файла. Позвояет проверить был ли изменён статус.

	  case 1:
	           $res = array(
			   "error"    => 0,
			   "pin"      => $pinNum,
			   "log"      => "%WEBON%  $pinNum > $moment",
			   "filedata" => 1
			   );
			   
	           fwrite($stfile,"%WEBON%     $pinNum > $moment\n");
	  break;
	  
	  case 0:
	  	       $res = array(
			   "error"    => 0,
			   "pin"      => $pinNum,
			   "log"      => "%WEBOFF% $pinNum > $moment",
			   "filedata" => 0
			   );
			   
	           fwrite($stfile,"%WEBOFF%     $pinNum > $moment\n"); 
	  break;
	  
   }
fclose($stfile);
return json_encode($res);
}


function readLog($num=1)
{
    $echer = file_get_contents(LOGFILE);
    $echer = str_replace(" ", "&nbsp;", $echer);
    $echer = str_replace("%WEBON%", "<img src='images/webon.png' class='logpicture'>", $echer);
    $echer = str_replace("%WEBOFF%", "<img src='images/weboff.png' class='logpicture'>", $echer);
    $echer = str_replace("%PLANON%", "<img src='/style/img/planon.png' class='logpicture'>", $echer);
    $echer = str_replace("%PLANOFF%", "<img src='/style/img/planoff.png' class='logpicture'>", $echer);
    $echer = str_replace("%BUTTONOFF%", "<img src='/style/img/butoff.png' class='logpicture'>", $echer);
    $echer = str_replace("%BUTTONON%", "<img src='/style/img/buton.png' class='logpicture'>", $echer);
    $echer = str_replace("%UP%", "<img src='/style/img/up.png' class='logpicture'>", $echer);
    $echer = str_replace("%DOWN%", "<img src='/style/img/down.png' class='logpicture'>", $echer);
    
	$echer = explode("\n",$echer);
	$echer = array_reverse($echer);
	$total = count($echer)-1;

    if($num > $total) $num = $total;
	if($num <= 1) return '<div class="logger">'.$echer[1].'</div>';
	
    for($i = 1; $i <= $num; $i++)
	   {
		  $res.= '<div class="logger">'.$echer[$i].'</div>';
	   }
	   
       return $res;	   
}
?>