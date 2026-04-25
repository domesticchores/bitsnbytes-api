from datetime import datetime, timezone
import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Float, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from api.models.base import Base

class ModelImage(Base):
    __tablename__ = 'model_images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(Text, nullable=False)
    filename = Column(String(255))
    assigned_to = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String(20), default='pending') # 'pending', 'submitted'
    split = Column(String(10), default='train') # 'train', 'val', 'test'
    
    # Relationship to the submission
    submission = relationship("ModelSubmission", back_populates="task", uselist=False)

class ModelSubmission(Base):
    __tablename__ = 'model_submissions'
    image_id = Column(UUID(as_uuid=True), ForeignKey('model_images.id'), primary_key=True)
    user_id = Column(String(50), nullable=False)
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_approved = Column(Boolean, default=False)
    
    task = relationship("ModelImage", back_populates="submission")
    boxes = relationship("ModelAnnotation", back_populates="submission", cascade="all, delete-orphan")

class ModelAnnotation(Base):
    __tablename__ = 'model_annotations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_id = Column(UUID(as_uuid=True), ForeignKey('model_submissions.image_id'))
    class_id = Column(Integer, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)

    submission = relationship("ModelSubmission", back_populates="boxes")

    @property
    def yolo_format(self):
        # yolo wants the center of the box, not the top-left
        center_x = self.x + (self.width / 2)
        center_y = self.y + (self.height / 2)
        return f"{self.class_id} {center_x} {center_y} {self.width} {self.height}"