# SHODAN WRITE UP - JWT ALGORITHM

> Tags : jwt  
> Difficulty : medium  
> Attack type : jwt weakness, payload crafting  

In this challenge, we will look at how a Json Web Token works.  
By opening the url, we come across a page where it is possible to do 2 things:  
- Generate a JWT
- Get the flag (but only for an admin)

![jwt-algo-site](/images/jwt-algo-site.png)

By clicking on send, our jw token is created, we can check it in the dev console of the browser, network part (it is preceded by 'Bearer').  

![jwt-algo-cookie](/images/jwt-algo-cookie.png)

By pressing the send flag, we have an error message, the token does not seem to be the one the server is waiting for.  
To play with this request, let's copy it in Postman with the option `copy as curl`.

![jwt-algo-postman](/images/jwt-algo-postman.png)

Now let's go to the online tool [jwt.io](https://jwt.io/), which will be used to decode our JWT.  
For information, a JWT is made up of 3 parts, separated by dots:  
- header
- payload
- secret

Each of these parts is base64 encoded. The secret, meanwhile, is encrypted according to the algorithm contained in the header (here, sha256).  

![jwt-algo-decode](/images/jwt-algo-decode.png)

Here we can see that our JWT contains a role `user` in its payload.  
The flag part being reserved for admin, let's try to change this value.  
Here is the final structure of our JWT:  

![jwt-algo-craft](/images/jwt-algo-craft.png)

The challenge is called `Algorithm`: we can deduce that we will have to play with the different algorithms that a JWT implements and the vulnerabilities that go with it.  
From [jwt.io](https://jwt.io/), it is not possible to directly modify the header in order to put the algorithm we want.  
Each part being in base64, it is quite simple to change it with tools like  [cyberchef](https://gchq.github.io/CyberChef) or the unix utility `base64`.  
Here is the first part of our JWT, decoded:  

![jwt-algo-cyberchef](/images/jwt-algo-cyberchef.png)

Now let's see what algorithms are available to us:  
- HS256 / HS384 / HS512
- RS256 / RS384 / RS512
- ES256 / ES384 / ES512
- PS256 / PS384
- none

The vulnerability we are looking for concerns the `none` algorithm.  
Indeed, when we specify `none` in our header, the secret of the token is completely useless because it will not be checked. (cf: [hacking jwt tokens with the none algorithm](https://blog.pentesteracademy.com/hacking-jwt-tokens-the-none-algorithm-67c14bb15771))  
As we do not have the secret, it would be possible to bruteforce but let's go on the first option.  
By taking back our token end, we can modify it on the fly, and replace the `alg` part with `none`, which generates a new part in b64.  

![jwt-algo-none](/images/jwt-algo-none.png)

It only remains for us to return to `Postman`, change the header of the cookie where our Bearer JWT is, replacing the first part of the token (until `.`) with our craft.   
The secret was not checked with this algorithm, no need to leave the part of the secret that causes a 500 error on the server side.  
Here is our final token:  
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
```

![jwt-algo-flag](/images/jwt-algo-flag.png)

We submit our request, and the flag is displayed !  