$(document).ready(function()
{

   var selectorName = '#buttons',
       freqLog = 3000;

/* Функция отрисовки кнопок */

function buttonLoad()
{
     xhr = $.ajax
           ({
               type: 'post',
               url: 'server.php',
               data: 'act=status_check',
               dataType: 'json'

           });
		   
	xhr.done(function(data){
		
	$(selectorName).empty();
	 
     for(let btn of data.dev) {
	
     const status  = btn.status
	 
     const button  = $('<button>', 
	 {
          'class'         : 'action',
          'data-num-pin'  : btn.pinNum,
          'data-status'   : status,
          'text'          : btn.deviceName,
          'css'           : {
                               'backgroundColor': status === 0
                               ? 'rgba(200,0,0,0.5)'
                               : 'rgba(0,200,0,0.5)'
                            }
	 });
	
       $(selectorName).append(button);
    }
	   
    });
   
   xhr.fail(function(err){
   console.log('Ошибка в функции buttonLoad()');   
   });
}

/* Отправляем запрос на предмет актуальности статусов
сервер возвращает json-массив на основе которого 
кнопки окрашиваются в соответствующие цвета */

buttonLoad();

//Функция вывода лога

function readLog()
      {
		 xhr = $.ajax
               ({
                   type: 'post',
                   url: 'server.php',
                   data: 'act=log_query',
                   dataType: 'html'
               });

			   
	   xhr.done(function(data){
	   $('#log_list').html(data);	   
	   });
	  
	  
	   xhr.fail(function(err){
	   console.log('Ошибка в функции readLog()');
	   });
	  }
	  
//Если в лог файле произошли изменения выводим его на страницу
//В противном случаи ничего не делаем.

    var time = 0;
	
setTimeout(function isChangeLog()
    {
		
	   req = $.ajax
              ({
                   type: 'post',
                   url: 'server.php',
                   data: 'act=is_change_log',
                   dataType: 'html'
              });

	  
      req.done(function(lastTimeUpdate){
		  
          if(time != lastTimeUpdate)
		     {
			    time = lastTimeUpdate;
			    readLog();
			    buttonLoad();
			    console.log('Лог был обновлён' +time);
		     }
		        setTimeout(isChangeLog, freqLog); 
		
	      });

      
      req.fail(function(err){
	  console.log('isChangeLog()'+err);
	  });
	  
    }, freqLog);

/* Эта функция отправляет ajax-запрос для смены статуса.
С сервера приходит ответ с текущим статусом пина 
исходя из этого кнопкам задаются цвета */
	
function request(e)
{
      /* e.preventDefault(); */
       var pin = $(this).attr('data-num-pin');
       var power_status = $(this).attr('data-status');
	  
       req = $.ajax
              ({
                  type: 'post',
                  url: 'server.php',
                  data: 'act=switch_button&pin='+pin+'&power_status='+power_status,
                  dataType: 'json'

              });

			  
    req.done(function(data){
	   
/* Если ошибок не возникло меняем цвет кнопки */
   if(data.error == 0)
   {
	   
           /* Данное условие проверяет статус который возвращает сервер
            и соответствующим образом меняет цвет кнопки(Именно той по которой был клик),
            а так же меняет значение атрибута data-status */

        if(data.filedata < 1)
        {
             $('[data-num-pin="' +data.pin+ '"]')
			 .css("background-color","rgba(200,0,0,0.5)")
             .attr('data-status',0);
        }
   
        else
        {
             $('[data-num-pin="' +data.pin+ '"]')
			 .css("background-color","rgba(0,200,0,0.5)")
             .attr('data-status',1);
        }
		
		 console.log('pin : ' +data.pin+ ' status : ' +data.filedata);
   }   
   });
   
   req.fail(function(err){
   console.log('Ошибка в функции request()');
   });
}

/* Обработчик события привязанный к кнопкам с классом .action 
он отвечает за отправку ajax-запроса после клика по кнопке*/
   $(document).on("click",".action",request);
});