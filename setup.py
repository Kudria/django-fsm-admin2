from setuptools import setup

setup(
    name='django-fsm-admin2',
    version='0.1',
    packages=['fsm_admin2'],
    include_package_data=True,
    url='https://github.com/Kudria/django-fsm-admin2',
    author='Alexandr Kudriavtcev',
    author_email='kudria15@gmail.com',
    description='django-fsm transition integration to django admin.',
    install_requires=[
        'django>=2.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
