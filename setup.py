from setuptools import setup, find_packages

setup(
    name='ezo_i2c_lib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # List any dependencies your package needs
    author='Rolston Dsouza',
    author_email='rolstonadsouza@gmail.com',
    description='A recreation of Ezo_I2C_lib from Atlas Scientific in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package',  # URL for your package
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Adjust based on your minimum version
)
