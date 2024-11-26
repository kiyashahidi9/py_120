class Television:
    @classmethod
    def manufacturer(cls):
        return 'Amazon'

    def model(self):
        return 'Omni Fire'

tv = Television()
print(tv.__class__.manufacturer())
print(tv.model())

print(Television.manufacturer())
print(Television.model())