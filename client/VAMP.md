# SHODAN WRITE UP - VAMP

> Tags : javascript  
> Difficulty : medium  
> Attack type : source code audit  

We arrive at the challenge, a page with a field offers us to enter an access token to access the back end.  

![vamp-site](/images/vamp-site.png)

When testing a token, we have a popup that shows that it is not good.  

![vamp-alert](/images/vamp-alert.png)

Let's take a look at the source code.  
Here, we can see that the script tag contains a function, called when the user clicks on submit.  

![vamp-source](/images/vamp-source.png)

We therefore understand that if the token is equal to the following string, obfuscated in hexa, we will be redirected to the second obfuscated string, contained in the `window.location.replace`.  
The token does not interest us anymore, it only remains for us to put the string in hexa in [Cyberchef](https://gchq.github.io) to know the page :
`backendc1sd59acds.html`  

By going to this page, we come across a "Backend : Nothing."  
Let's go back to the source code.    
As a reminder, we are looking for a flag in the format of a hash in sha512, of length 128.  
An element seems to stick: the image `./img/vamp.png` has an alt with a string in sha.  

![vamp-flag](/images/vamp-flag.png)

By entering it on the platform, the challenge is validated.