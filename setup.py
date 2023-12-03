from setuptools import setup, find_packages

setup(
    name='random_garden',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'random_garden_package': [
            'art/general/flowers/*.txt',
            'art/general/animals/*.txt',
            'art/general/buildings/*.txt',
            'art/day/flowers/*.txt',
            'art/day/animals/*.txt',
            'art/day/buildings/*.txt',
            'art/night/flowers/*.txt',
            'art/night/animals/*.txt',
            'art/night/buildings/*.txt',
            'art/rain/flowers/*.txt',
            'art/rain/animals/*.txt',
            'art/rain/buildings/*.txt',
            'art/snow/flowers/*.txt',
            'art/snow/animals/*.txt',
            'art/snow/buildings/*.txt',
            ],
    },
    description='An ASCII garden art generator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sam Loontjens',
    author_email='loontjenssam@gmail.com',
    url='https://github.com/SamLoontjens/random_garden',
    # Add more information as needed
)
