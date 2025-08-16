db = {
    "john": {
        "name": "john",
        "phone": "09012345485",
        "email": "john@gmail.com"
    },
    "precious": {
        "name": "precious",
        "phone": "09012345485",
        "email": "precious@gmail.com"
    },
    "mary": {
        "name": "mary",
        "phone": "09012345485",
        "email": "precious@gmail.com"
    }
}

name = "precious"

if name not in db:
    print("issue with here") 

db.pop(name)  # remove from dict

print(db)
