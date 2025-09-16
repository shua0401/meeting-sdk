from app import app as application

# Vercel Python runtime (serverless) will look for `app` or `application`.
# Expose both for compatibility.
app = application

