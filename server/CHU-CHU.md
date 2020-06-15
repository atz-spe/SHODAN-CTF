# SHODAN WRITE UP - CHU-CHU

> Tags : java  
> Difficulty : medium  
> Attack type : source code audit, path traversal  

When we open the url of this challenge, we come across a blank page.  
By looking at the source code with a ctrl+u, we can read an `APPLET` tag.   
This type of tag is used to embed Java in a web page.  

![chuchu-source](/images/chuchu-source.png)

After reading some documentation on its operation and its attributes, it is clear that:  
```
codebase
    this attribute gives an absolute or relative URL of the directory where the applet's class files must be placed.
```

So let's see what this `/out` folder contains.  

![chuchu-out](/images/chuchu-out.png)

Several Java class files are available at this index, let's download them to see in more detail what they contain.  
After opening them in a [decompiler java en ligne](http://javadecompilers.com/), we can see that the `mPage$2.class` file contains our flag.  

![chuchu-flag](/images/chuchu-flag.png)

We just have to validate this challenge on the platform.  