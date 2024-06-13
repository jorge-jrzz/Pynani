from abc import ABC, abstractmethod

class SocialMedia(ABC):
    @abstractmethod
    def verify_token(self, params, token):
        pass