Flask web project written and hosted on pythonanywhere.com.

Features include:

1) Authenticate sessions
For example, if the user with the username user1 logs in successfully, the browser is 
redirected to the URL /user/user1. Then if we try to open the page at /user/user2, 
the app redirects the browser to the login page.

2) SMS and email capability
After the user has authenticated, on the user's home page, provide forms so that the 
user can send an email using SendGrid account and can send an SMS text message 
using Twilio account. On the user's home page, provide a logout link so that the 
currently logged in user's session is terminated and the browser is redirected back to the URL /.

3) Basic username and password security features
Password require a minimum of 8 characters and maximum of 64 characters
Usernames are case-insensitive.

4) Environment variables are not hard-coded
Sensitive configuration strings and passwords are not hard-coded in flask_app.py

Custom 404 error page includes:

1) Include an animated GIF or image that is funny
2) Page includes date and time requests in 2 formats
  UTC and Client's time zone and locale settings

