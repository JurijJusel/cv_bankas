from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class JobPostModel(BaseModel):
    post_id: int = Field(..., description="Unique identifier for the job post")
    company: str = Field(..., description="Name of the company")
    company_city: str = Field(..., description="City where the company is located")
    position: str = Field(..., description="Position title")
    salary: str | None = Field(None, description="Salary information")
    salary_type: str | None = Field(None, description="Type of salary (e.g., gross, net, calculation method)")
    post_url: HttpUrl = Field(..., description="URL of the job post")
    company_logo_url: HttpUrl = Field(..., description="URL of the company logo")
    post_upload: str | None = Field(None, description="Date when the post was published")
    scraped_at: datetime = Field(default_factory=datetime.now, description="Time when the post was downloaded")
    people_viewed: int = Field(0, description="Number of people who viewed the post")
    people_applied: int = Field(0, description="Number of people who applied to the post")
