from setuptools import setup, find_packages

setup(
    name='dakis-lt',
    version='0.1',
    license='AGPLv3+',
    packages=find_packages(),
    install_requires=[
        'python-dateutil',  # Requirement for django-json-field
        'six',              # Requirement for django-json-field
        'django',
        'django-nose',
        'django-compressor',
        'django-libsass',
        'django-debug-toolbar',
        'django-extensions',
        'django-webtest',
        'django-autoslug',
        'django-allauth',
        'djangorestframework',
        'django-filter',
        'django-json-field',
        'factory_boy',
        'fake-factory',
        'unidecode',
        'markdown',
        'yattag',
        'psycopg2',
        'mock',
        'docutils',
        'exportrecipe',
        'pytz',
        'pathlib',
        'html_linter',
        'template-remover',
        'django-concurrency',  # Installed manually, because installation problems araised
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
)
