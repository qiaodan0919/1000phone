$(function () {
    $('#alipay').click(function () {
        console.log('success');

        var orderid = $(this).attr('orderid')
        $.getJSON('/one/payed',{'orderid': orderid}, function (data) {

            console.log(data)
            if(data['status'] === 200){
                window.open('/one/mine/', target='_self')
            }
        } )

    })
})