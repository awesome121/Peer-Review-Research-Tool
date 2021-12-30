# e.g.
# Author -> Agent               Subject: "submission-1"

# Agent -> Reviewer             Subject: "Review-Request"
# Reviewer -> Agent             Subject: "Re: Review-Request"

# Agent -> Original author      Subject: "evaluation-Request"
# Original author -> Agent      Subject: "Re: evaluation-Request"

class MailParser:
    def __init__(self):
        pass
        self.max_submission = 6

    def is_submission(self, subject):
        subject = subject.strip().lower().split('-')
        return len(subject) == 2 and subject[0] == 'submission' and \
            subject[1].isdigit() and (1 <= int(subject[1]) <= self.max_submission)

    def is_review(self, subject):
        subject = subject.strip().lower().split('-')
        return len(subject) == 2 and subject[0] == 're: review' \
                and subject[1] == 'request'

    def is_evaluation(self, subject):
        subject = subject.strip().lower().split('-')
        return len(subject) == 2 and subject[0] == 're: evaluation' \
                and subject[1] == 'request'

    def get_submission_success(self):
        return f"Submission-Success"

    def get_review_request(self):
        return f"Review-Request"

    def get_evaluation_request(self):
        return f"Evaluation-Request"

    def parse_mail(self, mail):
        msg_id = mail['id']
        subject = mail['subject']
        from_ = mail['from']['emailAddress']['address']
        return msg_id, subject, from_