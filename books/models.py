from sqlalchemy import Column, Integer, String, Float, Boolean, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Si vous utilisez déjà SQLAlchemy dans votre application principale, 
# vous pourriez vouloir réutiliser la configuration existante
DATABASE_URL = "postgresql://postgres:dali2004@localhost/student_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RecommendedBook(Base):
    __tablename__ = "recommended_books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    availability = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "category": self.category,
            "availability": self.availability,
            "description": self.description,
            "image_url": self.image_url
        }

# Créer les tables dans la base de données
def create_tables():
    Base.metadata.create_all(bind=engine)

# Obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
