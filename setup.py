from setuptools import setup

setup(name='evaporate',
      version='0.1',
      description='Turn a youtube playlist into an audio podcast.',
      long_description='Evaporate takes a youtube playlist as an argument, '
      'downloads the videos in it as mp3s and creates an XML file that would '
      'act as an RSS feed.',
      url='https://github.com/Sarmacid/evaporate',
      author='Sarmacid',
      license='GPLv3',
      packages=['evaporate'],
      install_requires=[
          'PyRSS2Gen',
          'youtube_dl',
      ],
      scripts=['bin/evaporate_run'],
      zip_safe=False)
