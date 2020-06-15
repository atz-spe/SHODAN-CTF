# SHODAN WRITE UP - CHINPOKOMON 2

> Tags : null  
> Difficulty : medium  
> Attack type : source code audit  

De retour sur notre fameux chinpokomon, pour la v2 cette fois ci.  
En ouvrant l'url, nous apercevons une liste de "monstres", avec une photo, un titre et une description.  

![chinpokomon2-site](/images/chinpokomon2-site.png)

We can try to exploit the path traversal, and will fall on an index of, but spoil alert: this will not work on this challenge.  

![chinpokomon2-indexof](/images/chinpokomon2-indexof.png)

Let's see the source code side.  
It is written on one line, rather unreadable, which can mean two things.  
Either this is done on purpose to make it more difficult for an attacker to understand, or the person who did it does not know how to code. Let’s take a closer look at the first option.  

![chinpokomon2-source](/images/chinpokomon2-source.png)

We know two things.  
The source code is several thousand columns long and would take a long time to decrypt manually.  
The flag we are looking for, in the usual format, is a string with alphanumeric characters, with a size of 128.  
It's time to call our friend `grep`.  

With the following command, let's try to isolate the flag from the rest of the code.  
```
curl -sk https://websecu.epitech.eu:1443/d2199e0151798b6d596d4fd4d4b31f43dafaf98f209111ef3488f3d253773b8e/ | grep -E '[a-z0-9]{128}'
```

The result works, here is what grep returns:  

![chinpokomon2-grep](/images/chinpokomon2-grep.png)

It only remains for us to enter the flag on the platform.  