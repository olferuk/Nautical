from setuptools import setup

setup(name='Nautical',
      version='1.0.0',
      description='The tool to make lightweight Telegram bots from plain Python functions',
      author='Alexander Olferuk and Danila Paluhin, Surf',
      license='MIT',
      install_requires=['python-telegram-bot', 'pandas'],
      packages=['nautical']
)
