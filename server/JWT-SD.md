# SHODAN WRITE UP - JWT SENSITIVE DATA

> Tags : jwt  
> Difficulty : easy  
> Attack type : jwt weakness, payload crafting  

In this challenge, we will look at how a Json Web Token works.  
By opening the url, we come across a page where it is possible to do 2 things:  
- Generate a JWT
- Get the flag (but only for an admin)

![jwt-sd-site](/images/jwt-sd-site.png)

By clicking on send, our jw token is created, we can check it in the dev console of the browser, network part (it is preceded by 'Bearer').  

![jwt-sd-cookie](/images/jwt-sd-cookie.png)

By pressing the send flag, we have an error message, the token does not seem to be the one the server is waiting for.  
To play with this request, let's copy it in Postman with the option `copy as curl`.  

![jwt-sd-postman](/images/jwt-sd-postman.png)

Now let's go to the online tool [jwt.io](https://jwt.io/), which will be used to decode our JWT.  
For information, a JWT is made up of 3 parts, separated by dots:  
- header
- payload
- secret

Each of these parts is base64 encoded. The secret, meanwhile, is encrypted according to the algorithm contained in the header (here, sha256).  

![jwt-sd-decode](/images/jwt-sd-decode.png)

Here we can see that our JWT contains in its payload two fields, a role `user` and a secret `rapacediabolique`.  
The flag part being reserved for admin, let's try to change this value.  
In addition, a secret seems to be revealed, let's enter it in the signature part of our JWT without encoding it.  

![jwt-sd-new](/images/jwt-sd-new.png)

Now let's test if everything works as expected.  
To do this, we copy the new JWT and replace it in the Postman headers.  

![jwt-sd-flag](/images/jwt-sd-flag.png)

After submitting, the flag appears!  
The token is good, all that remains is to validate the challenge on the platform.  