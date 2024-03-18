import threading

from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(
        self, subject: str,
        html_content: str,
        sender: str,
        recipient_list: list[str],
        dev_mode: bool,
    ):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.sender = sender
        self.dev_mode = dev_mode
        threading.Thread.__init__(self)

    def run(self):
        if self.dev_mode:
            return

        msg = EmailMessage(
            self.subject, self.html_content, self.sender, self.recipient_list
        )
        msg.content_subtype = 'html'
        msg.send()


def send_html_mail(
    subject: str,
    html_content: str,
    sender: str,
    recipient_list: list[str],
    dev_mode: bool,
):
    EmailThread(
        subject, html_content, sender, recipient_list, dev_mode
    ).start()
