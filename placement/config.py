import os
# POSTGRES_USER=os.getenv("POSTGRES_USER","admin")
# POSTGRES_PASS=os.getenv("POSTGRES_PASS","admin")
# POSTGRES_DB=os.getenv("POSTGRES_DB","vsLCM")
# POSTGRES_IP=os.getenv("POSTGRES_IP","localhost")
# POSTGRES_PORT=os.getenv("POSTGRES_PORT",5432)
# APP_SECRET=os.getenv("APP_SECRET","tenantManager")
# APP_PORT=os.getenv("APP_PORT",5000)
RABBIT_USER=os.getenv("RABBIT_USER","admin")
RABBIT_PASS=os.getenv("RABBIT_PASS","admin")
RABBIT_IP=os.getenv("RABBIT_IP","localhost")
RABBIT_PORT=os.getenv("RABBIT_PORT",5672)

REDIS_HOST=os.getenv("REDIS_HOST","localhost")
REDIS_PORT=os.getenv("REDIS_PORT",6379)
REDIS_PASS=os.getenv("REDIS_PASS","netorRedisPassword")
REDIS_DB=os.getenv("REDIS_DB",0)
