# SHODAN WRITE UP - CHINPOKOMON

> Tags : null  
> Difficulty : medium  
> Attack type : path traversal  

When arriving at this challenge, a photo is displayed and an alert popup prints us on the "CHIMPOKOMON" screen.  

![chinpokomon-site](/images/chinpokomon-site.png)

At the source code level, quite thin, we just have paths to the image and what seems to be the javascript part of our page.  

![chinpokomon-source](/images/chinpokomon-source.png)

When looking, there is just an `alert("CHIMPOKOMON!");`.  
One element catches the eye despite everything: we are looking at a file, included by the url in the `/data/js` folders.  
When trying to go back to the `/js` folder, an index of is displayed: this is a good sign, our server seems vulnerable to path traversal.  

![chinpokomon-indexof-js](/images/chinpokomon-indexof-js.png)

Within the `/data` folder, we can see the two folders we know as well as a file invisible until now:  

![chinpokomon-indexof-data](/images/chinpokomon-indexof-data.png)

By clicking on it to open it, we come across the flag.  