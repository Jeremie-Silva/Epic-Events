import uvicorn
from app.core.router import app
import sentry_sdk
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
sentry_sdk.init(
    dsn="https://8a6124151e27c8c34374a5dd210f2340@o4507430341902336.ingest.de.sentry.io/4507430350749776",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


if __name__ == "__main__":
    app = SentryWsgiMiddleware(app)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
