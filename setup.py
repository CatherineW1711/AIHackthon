from setuptools import setup, find_packages

setup(
    name="aihackthon",
    version="0.1.0",
    description="AI-Powered Code Analyzer & Enhancer for Warp Terminal",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="CatherineW1711",
    author_email="",  # Add if desired
    url="https://github.com/CatherineW1711/AlHackthon",
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'colorama>=0.4.6',  # For terminal colors (warp_assistant.py)
        'Flask>=2.3.2',     # For REST API (Enhanced Flask REST API)
        'sqlalchemy>=2.0.23' # Database support
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'warp_assistant=src.analyzer:main',  # Creates terminal command
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
