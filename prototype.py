from app import app, db
from app.models import Student, Therapist, Match, StudentMatchFormEntry, StudentCancelMatchFormEntry

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'Therapist' : Therapist, 'Match' : Match, 'StudentMatchFormEntry' : StudentMatchFormEntry, 'StudentCancelMatchFormEntry' : StudentCancelMatchFormEntry}