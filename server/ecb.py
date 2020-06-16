#!/usr/bin/env python2

import urllib
import re
import requests
import urllib3
from pip._vendor.colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers_flag = {
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'Origin': "https://websecu.epitech.eu:1443",
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Sec-Fetch-Site': "same-origin",
    'Sec-Fetch-Mode': "navigate",
    'Sec-Fetch-User': "?1",
    'Sec-Fetch-Dest': "document",
    'Referer': "https://websecu.epitech.eu:1443/990f0030f2f742da88dec57cf0d261adf2c91968825b490f84a18f139c8a000e/",
    'Accept-Language': "en-US,en;q=0.9",
}

headers = {
    'Connection': "keep-alive",
    'Accept': "*/*",
    'X-Requested-With': "XMLHttpRequest",
    'User-Agent': "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)",
    'Content-Type': "application/json",
    'Origin': "https://websecu.epitech.eu:1443",
    'Sec-Fetch-Site': "same-origin",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Dest': "empty",
    'Referer': "https://websecu.epitech.eu:1443/990f0030f2f742da88dec57cf0d261adf2c91968825b490f84a18f139c8a000e/",
    'Accept-Language': "en-US,en;q=0.9"
}
encrypt = "https://websecu.epitech.eu:1443/990f0030f2f742da88dec57cf0d261adf2c91968825b490f84a18f139c8a000e/encrypt"
decrypt = "https://websecu.epitech.eu:1443/990f0030f2f742da88dec57cf0d261adf2c91968825b490f84a18f139c8a000e/decrypt"
flag = "https://websecu.epitech.eu:1443/990f0030f2f742da88dec57cf0d261adf2c91968825b490f84a18f139c8a000e/flag"


def encrypt_aes(plaintext):
    print(Fore.LIGHTYELLOW_EX + "[-] Sending encrypt request : " + Fore.CYAN + plaintext + Fore.RESET)
    response = requests.request("POST", encrypt, data='{"plaintext":"' + plaintext + '"}', verify=False,
                                headers=headers)
    # print(response.text)
    return response.json()['ciphertext']


def decrypt_aes(ciphertext):
    print(Fore.LIGHTYELLOW_EX + "[-] Sending decrypt request" + Fore.RESET)

    response = requests.request("POST", decrypt, data='{"ciphertext":"' + ciphertext.rstrip() + '"}', verify=False,
                                headers=headers)

    return response.json()['plaintext']


def flag_aes(token):
    payload = {'token': token}
    urllib.urlencode(payload)
    response = requests.request("POST", flag, data=payload, headers=headers_flag)
    pattern = re.compile("[0-9a-f]{96}")
    result = re.search(pattern, response.text)
    print(Fore.LIGHTGREEN_EX + "[+] Flag :\t " + Fore.LIGHTMAGENTA_EX + result.group(0) + Fore.RESET)


def main():
    false_encrypt = encrypt_aes('False]')
    true_encrypt = encrypt_aes('True]')
    for i in range(0, 100):
        plaintext = "[name=admin;password=" + 'z' * i + ";is_admin=False]"
        token = encrypt_aes(plaintext)
        if false_encrypt in token:
            print(Fore.LIGHTGREEN_EX + "[+] Found right padding : " + Fore.LIGHTMAGENTA_EX + token + Fore.RESET)
            new_token = token.replace(false_encrypt, true_encrypt)
            new_plain_text = decrypt_aes(new_token)
            print(Fore.LIGHTGREEN_EX + "[-] New Token :\t " + Fore.LIGHTMAGENTA_EX + new_token + Fore.RESET)
            print(Fore.LIGHTGREEN_EX + "[-] Decrypted :\t " + Fore.LIGHTMAGENTA_EX + new_plain_text + Fore.RESET)
            flag_aes(new_token)
            exit()
        else:
            print(Fore.LIGHTRED_EX + "[-] Wrong blocks :\t " + token + Fore.RESET)


if __name__ == '__main__':
    main()
