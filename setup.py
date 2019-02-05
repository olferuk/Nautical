from setuptools import setup

setup(name='Spindrift',
      version='0.1',
      description='The tool to make lightweight Telegram bots from plain Python functions',
      author='Alexander Olferuk and Danila Paluhin, Surf',
      license='MIT',
      install_requires=['python-telegram-bot', 'pandas'],
      packages=['spindrift']
)
