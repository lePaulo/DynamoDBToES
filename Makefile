build:
	@pip install -r requirements.txt -t ./

clean: 
	@rm -r HISTORY.rst LICENSE NOTICE README.rst certifi-2017.11.5.dist-info/ certifi/ chardet-3.0.4.dist-info/ chardet/ elasticsearch-6.0.0.dist-info/ elasticsearch/ elasticsearch5/ idna-2.6.dist-info/ idna/ requests-2.18.4.dist-info/ requests/ requests_aws4auth-0.9.dist-info/ requests_aws4auth/ urllib3-1.22.dist-info/ urllib3/