from setuptools import setup


setup(
    name='cldfbench_glottolog',
    py_modules=['cldfbench_glottolog'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'glottolog=cldfbench_glottolog:GlottologDataset',
        ],
    },
    install_requires=[
        'cldfbench>=1.7.1',
        'clldutils',
        'pycldf',
        'pyglottolog',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
