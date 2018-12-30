from google.cloud import translate

class Translator:
    def __init__(self, target, source):
        self.translate_client = translate.Client()
        self.target = target
        self.source = source
    def translate(self, text):
        return self.translate_client.translate(
            text,
            target_language=self.target,
            source_language=self.source)