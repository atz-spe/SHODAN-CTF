# SHODAN WRITE UP - CARTMAN

> Tags : javascript  
> Difficulty : medium  
> Attack type : source code audit  

By opening the page given on the platform, we have a login form username / password.  
There does not seem to be any other functionality.  

![cartman-site](/images/cartman-site.png)

Let's not waste time and look at the source code.  

![cartman-source](/images/cartman-source.png)

The content of the script tag seems interesting.  
By carefully reading its content, we notice that there are clear conditions regarding authentication on the platform.  
If we enter the login `Kyle`, we will have no results.  
However, with the `Cartman` login, a post of `login.php` will be sent to the server and a page will be displayed to us.  
Above, we can see that another if seems to contain the format of the expected password.  
By deciphering it, we understand that the `7` must replace the `t`, similarly for the `0` with the `o`. Then, our password is separated by the `_` which serve as delimiters, then compared with hard values.  

The password will therefore be : `wh47_4_h4x0r`.  
It works ! Here's the page that is displayed :  

![cartman-success](/images/cartman-success.png)

It only remains for us to recover the flag and return it to the platform.  