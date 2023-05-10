# Running FastAPI on Docker

## Compose up
```shell
$ make fast-api
```

## Compose down
```shell
$ make fast-api-clean
```

# Test on EC2
using postman
### POST
```shell
http://15.164.148.99:8888/predict
```
### Body
```JSON
{
    "sentence": "사랑해요~" 
}
```
### Response
```JSON
{
    "sentence": "사랑해요~",
    "result": "0.0"
}
```