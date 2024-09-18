# GraphQL

run `strawberry` server :

```
strawberry server app --host 0.0.0.0 --port 8000
```

### QUERY 1

Get the information of a specific user

```
{
  getUser(id: 1) {
    id
    username
    hashedPassword
    isActive
  }
}
```


### QUERY 2
Get a list of all users

```
{
    allUsers { 
        id
        hashedPassword
        isActive 
    }
}
```

PyPi : https://pypi.org/project/strawberry-graphql/

Website : https://graphql.org/

Github : https://github.com/strawberry-graphql/strawberry