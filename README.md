### prerequisites
- running docker
- postman
### startup
`docker compose up -d`
### documentation
localhost:8000/docs

### known errors
- book which exists, has a rating by a user, but that user has no other rankings would fail: 0394571770

### planned features
- DELETE /users/ratings/{isbn}
- DELETE /users/ratings/{rating_id}