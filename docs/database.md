# Database design

## Relationship diagram

```mermaid
erDiagram
    USER {
        UUID id PK
        STRING email
        STRING username
        STRING bio
        STRING profile_picture
        BOOLEAN is_private
    }

    POST {
        UUID id PK
        UUID user_id FK
        TEXT content
        DATE created_at
        DATE updated_at
    }

    MEDIA {
        UUID id PK
        UUID post_id FK
        STRING media_url
        STRING media_type
    }

    COMMENT {
        UUID id PK
        UUID post_id FK
        UUID user_id FK
        TEXT content
        DATE created_at
    }

    USER ||--o{ POST : "creates"
    POST ||--o{ MEDIA : "includes"
```
