# SHODAN WRITE UP - AUTHENTICATION AES ECB

> Tags : aes  
> Difficulty : medium  
> Attack type : block cipher known-text  



As the title says, this challenge is about AES ECB.

First of all wee can see in view source some useful information.

```html
 <body>
    <h1>Auth AES_ECB</h1>
    <div id="divCheckbox" style="display: none;">
      Usefull informations:
      BLOCK_SIZE: 16
      endpoints: /, encrypt, decrypt, flag
    </div>

...

<script>
      function createToken() {
        name = document.getElementById("name").value;
        password = document.getElementById("password").value;
        $.ajax({
          timeout: 0,
          type: 'POST',
          url: window.location.href + 'encrypt',
          contentType: 'application/json',
          data: JSON.stringify({
            'plaintext': '[name=' + name + ';password=' + password + ';is_admim=False]'
          }),
          success: data => {
            document.getElementById("token").innerHTML = data.slice(16, -2);
          }
        });
      }
    </script>
```

Then we change `is_admim=False` to `admim=True` on `/encrypt` and get this error :

```json
{"ciphertext": "\u00a1No, no, no, mi querido amigo!"}
```

But we can still encrypt `False]` and then `True]` to get their values on one block, this will be useful later.
```
False] -> UMk8uZZQX9GvlQrGzPy8vQ==
True]  -> AzCp1hYuf+giBvkFpJ1uHA==
```

Thus we can try to put enough padding in other filed of the request to isolate `False]` by comparing the whole ciphertext with its ciphertext we got earlier 

So I did a [script](ecb.py) trying different size of padding until we found `UMk8uZZQX9GvlQrGzPy8vQ==` in it.  
When we got it, we just need to replace this last block with `AzCp1hYuf+giBvkFpJ1uHA==` block, and we got an admin Token !
We can know send it to `/flag` to claim the flag.  
But no worries, the [script](ecb.py) does for us !
