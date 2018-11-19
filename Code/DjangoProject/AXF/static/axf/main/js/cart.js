$(function () {
    var $confirms_span = $('ul li div span span')

    $(".confirm").click(function () {
        var $confirm = $(this);
        var cartid = $confirm.parents("li").attr('cartid')

        $.getJSON('/one/changecartstate/', {'cartid': cartid}, function (data) {
            if (data['status'] === 301) {
                window.open('/one/login/', target = '_self')
            } else if (data['status'] === 200) {
                $("#total_price").html(data['total_price'])

                if (data['c_is_select']) {
                    $confirm.find('span').find('span').html("√")
                } else {
                    $confirm.find('span').find('span').html("")
                }
                if (data['is_all_select'] === true) {
                    $("#all_span").find('span').html('√')
                } else {
                    $("#all_span").find('span').html('')
                }
            }
        })
        return false
    })


    $("#all_span").click(function () {
        var $all_span = $(this);
        var select_list = [];
        var unselect_list = [];
        $confirms_span.each(function () {
            var $confirm = $(this);
            var cartid = $confirm.parents('li').attr('cartid');
            if ($confirm.html().trim() === '') {
                unselect_list.push(cartid);
            } else {
                select_list.push(cartid);
            }
        });
        if (unselect_list.length > 0) {
            $.getJSON('/one/allselect', {'cart_list': unselect_list.join('#')}, function (data) {
                if (data['status'] === 200) {
                    $("#total_price").html(data['total_price'])
                    $all_span.find('span').html('√');
                    $confirms_span.html('√')
                }
            })
        } else {
            if (select_list.length > 0) {
                $.getJSON('/one/allselect', {'cart_list': select_list.join('#')}, function (data) {
                    if (data['status'] === 200) {
                        $("#total_price").html(data['total_price'])
                        $all_span.find('span').html('');
                        $confirms_span.html('')
                    }
                })
            }
        }
        return false
    });


    $(".subShopping").click(function () {
        var $sub = $(this);
        var $li = $sub.parents('li');
        var cartid = $li.attr('cartid');
        $.getJSON('/one/changeshopping/', {'cartid': cartid, 'type': 'sub'}, function (data) {
            if (data['status'] === 200) {
                $("#total_price").html(data['total_price'])
                var $span = $sub.next('span');
                console.log(data);
                if (data['goods_num'] > 0) {
                    $span.html(data['goods_num'])
                } else {
                    $li.remove()
                }
            }
        })
    })


    $(".addShopping").click(function () {

        var $add = $(this);
        var $li = $add.parents('li');

        var cartid = $li.attr('cartid');
        $.getJSON('/one/changeshopping/', {'cartid': cartid, 'type': 'add'}, function (data) {

            if (data['status'] === 200) {
                $("#total_price").html(data['total_price'])
                var $span = $add.prev('span');
                $span.html(data['goods_num']);
            }
        })
    });

    $("#make_order").click(function () {
        var select_list = [];
        var unselect_list = [];
        $confirms_span.each(function () {
            var $confirm = $(this);
            var cartid = $confirm.parents('li').attr('cartid');
            if ($confirm.html().trim() === '') {
                unselect_list.push(cartid);
            } else {
                select_list.push(cartid);
            }

            if (select_list.length === 0) {
                return
            }
        });
        $.getJSON('/one/makeorder/', function (data) {
            console.log(data)
            if(data['status'] === 200){
                window.open('/one/orderdetail/?orderid=' + data['order_id'], target='_self')
            }
        })


        return false
    })


})