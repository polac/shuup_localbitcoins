import setuptools


if __name__ == '__main__':
    setuptools.setup(
        name="shuup-localbitcoins",
        version="0.0.2",
        description="Localbitcoins merchant integration for Shuup",
        packages=setuptools.find_packages(),
        install_requires=["shuup>=0.4", "lbcapi>=1.0"],
        entry_points={"shuup.addon": "shuup_localbitcoins=shuup_localbitcoins"}
    )

