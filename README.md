# compressor_server
## installation
-  directly on the computer: yarn install
- in the docker container: docker-compose run --rm --no-deps backend yarn install
## polka server on port 3100
### reads status of cyromech compressor over modbus serial interface
- ip:3100 -> hello there
- ip:3100/query/sensors  -> outputs json with all sensor readings
#### Example of sensors output
```
{
   "4K": 295.201,
   "40K": 296.64
}
```
