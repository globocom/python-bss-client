from setuptools import setup, find_packages

__version__ = '0.1.0'

setup(
    name="bss-client",
    url="https://github.com/globocom/python-bss-client",
    version=__version__,
    packages=find_packages(),
    description="CPBM BSS API client.",
    author="tsuru",
    author_email="tsuru@corp.globo.com",
    include_package_data=True,
    install_requires=[
        "requests==2.3.0"
    ],
    extras_require={
        'tests': [
            "pytest==2.5.2",
            "flake8==2.0",
            "mock==1.0.1",
            "freezegun==0.1.18",
        ],
    },
)
