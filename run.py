import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", 8000))
    env = os.getenv("APP_ENV", "development")
    
    print(f"""
    ╔══════════════════════════════════╗
    ║         OrBit is Running         ║
    ║  http://localhost:{port}            ║
    ╚══════════════════════════════════╝
    """)
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=True if env == "development" else False,
        log_level="info"
    )