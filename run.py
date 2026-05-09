import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", os.getenv("APP_PORT", 8000)))
    
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
        reload=False,
        log_level="info"
    )