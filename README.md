# PhishOracle
# PhishOracle
A Phishing Web Page Generator

******************************************************************************************************************************************************************
'''''''''''''''''''''''''''''''''''''''''''
Steps for generating the phishing web pages
'''''''''''''''''''''''''''''''''''''''''''
1. Add legitimate URLs to the file 'target_URLs.txt'
2. Select the total number of phishing features you want to add to the target web pages. This can be done by adding a number from 1 to 15 in the file 'feature_count.txt'. Since the total number of features implemented is 20. Hence we are keeping the feature addition count to be below 15. In the course of time, new phishing features will be made available.
3. Install all the required packages required for running the main file by typing the command - pip install -r requirements.txt.
4. Now the package requriements set up will be eready at your system.
5. Before running the main file 'adding_phishing_features.py' do the following modifications.
	1) For the variable name 'user_agent_values' add your systems information that can be obtained by running the file 'get_user_agents.py'
	2) Add destination folder path for storing the requested legitimate web pages in the variable 'legitimate_folder'
	3) Add destination folder path for storing the generated phishing web pages in the variable 'write_file'
5. Now you can run the main file 'adding_phishing_features.py' and obtain the generated phishing web pages with randomly added phishing features on the corresponding legitimate web pages at the given folder location.
6. DONE!

******************************************************************************************************************************************************************

Abstract - Phishing attacks, where cyber criminals deceive victims into providing personal information, are becoming more common through emails, texts, and websites. Phishing websites, which appear authentic, are designed to gather private data from users. Researchers have developed machine learning models to detect phishing websites using publicly available datasets containing URL and content-based features. However, collecting datasets containing a variety of phishing features can be a cumbersome task. Additionally, if models are not trained with effective features, they fail to detect new phishing web pages. Limited target domain lists used by existing phishing web page generators prevent generated datasets from being used for model training. Furthermore, creating a dataset containing an equal number of legitimate and phishing web pages with effective phishing features is another challenge. To overcome these challenges, we introduce 'PhishOracle' which adds randomly selected content and visual-based features to any given set of legitimate URLs to create phishing web pages. The tool creates an equal proportion of legitimate and phishing web pages that can be used for model training and evaluation of phishing detection solutions. We demonstrate that excluding effective content and visual-based features in creating models can drastically reduce their detection capability. We propose solutions to improve the models’ capabilities and show that PhishOracle is a valuable resource for developing and testing machine learning-based phishing detection solutions.

