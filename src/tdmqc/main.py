from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import logging
from pathlib import Path





# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Пути
BASE_DIR = Path(__file__).parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"
STATIC_DIR = BASE_DIR / "frontend" / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Запуск приложения
    logger.info("🚀 Starting 3DModelQuickCalc v0.1.0")
    logger.info(f"📁 Project root: {BASE_DIR}")
    
    # Создаем необходимые директории
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    
    yield
    
    # Завершение работы
    logger.info("🛑 Shutting down 3DModelQuickCalc")

# Создание приложения FastAPI
app = FastAPI(
    title="3DModelQuickCalc",
    description="Web calculator for 3D parts parameters",
    version="0.1.0",
    lifespan=lifespan
)

# Настройка CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтирование статических файлов (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Инициализация шаблонов Jinja2
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# =================== БАЗОВЫЕ ЭНДПОИНТЫ ===================

@app.get("/")
async def root():
    """Корневой эндпоинт API"""
    return {
        "service": "3DModelQuickCalc",
        "version": "0.1.0",
        "description": "Web calculator for 3D parts parameters",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "frontend": "/app",
            "api_info": "/api/info"
        }
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {
        "status": "healthy",
        "service": "3DModelQuickCalc",
        "version": "0.1.0",
        "timestamp": "2026-01-01T00:00:00Z"  # TODO: заменить на реальное время
    }

@app.get("/api/info")
async def api_info():
    """Информация о API"""
    return {
        "name": "3DModelQuickCalc API",
        "version": "0.1.0",
        "architecture": "Clean Architecture with plugins",
        "features": [
            "STL file processing",
            "Volume calculation",
            "Material cost estimation",
            "3D preview",
            "Modular plugin system"
        ]
    }

@app.get("/app", include_in_schema=False)
async def serve_frontend(request: Request):
    """Главная страница фронтенда"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# =================== КОНФИГУРАЦИОННЫЕ ЭНДПОИНТЫ ===================

@app.get("/api/config/materials")
async def get_materials():
    """Получение списка материалов (заглушка)"""
    return {
        "materials": [
            {"id": "steel", "name": "Сталь", "density": 7.85, "price_per_kg": 150},
            {"id": "aluminum", "name": "Алюминий", "density": 2.70, "price_per_kg": 350},
            {"id": "pla", "name": "PLA пластик", "density": 1.24, "price_per_kg": 800}
        ]
    }

# =================== ЗАГЛУШКИ ДЛЯ БУДУЩЕЙ ФУНКЦИОНАЛЬНОСТИ ===================

@app.post("/api/upload", include_in_schema=False)
async def upload_file():
    """Загрузка файла (заглушка)"""
    return {"message": "File upload endpoint - to be implemented"}

@app.post("/api/calculate/volume", include_in_schema=False)
async def calculate_volume():
    """Расчет объема (заглушка)"""
    return {"message": "Volume calculation - to be implemented"}

@app.post("/api/calculate/cost", include_in_schema=False)
async def calculate_cost():
    """Расчет стоимости (заглушка)"""
    return {"message": "Cost calculation - to be implemented"}

# =================== СЛУЖЕБНЫЕ ФУНКЦИИ ===================

def get_app_info():
    """Информация о приложении"""
    return {
        "name": "3DModelQuickCalc",
        "version": "0.1.0",
        "status": "running"
    }

# Статика и шаблоны
BASE_DIR = Path(__file__).parent.parent.parent
STATIC_DIR = BASE_DIR / "frontend" / "static"
TEMPLATES_DIR = BASE_DIR / "frontend" / "templates"

# Создаем папки если не существуют
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/app")
async def serve_frontend(request: Request):
    """Serve the main frontend application"""
    return templates.TemplateResponse("index.html", {"request": request})


# Инициализация при запуске
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(
        "src.tdmqc.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

