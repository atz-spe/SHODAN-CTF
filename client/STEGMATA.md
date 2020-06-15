# SHODAN WRITE UP - STEGMATA

> Tags : flash / reverse  
> Difficulty : medium  
> Attack type : reverse engineering  

By opening the url of this challenge, we come across a page containing a flash module (displayed on some browsers).    

![stegmata-site](/images/stegmata-site.png)

From the source code side, nothing apart from the path to the flash used.   

![stegmata-source](/images/stegmata-source.png)

Following this link, we download the file `stegmata.swf`.  
The challenge being tagged with reverse, we will have to find the code that this flash contains.    

Thanks to the JPEXS utility, we open the file and can take a look at the source code.    

![stegmata-jpexs](/images/stegmata-jpexs.png)

Going down there, we find a variable `stegmata` which contains the flag.  

![stegmata-flag](/images/stegmata-flag.png)

It only remains to return it to the platform.  