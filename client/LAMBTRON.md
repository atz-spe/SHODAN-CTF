# SHODAN WRITE UP - LAMBTRON

> Tags : null  
> Difficulty : medium  
> Attack type : redirect checking  

On this challenge, we come across an image that turns in a loop.  

![lambtron-site](/images/lambtron-site.png)

As for the source code, nothing very conclusive: a `rotateAnimation()` function that rotates the image, with a statement for each type of browser.  

By having an eye, we can notice a change: the url on the platform is different from the one we end up on next.  
So there is a redirect.  
If we open the url with Burp, Postman or even more simply with curl, we arrive on the first page of use (redirects are not emitted by default with these tools).  

![lambtron-curl](/images/lambtron-curl.png)

By analyzing the html, we quickly understand that when this page is reached, a `window.location` is performed to go to the page containing the image that is rotating.  
In the `<head>` part, another url is specified.  
By adding it to the one we had initially, here is the result.  

![lambtron-redirect](/images/lambtron-redirect.png)

The error code is our flag, we are entering it on the platform, and this challenge is valid.  