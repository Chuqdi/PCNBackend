
from django.urls import path
from .views import ActivateUserEmail, CompletePasswordReset, ContinueForgotOTPPassword, DeleteUserWithEmail, ForgotPasswordRequest, GetUserReferalCode, GetUserWithID, LoginUserView, UpdateProfileImage, UpdateUserBasicInformation, UpdateUserPassword, UpdateUserPhoneNumber, UserMe, LogoutUser,UserMeAuth,GetUserTokenWithEmail, RegisterUserView, EditUserWithProfileImageView,GetPostAdministrators,EditUserView, ToggleUserActiveState, UsersStatsView, UpdateAdminPassword,AddUserDeviceToken, UsersDashboardStats





urlpatterns = [
    
    
    
    
    ###ADMIN
    path("dashboard_stats/", UsersDashboardStats.as_view()),
    path("get_users/",GetPostAdministrators.as_view(),),
    path("update_user_token/", AddUserDeviceToken.as_view(),),
    path("get_users_stats/", UsersStatsView.as_view(),),
    path("toggle_user_active_state/<int:id>/", ToggleUserActiveState.as_view()),
    path("edit_user_with_profile_image/",EditUserWithProfileImageView.as_view(),),
    path("update_admin_password/", UpdateAdminPassword.as_view()),
    path("edit_user/<int:id>/", EditUserView.as_view(),),
    
    
    ##USER
    path("login/", LoginUserView.as_view()),
    path("register/", RegisterUserView.as_view()),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("me/", UserMeAuth.as_view(), name="user_me_auth"),
    path("get_user_referal_code/", GetUserReferalCode.as_view(), name="get_user_referal_code"),
    path("forgot_password/", ForgotPasswordRequest.as_view(), name="forgot_password"),
    path("continue_forgot_password/", ContinueForgotOTPPassword.as_view(), name="continue_forgot_password"),
    path("complete_password_reset/", CompletePasswordReset.as_view(), name="complete_password_reset"),
    path("delete_user_with_email/<email>/", DeleteUserWithEmail.as_view(), name="delete_user"),
    path("activate_account/<token>/<uidb64>/",  ActivateUserEmail.as_view(), name="activateUserAccount"),
    path("update_user_basic_informations/", UpdateUserBasicInformation.as_view(), name="update_user_basic_informations"),
    path("update_profile_image/", UpdateProfileImage.as_view(), name="update_profile_image"),
    path("update_user_password/", UpdateUserPassword.as_view(), name="update_user_password"),
    path("get_user/<id>/", GetUserWithID.as_view(), name="get_user"),
    path("me/<int:id>/", UserMe.as_view(), name="user_me"),
    path("update_phone_number/<email>/", UpdateUserPhoneNumber.as_view()),
    path("get_user_token_with_email/<email>/",GetUserTokenWithEmail.as_view())
]