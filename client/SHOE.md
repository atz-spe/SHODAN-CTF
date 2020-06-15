# SHODAN WRITE UP - SHOE

> Tags : sql  
> Difficulty : medium  
> Attack type : api route checking  

When arriving at the url provided by the platform, we have an error code directly:  

![shoe-forbidden](/images/shoe-forbidden.png)

At the start, it is possible to believe that the challenge does not work.
However, let's try to test other options by opening `Postman`.    
Sometimes, certain routes can allow to reach a page when it contains a connection field, because this one could not be implemented to receive any type of request.   
  
Let's test here if the `GET` route is not the only one to be restricted, by making a `VIEW` request.  

![shoe-view](/images/shoe-view.png)

Bingo. With a `VIEW` request, the` 403 forbidden` which prevented us from seeing the page is not active.  
We can therefore retrieve the flag, contained in the alt tag of our page.  