# Ride App

A simple ride-sharing application.

## What You Need

Before starting, install:
- Docker
- Docker Compose

## How to Set Up

### 1. Create Environment File

Copy the example environment file:
```bash
cp example.env .env
```

### 2. Build the Project

Run this command to build the Docker image:
```bash
docker compose build
```

### 3. Start the Project

Run the project:
```bash
docker compose up
```

The app will run at `http://localhost:8000`

## Create Admin User (Optional)

After the project is running, open a new terminal and run:
```bash
docker compose exec -it app python manage.py createsuperuser
```

Follow the prompts to create your admin account.

## API Routes & Examples

### Authentication

**Obtain Access Token:**
```bash
curl -X POST http://localhost:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Refresh Token:**
```bash
curl -X POST http://localhost:8000/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your_refresh_token"
  }'
```

### Users

**List Users (Admin):**
```bash
curl -X GET http://localhost:8000/users/ \
  -H "Authorization: Bearer your_access_token"
```

**Create User:**
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe",
    "role": "driver",
    "phone_number": "555-1234"
  }'
```

**Retrieve User:**
```bash
curl -X GET http://localhost:8000/users/{id}/ \
  -H "Authorization: Bearer your_access_token"
```

**Update User:**
```bash
curl -X PATCH http://localhost:8000/users/{id}/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "555-5678"
  }'
```

**Delete User:**
```bash
curl -X DELETE http://localhost:8000/users/{id}/ \
  -H "Authorization: Bearer your_access_token"
```

### Rides

**List Rides (Admin):**
```bash
curl -X GET http://localhost:8000/rides/ \
  -H "Authorization: Bearer your_access_token"
```

**List Rides with Filters and Ordering:**

Filter by status:
```bash
curl -X GET "http://localhost:8000/rides/?status=en-route" \
  -H "Authorization: Bearer your_access_token"
```

Filter by rider email:
```bash
curl -X GET "http://localhost:8000/rides/?rider_email=john@example.com" \
  -H "Authorization: Bearer your_access_token"
```

Filter by distance (find rides near coordinates, ordered by distance):
```bash
curl -X GET "http://localhost:8000/rides/?pickup_lat=40.7128&pickup_lon=-74.0060" \
  -H "Authorization: Bearer your_access_token"
```

Order by pickup time (ascending):
```bash
curl -X GET "http://localhost:8000/rides/?ordering=pickup_time" \
  -H "Authorization: Bearer your_access_token"
```

Order by pickup time (descending):
```bash
curl -X GET "http://localhost:8000/rides/?ordering=-pickup_time" \
  -H "Authorization: Bearer your_access_token"
```

Combine filters and ordering (active rides by rider email, ordered by pickup time):
```bash
curl -X GET "http://localhost:8000/rides/?status=en-route&rider_email=john@example.com&ordering=pickup_time" \
  -H "Authorization: Bearer your_access_token"
```

**Create Ride:**
```bash
curl -X POST http://localhost:8000/rides/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "en-route",
    "id_rider": 1,
    "id_driver": 2,
    "pickup_latitude": 40.7128,
    "pickup_longitude": -74.0060,
    "dropoff_latitude": 34.0522,
    "dropoff_longitude": -118.2437,
    "pickup_time": "2024-01-29T14:30:00Z"
  }'
```

**Retrieve Ride:**
```bash
curl -X GET http://localhost:8000/rides/{id}/ \
  -H "Authorization: Bearer your_access_token"
```

**Update Ride:**
```bash
curl -X PATCH http://localhost:8000/rides/{id}/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

**Delete Ride:**
```bash
curl -X DELETE http://localhost:8000/rides/{id}/ \
  -H "Authorization: Bearer your_access_token"
```

### Ride Events

**List Ride Events (Admin):**
```bash
curl -X GET http://localhost:8000/ride-events/ \
  -H "Authorization: Bearer your_access_token"
```

**Create Ride Event:**
```bash
curl -X POST http://localhost:8000/ride-events/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "id_ride": 1,
    "description": "Status changed to pickup"
  }'
```

**Retrieve Ride Event:**
```bash
curl -X GET http://localhost:8000/ride-events/{id}/ \
  -H "Authorization: Bearer your_access_token"
```

**Delete Ride Event:**
```bash
curl -X DELETE http://localhost:8000/ride-events/{id}/ \
  -H "Authorization: Bearer your_access_token"
```

### API Documentation

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

## Useful Commands

**View logs:**
```bash
docker compose logs -f app
```

**Stop the project:**
```bash
docker compose down
```

**Reset database:**
```bash
docker compose down -v
docker compose up
```

## Monthly Trip Reports

Get trips longer than 1 hour grouped by month:

```sql
WITH ride_duration AS (
    SELECT
        ride.id_ride,
        ride.id_driver,
        DATE_TRUNC('month', pickup.created_at) AS ride_month,
        pickup.created_at AS pickup_time,
        dropoff.created_at AS dropoff_time,
        dropoff.created_at - pickup.created_at AS trip_duration
    FROM ride
    JOIN ride_event pickup
        ON pickup.id_ride = ride.id_ride
       AND pickup.description = 'Status changed to pickup'
    JOIN ride_event dropoff
        ON dropoff.id_ride = ride.id_ride
       AND dropoff.description = 'Status changed to dropoff'
       AND dropoff.created_at > pickup.created_at
)
SELECT
    TO_CHAR(ride_month, 'YYYY-MM') AS month,
    u.first_name || ' ' || SUBSTRING(u.last_name FROM 1 FOR 1) AS driver,
    COUNT(*) AS "Count of Trips > 1 hr"
FROM ride_duration
JOIN user
    ON user.id_user = ride_duration.id_driver
WHERE ride_duration.trip_duration > INTERVAL '1 hour'
GROUP BY ride_month, driver
ORDER BY ride_month, driver;
```