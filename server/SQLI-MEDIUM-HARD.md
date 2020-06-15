# SHODAN WRITE UP - SQLI MEDIUM & HARD

> Tags : sql  
> Difficulty : hard  
> Attack type : blind sql injection  

In this challenge, following the walklough of sql injections, we will tackle another attack, the blind sqli.  
This more extensive attack is used when it is impossible to have visual output on the data we are trying to extract.  
It can take several forms, taking the different ways that one has to interact with a database: for example, time-based blind sql injection will allow the use of time-out functions in order to create conditions.  
For example, if our database contains a table `customer`, then time-out of 2 seconds, otherwise nothing.  
By observing the time taken by the request, we can move blindly.  

For this challenge, the method used to perform the blind sql injection is slightly different, we will see it in more detail.  
The `sqli medium` and `sqli hard` taking the same attack vectors and substantially the same payloads, they will be described in a single write-up.  

![sql-medium-site](/images/sql-medium-site.png)

Here is the interface on which we arrive.  
As before, we have a search field, which it is possible to check as vulnerable thanks to the keyword `IGNOREME` in the source code.  
But this time, the search is a little different: indeed, instead of a word, we are now looking for an amount, in the form of an integer.  
We can assume that the SQL request on the server side therefore changes slightly :  
```sql
SELECT * FROM item WHERE price <= $user_input [...]
```

Now try to enter a random price :  

![sql-medium-random](/images/sql-medium-random.png)

We have 2 results.  
The reasoning is therefore as follows: we have a request that will compare an integer to data, and return corresponding articles to us.  
We can divert this operation to our advantage.  
The cheapest item is the shuriken: if we enter 2, it will be displayed. If we enter a lower price, it will not appear on the page. So here is our success / failure condition for our blind attack.  

Here is the basic payload created to exploit this vector :  
```sql
1+(select 1 where database() = 'park_county_fair')
```

The way we will inject our request and check our return will be done with `true / false statement`.  
We will test conditions, and we will use true and false to find out if it works.  
Indeed, `true = 1` and `false = 0` : our SQL query expects an integer, the shuriken is worth 2, so just do `1 + true` and `1 + false` to get a rendering.  

`select` will return 1 if the following condition is true, otherwise 0.  
Now that we have the theory, let's move on to practice.  
For the payload above, the shuriken will be displayed because the database is well named `park_county_fair`.  

![sql-medium-db](/images/sql-medium-db.png)

Conversely, if we had entered a wrong name, the request would have returned us nothing.  

![sql-medium-wrong](/images/sql-medium-wrong.png)

Now let's find out if our flag is in the same format as on the previous challenges.  
For this, we check if the customer table, now that we know the global schema, contains a password of size 128.  
```sql
1+(select 1 where length((select password from customer where length(password) = 128))<=128)
```

![sql-medium-pass](/images/sql-medium-pass.png)

The query shows us the shuriken, so it's positive.  
So now we have to go to the longest part of the blind sql injection, the flag dump.  
The query can return us only `true` or `false`, we must test each character of our flag by advancing the offset, and comparing the decimal vs ascii value of each.  
Here is the payload :
```sql
1+(select 1 where substr((select password from customer where length(password)=128), $offset, 1)=char($decimal))
```
For example, if the character we are testing at the index `2` is indeed `55` (7), then we have it and can move on.  

![sql-medium-test](/images/sql-medium-test.png)

Our flag making 128 characters and containing base characters 16, that gives us 2048 possibilities. We will not test this by hand and use a very powerful tool to carry out attacks of any type or pentest : the [Burp Suite](https://portswigger.net/burp).  

It has a proxy functionality which makes it possible to recover requests, analyze them and then repeat them (Repeater module) or exploit them (Intruder module).  
Here is our request with the payload seen above :  

![sql-medium-burp-launch](/images/sql-medium-burp-launch.png)

We send this request to the intruder, and can modify the body in order to place payload positions there. These positions are the `offset` of our flag and the `decimal` character that will be tested.  

![sql-medium-position](/images/sql-medium-position.png)

Next, we will import two lists, with an offset from 1 to 128, and the decimal values of `0123456789abcdef`.  

![sql-medium-set](/images/sql-medium-set.png)

Before starting our attack, we have one thing to clarify in order to see more clearly: our condition for success.  
For this, we will specify to Burp that he must perform a grep on the body of http responses in order to search for the term `shuriken`, specifying that our check has succeeded.  

![sql-medium-grep](/images/sql-medium-grep.png)

We can launch the attack.  
A new page will open, and will test for each offset our list of decimal values.  
When the `shuriken` box is checked, we are on the right character.  

![sql-medium-flag](/images/sql-medium-flag.png)

We just have to recover all the decimal values, enter them in a tool like [cyberchef](https://gchq.github.io/CyberChef) in order to convert decimal / ascii, and enter our flag on the platform.  