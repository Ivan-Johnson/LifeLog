from setuptools import find_packages, setup

setup(
    name='lifelogserver',
    version='0.5.0a0.dev0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 'waitress>=1.4.4'
    ],
    extras_require={"test": ["pytest", "coverage"]},
)
