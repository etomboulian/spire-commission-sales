from typing import List, Optional
from pydantic import BaseModel

# /api/v2/companies/
# Allows: [GET, HEAD, OPTIONS]


class BackupSchedule(BaseModel):
    next_backup: Optional[str]
    last_success: Optional[str]
    interval: Optional[str]
    keep: Optional[int]


class Company(BaseModel):
    name: str
    description: str
    needs_upgrade: bool
    valid: bool
    url: str
    locations: dict
    backup_schedules: List[BackupSchedule]


class CompanyList(BaseModel):
    records: List[Company]
