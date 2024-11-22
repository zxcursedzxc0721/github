from setuptools import setup, find_packages

setup(
    name='github-uploader',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'PyGithub',
    ],
    entry_points={
        'console_scripts': [
            'github=github_uploader.uploader:main',
        ],
    },
    author='Your Name',
    author_email='your_email@example.com',
    description='Command-line tool to upload projects to GitHub.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/github-uploader',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)