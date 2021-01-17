$(document).ready(function(){
    $('form#price-range').submit(function(e){
        var $form = $(this),
            min_price = $form.find('input#min-price').val()
            max_price = $form.find('input#max-price').val()
            url = $form.attr("action")
        var post_price = $.post('/prices', {min_price:min_price, max_price:max_price})

        post_price.done(function(data){
            console.log(data)
        })

        e.preventDefault();
    });

    $('form#search-more').submit(function(e){
        console.log($('input[name="amenities"]:checked').serialize());
        console.log($('input[name="facilities"]:checked').serialize());
        console.log($('input[name="PropType"]:checked').serialize());
        var $form_search = $(this),
            url = $form_search.attr("action")
        var post_search_more = $.post(url, {amenities:$('input[name="amenities"]:checked').val(), PropType:$('input[name="PropType"]:checked').val(), facilities:$('input[name="facilities"]:checked').val()})

        post_search_more.done(function(data){
            console.log(data)
        });
            
        e.preventDefault();
    });
});