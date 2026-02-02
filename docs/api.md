# API Documentation

## Base URL

```
http://localhost:5000
```

## Authentication

Most endpoints require JWT authentication. Include the token in the request header:

```
Authorization: Token <jwt_token>
```

## Endpoints

### Authentication

#### Register
- **POST** `/api/users`
- **Body**: `{"user": {"email": "...", "password": "...", "username": "..."}}`
- **Response**: User object with token

#### Login
- **POST** `/api/users/login`
- **Body**: `{"user": {"email": "...", "password": "..."}}`
- **Response**: User object with token

#### Get Current User
- **GET** `/api/user`
- **Auth**: Required
- **Response**: User object

#### Update User
- **PUT** `/api/user`
- **Auth**: Required
- **Body**: `{"user": {"email": "...", "bio": "...", ...}}`

### Profiles

#### Get Profile
- **GET** `/api/profiles/:username`
- **Auth**: Optional

#### Follow User
- **POST** `/api/profiles/:username/follow`
- **Auth**: Required

#### Unfollow User
- **DELETE** `/api/profiles/:username/follow`
- **Auth**: Required

### Articles

#### List Articles
- **GET** `/api/articles`
- **Query params**: `tag`, `author`, `favorited`, `limit`, `offset`

#### Get Article
- **GET** `/api/articles/:slug`

#### Create Article
- **POST** `/api/articles`
- **Auth**: Required
- **Body**: `{"article": {"title": "...", "description": "...", "body": "...", "tagList": [...]}}`

#### Update Article
- **PUT** `/api/articles/:slug`
- **Auth**: Required (must be author)

#### Delete Article
- **DELETE** `/api/articles/:slug`
- **Auth**: Required (must be author)

#### Favorite Article
- **POST** `/api/articles/:slug/favorite`
- **Auth**: Required

#### Unfavorite Article
- **DELETE** `/api/articles/:slug/favorite`
- **Auth**: Required

#### Get Feed
- **GET** `/api/articles/feed`
- **Auth**: Required
- **Query params**: `limit`, `offset`

### Comments

#### Add Comment
- **POST** `/api/articles/:slug/comments`
- **Auth**: Required
- **Body**: `{"comment": {"body": "..."}}`

#### Get Comments
- **GET** `/api/articles/:slug/comments`

#### Delete Comment
- **DELETE** `/api/articles/:slug/comments/:id`
- **Auth**: Required (must be author)

### Tags

#### Get Tags
- **GET** `/api/tags`
- **Response**: List of tags

### IAST Security Testing

#### Propagation Test
- **GET** `/iast/propagation?string1=test&password=secret`
- **Purpose**: Test taint propagation and vulnerability detection

#### SQL Injection Test
- **GET** `/iast/sqli?q=test`

#### Weak Hash Test
- **GET** `/iast/weak_hash?q=test`

#### Articles with IAST
- **GET** `/iast/articles?tag=test`

For complete API spec, see [RealWorld API Specification](https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints).
