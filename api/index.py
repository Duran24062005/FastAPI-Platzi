from mangum import Mangum
from main import app

# Handler para Vercel usando Mangum
handler = Mangum(app, lifespan="off")