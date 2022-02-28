"""
    e.g.
    Author -> Agent               Subject: "submission-1"

    Agent -> Reviewer             Subject: "Review-Request-1"
    Reviewer -> Agent             Subject: "Re: Review-Request-1"

    Agent -> Original author      Subject: "evaluation-Request-1"
    Original author -> Agent      Subject: "Re: evaluation-Request-1"
"""

class MailParser:
    """
        MailParser class, this class is used to get and analyse basic mail subjects.
        Subject is valid only if it satisfies certain formats, please see example 
        sabove.
    """
    def __init__(self):
        self.MAX_NUM_SUBMISSION = 20

    def is_subm(self, subject):
        """
            Param:
                subject: a string of email subject
            Return:
                True if subject is submission e.g. "submission-1"
        """
        subject = subject.strip().lower().split('-')
        return len(subject) == 2 and subject[0] == 'submission' and \
            subject[1].isdigit() and (1 <= int(subject[1]) <= self.MAX_NUM_SUBMISSION)

    def is_review_req(self, subject):
        """
            Param:
                subject: a string of email subject
            Return:
                True if subject is review request e.g. "review-request-1"
        """
        subject = subject.strip().lower().split('-')
        return len(subject) == 3 and subject[0] == 'review' \
                and subject[1] == 'request' and subject[2].isdigit()\
                and (1 <= int(subject[2]) <= self.MAX_NUM_SUBMISSION)

    def is_review(self, subject):
        """
            Param:
                subject: a string of email subject
            Return:
                True if subject is review e.g. "Re: review-request-1"
        """
        subject = subject.strip().lower().split('-')
        return len(subject) == 3 and subject[0] == 're: review' \
                and subject[1] == 'request' and subject[2].isdigit()\
                and (1 <= int(subject[2]) <= self.MAX_NUM_SUBMISSION)

    def is_eval_req(self, subject):
        """
            Param:
                subject: a string of email subject
            Return:
                True if subject is evaluation request 
                e.g. "evaluation-request-1"
        """
        subject = subject.strip().lower().split('-')
        return len(subject) == 3 and subject[0] == 'evaluation' \
                and subject[1] == 'request' and subject[2].isdigit()\
                and (1 <= int(subject[2]) <= self.MAX_NUM_SUBMISSION)

    def is_eval(self, subject):
        """
            Param:
                subject: a string of email subject
            Return:
                True if subject is evaluation
                e.g. "Re: evaluation-request-1"
        """
        subject = subject.strip().lower().split('-')
        return len(subject) == 3 and subject[0] == 're: evaluation' \
                and subject[1] == 'request' and subject[2].isdigit()\
                and (1 <= int(subject[2]) <= self.MAX_NUM_SUBMISSION)

    def get_subm_id(self, subject):
        """
            Param:
                subject: a string of email subject
            Return:
                Return an integer of submission id
        """
        subject = subject.strip().lower().split('-')
        return int(subject[-1])

    def get_review_req(self, id):
        """
            Param:
                id: an integer of submission id
            Return:
                Return subject of review request
        """
        return f"Review-Request-{id}"

    def get_eval_req(self, id):
        """
            Param:
                id: an integer of submission id
            Return:
                Return subject of evaluation request
        """
        return f"Evaluation-Request-{id}"

    def parse_mail(self, mail):
        """
            Param:
                mail: an email object in dictionary format
            Return:
                a tuple of information in mail
        """
        msg_id = mail['id']
        subject = mail['subject']
        from_ = mail['from']['emailAddress']['address']
        convo_id = mail['conversationId']
        date = mail['receivedDateTime']
        return msg_id, convo_id, subject, from_, date

    def get_eval(self, mail):
        """
            Param:
                an mail object in JSON form
            Return:
                rating: a single integer 1-7 inclusive on success
                        -1 on failure.
                comment: a string of comment, '' string on failure
        """
        body = mail['body']['content'].lower()
        pos = body.find('rating-')
        if pos != -1 and body[pos + len('rating-')].isdigit():
            rating = int(body[pos + len('rating-')])
            if rating in range(1, 8):
                return rating, ''
        return -1, ''
        