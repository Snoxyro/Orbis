#!/usr/bin/env python3
"""
⚠️ TEMPORARY INGESTION SCRIPT ⚠️

This is a standalone utility script for initial data population.
NOT part of the main application architecture - can be modified or removed anytime.

Purpose:
    - Quick database population during development/setup
    - Self-contained with duplicated models (intentional)
    - Bypasses application layers (Routes → Services → Repositories)

Usage:
    cd api/database/ingest
    python3 ingest.py example_courses.json

Requirements:
    - PostgreSQL with pgvector extension running
    - Embedding service running (docker-compose up -d embeddings)

Note:
    For production data management, use proper admin APIs/tools.
    This script is just a convenience tool, not a maintainable solution.
"""

import json
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pgvector.sqlalchemy import Vector

# Add parent directory to path to import services
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from services.embedding_service import get_embedding_service

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/orbisdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Models (duplicated here to be standalone)
Base = declarative_base()

# Initialize embedding service
print("Initializing embedding service...")
try:
    embedding_service = get_embedding_service()
    EMBEDDING_DIM = embedding_service.get_dimension()
    print(f"✓ Embedding service ready! Dimension: {EMBEDDING_DIM}")
except Exception as e:
    print(f"❌ Failed to initialize embedding service: {e}")
    print("Make sure Docker container is running: docker-compose up -d embeddings")
    sys.exit(1)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    keywords = Column(Text)
    embedding = Column(Vector(EMBEDDING_DIM))
    content = relationship("CourseContent", back_populates="course")


class CourseContent(Base):
    __tablename__ = "course_content"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    topic = Column(Text, nullable=False)
    course = relationship("Course", back_populates="content")


def ingest_courses(filepath: str):
    """Load courses from JSON and generate embeddings"""
    
    # Load data
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both formats: {"courses": [...]} or [...]
    courses = data.get('courses', data) if isinstance(data, dict) else data
    
    # Database session
    db = SessionLocal()
    
    try:
        for course_data in courses:
            # Create text for embedding from keywords or description
            embed_text = course_data.get('keywords', course_data.get('description', course_data['name']))
            
            # Generate embedding using EmbeddingService
            embedding = embedding_service.embed_text(embed_text)
            
            # Create course
            course = Course(
                code=course_data['code'],
                name=course_data['name'],
                description=course_data.get('description'),
                keywords=course_data.get('keywords'),
                embedding=embedding
            )
            db.add(course)
            db.flush()  # Get the ID
            
            # Add weekly content - handle both 'week' and 'week_number' fields
            for week in course_data.get('content', []):
                week_num = week.get('week_number') or week.get('week')
                content = CourseContent(
                    course_id=course.id,
                    week_number=week_num,
                    topic=week['topic']
                )
                db.add(content)
            
            print(f"✓ Added: {course.code} - {course.name}")
        
        db.commit()
        print(f"\n✓ Successfully imported {len(courses)} courses with embeddings!")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    ingest_courses("example_courses.json")
