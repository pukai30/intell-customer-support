"""
Main entry point for the Intelligent Customer Support System
"""
import uvicorn
from app.config import settings


def main():
    """Start the application"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Intelligent Customer Support System                    ║
    ║   RAG-based Multi-Channel Support Platform               ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Start FastAPI server (background tasks start in startup event)
    uvicorn.run(
        "app.api:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )


if __name__ == "__main__":
    main()
