"""
These are the prompt message prepend into message
Format can be HTML with CSS.
"""

SUBMISSION_INVITATION = \
"""
"""

SUBMISSION_SUCCESS = \
"""<p>Thanks for your submission!<br>We&apos;ve received your submission successfully.</p>
<p>Your submission will be anonymously distributed to at most 3 randomly selected reviewers.&nbsp;</p>
<p>Please check your mailbox later for new updates.</p>
<p><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>"""

SUBMISSION_FAILURE = \
"""<p>Hi<br>We&apos;ve received your message.</p>
<p>However, you've a submission existing, please wait for reviewing.&nbsp;</p>
<p>Please check your mailbox later for new updates.</p>
<p><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>"""

REVIEW_REQUEST_PROMPT = \
"""<p style="font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 11px; background-color: rgb(255, 255, 255);"><strong><em><span style="font-size: 10px; font-family: Arial, Helvetica, sans-serif;">------------------------------<wbr>------------------</span></em></strong></p>
<p style="font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 11px; background-color: rgb(255, 255, 255);"><span style="font-size: 10px; font-family: Arial, Helvetica, sans-serif;"><strong><em>------------------------------<wbr>------------------</em></strong></span><span style="font-family: Arial, Helvetica, sans-serif;"><br></span></p>
<div style="font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 11px; background-color: rgb(255, 255, 255);">
    <div dir="ltr">
        <div style="caret-color: rgb(34, 34, 34); color: rgb(34, 34, 34); font-family: Arial, Helvetica, sans-serif;">
            <div dir="ltr">
                <div style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: rgb(32, 31, 30);"><span style="font-family: Arial, Helvetica, sans-serif;"><b style="font-variant-caps: inherit; color: rgb(32, 33, 34); font-family: sans-serif;"><em>Message from instructor:</em></b></span></div>
                <div style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: rgb(32, 31, 30);"><span style="font-family: Arial, Helvetica, sans-serif;"><b style="font-variant-caps: inherit; color: rgb(32, 33, 34); font-family: sans-serif;"><em><br aria-hidden="true"></em></b></span></div>
                <div style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: rgb(32, 31, 30);"><span style="font-family: Arial, Helvetica, sans-serif;"><b style="font-variant-caps: inherit; color: rgb(32, 33, 34); font-family: sans-serif;"><em>This is one of the review requests for homework 1, PRODxxx, School of Product Design.&nbsp;</em></b></span></div>
                <div style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: rgb(32, 31, 30);"><span style="font-family: Arial, Helvetica, sans-serif;"><b style="font-variant-caps: inherit; color: rgb(32, 33, 34); font-family: sans-serif;"><em><br aria-hidden="true"></em></b></span></div>
                <div style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: rgb(32, 31, 30);"><span style="font-family: Arial, Helvetica, sans-serif;"><em><strong><span style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-style: inherit; font-variant-caps: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: inherit;">Double-blinded peer-review is very important process for this course,&nbsp;</span></strong><strong><span style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-style: inherit; font-variant-caps: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: inherit;">please carefully review this work as we&nbsp;</span></strong></em><strong><em><span style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-style: inherit; font-variant-caps: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: inherit;">also <span class="il">expect</span> others will do the same. This is the work from an&nbsp;</span>anonymous<span style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-style: inherit; font-variant-caps: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: inherit;">&nbsp;author.</span></em></strong></span></div>
                <div style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: rgb(32, 31, 30);"><span style="font-family: Arial, Helvetica, sans-serif;"><em><br aria-hidden="true"></em></span></div>
                <div style="margin: 0px; padding: 0px; border: 0px; font-size: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: rgb(32, 31, 30);"><span style="font-family: Arial, Helvetica, sans-serif;"><strong><em>To submit your review, please click &apos;Reply&apos; to this message.</em></strong></span></div><span style="font-family: Arial, Helvetica, sans-serif;"><b style="font-variant-caps: inherit; color: rgb(32, 33, 34); font-family: sans-serif;">
                        <div style="margin: 0px; padding: 0px; border: 0px; font-family: inherit; font-size: inherit; font-style: inherit; font-variant-caps: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; vertical-align: baseline; color: inherit;"><br></div>
                    </b></span><span style="font-size: 10px; font-family: Arial, Helvetica, sans-serif;"><strong><em>------------------------------<wbr>------------------</em></strong></span>
            </div>
        </div>
        <div dir="ltr">
            <p><span style="font-size: 10px;"><strong><em><span style="font-weight: 700; font-family: Arial, Helvetica, sans-serif; font-size: 10px;"><em>------------------------------<wbr>------------------</em></span></em></strong></span></p>
        </div>
    </div>
</div><br><br><br>"""

