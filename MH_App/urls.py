from django.urls import path
from MH_App import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<str:pk>', views.product_detail, name='product-detail'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),

    path('top-wear/', views.top_wear, name='top-wear'),
    path('top-wear/<slug:data>', views.top_wear, name='top-wear-data'),

    path('bottom-wear/', views.bottom_wear, name='bottom-wear'),
    path('bottom-wear/<slug:data>', views.bottom_wear, name='bottom-wear-data'),

    path('search/', views.search, name='search'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='main/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='main/changepassword.html', form_class=MyPasswordChangeForm, success_url='/changepassworddone/'), name='changepassword'),
    path('changepassworddone/', auth_views.PasswordChangeDoneView.as_view(template_name='main/changepassworddone.html'), name='changepassworddone'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='main/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'), name='password_reset_complete'),

    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.show_cart, name='show_cart'),
    path('plus_cart/', views.plus_cart, name='plus_cart'),
    path('minus_cart/', views.minus_cart, name='minus_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('orders/', views.orders, name='orders'),


    path('buy/', views.buy_now, name='buy-now'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
