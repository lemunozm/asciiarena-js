from setuptools import setup
import asciiarena.common.version as Version

setup(name = "asciiarena",
      version = Version.CURRENT,
      description = "An arcade multiplayer game for terminals.",
      url = "http://github.com/lemunozm/asciiarena",
      author = "Luis Enrique Munoz",
      author_email = "lemunozm@gmail.com",
      license='MIT',
      packages=['funniest'],
      zip_safe=False)
