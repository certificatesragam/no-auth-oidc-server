# No-Auth OIDC Server

This repository provides a minimal OpenID Connect (OIDC) server for personal use in private networks. No user management or authentication is implemented—this is for internal, non-public setups only.

## Description
A simple OIDC server for development, testing, or private use. All configuration is done via environment variables. No authentication or user management is included. **Do not use in public or production environments!**

## Endpoints
| Endpoint                                 | Description                                 |
|------------------------------------------|---------------------------------------------|
| `/`                                      | Health check (returns status)               |
| `/.well-known/openid-configuration`      | OIDC discovery endpoint                     |
| `/.well-known/oidc-discovery`            | Alternative OIDC discovery endpoint         |
| `/authorize`                             | Issues a static code for OIDC flow          |
| `/token`                                 | Issues a JWT token if the code is valid     |
| `/userinfo`                              | Returns static user info                    |
| `/jwks`                                  | Returns empty JWKS                         |

## Environment Variables
| Variable                     | Description                                 | Example Value                        |
|:-----------------------------|:--------------------------------------------|--------------------------------------|
| `NO_AUTH_REDIRECT_URL`       | Redirect URI for OIDC client                | `http://localhost:3000/auth/oidc/callback` |
| `NO_AUTH_OIDC_HOST`          | Hostname/URL of this OIDC server            | `http://localhost:4000`                |
| `NO_AUTH_OIDC_USER_NAME`     | Username for userinfo and token             | `admin`                                |
| `NO_AUTH_OIDC_USER_MAIL`     | Email for userinfo and token                | `admin@local.net`                      |
| `NO_AUTH_OIDC_CLIENT_ID`     | OIDC client ID                              | `client-id`                       |
| `NO_AUTH_OIDC_CLIENT_SECRET` | OIDC client secret                        | `client-secret`                       |

Set these variables in your Docker environment or `.env` file to configure the server for your needs.
  

## Example docker-compose.yml
```yaml
services:
	oidc:
		container_name: oidc
		image: ghcr.io/ceviixx/no-auth-oidc-server:latest
		ports:
			- "4000:4000"
		restart: unless-stopped
		environment:
			- NO_AUTH_REDIRECT_URL=REPLACE_ME
			- NO_AUTH_OIDC_HOST=REPLACE_ME
			- NO_AUTH_OIDC_USER_NAME=REPLACE_ME
			- NO_AUTH_OIDC_USER_MAIL=REPLACE_ME
			- NO_AUTH_OIDC_CLIENT_ID=REPLACE_ME
			- NO_AUTH_OIDC_CLIENT_SECRET=REPLACE_ME
```


