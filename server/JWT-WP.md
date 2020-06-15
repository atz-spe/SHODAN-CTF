# SHODAN WRITE UP - JWT WEAK PASSWORD

> Tags : jwt  
> Difficulty : easy  
> Attack type : jwt weakness, payload crafting  

In this challenge, we will look at how a Json Web Token works.  
By opening the url, we come across a page where it is possible to do 2 things:  
- Generate a JWT
- Get the flag (but only for an admin)

![jwt-wp-site](/images/jwt-wp-site.png)

By clicking on send, our jw token is created, we can check it in the dev console of the browser, network part (it is preceded by 'Bearer').  

![jwt-wp-cookie](/images/jwt-wp-cookie.png)

By pressing the send flag, we have an error message, the token does not seem to be the one the server is waiting for.  
To play with this request, let's copy it in Postman with the option `copy as curl`.  

![jwt-wp-postman](/images/jwt-wp-postman.png)

Now let's go to the online tool [jwt.io](https://jwt.io/), which will be used to decode our JWT.  
For information, a JWT is made up of 3 parts, separated by dots:  
- header
- payload
- secret

Each of these parts is base64 encoded. The secret, meanwhile, is encrypted according to the algorithm contained in the header (here, sha256).  

![jwt-wp-decode](/images/jwt-wp-decode.png)

Here we can see that our JWT contains a `user` role in its payload.  
The flag part being reserved for admin, let's try to change this value.  
The challenge is called `Weak password`: we can deduce that the signature of the JWT has a weak secret.  
In the list of the most used passwords, we have the famous 1234, 123456789, azerty,..  
Let's go this time for `password`. Here is the final structure of our JWT:  

![jwt-wp-craft](/images/jwt-wp-craft.png)

Now let's test if everything works as expected.  
To do this, we copy the new JWT and replace it in the Postman headers.  

![jwt-wp-flag](/images/jwt-wp-flag.png)

After submitting, the flag appears!  
The token is good, all that remains is to validate the challenge on the platform.  