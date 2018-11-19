$(function () {
    $("#login").click(function () {
        window.open('/one/login', target='_self');
    });

    $("#regis").click(function () {
        window.open('/one/register', target='_self');
    });

    $("#not_pay").click(function () {
        window.open('/one/orderlistnotpay/', target='_self')
    })


})

