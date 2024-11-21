# Receipt Processor
This is an implementation of the API specified in this exercise:
https://github.com/fetch-rewards/receipt-processor-challenge. It is a minimal Flask webserver with endpoint tests and a Docker image.

## Instructions
Build docker images: `./build.sh`

Run pytest:  `./run_test.sh`

Run local server on port 5000: `./run_server.sh`

## Endpoints
`localhost:5000/receipts/process` (POST)

`localhost:5000/receipts/{id}/points` (GET)