EVAL_REQUEST_PROMPT = \
"""<p style="font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 11px; background-color: rgb(255, 255, 255);"><strong><em><span style="font-size: 10px;">------------------------------<wbr>------------------</span></em></strong></p>
<p style="font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 11px; background-color: rgb(255, 255, 255);"><span style="font-size: 10px;"><strong><em>------------------------------<wbr>------------------</em></strong></span></p>
<div style="font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 11px; background-color: rgb(255, 255, 255);">
    <div dir="ltr">
        <div dir="ltr"><span style="font-size: 10px;"><strong><em>Message from instructor:</em></strong><strong><em>&nbsp;<br></em></strong><strong><em><br>This is one of the evaluation requests for homework 1, PRODxxx, School of Product Design.&nbsp;</em></strong><strong><em>&nbsp;<br><br></em></strong><strong><em>Rating-1 No information&nbsp;at all<br></em></strong><strong><em>Rating-2 <strong><em>Not very helpful information <br></em></strong></em></strong><strong><em><strong><em>Rating-3 <strong><em>Limited information</em></strong></em></strong><br><strong><em>Rating-4 Neutral</em></strong><br></em></strong><strong><em><strong><em>Rating-5 Just good</em></strong><br><strong><em>Rating-6 Good review overall</em></strong><br></em></strong><strong><em><strong><em>Rating-7 Excellent review, very detailed&nbsp;</em></strong><br><br></em></strong><strong><em><strong><em>To submit your rating, please click &apos;Reply&apos; and follow the example (Rating-4) format:<br></em></strong><br></em></strong> <strong><em>Rating-4<br></em></strong><strong><em><strong><em>Comment-for-Rating-4: &nbsp;<u>your additional comment goes to here, please include constructive comments</u></em></strong></em></strong>&nbsp;</span>
            <p><span style="font-size: 10px;"><strong><em>------------------------------<wbr>------------------</em></strong></span></p>
            <p><span style="font-size: 10px;"><strong><em><span style="font-weight: 700; font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 10px;"><em>------------------------------<wbr>------------------</em></span></em></strong></span></p>
        </div>
    </div>
</div><br><br><br>"""

INVALID_SUBJECT = \
"""<p>Thanks for your email!<br></p>
<p>It seems you have an invalid subject<br><br></p>
<p>To submit your work, please send us an email with subject "submission-x" where "x" is the submission id<br></p>
<p>To submit your review, please click "reply" to review request<br><</p>
<p>To submit your evaluation, please click "reply" to evaluation request<br><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>"""

NON_EXISTING_SUBM = \
"""<p>Sorry, this submission isn&apos;t scheduled yet. <br><br></p>
<p>To submit your work, please send us an new email with subject &quot;submission-x&quot; where &quot;x&quot; is the submission id<br><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>"""

NON_STARTING_SUBM = \
"""<p>Submission {} hasn&apos;t started yet, schedule for this submission:</p>
<p>Submission: {} - {}</p>
<p>Review: &nbsp; &nbsp; &nbsp; {} - {}</p>
<p>Evaluation: &nbsp;{} - {}<br><br></p>
<p>To submit your work, please send us an new email with subject &quot;submission-x&quot; where &quot;x&quot; is the submission id once the submission starts.<br><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>
"""

LATE_SUBM_PROMPT = \
"""<p>Sorry, submission {} is ended at {}, your submission is not accepted, if you have other questions, please contact instructor.</p>
<p>To submit your work, please send us an new email with subject &quot;submission-x&quot; where &quot;x&quot; is the submission id.<br><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>
"""

LATE_REVIEW = \
"""<p>Sorry, review for submission {} is ended at {}, your review is not accepted, if you have other questions, please contact instructor.<br><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>
"""

LATE_EVAL = \
"""<p>Sorry, evaluation for submission {} is ended at {}, your review is not accepted, if you have other questions, please contact instructor.<br><br></p>
<p>Kind Regards,<br>Dropbox of Product Design</p>
"""