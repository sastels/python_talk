import setuptools


setuptools.setup(
    name='talk',
    version='0.0.1',
    long_description='CI / CD demo',
    author='Steve Astels',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
