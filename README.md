# PII Firewall (alpha)

The PII Firewall is a standalone program built as proof of concept for The Data Station Project, it is designed to run in a local context and it’s primary objectives are as follows:

1. Provide flexible and extensible tools to identify PII in any given data source

2.  Prevent the in inadvertent transmission of PII to federated data systems

3.  Provide a one stop hub for PII detection, analysis, and mitigation by integrating disparate PII detection models and approaches under a single platform

4.  Do the above in a efficient and performative manner, though primary focus is on extensibility now and performance later

## Key Traits



## Contents of Directory
- **example_config.json** - Is an example config file for the runtime and thread level configurations. Use this file to map endpoints, set thread and core counts.

- **main.py-**  - A  non-critical package file, this is included simply to demonstrate how one can initialize and run the pii_firewall

- **pii_firewall.py**  - The facade class for all of the PII Firewall functionality, controls program flow and execution sequence

- **requirements.txt** - A pip freeze that contains all of the necessary packages to run the PII Firewall, useful if running within a virtual environment

## Initial Setup and Execution

#### *Installation Requirements*
As always, it is highly recommended that you run your PII Firewall in a self-contained virtual environment. To setup up your own virtual environment I recommend you check out [this link](https://docs.python.org/3/tutorial/venv.html) for more details. Once you *have activated the venv*, execute the following instructions in your command line.

```python -m pip install -r requirements.txt```

One should also note that  due to issues with thread-safe data types in python, Windows OS is not currently supported for this project. While code execution may work, behavior could be non-deterministic.

#### *Execution*

Once a configuration is structured and complete, execution is a simple as parsing said config.json in python (preferably using the json library) and passing said json object (python dictionary) to the constructor of a PII_Firewall object. Note that using a JSON config file is actually necessary since a user could theoretically construct a nested python dictionary with all of the appropriate values. This is a feature and not a bug as it allows for a scheduler process to generate multiple instances of the PII Firewall on separate nodes or machines and customize their configurations.

**Once a PIIFirewall object has been instantiated with the proper runtime configuration, simply call the *run()* method and execution will begin.**

#### *Quick Notes Endpoint Configurations*

For the purpose of this program, an endpoint is considered to be a local directory with the following syntax:

``<input_directory> --> <output_directory>``

***ALL INPUT AND OUTPUT SOURCES SHOULD BE DIRECTORIES!***

The PII Firewall will automatically parse subdirectories of the input source and identify files it can ingest and anonymize, it will also automatically generate subdirectories in the output directory to place profiles and processed data.


##  Simplified Architecture

![](https://github.com/jmskinner/pii_firewall/blob/main/read_me_images/high_level.png)

## Strategy UML for Work and Write
![](https://github.com/jmskinner/pii_firewall/blob/main/read_me_images/strategy_uml.png)


## Parallel Processing Flow
![](https://github.com/jmskinner/pii_firewall/blob/main/read_me_images/par_processing_flow.png)

