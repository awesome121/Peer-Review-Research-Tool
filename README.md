# __Peer Review Research Project__

## Table of Contents
* [General Info](#General-Info)
* [Setup](#Setup)
* [Privacy](#Privacy)
* [Security](#Security)
* [Dependencies](#Dependencies)


## __Brief__
<p>This is a peer-review research project for Product Design department at University of Canterbury.</p>
<p>To aid instructors in proceeding the peer review process, this project is to develop an email forwarding application capable of supporting randomized, double blind review of design work. Authors submit their anonymized work either to an email address, and the work is then sent to three randomly chosen reviewers from a specified list. (Author will not receive their own work) The reviewers submit their reviews back to this dropbox, and the anonymized reviews are returned to the author. The author can then rate the feedback they reviewed. Although the review process is double blind to authors and reviewers, system administrators need to be able to identify owners of work and reviews, as well as collect analytics related to the usage of the system.</p>

## __Setup__
* ### App Registration
    <p> In order to register this application, one needs to go to Azure portal -> Azure Active Directory -> App registration.
    Once the application is registerd and certain API permissions are configured, any service accounts within the university will be able to use it (Note: only one service account per application). </p>


* ### API Permission
    To send/read email, "Mail.Read", "Mail.ReadWrite", "Mail.Send", "Mail.ReadBasic" permissions are required.


* ### Initial Token Acquisition
    Once the application starts, it prompts a code (e.g. FWG8UF447).
    The user who holds the service account opens a browser (or from another device) navigating to https://microsoft.com/devicelogin. Microsoft Device Login page will also display the API permissions this application is requesting.
    Upon successful authentication, the application will receive a token and use it to perform web API calls throughout
    an academic semester.


* ### Token Refresh
    Token refresh is performed by acquire_token_silent() from [MSAL](https://msal-python.readthedocs.io/en/latest/) without user
    interaction. A token typically lasts ~5000 seconds and will be refreshed when there are ~300 seconds left.

## __Privacy__
* ### User Credential
    This project is an email-based solution. It uses [Microsoft Authentication Library](https://docs.microsoft.com/en-au/azure/active-directory/develop/msal-authentication-flows) (MSAL) on Python. This application only needs the access token from an service account through [MSAL Device Code Flow](https://github.com/Azure-Samples/ms-identity-python-devicecodeflow). The initially acquired token will be refreshed throughout the semester. Therefore, it doesn't handle any passwords neither from instructors nor students. 


* ### Analytics Access Rights
    Only privileged person such as instructor who holds the service account credential has access rights to view students' submission/review/evaluation information involved with this application. 


* ### Email Content
    Furthermore, it captures email header information such as subject, from, receive date, message id, conversation id. It only parses the email body to acquire rating and comment while storing evaluation. For more detailed information such as content of attachments and submission content, please log in the service account on Microsoft Outlook (This application also provides relevant author/reviewer information for looking up).

## __Security__
    It runs on a server within the university network. Only certain APIs are used. This application keeps a list of students and instructors, it only serves this group of email addresses. If there is an email from an unknown address, it will be ignored.

## __Dependencies__
Python 3.7+

Microsoft Authentication Library 1.16.0

Requests 2.25.1