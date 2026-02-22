from setuptools import setup, find_packages

setup(
    name="pyjam",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "pydub"
    ],
    author="Omar Soudan",
    description="A Python-based Digital Audio Workstation (DAW) for programmatic music generation.",
    keywords="music daw synthesis audio guitar piano",
    python_requires=">=3.7",
)
