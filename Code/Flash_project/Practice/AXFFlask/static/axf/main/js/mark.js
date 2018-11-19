$(function () {

    $('aside,menu').scroll(function (event) {
        event.stopPropagation();
        event.preventDefault();

        return false;
    });

    $('#all_type').click(function () {
        $('#all_view').slideDown();
        $('#all_type div').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');

        $('#sort_view').hide();
        $('#all_sort div').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    })


    $('#all_view').click(function () {
        $('#all_view').hide();
        $('#all_type div').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');

    })

    $('#all_sort').click(function () {
        $('#sort_view').slideDown();
        $('#all_sort div').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');

        $('#all_view').hide();
        $('#all_type div').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    })

    $('#sort_view').click(function () {
        $('#sort_view').hide();
        $('#all_sort div').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');

    })

    $('.subShopping').click(function () {
        console.log('sub')
    })

    $(".addShopping").click(function () {
        var $add = $(this);
        var goodid = $add.attr('goodid');
        $.get('/one/addtocart/', {'goodid': goodid, 'type':'add'}, function (data) {
            console.log(data)
            if (data['status'] === 301){
                window.open('/one/login/', target='_self')
            }else if(data['status'] === 200){
                console.log(data['c_good_num']);
                $add.prev('span').html(data['c_good_num']);
            }
        })
    })

        $(".subShopping").click(function () {
        var $sub = $(this);
        var goodid = $sub.attr('goodid');
        $.get('/one/addtocart/', {'goodid': goodid, 'type':'sub'}, function (data) {
            console.log(data)
            if (data['status'] === 301){
                window.open('/one/login/', target='_self')
            }else if(data['status'] === 200){
                console.log(data['c_good_num']);
                $sub.next('span').html(data['c_good_num']);
            }
        })
    })

    $(".num_span").each(function () {
        var $num_span = $(this)
        console.log($num_span.html().trim())
        if($num_span.html().trim() === ''){
            $num_span.html("0")
        }
    })


});