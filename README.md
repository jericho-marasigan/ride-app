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