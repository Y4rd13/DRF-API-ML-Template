'''
Here you can define your custom services. Remember to integrate them in __init__.py to be able to import them in your tasks.py and other modules.
'''
class MyCustomService:
    def __init__(self):
        self.y = 'Hello World'

    def execute(self, x):
        return f'{self.y}: {x}'