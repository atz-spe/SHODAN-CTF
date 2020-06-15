# SHODAN WRITE UP - COSMONEWT & ROIDRAT

> Tags : upload  
> Difficulty : medium  
> Attack type : php file upload  

In this challenge, we will have to exploit a flaw via php that can allow the simple execution of commands on the server side, until a complete compromise of the system.  
On arriving at the url which is provided to us, here is the page which is displayed to us:  

![upload-site](/images/upload-site.png)

We have the possibility to consult a `Gallery`, choose a file, and upload it to the site.  
From what is written, it seems that the server is waiting for an image.  

Let’s take a look at some theory before.  
The file upload attack consists, when it is possible to send a file to a server in php, to embed code which will be interpreted on the server side.  
By consulting the path of our file on the site, for example `www.site.com/file/my_file.php`, the server will retrieve the file and interpret it.  
What will be displayed on the page will therefore be the result of the order.  
```php
<?php
system('id');
?>
```
With a payload of this type, by consulting the url of our file, the content of the page should therefore be the result of the `id` command on the server !  

Now let's go to practice.  
First, we need to know what type of file we can upload, and which are prohibited.  
Let's start at the simplest with a file in `.php`.  

![upload-basic](/images/upload-basic.png)

Here is the result. The site does not seem to accept a file with the `.php` extension.  
However, to guarantee that the file will be correctly interpreted as server side code, we cannot add an extension such as `.txt`, `.png`, etc..  
With the [Burp Suite](https://portswigger.net/burp), it is possible to send an extension wordlist in order to test one by one the server returns for each of them.  
Let's test with a variant, `.pht`.  

![upload-pht](/images/upload-pht.png)

This time, the file has been uploaded. The problem is that the server is waiting for an image and seems to check the header of our upload: as ours does not contain any of the basic headers such as `image/gif`, `image/jpeg` or `image/png`, the upload does not go to the Gallery folder, the only place we have access to via url (for execution).  

Let's test with a basic complaintxt header for GIFs, `GIF89a;`.  
By writing this header in our file, with a utility like `nano`, we can now see if the server accepts our upload.  

![upload-complete](/images/upload-complete.png)

Perfect ! We managed to find the extension that is going well, and the header that will allow us to find our "photo" in the Gallery.  

![upload-gallery](/images/upload-gallery.png)

Here is what the gallery source code looks like in normal times: our file, once uploaded to the server, will be accessible at the url `/images/payload.pht`.  
We now need to write a payload in php which we will embed in our GIF.  

Here is the code chosen to make the payload for the exploit :
```php
GIF89a;
<?
system("cat /etc/passwd");
?>
```

Let's try the upload, everything seems to work. Going to the url of our file, here is the result :

![upload-flag](/images/upload-flag.png)

We have our flag !  

Having the power to execute server side code, we can still go further and try to compromise it and access the flag.  
The idea is to set up a reverse-shell, with the tools present on the machine, to take control of the current session.  
Reverse-shell can be executed with all kinds of binaries. Among them, `python`, `perl`, `netcat`, `socat`, `telnet`,..
So let's see what utilities are available to us :
```php
GIF89a;
<?
system("ls -la /usr/bin");
?>
```

Among all, `python3.x` has performance rights and responds positively with a payload `python3.x -V`.  
Now write our reverse-shell payload.  
We inject it into our file, and wait with a listener which will handle our incoming connection :
```
nc -lnvp 1337
```

We upload the file, we go to the url, and we have access to the server.  

![upload-pwn](/images/upload-pwn.png)

Let's see if everything is good with our initial order, `cat /etc/passwd`.  

![upload-pwn-flag](/images/upload-pwn-flag.png)

At this stage, we can try to make a `privilege escalation` in order to become root, thanks to the SUID bit of certain binaries.  
The SUID is a right attributed to certain binaries, in order to allow it to be executed as root (for those who require root rights on the system, but accessible to an average user, like the binary `passwd` which allows us to change our password in `/etc/shadow` without having write and read rights on it).  
When this bit is assigned on certain programs, it is possible to use it to gain privilege and become root.  
The website [GTFOBins](https://gtfobins.github.io/) lists all the binaries that allow you to write file, launch a shell, become sudo or pwn the system.  

To find the binaries on which the SUID bit is active, we can use the command `find` :  
```
find / -perm -u=s -type f 2>/dev/null
```

After running it on the server, we can find several binaries and look for them in GTFOBins. Among them, `mount` is the only one that has an attack vector.  

![upload-suid](/images/upload-suid.png)

As we can see here, if the `mount` command is accessible via sudo, it is possible to bind a shell to the binary, so that we can then execute the command as root and have a full privilege bash.  
Unfortunately, sudo not being active on this binary and on our user in general, it was impossible to use this axis.  

So we saw how to find the flag in two ways, but couldn't go any further (the goal of the challenge was not to damage the server or compromise the integrity or availability of the flag).  
It only remains to enter the flag on the platform to validate it!  