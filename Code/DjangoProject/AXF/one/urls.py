from django.conf.urls import url

from one import views

urlpatterns = [
    url(r'^hello/', views.hello, name='hello'),
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r"^market_with_params/(?P<typeid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/", views.market_with_params, name='market_with_params'),

    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^checkuser/', views.checkuser, name='checkuser'),
    url(r'^checkemail/', views.checkemail, name='checkemail'),

    url(r'^logout/', views.logout, name='logout'),

    url(r'^activate/', views.activate, name='activate'),

    url(r'^addtocart/', views.add_to_cart, name='addtocart'),

    url(r'^changecartstate/', views.change_cart_state, name='changecartstate'),
    url(r'^changeshopping/', views.change_shopping, name='changeshopping'),
    url(r'^allselect/', views.all_select, name='allselect'),
    url(r'^makeorder/', views.make_order, name='makeorder'),
    url(r'^orderdetail/', views.order_detail, name='orderdetail'),
    url(r'^orderlistnotpay/', views.order_list_not_pay, name='orderlistnotpay'),
    url(r'^payed/', views.payed, name='payed'),
    url(r'^alipay/', views.alipay, name='alipay'),
]