vendor:
	rm -rf vendor
	mkdir -p vendor
	pipenv lock -r > requirements.txt
	pip install -r requirements.txt --no-deps -t vendor
	wget https://files.pythonhosted.org/packages/a4/da/2bd281c875686230eabc13d20ab590ea617563b0e746abfb0698c4d5b645/Pillow-6.1.0-cp37-cp37m-manylinux1_x86_64.whl
	unzip -u Pillow-6.1.0-cp37-cp37m-manylinux1_x86_64.whl -d vendor
	rm Pillow-6.1.0-cp37-cp37m-manylinux1_x86_64.whl

package:
	rm -rf api.zip
	rm -rf resizer.zip
	cd vendor && zip -r ../api.zip .
	cp api.zip resize.zip
	zip -g api.zip api.py
	zip -g resize.zip resize.py

publish:
	aws lambda update-function-code --function-name TeamRoster_API --zip-file fileb://api.zip --profile civic
	aws lambda update-function-code --function-name TeamRoster_Resizer --zip-file fileb://resize.zip --profile civic
