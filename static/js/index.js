$(document).ready(function(){
    $('#btn_1').click(function(){
        html_data = {
            flag: 1,
            sd: $('#sheduled_departure').val(),
            fc: $('#fare_conditions').val()
        }
        $.ajax({
            url: '',
            type: 'post',
            data: html_data,
            success: function(response){
                $('#flight_no').children().remove();
                for(i = 0; i < response.res.length; i++ ){
                    $('#flight_no').append(`<option>${response.res[i]}</option>`);
                }
                $('#div_2').attr('hidden', false);
            },
            error: function(){	
                alert('Что-то пошло не так!')
            }
        });
    
    })
    $('#btn_2').click(function(){
        html_data = {
            flag: 2,
            sd: $('#sheduled_departure').val(),
            fc: $('#fare_conditions').val(),
            fn: $('#flight_no').val()
        }
        $.ajax({
            url: '',
            type: 'post',
            data: html_data,
            success: function(response){
                $('#p_sheduled_departure').text(`Запланирован вылет: ${response.res[0][0]}`);
                $('#p_sheduled_arrival').text(`Запланирован прилет: ${response.res[0][1]}`);
                $('#p_departure_airport').text(`Отлет из: ${response.res[0][2]}`);
                $('#p_arrival_airport').text(`Прилет в: ${response.res[0][3]}`);
                $('#p_status').text(`Статус рейса: ${response.res[0][4]}`);
                $('#p_aircraft_code').text(`Код самолета: ${response.res[0][5]}`);
                $('#p_actual_departure').text(`Актуальная дата вылета: ${response.res[0][6]}`);
                $('#p_actual_arrival').text(`Актуальная дата прилета: ${response.res[0][7]}`);
                $('#p_count').text(`Количество билетов: ${response.res[0][9]}`);
                $('#p_amount').text(`Цена билета: ${response.res[0][8]}`);
            },
            error: function(){	
                alert('Что-то пошло не так!')
            }
        });   
    })
});


