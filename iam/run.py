"""Implementation of the entry point."""
from iam.utils.models import db
from iam.handler.login import main
db.create_all()
main().login_master(db)

