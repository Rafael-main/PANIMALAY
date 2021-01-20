$(document).ready(function(){
    var myDiv = $('#description');
    myDiv.text(myDiv.text().substring(0,100) + '...')

    $('form#reserve').submit(function(e){
        var $form_reserve = $(this)
        max_price = $form.find('input#max-price').val()
            date_of_reserve = $form_reserve.find('input#date-reserve')
            url = $form_reserve.attr("action");
        var post_date_reserve = $.post(url, {date_reserve: date_of_reserve})

        post_date_reserve.done(function(data){
            console.log(data);
            console.log('success')
        });
        e.preventDefault();
    });
});