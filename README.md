sudo docker run --name watch_share -p 5432:5432 -e POSTGRES_PASSWORD=1234 -e POSTGRES_USER=liro -e POSTGRES_DB=watch_share -d postgres:alpine3.20

