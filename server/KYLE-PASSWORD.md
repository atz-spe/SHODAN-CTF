# SHODAN WRITE UP - KYLE PASSWORD v1 / v2

> Tags : php  
> Difficulty : medium  
> Attack type : basic test  

This challenge is relatively simple.  
When opening the url, we come across a page of terms and conditions.  

![kyle-site](/images/kyle-site.png)

By accepting them, a new page opens.  

![kyle-accept](/images/kyle-accept.png)

So we are trapped, a cookie has been generated and we can not go back to refuse them.  
The only way, find our `Ipple cancel key`.  

Sometimes you have to go to the simplest and test basic things.  
Here is the result when we enter `Ipple`:  

![kyle-flag](/images/kyle-flag.png)

So we have the flag, it only remains to return it.  
The solution is the same for v2.  