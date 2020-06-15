# SHODAN WRITE UP - SQLI EASY

> Tags : sql  
> Difficulty : medium  
> Attack type : basic sql injection  

The challenge presented here is the first of a series of 6 challenges concerning SQL injections.  
Once the url is open, we arrive on the home page of a weapon sales site.  

![sql-easy-site](/images/sql-easy-site.png)

By wandering around a bit, we can see 3 sections, `Looking for a specific item?`, `All shops`, and `My profile`.  
Throughout the sqli challenge suite, pages containing a vulnerable field can be identified by the presence in the source code of an `IGNOREME` appendix.  
Here our candidate is the item search page.  

![sql-easy-search](/images/sql-easy-search.png)

Let's try to find a weapon.  
After some arbitrary tests, here is one.  
This allows us to observe at first what the database returns to us, and what we can put in the search bar (word, number, ..).  

![sql-easy-shuriken](/images/sql-easy-shuriken.png)

The field therefore waits for a word, surely delimited by quotes in the SQL query, and returns to us several elements rendered by the code, such as a name, a link, a price, a photo.  
Here is what the source code looks like, with our famous appendix `IGNOREME`.  

![sql-easy-source](/images/sql-easy-source.png)

Now let's try some basic SQL injections.  
These are easily found on the net by looking for cheat sheet sqli.  
Our first payload is probably the best known of them : `' OR 1=1 #`.  
Some explanations :  
The SQL request on the server side must surely look like something of the format :  
```sql
SELECT * FROM item WHERE item_name = '$user_input' [...]
```
The starting quote in our payload is therefore used to close the field in which a word is contained, and the ending hashtag, comment in SQL, is used not to interpret the rest of the initial request (including the IGNOREME).  
As to `OR 1=1`, it allows to generate the following request :  
```sql
SELECT * FROM item WHERE item_name = '' OR 1=1
```
`1=1` being always true, the database is supposed to return to us all that contains `item`.  

![sql-easy-dump](/images/sql-easy-dump.png)

Now is the time to make more complex and precise payloads in order to descend the layers of the database to our flag.  
For this, we can use a second technique, the keyword `UNION`.  
In SQL, this allows you to combine two requests in one, like a `&&` in unix.  
So we're going to close our field, and create a second request over which we have full control.  
Here is the payload we are using now:  
```sql
' UNION SELECT 'a',valeur,1,1,'a' #
```
The `SELECT` allows us to get values. For the rest, looking for a few minutes, we can see that the rendering of the page expects 5 values to display an article.  
The first is a string that represents the url of the article, for a href. Then, we have the name of the article, its price, another integer, and a last string which represents the url of the photo.  
So we can put values in hard, and make our article name dynamic in order to display what we want.  
  
Display of the version of the database :
```sql
' UNION SELECT 'a',@@version,1,1,'a' #
```

![sql-easy-version](/images/sql-easy-version.png)

Display the username :
```sql
' UNION SELECT 'a',user(),1,1,'a' #
```

![sql-easy-user](/images/sql-easy-user.png)


Display the database name :
```sql
' UNION SELECT 'a',database(),1,1,'a' #
```

![sql-easy-db](/images/sql-easy-db.png)

The results are satisfactory, we now have available the name of the database.  
To go down in depth, we now need to know the names of the tables, then the columns of each table, then the values contained in each column.  

Here is our payload to print all the tables :  
```sql
' UNION SELECT 'a',table_name,1,1,'a' FROM information_schema.tables #
```

![sql-easy-table](/images/sql-easy-table.png)

So here we are with the name of each table. The one that interests us, because often fruitful, is the one that contains customer data: `customer`.  
Now we need to know which columns are contained in the `customer` table.  

Here is our payload for the columns :
```sql
' UNION SELECT 'a',column_name,1,1,'a' FROM information_schema.columns WHERE table_name = 'customer' #
```

![sql-easy-column](/images/sql-easy-column.png)

There are 5 columns, and the one that catches our eye is the `password` column.  
We now have 3 options, from the widest to the most precise :  
- Dump toutes les colonnes
- Dump uniquement l'user qui nous interesse
- Dump uniquement le flag

For the first option, we can use `SELECT *` because our table contains as many columns as the renderer expects from the argument. So it will automatically fill in the fields.  

Here's the payload :  
```sql
' UNION SELECT * FROM customer #
```

![sql-easy-all](/images/sql-easy-all.png)

All users of the site are therefore visible.  
To select only the user that interests us, we can use information that we have known since the start of this challenge: the flag is 128 characters.  

Here's the payload :
```sql
' UNION SELECT * FROM customer WHERE length(password) = 128 #
```

![sql-easy-focus](/images/sql-easy-focus.png)

This request will therefore be returned to us via SELECT, the elements of the customer columns whose password is 128 in length.  
We can use this statement to further refine our request and display only the flag.  

Here's the payload :
```sql
' UNION SELECT 'a',password,1,1,'a' FROM customer WHERE length(password) = 128 #
```

![sql-easy-flag](/images/sql-easy-flag.png)

We have the flag, we just have to put it back on the platform.  