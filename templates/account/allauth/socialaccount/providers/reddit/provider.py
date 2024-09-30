from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.reddit.views import RedditAdapter


class RedditAccount(ProviderAccount):
    pass


class RedditProvider(OAuth2Provider):
    id = "reddit"
    name = "Reddit"
    account_class = RedditAccount
    oauth2_adapter_class = RedditAdapter

    def extract_uid(self, data):
        return data["name"]

    def extract_common_fields(self, data):
        return dict(username=data.get("name"))

    def get_default_scope(self):
        scope = ["identity"]
        return scope


provider_classes = [RedditProvider]
