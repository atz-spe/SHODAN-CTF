# SHODAN WRITE UP - PARK COUNTRY THE RETURN

> Tags : sql  
> Difficulty : medium  
> Attack type : blind sql injection  

In this challenge, following the walklough of sql injections, we will tackle another attack, the blind sqli.  
This more extensive attack is used when it is impossible to have visual output on the data we are trying to extract.  
It can take several forms, taking the different ways that one has to interact with a database: for example, time-based blind sql injection will allow the use of time-out functions in order to create conditions.  
For example, if our database contains a table `customer`, then time-out of 2 seconds, otherwise nothing.  
By observing the time taken by the request, we can advance blindly.   

For this challenge, the method used to perform the blind sql injection is slightly different, we will see it in more detail.  
On the interface, this time we are interested in the `All shops` page (vulnerability verifiable in the source code, thanks to the keyword IGNOREME).   

![sql-park-shop](/images/sql-park-shop.png)

We can select stores, and are redirected to their page, with the weapons sold.  

![sql-park-page](/images/sql-park-page.png)

Now let's take a look at the source code to see how the page works, as well as the store display.  

![sql-park-source](/images/sql-park-source.png)

Here are the elements that seem to be interesting: an `input` hidden sends an `id` when the form of each store is submitted via the `post` method.  
So we understand that by manipulating the id that is submitted in the request, we can determine which store will be loaded. This gives us an entry point for our attack.  

Let's try to modify the value of this `id` using a powerful tool to perform web attacks or pentests, the [Burp Suite](https://portswigger.net/burp).

It has a proxy functionality which makes it possible to recover requests, analyze them and then repeat them (Repeater module) or exploit them (Intruder module).  
Here is our basic request when we click on the first store:  

![sql-park-burp](/images/sql-park-burp.png)

Now try to inject a payload into this parameter, in order to create a statement `true / false`, which will give us an error or a valid request: for example, `id = 1 AND 1=0` or `id = 1 AND 1=1`.  
Let us observe the results with the following payload, which verifies whether the database does indeed contain a flag in the usual format (sha512 of 128 characters), according to the diagram seen previously:  
```sql
id=1 AND length((select password from customer where length(password) = 128))=128 IGNOREME
```

![sql-park-valid](/images/sql-park-valid.png)

Bingo. Our payload is working, the store page with id 1 is displayed correctly. The request did not emit an error, so our flag exists.  
Now let's see what would have been displayed if we were looking for a 129 character flag.  

![sql-park-wrong](/images/sql-park-wrong.png)

The page returns a `SQL error ...`, so we have our two failure / success conditions.  
Let's move on and activate Burp's `Intruder` module to test payloads, the flag dump phase being the longest during a blind sql injection.  

![sql-park-position](/images/sql-park-position.png)

The goal here is to test each character of our flag, comparing it to the decimal values of `0123456789abcdef`, and incrementing the offset of our position if the character is good.  
We therefore place payload positions on these two values in our body.   

This is our payload :
```sql
id=1 AND substr((select password from customer where length(password)=128), $offset, 1)=char($decimal) IGNOREME
```

![sql-park-options](/images/sql-park-options.png)

In the Payload Sets part, we import an integer list going from 1 to 128, then a list of decimal values, which we will use to compare the characters of our flag.  
Finally, we will specify our condition of victory at Burp in order to go back when the character is good, in the `Grep - Match` part: we know that the store `Park Park Fair` is displayed when the query is good, Burp will search so this expression in the body of http requests.  

![sql-park-grep](/images/sql-park-grep.png)

We can now launch the attack.  
A new page will open, and will test our payloads one by one, by comparing the decimal value of each character of the flag with our list.  
If Burp detects our match, the `Park County Fair [...]` box will be checked.  

![sql-park-flag](/images/sql-park-flag.png)

We just have to recover all the decimal values, enter them in a tool like  [cyberchef](https://gchq.github.io/CyberChef) in order to convert decimal / ascii, and enter our flag on the platform.  