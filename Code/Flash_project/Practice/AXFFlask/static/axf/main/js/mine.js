$(function () {
    $("#login").click(function () {
        window.open('/userAction/login', target='_self');
    });

    $("#regis").click(function () {
        window.open('/userAction/register', target='_self');
    });

    $("#not_pay").click(function () {
        window.open('/userAction/orderlistnotpay/', target='_self')
    })


})

