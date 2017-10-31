from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pybotframework',
      version='0.1',
      description='A python wrapper for the Microsoft Bot Framework',
      url='http://github.com/michhar/python-botframework-wrapper',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Bot Framework :: Chat Bots',
      ],
      keywords='botframework',
      author='PythonWorkshop',
      author_email='micheleenharris@gmail.com',
      license='MIT',
      # packages=['pybotframework'],
      packages=find_packages(exclude=("tests",)),
      install_requires=[
          'flask>=0.12',
          'flask-compress',
          'Celery',
          'requests',
          'luis',
          'flask_oidc',
      ],
      # test_suite='nose.collector',
      setup_requires=[
          'pytest-runner',
      ],
      tests_require=['pytest',
                     'pytest-cov'
                     'requests-mock'],
      entry_points={
      },
      include_package_data=True,
      zip_safe=False)
