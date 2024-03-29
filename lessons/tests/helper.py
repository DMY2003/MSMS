from django.urls import reverse

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url
    
class LogInTester:

    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

    def login(self, user):
        self.client.force_login(user)

    def log_out(self):
        url = reverse('log_out')
        self.client.get(url)