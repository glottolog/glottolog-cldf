from setuptools import setup


setup(
    name='cldfbench_glottolog',
    py_modules=['cldfbench_glottolog', 'schema'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'glottolog=cldfbench_glottolog:GlottologDataset',
        ],
    },
    install_requires=[
        'pycldf>=1.34.0',
        'cldfbench>=1.7.1',
        'clldutils',
        'pyglottolog[geo]>=3.11',
        'python-nexus',
    ],
    extras_require={
        'geo': [
            'pyproj',
        ],
        'test': [
            'pytest-cldf',
        ],
    },
)
