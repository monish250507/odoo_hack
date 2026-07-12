
from models.compliance_issue import ComplianceIssue
from repositories.base import BaseRepository

class ComplianceIssueRepository(BaseRepository[ComplianceIssue]):
    pass

compliance_issue_repo = ComplianceIssueRepository(ComplianceIssue)