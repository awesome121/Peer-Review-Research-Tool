"""

    e.g.
    Author -> Agent               Subject: "subm-1"

    Agent -> Reviewer             Subject: "Review-Request"
    Reviewer -> Agent             Subject: "Re: Review-Request"

    Agent -> Original author      Subject: "evaluation-Request"
    Original author -> Agent      Subject: "Re: evaluation-Request"
"""

from html.parser import HTMLParser

class MailParser:
    """
        MailParser class, this class is used to get and analyse basic mail subjects.
        Subject is valid only if it satisfies certain formats, please see examples
        above.
    """
    def __init__(self):
        pass
        self.max_subm = 6

    def is_subm(self, subject):
        subject = subject.strip().lower().split('-')
        return len(subject) == 2 and subject[0] == 'submission' and \
            subject[1].isdigit() and (1 <= int(subject[1]) <= self.max_subm)

    def is_review(self, subject):
        subject = subject.strip().lower().split('-')
        return len(subject) == 2 and subject[0] == 're: review' \
                and subject[1] == 'request'

    def is_eval(self, subject):
        subject = subject.strip().lower().split('-')
        return len(subject) == 2 and subject[0] == 're: evaluation' \
                and subject[1] == 'request'

    def get_subm_id(self, subject):
        """Give a string of subject, return an integer"""
        subject = subject.strip().lower().split('-')
        return int(subject[1])

    def get_subm_success(self):
        return f"Submission-Success"

    def get_review_req(self):
        return f"Review-Request"

    def get_eval_req(self):
        return f"Evaluation-Request"

    def parse_mail(self, mail):
        msg_id = mail['id']
        subject = mail['subject']
        from_ = mail['from']['emailAddress']['address']
        convo_id = mail['conversationId']
        date = mail['receivedDateTime']
        return msg_id, convo_id, subject, from_, date

    def get_eval(self, mail):
        """
            Provided:
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
        