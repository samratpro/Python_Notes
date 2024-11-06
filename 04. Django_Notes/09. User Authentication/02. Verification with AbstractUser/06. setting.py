
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxxxxxx'   
# Step 1: https://myaccount.google.com/
# Step 2: From Security section turn on 2 step verification
# Step 3: Search with " App Passwords "
# Step 4 : Create App selete others and generate token


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mdsamrat25800@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxxxxx'   
DEFAULT_FROM_EMAIL = 'mdsamrat25800@gmail.com'
PASSWORD_RESET_TIMEOUT = 14400  # Seconds



# This is required when create custom user type with AbstractUser
AUTH_USER_MODEL = 'userapp.AppUser'    # ----------------- userapp is app name here, this is required if a custom user want to login
# This is required for admin backend
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'App_Name.auth_email.EmailBackend',           # App name must be current app name
]

